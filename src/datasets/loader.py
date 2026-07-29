"""
Project: Adaptive Knowledge Injection
Module: src.datasets.loader
Purpose: Load cached datasets and convert examples to the unified schema.
Dependencies: pathlib, datasets
Author: Adaptive Knowledge Injection Research
Version: 1.0.0
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.datasets.downloader import verify_checksum_manifest
from src.datasets.validator import (
    DatasetValidationError,
    validate_dataset_columns,
    validate_dataset_config,
    validate_unified_record,
)
from src.utils.config import ConfigNode
from src.utils.constants import (
    DATASETS_CONFIG,
    QUESTION_ANSWERING,
    SUMMARIZATION,
)
from src.utils.io import ensure_directory, load_yaml_config, resolve_path
from src.utils.logger import get_logger


logger = get_logger(__name__, log_to_file=False)


class DatasetLoaderError(Exception):
    """Raised when cached datasets cannot be loaded or converted."""


@dataclass(frozen=True)
class UnifiedDatasetRecord:
    """Internal schema for all supported datasets.

    Attributes:
        sample_id:
            Stable sample identifier.
        dataset:
            Internal dataset name.
        task:
            Task name.
        domain:
            Dataset domain.
        input:
            Model input text.
        context:
            Optional source context.
        target:
            Target answer or summary.
        metadata:
            Additional source metadata.
    """

    sample_id: str
    dataset: str
    task: str
    domain: str
    input: str
    context: str | None
    target: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert the record to a dictionary."""

        return {
            "sample_id": self.sample_id,
            "dataset": self.dataset,
            "task": self.task,
            "domain": self.domain,
            "input": self.input,
            "context": self.context,
            "target": self.target,
            "metadata": self.metadata,
        }


def _import_huggingface_datasets() -> Any:
    """Import Hugging Face Datasets lazily."""

    try:
        import datasets  # noqa: PLC0415
    except ImportError as exc:
        raise DatasetLoaderError(
            "Hugging Face Datasets is required for cached dataset loading."
        ) from exc

    return datasets


def _to_dict(config: ConfigNode | Mapping[str, Any]) -> dict[str, Any]:
    """Convert a config node or mapping into a dictionary."""

    if isinstance(config, ConfigNode):
        return config.to_dict()

    return dict(config)


def _get_dataset_config(
    datasets_config: ConfigNode | Mapping[str, Any],
    dataset_name: str,
) -> dict[str, Any]:
    """Return one dataset configuration."""

    config_dict = _to_dict(datasets_config)
    registry = config_dict.get("datasets", {})

    if dataset_name not in registry:
        raise DatasetLoaderError(f"Unknown dataset: {dataset_name}")

    dataset_config = dict(registry[dataset_name])
    validate_dataset_config(dataset_name, dataset_config)
    return dataset_config


def normalize_text(value: Any) -> str:
    """Normalize scalar source values into text."""

    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    return str(value).strip()


def normalize_context(value: Any) -> str | None:
    """Normalize source context values into a string or None.

    PubMedQA contexts may arrive as dictionaries containing a `contexts` list.
    Other datasets usually provide context as a plain string or null value.
    """

    if value is None:
        return None

    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None

    if isinstance(value, Mapping):
        contexts = value.get("contexts")

        if isinstance(contexts, list):
            joined_contexts = "\n".join(normalize_text(item) for item in contexts)
            return joined_contexts.strip() or None

        return normalize_text(value) or None

    if isinstance(value, list):
        joined_values = "\n".join(normalize_text(item) for item in value)
        return joined_values.strip() or None

    return normalize_text(value) or None


def convert_record_to_unified_schema(
    record: Mapping[str, Any],
    dataset_name: str,
    dataset_config: Mapping[str, Any],
    index: int,
) -> dict[str, Any]:
    """Convert one source record into the unified internal schema."""

    text_column = dataset_config["text_column"]
    target_column = dataset_config["target_column"]
    context_column = dataset_config.get("context_column")
    id_column = dataset_config.get("id_column")

    sample_id_value = record.get(id_column) if id_column else None
    sample_id = normalize_text(sample_id_value) or f"{dataset_name}_{index}"
    context_value = record.get(context_column) if context_column else None

    unified = UnifiedDatasetRecord(
        sample_id=sample_id,
        dataset=dataset_name,
        task=dataset_config["task"],
        domain=dataset_config["domain"],
        input=normalize_text(record.get(text_column)),
        context=normalize_context(context_value),
        target=normalize_text(record.get(target_column)),
        metadata={
            "source_dataset": dataset_config["hf_dataset"],
            "subset": dataset_config.get("subset"),
            "source_id_column": id_column,
        },
    ).to_dict()

    validate_unified_record(unified)
    return unified


def convert_records_to_unified_schema(
    records: Iterable[Mapping[str, Any]],
    dataset_name: str,
    dataset_config: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Convert multiple source records into unified schema dictionaries."""

    return [
        convert_record_to_unified_schema(
            record=record,
            dataset_name=dataset_name,
            dataset_config=dataset_config,
            index=index,
        )
        for index, record in enumerate(records)
    ]


def _convert_split_dataset(
    split_dataset: Any,
    dataset_name: str,
    dataset_config: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Convert a split-like object into unified records."""

    records: list[Mapping[str, Any]]

    if hasattr(split_dataset, "to_list"):
        records = split_dataset.to_list()
    else:
        records = list(split_dataset)

    return convert_records_to_unified_schema(records, dataset_name, dataset_config)


def convert_dataset_to_unified_schema(
    dataset: Any,
    dataset_name: str,
    dataset_config: Mapping[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    """Convert a DatasetDict-like object into unified schema splits."""

    validate_dataset_columns(dataset_name, dataset, dataset_config)

    if isinstance(dataset, Mapping):
        split_names = list(dataset.keys())
    elif hasattr(dataset, "keys"):
        split_names = list(dataset.keys())
    else:
        split_names = ["data"]
        dataset = {"data": dataset}

    converted: dict[str, list[dict[str, Any]]] = {}

    for split_name in split_names:
        converted[str(split_name)] = _convert_split_dataset(
            split_dataset=dataset[split_name],
            dataset_name=dataset_name,
            dataset_config=dataset_config,
        )

    return converted


class DatasetLoader:
    """Loader for cached supported datasets."""

    def __init__(
        self,
        datasets_config: ConfigNode | Mapping[str, Any] | None = None,
    ) -> None:
        """Initialize the loader.

        Args:
            datasets_config:
                Optional loaded dataset configuration. When omitted,
                `configs/datasets.yaml` is loaded.
        """

        if datasets_config is None:
            datasets_config = load_yaml_config(f"configs/{DATASETS_CONFIG}")

        self.datasets_config = datasets_config
        self.config_dict = _to_dict(datasets_config)
        self.raw_data_dir = ensure_directory(self.config_dict["paths"]["raw_data"])

    def get_cache_dir(self, dataset_name: str) -> Path:
        """Return local cache directory for a dataset."""

        return self.raw_data_dir / dataset_name

    def load_cached_dataset(
        self,
        dataset_name: str,
        verify_checksum: bool = True,
    ) -> Any:
        """Load one cached dataset saved by `DatasetDownloader`."""

        cache_dir = self.get_cache_dir(dataset_name)

        if not cache_dir.exists():
            raise DatasetLoaderError(f"Cached dataset not found: {cache_dir}")

        if verify_checksum and not verify_checksum_manifest(cache_dir):
            raise DatasetLoaderError(f"Checksum verification failed: {cache_dir}")

        datasets = _import_huggingface_datasets()
        return datasets.load_from_disk(str(resolve_path(cache_dir)))

    def load_unified_dataset(
        self,
        dataset_name: str,
        verify_checksum: bool = True,
    ) -> dict[str, list[dict[str, Any]]]:
        """Load a cached dataset and convert it into unified schema splits."""

        dataset_config = _get_dataset_config(self.datasets_config, dataset_name)
        dataset = self.load_cached_dataset(
            dataset_name=dataset_name,
            verify_checksum=verify_checksum,
        )
        return convert_dataset_to_unified_schema(
            dataset=dataset,
            dataset_name=dataset_name,
            dataset_config=dataset_config,
        )


def load_unified_dataset(
    dataset_name: str,
    datasets_config: ConfigNode | Mapping[str, Any] | None = None,
    verify_checksum: bool = True,
) -> dict[str, list[dict[str, Any]]]:
    """Convenience wrapper for loading one unified dataset."""

    loader = DatasetLoader(datasets_config=datasets_config)
    return loader.load_unified_dataset(
        dataset_name=dataset_name,
        verify_checksum=verify_checksum,
    )

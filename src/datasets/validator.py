"""
Project: Adaptive Knowledge Injection
Module: src.datasets.validator
Purpose: Validate dataset configuration, raw datasets, and unified schema rows.
Dependencies: collections.abc
Author: Adaptive Knowledge Injection Research
Version: 1.0.0
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from src.utils.constants import (
    QUESTION_ANSWERING,
    SUMMARIZATION,
    SUPPORTED_DATASETS,
    SUPPORTED_TASKS,
    UNIFIED_SCHEMA_FIELDS,
)
from src.utils.logger import get_logger


logger = get_logger(__name__, log_to_file=False)

REQUIRED_DATASET_CONFIG_KEYS = (
    "enabled",
    "task",
    "domain",
    "source",
    "hf_dataset",
    "subset",
    "text_column",
    "target_column",
    "context_column",
    "id_column",
)


class DatasetValidationError(Exception):
    """Raised when dataset configuration or records are invalid."""


@dataclass(frozen=True)
class ValidationResult:
    """Structured validation result.

    Attributes:
        name:
            Dataset or validation target name.
        passed:
            Whether validation passed.
        errors:
            Validation error messages.
        warnings:
            Non-fatal validation warning messages.
    """

    name: str
    passed: bool
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


def _get_column_names(split_dataset: Any) -> set[str]:
    """Extract column names from a split-like dataset object."""

    column_names = getattr(split_dataset, "column_names", None)

    if column_names is not None:
        return set(column_names)

    if isinstance(split_dataset, Sequence) and split_dataset:
        first_record = split_dataset[0]

        if isinstance(first_record, Mapping):
            return set(first_record.keys())

    if isinstance(split_dataset, Mapping):
        return set(split_dataset.keys())

    return set()


def _iter_splits(dataset: Any) -> Iterable[tuple[str, Any]]:
    """Yield split names and split datasets from DatasetDict-like objects."""

    if isinstance(dataset, Mapping):
        yield from dataset.items()
        return

    keys = getattr(dataset, "keys", None)

    if callable(keys):
        for split_name in keys():
            yield split_name, dataset[split_name]
        return

    yield "data", dataset


def validate_dataset_name(dataset_name: str) -> None:
    """Validate that a dataset name is part of the active benchmark."""

    if dataset_name not in SUPPORTED_DATASETS:
        raise DatasetValidationError(f"Unsupported dataset: {dataset_name}")


def validate_dataset_config(
    dataset_name: str,
    dataset_config: Mapping[str, Any],
) -> ValidationResult:
    """Validate one dataset registry entry.

    Args:
        dataset_name:
            Internal dataset key.
        dataset_config:
            Dataset configuration mapping.

    Returns:
        Validation result.

    Raises:
        DatasetValidationError: If validation fails.
    """

    errors: list[str] = []

    if dataset_name not in SUPPORTED_DATASETS:
        errors.append(f"Unsupported dataset: {dataset_name}")

    missing_keys = [
        key for key in REQUIRED_DATASET_CONFIG_KEYS if key not in dataset_config
    ]

    if missing_keys:
        errors.append(f"Missing config keys: {', '.join(missing_keys)}")

    task = dataset_config.get("task")

    if task not in SUPPORTED_TASKS:
        errors.append(f"Unsupported task for {dataset_name}: {task}")

    if dataset_config.get("source") != "huggingface":
        errors.append(f"Only Hugging Face datasets are supported: {dataset_name}")

    for key in ("hf_dataset", "text_column", "target_column"):
        if not dataset_config.get(key):
            errors.append(f"Required config value is empty: {key}")

    if task == QUESTION_ANSWERING and not dataset_config.get("context_column"):
        errors.append(f"Question answering dataset needs context_column: {dataset_name}")

    if errors:
        raise DatasetValidationError("; ".join(errors))

    return ValidationResult(name=dataset_name, passed=True)


def validate_dataset_columns(
    dataset_name: str,
    dataset: Any,
    dataset_config: Mapping[str, Any],
) -> ValidationResult:
    """Validate that dataset splits contain configured source columns."""

    validate_dataset_config(dataset_name, dataset_config)
    errors: list[str] = []

    required_columns = {
        dataset_config["text_column"],
        dataset_config["target_column"],
    }

    context_column = dataset_config.get("context_column")
    id_column = dataset_config.get("id_column")

    if context_column:
        required_columns.add(context_column)

    if id_column:
        required_columns.add(id_column)

    for split_name, split_dataset in _iter_splits(dataset):
        available_columns = _get_column_names(split_dataset)
        missing_columns = sorted(required_columns - available_columns)

        if missing_columns:
            errors.append(
                f"{dataset_name}/{split_name} missing columns: "
                f"{', '.join(missing_columns)}"
            )

    if errors:
        raise DatasetValidationError("; ".join(errors))

    return ValidationResult(name=dataset_name, passed=True)


def validate_unified_record(record: Mapping[str, Any]) -> ValidationResult:
    """Validate one record after conversion to the internal unified schema."""

    errors: list[str] = []
    missing_fields = [
        field for field in UNIFIED_SCHEMA_FIELDS if field not in record
    ]

    if missing_fields:
        errors.append(f"Missing unified fields: {', '.join(missing_fields)}")

    if record.get("task") not in SUPPORTED_TASKS:
        errors.append(f"Unsupported task: {record.get('task')}")

    for field in ("sample_id", "dataset", "task", "domain", "input", "target"):
        if not record.get(field):
            errors.append(f"Unified field is empty: {field}")

    if record.get("metadata") is not None and not isinstance(
        record.get("metadata"), Mapping
    ):
        errors.append("metadata must be a mapping")

    if errors:
        raise DatasetValidationError("; ".join(errors))

    return ValidationResult(name=str(record.get("sample_id", "")), passed=True)


def validate_unified_records(records: Iterable[Mapping[str, Any]]) -> ValidationResult:
    """Validate multiple unified-schema records."""

    errors: list[str] = []

    for index, record in enumerate(records):
        try:
            validate_unified_record(record)
        except DatasetValidationError as exc:
            errors.append(f"record {index}: {exc}")

    if errors:
        raise DatasetValidationError("; ".join(errors))

    return ValidationResult(name="unified_records", passed=True)


def validate_split_ratios(splits_config: Mapping[str, float]) -> ValidationResult:
    """Validate train/validation/test split ratios."""

    required = ("train", "validation", "test")
    errors: list[str] = []

    for key in required:
        if key not in splits_config:
            errors.append(f"Missing split ratio: {key}")
        elif not 0 < float(splits_config[key]) < 1:
            errors.append(f"Split ratio must be between 0 and 1: {key}")

    total = sum(float(splits_config[key]) for key in required if key in splits_config)

    if round(total, 6) != 1.0:
        errors.append(f"Split ratios must sum to 1.0, got {total}")

    if errors:
        raise DatasetValidationError("; ".join(errors))

    return ValidationResult(name="split_ratios", passed=True)


def validate_low_resource_ratios(ratios: Iterable[float]) -> ValidationResult:
    """Validate low-resource training ratios."""

    errors: list[str] = []
    ratio_values = [float(ratio) for ratio in ratios]

    if not ratio_values:
        errors.append("At least one low-resource ratio is required.")

    for ratio in ratio_values:
        if not 0 < ratio <= 1:
            errors.append(f"Low-resource ratio must be in (0, 1]: {ratio}")

    if 1.0 not in ratio_values:
        errors.append("Low-resource ratios must include 1.0 baseline.")

    if errors:
        raise DatasetValidationError("; ".join(errors))

    return ValidationResult(name="low_resource_ratios", passed=True)

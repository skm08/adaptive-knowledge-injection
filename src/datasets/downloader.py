"""
Project: Adaptive Knowledge Injection
Module: src.datasets.downloader
Purpose: Download configured Hugging Face datasets with caching and checksums.
Dependencies: hashlib, pathlib, datasets, tqdm
Author: Adaptive Knowledge Injection Research
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import time
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.datasets.validator import DatasetValidationError, validate_dataset_config
from src.utils.config import ConfigNode
from src.utils.constants import DATASETS_CONFIG, SUPPORTED_DATASETS
from src.utils.io import ensure_directory, load_yaml_config, read_json, write_json
from src.utils.logger import get_logger


logger = get_logger(__name__, log_to_file=False)

CHECKSUM_FILENAME = "checksums.json"
DATASET_INFO_FILENAME = "dataset_info.json"
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY_SECONDS = 2.0


class DatasetDownloadError(Exception):
    """Raised when dataset download or cache verification fails."""


@dataclass(frozen=True)
class DatasetDownloadResult:
    """Summary of a dataset download or cache reuse operation.

    Attributes:
        name:
            Internal dataset key from `datasets.yaml`.
        cache_dir:
            Local directory containing the saved dataset artifact.
        checksum_file:
            Path to the checksum manifest.
        reused_cache:
            Whether an existing local cache was reused.
    """

    name: str
    cache_dir: Path
    checksum_file: Path
    reused_cache: bool


def _import_huggingface_datasets() -> Any:
    """Import Hugging Face Datasets lazily.

    Returns:
        Imported `datasets` module.

    Raises:
        DatasetDownloadError: If Hugging Face Datasets is unavailable.
    """

    try:
        import datasets  # noqa: PLC0415
    except ImportError as exc:
        raise DatasetDownloadError(
            "Hugging Face Datasets is required for dataset download."
        ) from exc

    return datasets


def _import_tqdm() -> Any:
    """Import tqdm lazily and return a fallback when unavailable."""

    try:
        from tqdm.auto import tqdm  # noqa: PLC0415
    except ImportError:
        return lambda values, **_: values

    return tqdm


def _to_dict(config: ConfigNode | Mapping[str, Any]) -> dict[str, Any]:
    """Convert a config node or mapping into a dictionary."""

    if isinstance(config, ConfigNode):
        return config.to_dict()

    return dict(config)


def _get_dataset_config(
    datasets_config: ConfigNode | Mapping[str, Any],
    dataset_name: str,
) -> dict[str, Any]:
    """Return one dataset configuration by name."""

    root_config = _to_dict(datasets_config)
    registry = root_config.get("datasets", {})

    if dataset_name not in registry:
        raise DatasetDownloadError(f"Unknown dataset: {dataset_name}")

    dataset_config = dict(registry[dataset_name])
    validate_dataset_config(dataset_name, dataset_config)
    return dataset_config


def _load_hf_dataset(dataset_config: Mapping[str, Any]) -> Any:
    """Load a dataset from Hugging Face Datasets."""

    datasets = _import_huggingface_datasets()
    subset = dataset_config.get("subset")

    if subset is None:
        return datasets.load_dataset(dataset_config["hf_dataset"])

    return datasets.load_dataset(dataset_config["hf_dataset"], subset)


def _load_hf_dataset_with_retry(
    dataset_name: str,
    dataset_config: Mapping[str, Any],
    max_retries: int,
    retry_delay_seconds: float,
) -> Any:
    """Load a Hugging Face dataset with retry behavior."""

    last_error: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            logger.info("Downloading dataset %s (attempt %s)", dataset_name, attempt)
            return _load_hf_dataset(dataset_config)
        except Exception as exc:  # noqa: BLE001 - retry diagnostics need context.
            last_error = exc
            logger.warning(
                "Dataset download failed for %s on attempt %s/%s: %s",
                dataset_name,
                attempt,
                max_retries,
                exc,
            )

            if attempt < max_retries:
                time.sleep(retry_delay_seconds)

    raise DatasetDownloadError(
        f"Failed to download dataset '{dataset_name}' after {max_retries} attempts."
    ) from last_error


def compute_file_sha256(path: str | Path) -> str:
    """Compute a SHA-256 checksum for one file.

    Args:
        path:
            File path.

    Returns:
        Hex digest.
    """

    file_path = Path(path)
    digest = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def build_checksum_manifest(directory: str | Path) -> dict[str, str]:
    """Build a checksum manifest for all files in a directory.

    Args:
        directory:
            Directory to inspect recursively.

    Returns:
        Mapping from POSIX relative paths to SHA-256 digests.
    """

    root = Path(directory).resolve()
    manifest: dict[str, str] = {}

    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == CHECKSUM_FILENAME:
            continue

        relative_path = path.relative_to(root).as_posix()
        manifest[relative_path] = compute_file_sha256(path)

    return manifest


def write_checksum_manifest(directory: str | Path) -> Path:
    """Write a checksum manifest for a saved dataset directory."""

    root = Path(directory).resolve()
    checksum_file = root / CHECKSUM_FILENAME
    write_json(checksum_file, build_checksum_manifest(root))
    return checksum_file


def verify_checksum_manifest(directory: str | Path) -> bool:
    """Verify a saved dataset directory against its checksum manifest."""

    root = Path(directory).resolve()
    checksum_file = root / CHECKSUM_FILENAME

    if not checksum_file.exists():
        return False

    expected = read_json(checksum_file)
    actual = build_checksum_manifest(root)
    return expected == actual


def save_dataset_info(
    dataset_name: str,
    dataset_config: Mapping[str, Any],
    cache_dir: str | Path,
) -> Path:
    """Save dataset metadata next to the cached dataset artifact."""

    info = {
        "name": dataset_name,
        "hf_dataset": dataset_config["hf_dataset"],
        "subset": dataset_config.get("subset"),
        "task": dataset_config["task"],
        "domain": dataset_config["domain"],
    }
    return write_json(Path(cache_dir) / DATASET_INFO_FILENAME, info)


class DatasetDownloader:
    """Downloader for the configured Hugging Face dataset registry."""

    def __init__(
        self,
        datasets_config: ConfigNode | Mapping[str, Any] | None = None,
    ) -> None:
        """Initialize the downloader.

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

    def get_enabled_dataset_names(self) -> list[str]:
        """Return enabled supported dataset names from configuration."""

        registry = self.config_dict.get("datasets", {})
        enabled_names = [
            name
            for name, config in registry.items()
            if name in SUPPORTED_DATASETS and config.get("enabled", False)
        ]
        return sorted(enabled_names)

    def get_cache_dir(self, dataset_name: str) -> Path:
        """Return the cache directory for one dataset."""

        return self.raw_data_dir / dataset_name

    def download_dataset(
        self,
        dataset_name: str,
        overwrite: bool | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay_seconds: float = DEFAULT_RETRY_DELAY_SECONDS,
    ) -> DatasetDownloadResult:
        """Download or reuse one configured dataset.

        Args:
            dataset_name:
                Internal dataset key.
            overwrite:
                Whether to replace an existing cache. Defaults to config.
            max_retries:
                Maximum Hugging Face download attempts.
            retry_delay_seconds:
                Delay between retry attempts.

        Returns:
            Download result summary.
        """

        dataset_config = _get_dataset_config(self.datasets_config, dataset_name)
        cache_dir = self.get_cache_dir(dataset_name)

        if overwrite is None:
            overwrite = bool(self.config_dict.get("download", {}).get("overwrite"))

        if cache_dir.exists() and not overwrite and verify_checksum_manifest(cache_dir):
            logger.info("Reusing verified dataset cache: %s", cache_dir)
            return DatasetDownloadResult(
                name=dataset_name,
                cache_dir=cache_dir,
                checksum_file=cache_dir / CHECKSUM_FILENAME,
                reused_cache=True,
            )

        ensure_directory(cache_dir)
        dataset = _load_hf_dataset_with_retry(
            dataset_name=dataset_name,
            dataset_config=dataset_config,
            max_retries=max_retries,
            retry_delay_seconds=retry_delay_seconds,
        )

        if not hasattr(dataset, "save_to_disk"):
            raise DatasetDownloadError(
                "Downloaded dataset object does not support save_to_disk()."
            )

        dataset.save_to_disk(str(cache_dir))
        save_dataset_info(dataset_name, dataset_config, cache_dir)
        checksum_file = write_checksum_manifest(cache_dir)
        logger.info("Saved dataset %s to %s", dataset_name, cache_dir)

        return DatasetDownloadResult(
            name=dataset_name,
            cache_dir=cache_dir,
            checksum_file=checksum_file,
            reused_cache=False,
        )

    def download_all(
        self,
        overwrite: bool | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay_seconds: float = DEFAULT_RETRY_DELAY_SECONDS,
        show_progress: bool = True,
    ) -> dict[str, DatasetDownloadResult]:
        """Download all enabled supported datasets.

        Args:
            overwrite:
                Whether to replace existing caches.
            max_retries:
                Maximum Hugging Face download attempts.
            retry_delay_seconds:
                Delay between retry attempts.
            show_progress:
                Whether to wrap dataset names with a progress bar.

        Returns:
            Mapping from dataset name to download result.
        """

        dataset_names = self.get_enabled_dataset_names()
        iterator: Any = dataset_names

        if show_progress:
            tqdm = _import_tqdm()
            iterator = tqdm(dataset_names, desc="Downloading datasets")

        results: dict[str, DatasetDownloadResult] = {}

        for dataset_name in iterator:
            results[dataset_name] = self.download_dataset(
                dataset_name=dataset_name,
                overwrite=overwrite,
                max_retries=max_retries,
                retry_delay_seconds=retry_delay_seconds,
            )

        return results


def download_dataset(
    dataset_name: str,
    datasets_config: ConfigNode | Mapping[str, Any] | None = None,
    overwrite: bool | None = None,
) -> DatasetDownloadResult:
    """Convenience wrapper for downloading one dataset."""

    downloader = DatasetDownloader(datasets_config=datasets_config)
    return downloader.download_dataset(dataset_name, overwrite=overwrite)


def download_all_datasets(
    datasets_config: ConfigNode | Mapping[str, Any] | None = None,
    overwrite: bool | None = None,
) -> dict[str, DatasetDownloadResult]:
    """Convenience wrapper for downloading all enabled datasets."""

    downloader = DatasetDownloader(datasets_config=datasets_config)
    return downloader.download_all(overwrite=overwrite)

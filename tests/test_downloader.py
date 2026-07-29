"""Tests for Hugging Face dataset download helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.datasets import downloader
from src.datasets.downloader import (
    CHECKSUM_FILENAME,
    DatasetDownloadError,
    DatasetDownloader,
    build_checksum_manifest,
    compute_file_sha256,
    verify_checksum_manifest,
    write_checksum_manifest,
)


class FakeDataset:
    """Small fake dataset with a Hugging Face-like save method."""

    def __init__(self, content: str = "sample") -> None:
        self.content = content

    def save_to_disk(self, path: str) -> None:
        """Save a deterministic artifact."""

        target = Path(path)
        target.mkdir(parents=True, exist_ok=True)
        (target / "data.txt").write_text(self.content, encoding="utf-8")


def make_dataset_config(tmp_path: Path) -> dict[str, object]:
    """Create a minimal valid dataset configuration."""

    return {
        "paths": {
            "raw_data": str(tmp_path / "raw"),
            "interim_data": str(tmp_path / "interim"),
            "processed_data": str(tmp_path / "processed"),
            "split_data": str(tmp_path / "splits"),
        },
        "download": {"overwrite": False},
        "datasets": {
            "sciq": {
                "enabled": True,
                "task": "question_answering",
                "domain": "science",
                "source": "huggingface",
                "hf_dataset": "sciq",
                "subset": None,
                "text_column": "question",
                "target_column": "correct_answer",
                "context_column": "support",
                "id_column": None,
            }
        },
    }


def test_compute_file_sha256_is_stable(tmp_path: Path) -> None:
    """File checksums should be deterministic."""

    path = tmp_path / "sample.txt"
    path.write_text("hello", encoding="utf-8")

    assert compute_file_sha256(path) == compute_file_sha256(path)


def test_checksum_manifest_excludes_manifest_file(tmp_path: Path) -> None:
    """Checksum manifests should not include themselves."""

    (tmp_path / "data.txt").write_text("hello", encoding="utf-8")
    checksum_file = write_checksum_manifest(tmp_path)

    manifest = build_checksum_manifest(tmp_path)

    assert checksum_file.name == CHECKSUM_FILENAME
    assert "data.txt" in manifest
    assert CHECKSUM_FILENAME not in manifest
    assert verify_checksum_manifest(tmp_path) is True


def test_checksum_verification_detects_file_changes(tmp_path: Path) -> None:
    """Checksum verification should fail after cached file mutation."""

    path = tmp_path / "data.txt"
    path.write_text("original", encoding="utf-8")
    write_checksum_manifest(tmp_path)
    path.write_text("changed", encoding="utf-8")

    assert verify_checksum_manifest(tmp_path) is False


def test_downloader_downloads_and_saves_checksum(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """DatasetDownloader should save a dataset and checksum manifest."""

    config = make_dataset_config(tmp_path)
    monkeypatch.setattr(
        downloader,
        "_load_hf_dataset",
        lambda _: FakeDataset("downloaded"),
    )

    result = DatasetDownloader(config).download_dataset(
        "sciq",
        retry_delay_seconds=0,
    )

    assert result.name == "sciq"
    assert result.reused_cache is False
    assert (result.cache_dir / "data.txt").read_text(encoding="utf-8") == "downloaded"
    assert result.checksum_file.is_file()
    assert verify_checksum_manifest(result.cache_dir) is True


def test_downloader_reuses_verified_cache(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Existing verified caches should be reused when overwrite is false."""

    config = make_dataset_config(tmp_path)
    cache_dir = tmp_path / "raw" / "sciq"
    cache_dir.mkdir(parents=True)
    (cache_dir / "data.txt").write_text("cached", encoding="utf-8")
    write_checksum_manifest(cache_dir)

    def fail_if_called(_: object) -> FakeDataset:
        raise AssertionError("download should not be called")

    monkeypatch.setattr(downloader, "_load_hf_dataset", fail_if_called)

    result = DatasetDownloader(config).download_dataset("sciq")

    assert result.reused_cache is True
    assert result.cache_dir == cache_dir.resolve()


def test_downloader_retries_before_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Downloader retry logic should recover from transient failures."""

    config = make_dataset_config(tmp_path)
    calls = {"count": 0}

    def flaky_load(_: object) -> FakeDataset:
        calls["count"] += 1

        if calls["count"] == 1:
            raise RuntimeError("temporary failure")

        return FakeDataset("ok")

    monkeypatch.setattr(downloader, "_load_hf_dataset", flaky_load)

    result = DatasetDownloader(config).download_dataset(
        "sciq",
        max_retries=2,
        retry_delay_seconds=0,
    )

    assert calls["count"] == 2
    assert result.reused_cache is False


def test_downloader_raises_after_retry_exhaustion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Downloader should fail clearly after retry exhaustion."""

    config = make_dataset_config(tmp_path)
    monkeypatch.setattr(
        downloader,
        "_load_hf_dataset",
        lambda _: (_ for _ in ()).throw(RuntimeError("down")),
    )

    with pytest.raises(DatasetDownloadError):
        DatasetDownloader(config).download_dataset(
            "sciq",
            max_retries=2,
            retry_delay_seconds=0,
        )


def test_get_enabled_dataset_names_filters_supported_enabled(
    tmp_path: Path,
) -> None:
    """Only enabled supported datasets should be returned."""

    config = make_dataset_config(tmp_path)
    config["datasets"]["unsupported"] = {"enabled": True}
    config["datasets"]["pubmedqa"] = {
        **config["datasets"]["sciq"],
        "enabled": False,
        "hf_dataset": "qiaojin/PubMedQA",
    }

    assert DatasetDownloader(config).get_enabled_dataset_names() == ["sciq"]


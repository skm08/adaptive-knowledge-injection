"""Tests for cached dataset loading and unified-schema conversion."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from src.datasets import loader
from src.datasets.loader import (
    DatasetLoader,
    DatasetLoaderError,
    convert_dataset_to_unified_schema,
    convert_record_to_unified_schema,
    normalize_context,
)


SCIQ_CONFIG = {
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

PUBMEDQA_CONFIG = {
    "enabled": True,
    "task": "question_answering",
    "domain": "biomedical",
    "source": "huggingface",
    "hf_dataset": "qiaojin/PubMedQA",
    "subset": "pqa_labeled",
    "text_column": "question",
    "target_column": "long_answer",
    "context_column": "context",
    "id_column": "pubid",
}

CNN_CONFIG = {
    "enabled": True,
    "task": "summarization",
    "domain": "news",
    "source": "huggingface",
    "hf_dataset": "cnn_dailymail",
    "subset": "3.0.0",
    "text_column": "article",
    "target_column": "highlights",
    "context_column": None,
    "id_column": None,
}


def make_dataset_config(tmp_path: Path) -> dict[str, object]:
    """Create a loader-compatible dataset configuration."""

    return {
        "paths": {
            "raw_data": str(tmp_path / "raw"),
            "interim_data": str(tmp_path / "interim"),
            "processed_data": str(tmp_path / "processed"),
            "split_data": str(tmp_path / "splits"),
        },
        "datasets": {
            "sciq": SCIQ_CONFIG,
            "pubmedqa": PUBMEDQA_CONFIG,
            "cnn_dailymail": CNN_CONFIG,
        },
    }


def test_normalize_context_handles_pubmedqa_context_dict() -> None:
    """PubMedQA context dictionaries should become newline-joined text."""

    context = {"contexts": ["first sentence", "second sentence"]}

    assert normalize_context(context) == "first sentence\nsecond sentence"


def test_normalize_context_handles_empty_values() -> None:
    """Empty contexts should normalize to None."""

    assert normalize_context(None) is None
    assert normalize_context("") is None
    assert normalize_context([]) is None


def test_convert_record_to_unified_schema_for_sciq() -> None:
    """SciQ records should convert to the internal schema."""

    record = {
        "question": "What is gravity?",
        "correct_answer": "A force",
        "support": "Gravity attracts masses.",
    }

    unified = convert_record_to_unified_schema(record, "sciq", SCIQ_CONFIG, 0)

    assert unified["sample_id"] == "sciq_0"
    assert unified["dataset"] == "sciq"
    assert unified["task"] == "question_answering"
    assert unified["input"] == "What is gravity?"
    assert unified["context"] == "Gravity attracts masses."
    assert unified["target"] == "A force"


def test_convert_record_to_unified_schema_for_pubmedqa() -> None:
    """PubMedQA records should use source IDs and normalize contexts."""

    record = {
        "pubid": 123,
        "question": "Does treatment help?",
        "long_answer": "Yes.",
        "context": {"contexts": ["trial one", "trial two"]},
    }

    unified = convert_record_to_unified_schema(
        record,
        "pubmedqa",
        PUBMEDQA_CONFIG,
        0,
    )

    assert unified["sample_id"] == "123"
    assert unified["context"] == "trial one\ntrial two"


def test_convert_record_to_unified_schema_for_summarization() -> None:
    """Summarization records should allow null context."""

    record = {"article": "Long article", "highlights": "Short summary"}

    unified = convert_record_to_unified_schema(
        record,
        "cnn_dailymail",
        CNN_CONFIG,
        0,
    )

    assert unified["task"] == "summarization"
    assert unified["context"] is None
    assert unified["target"] == "Short summary"


def test_convert_dataset_to_unified_schema_for_split_mapping() -> None:
    """Split mappings should convert split-wise into unified records."""

    dataset = {
        "train": [
            {
                "question": "What is gravity?",
                "correct_answer": "A force",
                "support": "Context",
            }
        ]
    }

    converted = convert_dataset_to_unified_schema(dataset, "sciq", SCIQ_CONFIG)

    assert list(converted) == ["train"]
    assert converted["train"][0]["sample_id"] == "sciq_0"


def test_dataset_loader_loads_cached_dataset(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """DatasetLoader should load a verified cache through Hugging Face APIs."""

    config = make_dataset_config(tmp_path)
    cache_dir = tmp_path / "raw" / "sciq"
    cache_dir.mkdir(parents=True)
    fake_dataset = {"train": []}
    fake_module = SimpleNamespace(load_from_disk=lambda _: fake_dataset)

    monkeypatch.setattr(loader, "verify_checksum_manifest", lambda _: True)
    monkeypatch.setattr(loader, "_import_huggingface_datasets", lambda: fake_module)

    loaded = DatasetLoader(config).load_cached_dataset("sciq")

    assert loaded == fake_dataset


def test_dataset_loader_rejects_failed_checksum(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """DatasetLoader should fail clearly when checksum verification fails."""

    config = make_dataset_config(tmp_path)
    cache_dir = tmp_path / "raw" / "sciq"
    cache_dir.mkdir(parents=True)
    monkeypatch.setattr(loader, "verify_checksum_manifest", lambda _: False)

    with pytest.raises(DatasetLoaderError):
        DatasetLoader(config).load_cached_dataset("sciq")


def test_dataset_loader_load_unified_dataset(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """DatasetLoader should load cached data and convert it to unified schema."""

    config = make_dataset_config(tmp_path)
    fake_dataset = {
        "train": [
            {
                "question": "What is gravity?",
                "correct_answer": "A force",
                "support": "Context",
            }
        ]
    }

    monkeypatch.setattr(
        DatasetLoader,
        "load_cached_dataset",
        lambda self, dataset_name, verify_checksum=True: fake_dataset,
    )

    unified = DatasetLoader(config).load_unified_dataset("sciq")

    assert unified["train"][0]["dataset"] == "sciq"


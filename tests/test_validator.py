"""Tests for dataset validation helpers."""

from __future__ import annotations

import pytest

from src.datasets.validator import (
    DatasetValidationError,
    validate_dataset_columns,
    validate_dataset_config,
    validate_low_resource_ratios,
    validate_split_ratios,
    validate_unified_record,
    validate_unified_records,
)


VALID_SCIQ_CONFIG = {
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


def test_validate_dataset_config_accepts_supported_dataset() -> None:
    """Supported dataset configs should pass validation."""

    result = validate_dataset_config("sciq", VALID_SCIQ_CONFIG)

    assert result.passed is True


def test_validate_dataset_config_rejects_unsupported_dataset() -> None:
    """Unsupported dataset names should fail validation."""

    with pytest.raises(DatasetValidationError):
        validate_dataset_config("bioasq", VALID_SCIQ_CONFIG)


def test_validate_dataset_config_rejects_missing_required_key() -> None:
    """Missing required keys should fail validation."""

    invalid_config = dict(VALID_SCIQ_CONFIG)
    invalid_config.pop("target_column")

    with pytest.raises(DatasetValidationError):
        validate_dataset_config("sciq", invalid_config)


def test_validate_dataset_columns_accepts_list_split() -> None:
    """Column validation should support mapping of split names to record lists."""

    dataset = {
        "train": [
            {
                "question": "What is science?",
                "correct_answer": "study",
                "support": "context",
            }
        ]
    }

    result = validate_dataset_columns("sciq", dataset, VALID_SCIQ_CONFIG)

    assert result.passed is True


def test_validate_dataset_columns_rejects_missing_columns() -> None:
    """Missing configured columns should fail validation."""

    dataset = {"train": [{"question": "What is science?"}]}

    with pytest.raises(DatasetValidationError):
        validate_dataset_columns("sciq", dataset, VALID_SCIQ_CONFIG)


def test_validate_unified_record_accepts_valid_record() -> None:
    """A complete unified-schema record should pass validation."""

    record = {
        "sample_id": "sciq_0",
        "dataset": "sciq",
        "task": "question_answering",
        "domain": "science",
        "input": "Question?",
        "context": "Context",
        "target": "Answer",
        "metadata": {},
    }

    result = validate_unified_record(record)

    assert result.passed is True


def test_validate_unified_record_rejects_missing_fields() -> None:
    """Incomplete unified records should fail validation."""

    with pytest.raises(DatasetValidationError):
        validate_unified_record({"sample_id": "x"})


def test_validate_unified_records_reports_record_index() -> None:
    """Batch validation errors should include the failing record index."""

    records = [
        {
            "sample_id": "ok",
            "dataset": "sciq",
            "task": "question_answering",
            "domain": "science",
            "input": "Question?",
            "context": "Context",
            "target": "Answer",
            "metadata": {},
        },
        {"sample_id": "bad"},
    ]

    with pytest.raises(DatasetValidationError, match="record 1"):
        validate_unified_records(records)


def test_validate_split_ratios_accepts_valid_ratios() -> None:
    """Split ratios should pass when they sum to one."""

    result = validate_split_ratios(
        {"train": 0.8, "validation": 0.1, "test": 0.1}
    )

    assert result.passed is True


def test_validate_split_ratios_rejects_invalid_total() -> None:
    """Split ratios must sum to one."""

    with pytest.raises(DatasetValidationError):
        validate_split_ratios({"train": 0.7, "validation": 0.1, "test": 0.1})


def test_validate_low_resource_ratios_accepts_valid_ratios() -> None:
    """Low-resource ratios should support configured benchmark ratios."""

    result = validate_low_resource_ratios([1.0, 0.5, 0.1])

    assert result.passed is True


def test_validate_low_resource_ratios_requires_baseline() -> None:
    """Low-resource ratios should include the full-data baseline."""

    with pytest.raises(DatasetValidationError):
        validate_low_resource_ratios([0.5, 0.1])


"""Tests for shared repository constants."""

from __future__ import annotations

from pathlib import Path

from src.utils import constants


def test_project_root_points_to_repository() -> None:
    """PROJECT_ROOT should resolve to the repository root."""

    assert constants.PROJECT_ROOT.is_dir()
    assert (constants.PROJECT_ROOT / "configs").is_dir()
    assert (constants.PROJECT_ROOT / "src").is_dir()


def test_config_files_are_registered() -> None:
    """All expected YAML configuration filenames should be listed."""

    assert constants.CONFIG_FILES == (
        "datasets.yaml",
        "preprocessing.yaml",
        "models.yaml",
        "retrieval.yaml",
        "training.yaml",
        "evaluation.yaml",
    )


def test_supported_research_entities_are_stable() -> None:
    """Supported tasks, datasets, methods, and splits should match the roadmap."""

    assert constants.SUPPORTED_TASKS == (
        constants.QUESTION_ANSWERING,
        constants.SUMMARIZATION,
    )
    assert constants.SUPPORTED_DATASETS == (
        constants.PUBMEDQA,
        constants.SCIQ,
        constants.CNN_DAILYMAIL,
        constants.GOVREPORT,
    )
    assert constants.SUPPORTED_METHODS == (
        constants.RAG,
        constants.PEFT,
        constants.HYBRID,
    )
    assert constants.SUPPORTED_SPLITS == (
        constants.TRAIN_SPLIT,
        constants.VALIDATION_SPLIT,
        constants.TEST_SPLIT,
    )


def test_unified_schema_fields_are_complete() -> None:
    """The unified schema should contain the required downstream fields."""

    assert constants.UNIFIED_SCHEMA_FIELDS == (
        "sample_id",
        "dataset",
        "task",
        "domain",
        "input",
        "context",
        "target",
        "metadata",
    )


def test_directory_constants_are_paths() -> None:
    """Directory constants should be pathlib Path instances."""

    path_constants = (
        constants.CONFIG_DIR,
        constants.DATA_DIR,
        constants.OUTPUTS_DIR,
        constants.CHECKPOINTS_DIR,
        constants.SRC_DIR,
        constants.TESTS_DIR,
    )

    assert all(isinstance(path, Path) for path in path_constants)


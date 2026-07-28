"""
Project: Adaptive Knowledge Injection
Module: src.utils.constants
Purpose: Define shared repository constants used across implementation layers.
Dependencies: pathlib
Author: Adaptive Knowledge Injection Research
Version: 1.0.0
"""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONFIG_DIR = PROJECT_ROOT / "configs"
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CHECKPOINTS_DIR = PROJECT_ROOT / "checkpoints"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"

RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SPLIT_DATA_DIR = DATA_DIR / "splits"

LOGS_DIR = OUTPUTS_DIR / "logs"
METRICS_DIR = OUTPUTS_DIR / "metrics"
PREDICTIONS_DIR = OUTPUTS_DIR / "predictions"
FIGURES_DIR = OUTPUTS_DIR / "figures"
TABLES_DIR = OUTPUTS_DIR / "tables"
REPORTS_DIR = OUTPUTS_DIR / "reports"

DATASETS_CONFIG = "datasets.yaml"
PREPROCESSING_CONFIG = "preprocessing.yaml"
MODELS_CONFIG = "models.yaml"
RETRIEVAL_CONFIG = "retrieval.yaml"
TRAINING_CONFIG = "training.yaml"
EVALUATION_CONFIG = "evaluation.yaml"

CONFIG_FILES = (
    DATASETS_CONFIG,
    PREPROCESSING_CONFIG,
    MODELS_CONFIG,
    RETRIEVAL_CONFIG,
    TRAINING_CONFIG,
    EVALUATION_CONFIG,
)

QUESTION_ANSWERING = "question_answering"
SUMMARIZATION = "summarization"

SUPPORTED_TASKS = (
    QUESTION_ANSWERING,
    SUMMARIZATION,
)

PUBMEDQA = "pubmedqa"
SCIQ = "sciq"
CNN_DAILYMAIL = "cnn_dailymail"
GOVREPORT = "govreport"

SUPPORTED_DATASETS = (
    PUBMEDQA,
    SCIQ,
    CNN_DAILYMAIL,
    GOVREPORT,
)

RAG = "rag"
PEFT = "peft"
HYBRID = "hybrid"

SUPPORTED_METHODS = (
    RAG,
    PEFT,
    HYBRID,
)

TRAIN_SPLIT = "train"
VALIDATION_SPLIT = "validation"
TEST_SPLIT = "test"

SUPPORTED_SPLITS = (
    TRAIN_SPLIT,
    VALIDATION_SPLIT,
    TEST_SPLIT,
)

UNIFIED_SCHEMA_FIELDS = (
    "sample_id",
    "dataset",
    "task",
    "domain",
    "input",
    "context",
    "target",
    "metadata",
)

DEFAULT_ENCODING = "utf-8"
DEFAULT_JSON_INDENT = 2
EXPERIMENT_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
DEFAULT_RANDOM_SEED = 42

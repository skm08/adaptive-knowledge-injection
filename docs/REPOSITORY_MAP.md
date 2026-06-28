# Repository Map

**Project:** Adaptive Knowledge Injection for Low-Resource Knowledge-Intensive Language Tasks: A Unified Framework Integrating Retrieval-Augmented Generation, Parameter-Efficient Fine-Tuning, and Hybrid Adaptation

**Version:** 1.0

**Last Updated:** 2026-06-27

---

# Purpose

This document defines the official repository structure and the responsibility of every directory and major file.

Rules:

* Every new file must have a clear responsibility.
* Do not place business logic outside `src/`.
* If a new module does not fit the existing architecture, update this document before implementing it.

---

# Repository Overview

```text
adaptive-knowledge-injection/

├── checkpoints/
├── configs/
├── data/
├── docs/
├── notebooks/
├── outputs/
├── scripts/
├── src/
├── tests/
├── README.md
├── requirements.txt
└── environment.yml
```

---

# Root Directory

## README.md

Repository overview, installation guide, project description, and usage instructions.

---

## requirements.txt

Python package dependencies.

---

## environment.yml

Optional Conda environment specification.

---

## pyproject.toml

Python packaging, tool configuration, and formatting metadata.

---

# checkpoints/

Purpose

Store model checkpoints generated during training.

Examples

```text
checkpoints/

lora/

hybrid/

best_model/

latest/
```

Rules

* Never commit large checkpoints to Git.
* Use Git LFS or external storage if required.

---

# configs/

Purpose

Centralized YAML configuration files.

Files

```text
datasets.yaml
preprocessing.yaml
models.yaml
retrieval.yaml
training.yaml
evaluation.yaml
```

Rules

* No hardcoded hyperparameters in Python code.
* Every configurable value should originate here.

---

# data/

Purpose

All datasets and intermediate artifacts.

Structure

```text
data/

raw/

interim/

processed/

splits/
```

## raw/

Downloaded public datasets.

Never modify.

---

## interim/

Temporary outputs.

Examples

* cleaned data
* tokenized data
* cached files

---

## processed/

Unified dataset format used by the framework.

---

## splits/

Train, validation, and test splits, including low-resource subsets.

---

# docs/

Purpose

Project documentation.

Files

```text
README.md

CODING_STANDARD.md

DESIGN_DECISIONS.md

PROJECT_STATUS.md

REPOSITORY_MAP.md

TODO.md

EXPERIMENTS.md

PROMPTS.md

SESSION_CONTEXT.md

CHANGELOG.md

PAPER_PLAN.md
```

Responsibilities

* Architecture
* Planning
* Progress
* Documentation
* AI collaboration

---

# notebooks/

Purpose

Google Colab notebooks for executing the pipeline.

Business logic is prohibited.

Notebook responsibilities

---

## 01_environment.ipynb

* Install dependencies
* Verify environment
* Mount Google Drive
* Check GPU

---

## 02_prepare_data.ipynb

* Download datasets
* Validate datasets
* Run preprocessing

---

## 03_build_rag.ipynb

* Build vector database
* Index documents
* Evaluate retrieval

---

## 04_train_peft.ipynb

* Fine-tune LoRA models
* Save checkpoints

---

## 05_build_hybrid.ipynb

* Build Hybrid Adaptation framework
* Validate integration

---

## 06_run_experiments.ipynb

* Execute benchmark experiments
* Save metrics

---

## 07_analysis.ipynb

* Statistical analysis
* Visualization
* Publication-ready figures

---

# outputs/

Purpose

All experiment outputs.

Structure

```text
outputs/

logs/

metrics/

predictions/

figures/

tables/

reports/
```

Rules

* Never overwrite previous experiments.
* Use timestamped directories.

Example

```text
outputs/

20260701_143500_EXP-003/
```

---

# scripts/

Purpose

Utility scripts for automation.

Examples

* download_models.py
* cleanup_outputs.py
* export_results.py

Scripts should not duplicate functionality from `src/`.

---

# src/

Purpose

Core implementation of the framework.

Only this directory should contain business logic.

---

# src/utils/

Purpose

Shared infrastructure used throughout the project.

Files

```text
config.py
logger.py
io.py
seed.py
constants.py
```

Responsibilities

* Configuration loading
* Logging
* File I/O
* Random seed management
* Shared constants

---

# src/datasets/

Purpose

Dataset management.

Files

```text
downloader.py
validator.py
loader.py
```

Responsibilities

* Download public datasets
* Validate dataset integrity
* Convert to unified schema
* Load datasets for experiments

---

# src/preprocessing/

Purpose

Dataset preprocessing.

Files

```text
schema.py
cleaner.py
splitter.py
```

Responsibilities

* Cleaning
* Schema normalization
* Low-resource sampling
* Dataset splitting

---

# src/retrieval/

Purpose

Knowledge retrieval pipeline.

Files

```text
chunking.py
vector_store.py
retriever.py
```

Responsibilities

* Text chunking
* Embedding generation
* FAISS index construction
* Retrieval
* Reranking

---

# src/models/

Purpose

Model implementations.

Files

```text
base_model.py

rag.py

peft.py

hybrid.py
```

Responsibilities

## base_model.py

Shared model utilities.

---

## rag.py

Retrieval-Augmented Generation.

---

## peft.py

Parameter-Efficient Fine-Tuning.

---

## hybrid.py

Proposed Hybrid Adaptation framework.

---

# src/evaluation/

Purpose

Evaluation toolkit.

Files

```text
metrics.py

hallucination.py

statistics.py
```

Responsibilities

* QA metrics
* Summarization metrics
* Retrieval metrics
* Hallucination analysis
* Statistical significance testing

---

# src/experiments/

Purpose

Experiment runners.

Files

```text
run_rag.py

run_peft.py

run_hybrid.py

run_full_benchmark.py
```

Responsibilities

* Execute experiments
* Load configurations
* Save metrics
* Log runtime information

---

# tests/

Purpose

Unit and integration tests.

Structure

```text
tests/

test_utils.py

test_datasets.py

test_retrieval.py

test_models.py

test_evaluation.py
```

Every public module should eventually have corresponding tests.

---

# Module Dependency Flow

```text
configs/

↓

utils/

↓

datasets/

↓

preprocessing/

↓

retrieval/

↓

models/

↓

evaluation/

↓

experiments/

↓

notebooks/
```

Dependencies should flow downward only.

Lower-level modules must not depend on higher-level modules.

---

# Data Flow

```text
Public Dataset

↓

Raw Data

↓

Processed Data

↓

Low-Resource Splits

↓

Retrieval Index

↓

Models

↓

Predictions

↓

Evaluation

↓

Statistics

↓

Figures & Tables
```

---

# Import Rules

Allowed example

```python
from src.utils.logger import get_logger
from src.utils.config import Config
```

Not allowed

* Relative imports across unrelated packages.
* Circular dependencies.
* Wildcard imports.

---

# File Placement Guidelines

| If you are implementing... | Place it in...       |
| -------------------------- | -------------------- |
| Dataset download           | `src/datasets/`      |
| Text cleaning              | `src/preprocessing/` |
| Chunking                   | `src/retrieval/`     |
| Vector indexing            | `src/retrieval/`     |
| RAG pipeline               | `src/models/`        |
| LoRA training              | `src/models/`        |
| Hybrid framework           | `src/models/`        |
| Evaluation metrics         | `src/evaluation/`    |
| Experiment orchestration   | `src/experiments/`   |
| Logging                    | `src/utils/`         |
| Configuration              | `configs/`           |
| Documentation              | `docs/`              |

---

# Architecture Principles

The repository should remain:

* Modular
* Configuration-driven
* Reproducible
* Extensible
* Testable
* Publication-ready

Every new component should follow these principles before being merged.

---

# Future Extensions

Potential additions without changing the architecture:

* Additional approved datasets
* New embedding models
* Alternative vector databases
* New PEFT methods (e.g., QLoRA, AdaLoRA)
* Multi-modal tasks
* Additional knowledge-intensive language tasks
* Distributed training support

These should extend existing modules rather than introducing parallel architectures.

---

# Architectural Rule

When introducing a new file:

1. Verify that an existing module cannot accommodate the functionality.
2. Ensure the new file has a single, well-defined responsibility.
3. Update this document before implementation if the repository structure changes.

Maintaining a stable architecture is essential for long-term maintainability, reproducibility, and publication-quality research.

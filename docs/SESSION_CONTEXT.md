# SESSION_CONTEXT

**Project:** Adaptive Knowledge Injection for Low-Resource Knowledge-Intensive Language Tasks

**Purpose:** Working memory for the current development session.

**Last Updated:** 2026-06-28

---

# Current Phase

Repository Foundation Cleanup

Status:

Utility foundation completed pending user review.

---

# Current Goal

Complete the repository utility foundation without changing the finalized
architecture.

---

# Current Working Module

Utilities

Completed:

- `src/utils/config.py`
- `src/utils/logger.py`
- `src/utils/io.py`
- `src/utils/seed.py`
- `src/utils/constants.py`
- `tests/test_io.py`
- `tests/test_seed.py`
- `tests/test_constants.py`

Next target after review approval:

```text
src/datasets/downloader.py
```

---

# Current Branch

```text
main
```

---

# Repository Status

## Foundation

Completed:

- Root README restored.
- MIT license added.
- `.gitignore` added.
- `requirements.txt` added.
- `environment.yml` added.
- `pyproject.toml` added.
- Package `__init__.py` files added.
- Python cache artifacts removed.
- `outputs/metrics/` added.

## Configuration

Completed:

- `datasets.yaml`
- `preprocessing.yaml`
- `models.yaml`
- `retrieval.yaml`
- `training.yaml`
- `evaluation.yaml`

Configuration ownership is normalized.

## Documentation

Completed:

- `README.md`
- `CODING_STANDARD.md`
- `DESIGN_DECISIONS.md`
- `PROJECT_STATUS.md`
- `REPOSITORY_MAP.md`
- `TODO.md`
- `EXPERIMENTS.md`
- `PROMPTS.md`
- `SESSION_CONTEXT.md`
- `CHANGELOG.md`
- `PAPER_PLAN.md`

---

# Active Dataset Selection

Question Answering:

- PubMedQA
- SciQ

Summarization:

- CNN/DailyMail
- GovReport

---

# Active Decisions

- Generator model: `meta-llama/Llama-3.1-8B-Instruct`
- Embedding model: `BAAI/bge-base-en-v1.5`
- Reranker: `BAAI/bge-reranker-base`
- Vector database: FAISS
- PEFT method: LoRA
- Quantization: 4-bit NF4
- Primary tasks: Question Answering and Summarization

---

# Immediate Next Tasks

After user review approval:

1. Implement `src/datasets/downloader.py`.
2. Implement `src/datasets/validator.py`.
3. Implement `src/datasets/loader.py`.

Do not implement preprocessing, retrieval, model, evaluation, experiment, or
notebook modules before dataset contracts are stable.

---

# Outstanding Issues

- The default PowerShell `python` command points to the Windows Store shim in
  this Codex shell. Focused utility tests passed with
  `C:\Users\USER\anaconda3\python.exe`.

---

# Handoff Instructions

At the beginning of the next session:

1. Read the required repository documentation.
2. Confirm the user has approved the utility foundation.
3. Continue with `src/datasets/downloader.py` only if approved.
4. Preserve the finalized architecture.

# SESSION_CONTEXT

**Project:** Adaptive Knowledge Injection for Low-Resource Knowledge-Intensive Language Tasks

**Purpose:** Working memory for the current development session.

**Last Updated:** 2026-06-28

---

# Current Phase

Repository Foundation Cleanup

Status:

Completed pending user review.

---

# Current Goal

Prepare the repository for implementation without changing the finalized
architecture.

---

# Current Working Module

Utilities

Completed:

- `src/utils/config.py`
- `src/utils/logger.py`

Next target after review approval:

```text
src/utils/io.py
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

1. Implement `src/utils/io.py`.
2. Implement `src/utils/seed.py`.
3. Implement `src/utils/constants.py`.
4. Add utility tests.

Do not implement dataset, preprocessing, retrieval, model, evaluation,
experiment, or notebook modules before utility approval.

---

# Outstanding Issues

- Local `python` and `py` commands are not available from the current PowerShell
  path, so Python-based validation could not be executed locally.

---

# Handoff Instructions

At the beginning of the next session:

1. Read the required repository documentation.
2. Confirm the user has approved foundation cleanup.
3. Continue with `src/utils/io.py` only if approved.
4. Preserve the finalized architecture.

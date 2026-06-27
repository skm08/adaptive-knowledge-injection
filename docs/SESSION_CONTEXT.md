# SESSION_CONTEXT

**Project:** Adaptive Knowledge Injection for Low-Resource Knowledge-Intensive Language Tasks

**Purpose:** Working memory for the current development session.

**Last Updated:** 2026-06-27

---

# Current Phase

**Phase 1 — Repository Infrastructure**

Status:

🟡 In Progress

---

# Current Goal

Finalize repository documentation and configuration before beginning large-scale Python implementation.

Primary objective:

Prepare a complete, reproducible repository specification for implementation by Codex.

---

# Current Working Module

Utilities

Next target:

```text
src/utils/io.py
```

---

# Current Branch

```text
main
```

Update this if working on a feature branch.

Example

```text
feature/retrieval
```

---

# Repository Status

## Configuration

Completed

* datasets.yaml
* preprocessing.yaml
* models.yaml
* retrieval.yaml
* training.yaml
* evaluation.yaml

---

## Documentation

Completed

* README.md
* CODING_STANDARD.md
* DESIGN_DECISIONS.md
* PROJECT_STATUS.md
* TODO.md
* EXPERIMENTS.md
* PROMPTS.md
* SESSION_CONTEXT.md

Pending

* REPOSITORY_MAP.md
* PAPER_PLAN.md
* CHANGELOG.md

---

## Utilities

Completed

* config.py
* logger.py

Pending

* io.py
* seed.py
* constants.py

---

# Current Repository Priority

The next implementation order should remain:

```text
src/utils/

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

Do not change this order unless there is a documented architectural reason.

---

# Active Decisions

Current generator model

```text
meta-llama/Llama-3.1-8B-Instruct
```

Embedding model

```text
BAAI/bge-base-en-v1.5
```

Vector database

```text
FAISS
```

PEFT

```text
LoRA
```

Quantization

```text
4-bit NF4
```

Primary tasks

* Question Answering
* Summarization

---

# Files Modified This Session

Documentation

* README.md
* CODING_STANDARD.md
* DESIGN_DECISIONS.md
* PROJECT_STATUS.md
* TODO.md
* EXPERIMENTS.md
* PROMPTS.md
* SESSION_CONTEXT.md

Configuration

* preprocessing.yaml
* models.yaml
* retrieval.yaml
* training.yaml
* evaluation.yaml

Python

* src/utils/config.py
* src/utils/logger.py

---

# Outstanding Issues

None at this stage.

Future implementation should validate:

* YAML loading
* Configuration schemas
* Logger integration
* Path handling
* Deterministic behavior

---

# Known Risks

* Repository scope is large.
* Google Colab GPU availability may vary.
* Long-running experiments require checkpointing.
* Hybrid implementation should not duplicate RAG or PEFT logic.

---

# Coding Reminders

Every new Python module must:

* Follow `CODING_STANDARD.md`.
* Use YAML configuration.
* Use `config.py`.
* Use `logger.py`.
* Use `pathlib.Path`.
* Include type hints.
* Include Google-style docstrings.
* Avoid hardcoded values.
* Be independently testable.

---

# Immediate Next Tasks

1. Generate `REPOSITORY_MAP.md`.
2. Generate `PAPER_PLAN.md`.
3. Generate `CHANGELOG.md`.
4. Implement `src/utils/io.py`.
5. Implement `src/utils/seed.py`.
6. Implement `src/utils/constants.py`.

---

# Handoff Instructions

When starting the next ChatGPT or Codex session:

1. Read:

   * README.md
   * DESIGN_DECISIONS.md
   * CODING_STANDARD.md
   * PROJECT_STATUS.md
   * REPOSITORY_MAP.md
   * TODO.md
   * EXPERIMENTS.md
   * PROMPTS.md
   * SESSION_CONTEXT.md

2. Summarize the current repository state.

3. Confirm the next module to implement.

4. Do not redesign the architecture without updating `DESIGN_DECISIONS.md`.

---

# Session Summary

Completed during this session:

* Finalized core YAML configuration.
* Established documentation standards.
* Defined AI collaboration protocol.
* Prepared implementation roadmap.
* Completed foundational project documentation.

The repository is now ready to transition from planning to implementation.

---

# End-of-Session Checklist

Before ending today's work:

* [ ] Commit completed files to Git.
* [ ] Update `CHANGELOG.md`.
* [ ] Update `PROJECT_STATUS.md`.
* [ ] Review `TODO.md`.
* [ ] Confirm the next implementation target.
* [ ] Push changes to GitHub (if applicable).

---

# Notes

This file should remain concise and current.

Whenever development focus changes:

* Update the **Current Goal**.
* Update the **Current Working Module**.
* Update the **Files Modified This Session**.
* Update the **Outstanding Issues**.
* Update the **Immediate Next Tasks**.

Treat this file as the project's "working memory" rather than a permanent record.

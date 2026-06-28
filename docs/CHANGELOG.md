# Changelog

All notable changes to this project will be documented in this file.

This project follows the principles of **Keep a Changelog** and **Semantic Versioning** where appropriate.

---

# Versioning Strategy

## Repository Versions

* **v0.x.x** → Research & Development
* **v1.0.0** → First public release accompanying manuscript submission
* **v1.x.x** → Bug fixes, documentation updates, and post-publication improvements

---

# Change Categories

Use the following categories whenever possible:

* **Added** — New functionality or documentation.
* **Changed** — Existing behavior modified.
* **Deprecated** — Features scheduled for removal.
* **Removed** — Deleted functionality.
* **Fixed** — Bug fixes.
* **Security** — Security-related updates.
* **Research** — Methodology, experiments, or scientific changes.

---

# [Unreleased]

## Added

* Restored root `README.md`.
* Added MIT `LICENSE`.
* Added `.gitignore` rules for caches, generated data, checkpoints, and outputs.
* Added `requirements.txt` for pip and Google Colab-compatible environments.
* Added `environment.yml` for local Conda development.
* Added `pyproject.toml` with packaging and formatting metadata.
* Added package `__init__.py` files for clean imports.
* Added `.gitkeep` files for documented artifact directories, including
  `outputs/metrics/`.
* Restored `src/utils/logger.py` as the centralized logging utility.

## Changed

* Normalized configuration ownership across YAML files.
* Moved LoRA hyperparameters to `configs/training.yaml`.
* Standardized retrieval model keys to use `embedding.model` and
  `reranker.model`.
* Standardized active datasets to PubMedQA, SciQ, CNN/DailyMail, and GovReport.
* Updated project status, TODO, and session context to remove contradictory
  foundation status statements.

## Removed

* Removed generated Python cache artifacts from `src/utils/__pycache__/`.

---

# [0.1.0] - 2026-06-27

## Research

### Added

* Finalized research topic.
* Defined research objectives.
* Established research questions.
* Defined hypotheses.
* Identified expected contributions.
* Completed literature-gap analysis.
* Designed unified experimental methodology.
* Defined benchmark strategy for:

  * Retrieval-Augmented Generation (RAG)
  * Parameter-Efficient Fine-Tuning (PEFT)
  * Hybrid Adaptation
* Selected primary tasks:

  * Question Answering
  * Summarization
* Selected target Q1 journals.

---

## Repository

### Added

Initial repository architecture.

Created directories:

```text
checkpoints/
configs/
data/
docs/
notebooks/
outputs/
scripts/
src/
tests/
```

---

## Configuration

### Added

Created YAML configuration files:

* datasets.yaml
* preprocessing.yaml
* models.yaml
* retrieval.yaml
* training.yaml
* evaluation.yaml

---

## Documentation

### Added

Created:

* README.md
* CODING_STANDARD.md
* DESIGN_DECISIONS.md
* PROJECT_STATUS.md
* TODO.md
* EXPERIMENTS.md
* REPOSITORY_MAP.md
* PAPER_PLAN.md
* PROMPTS.md
* SESSION_CONTEXT.md
* CHANGELOG.md

---

## Utilities

### Added

Implemented:

* `src/utils/config.py`
* `src/utils/logger.py`

Planned:

* `src/utils/io.py`
* `src/utils/seed.py`
* `src/utils/constants.py`

---

## Architecture

### Added

Established repository-wide standards:

* Configuration-driven design
* Modular architecture
* Reproducibility-first workflow
* Documentation-first development
* AI-assisted development protocol

---

## Development Workflow

### Added

Defined collaboration strategy:

* ChatGPT → Research architect
* Codex → Implementation engineer
* Google Colab → Experiment execution

---

# Future Releases

## [0.2.0]

Planned

### Added

* Utility layer completed
* Dataset downloader
* Dataset validator
* Dataset loader

---

## [0.3.0]

Planned

### Added

* Preprocessing pipeline
* Unified schema
* Low-resource sampling
* Dataset splitting

---

## [0.4.0]

Planned

### Added

* Retrieval pipeline
* FAISS integration
* Embedding generation
* Chunking
* Reranking

---

## [0.5.0]

Planned

### Added

* RAG implementation
* PEFT implementation
* Hybrid framework

---

## [0.6.0]

Planned

### Added

* Evaluation toolkit
* Statistical analysis
* Hallucination metrics

---

## [0.7.0]

Planned

### Added

* Experiment manager
* Benchmark runner
* Automatic result aggregation

---

## [0.8.0]

Planned

### Added

* Publication-ready visualization
* Paper figures
* Paper tables

---

## [0.9.0]

Planned

### Added

* Final experiments
* Statistical validation
* Reproducibility audit

---

## [1.0.0]

Planned

### Added

* First public release
* Open-source repository
* Camera-ready manuscript
* Reproducibility package

---

# Updating Guidelines

Update this file whenever:

* A new module is implemented.
* A new experiment is introduced.
* A configuration changes.
* A dependency is added or removed.
* Repository architecture changes.
* A significant bug is fixed.
* Research methodology changes.

---

# Commit Message Convention

Use the following prefixes:

```text
feat:      New feature
fix:       Bug fix
docs:      Documentation
refactor:  Code refactoring
test:      Tests
style:     Formatting
perf:      Performance improvement
research:  Methodology or experiment change
config:    Configuration update
build:     Build or dependency update
```

Examples:

```text
feat: implement FAISS retriever

fix: resolve dataset loader bug

docs: update repository map

research: revise hybrid evaluation protocol

config: update LoRA hyperparameters
```

---

# Release Checklist

Before creating a new version:

* [ ] Update `PROJECT_STATUS.md`
* [ ] Update `SESSION_CONTEXT.md`
* [ ] Update `EXPERIMENTS.md`
* [ ] Update `DESIGN_DECISIONS.md` (if architecture changed)
* [ ] Verify documentation consistency
* [ ] Confirm reproducibility
* [ ] Tag the Git release (when applicable)

---

# Notes

* Record **what changed** and **why**, not just **that** something changed.
* Never rewrite historical entries. If a decision changes, add a new entry describing the revision.
* Keep entries concise but informative.
* Link major changes to experiments or documentation where appropriate.

Maintaining an accurate changelog is part of ensuring the project remains reproducible, auditable, and suitable for long-term research collaboration.

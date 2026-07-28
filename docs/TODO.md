# TODO

**Project:** Adaptive Knowledge Injection for Low-Resource Knowledge-Intensive Language Tasks

**Purpose:** Master execution roadmap for repository development.

---

# Phase 0 - Research Planning

- [x] Literature review
- [x] Gap analysis
- [x] Research questions
- [x] Hypotheses
- [x] Contributions
- [x] Novelty claims
- [x] Experimental design
- [x] Dataset selection
- [x] Experiment matrix
- [x] Ablation study plan
- [x] Statistical analysis plan

---

# Phase 1 - Repository Foundation

- [x] Repository structure
- [x] Folder hierarchy
- [x] Root README
- [x] `.gitignore`
- [x] MIT `LICENSE`
- [x] `requirements.txt`
- [x] `environment.yml`
- [x] `pyproject.toml`
- [x] Package `__init__.py` files
- [x] Remove generated Python cache artifacts
- [x] Add documented `outputs/metrics/` directory

---

# Phase 2 - Configuration

- [x] `datasets.yaml`
- [x] `preprocessing.yaml`
- [x] `models.yaml`
- [x] `retrieval.yaml`
- [x] `training.yaml`
- [x] `evaluation.yaml`
- [x] Normalize configuration ownership
- [x] Standardize datasets to PubMedQA, SciQ, CNN/DailyMail, and GovReport

---

# Phase 3 - Documentation

- [x] `README.md`
- [x] `CODING_STANDARD.md`
- [x] `DESIGN_DECISIONS.md`
- [x] `PROJECT_STATUS.md`
- [x] `REPOSITORY_MAP.md`
- [x] `TODO.md`
- [x] `EXPERIMENTS.md`
- [x] `PAPER_PLAN.md`
- [x] `PROMPTS.md`
- [x] `SESSION_CONTEXT.md`
- [x] `CHANGELOG.md`

---

# Phase 4 - Utility Layer

Completed:

- [x] `src/utils/config.py`
- [x] `src/utils/logger.py`
- [x] `src/utils/io.py`
- [x] `src/utils/seed.py`
- [x] `src/utils/constants.py`
- [x] Utility module tests added

Validation:

- [x] Focused utility pytest suite passed in the local Anaconda environment.

---

# Phase 5 - Dataset Pipeline

- [ ] `src/datasets/downloader.py`
- [ ] `src/datasets/validator.py`
- [ ] `src/datasets/loader.py`
- [ ] Download configured datasets
- [ ] Verify dataset integrity
- [ ] Store raw datasets

---

# Phase 6 - Preprocessing

- [ ] `src/preprocessing/schema.py`
- [ ] `src/preprocessing/cleaner.py`
- [ ] `src/preprocessing/splitter.py`
- [ ] Generate processed datasets
- [ ] Generate low-resource subsets

---

# Phase 7 - Retrieval Pipeline

- [ ] `src/retrieval/chunking.py`
- [ ] `src/retrieval/vector_store.py`
- [ ] `src/retrieval/retriever.py`
- [ ] Build FAISS index
- [ ] Validate retrieval quality

---

# Phase 8 - Model Implementation

- [ ] `src/models/base_model.py`
- [ ] `src/models/rag.py`
- [ ] `src/models/peft.py`
- [ ] `src/models/hybrid.py`
- [ ] Validate inference pipeline

---

# Phase 9 - Evaluation

- [ ] `src/evaluation/metrics.py`
- [ ] `src/evaluation/hallucination.py`
- [ ] `src/evaluation/statistics.py`
- [ ] Validate evaluation pipeline

---

# Phase 10 - Experiment Pipeline

- [ ] `src/experiments/run_rag.py`
- [ ] `src/experiments/run_peft.py`
- [ ] `src/experiments/run_hybrid.py`
- [ ] `src/experiments/run_full_benchmark.py`

---

# Current Sprint

Prepare the repository foundation for implementation without changing the
finalized architecture.

Current status:

- Utility foundation implementation complete.
- Awaiting review before continuing with `src/datasets/downloader.py`.

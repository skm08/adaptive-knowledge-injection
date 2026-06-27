# TODO

**Project:** Adaptive Knowledge Injection for Low-Resource Knowledge-Intensive Language Tasks

**Purpose:** Master execution roadmap for repository development.

---

# Progress Legend

* ⬜ Not Started
* 🟡 In Progress
* ✅ Completed
* ⏸️ On Hold

---

# Phase 0 — Research Planning

## Literature

* [x] Literature review
* [x] Gap analysis
* [x] Research questions
* [x] Hypotheses
* [x] Contributions
* [x] Novelty claims

---

## Methodology

* [x] Experimental design
* [x] Dataset selection
* [x] Experiment matrix
* [x] Ablation study plan
* [x] Statistical analysis plan

---

# Phase 1 — Repository Infrastructure

## Repository

* [x] Repository structure
* [x] Folder hierarchy
* [ ] GitHub repository initialization
* [ ] .gitignore
* [ ] LICENSE
* [ ] environment.yml

---

## Configuration Files

* [x] datasets.yaml
* [x] preprocessing.yaml
* [x] models.yaml
* [x] retrieval.yaml
* [x] training.yaml
* [x] evaluation.yaml

---

## Documentation

* [x] README.md
* [x] CODING_STANDARD.md
* [x] DESIGN_DECISIONS.md
* [x] PROJECT_STATUS.md

Remaining:

* [ ] REPOSITORY_MAP.md
* [ ] PAPER_PLAN.md
* [ ] EXPERIMENTS.md
* [ ] CHANGELOG.md
* [ ] PROMPTS.md

---

# Phase 2 — Utility Layer

Implementation order is important.

## Utilities

* [x] config.py
* [x] logger.py

Next:

* [ ] io.py
* [ ] seed.py
* [ ] constants.py

Checkpoint:

* [ ] Utility module testing

---

# Phase 3 — Dataset Pipeline

## Dataset Management

Implementation order:

* [ ] downloader.py
* [ ] validator.py
* [ ] loader.py

Checkpoint:

* [ ] Download all datasets
* [ ] Verify dataset integrity
* [ ] Store raw datasets

---

# Phase 4 — Preprocessing

Implementation order:

* [ ] schema.py
* [ ] cleaner.py
* [ ] splitter.py

Checkpoint:

* [ ] Generate processed datasets
* [ ] Generate low-resource subsets

---

# Phase 5 — Retrieval Pipeline

Implementation order:

* [ ] chunking.py
* [ ] vector_store.py
* [ ] retriever.py

Checkpoint:

* [ ] Build FAISS index
* [ ] Validate retrieval quality
* [ ] Save retrieval artifacts

---

# Phase 6 — Model Implementation

## Base Components

* [ ] base_model.py

---

## Retrieval-Augmented Generation

* [ ] rag.py

---

## Parameter-Efficient Fine-Tuning

* [ ] peft.py

---

## Hybrid Adaptation

* [ ] hybrid.py

Checkpoint:

* [ ] Validate inference pipeline

---

# Phase 7 — Evaluation

Implementation order:

* [ ] metrics.py
* [ ] hallucination.py
* [ ] statistics.py

Checkpoint:

* [ ] Validate evaluation pipeline

---

# Phase 8 — Experiment Pipeline

Implementation order:

* [ ] run_rag.py
* [ ] run_peft.py
* [ ] run_hybrid.py
* [ ] run_full_benchmark.py

Checkpoint:

* [ ] Run baseline experiments

---

# Phase 9 — Notebooks

Implementation order:

* [ ] 01_environment.ipynb
* [ ] 02_prepare_data.ipynb
* [ ] 03_build_rag.ipynb
* [ ] 04_train_peft.ipynb
* [ ] 05_build_hybrid.ipynb
* [ ] 06_run_experiments.ipynb
* [ ] 07_analysis.ipynb

---

# Phase 10 — Research Experiments

## Baselines

* [ ] RAG
* [ ] PEFT

---

## Proposed Method

* [ ] Hybrid Adaptation

---

## Low-Resource Evaluation

Training ratios:

* [ ] 100%
* [ ] 50%
* [ ] 20%
* [ ] 10%
* [ ] 5%
* [ ] 1%

---

## Retrieval Ablation

* [ ] Dense Retrieval
* [ ] BM25
* [ ] Hybrid Retrieval

---

## Chunking Ablation

* [ ] 256 / 64
* [ ] 512 / 128
* [ ] 1024 / 256

---

## LoRA Ablation

* [ ] Rank 8
* [ ] Rank 16
* [ ] Rank 32

---

## Embedding Ablation

* [ ] BGE
* [ ] E5
* [ ] GTE

---

# Phase 11 — Statistical Analysis

* [ ] Aggregate metrics
* [ ] Generate confidence intervals
* [ ] Paired t-test
* [ ] Wilcoxon Signed-Rank Test
* [ ] Cohen's d
* [ ] Bootstrap analysis

---

# Phase 12 — Visualization

* [ ] Performance tables
* [ ] Retrieval plots
* [ ] Ablation figures
* [ ] Statistical comparison plots
* [ ] Publication-ready figures

---

# Phase 13 — Manuscript Preparation

## Writing

* [ ] Abstract
* [ ] Introduction
* [ ] Related Work
* [ ] Methodology
* [ ] Experimental Setup
* [ ] Results
* [ ] Discussion
* [ ] Conclusion

---

## Supplementary Material

* [ ] Appendix
* [ ] Reproducibility checklist
* [ ] Hyperparameter tables
* [ ] Repository release

---

# Phase 14 — Submission

* [ ] Internal review
* [ ] Final proofreading
* [ ] Prepare cover letter
* [ ] Select target journal
* [ ] Submit manuscript

---

# Current Sprint

## Goal

Complete the repository specification and begin implementation of the utility layer.

Priority tasks:

1. Finish remaining documentation.
2. Initialize the GitHub repository.
3. Implement `src/utils/io.py`.
4. Implement `src/utils/seed.py`.
5. Implement `src/utils/constants.py`.

---

# Notes

## Development Workflow

ChatGPT:

* Research supervision
* Architecture
* Documentation
* Code review

Codex:

* Python implementation
* Refactoring
* Testing support

Google Colab:

* Experiment execution
* Training
* Evaluation
* Visualization

---

# Completion Criteria

The project is considered complete when:

* All modules are implemented.
* All experiments are reproducible.
* Statistical analysis is finished.
* The manuscript is prepared for Q1 journal submission.
* The repository is ready for public release with documentation and reproducible workflows.

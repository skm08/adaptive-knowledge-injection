# EXPERIMENTS

**Project:** Adaptive Knowledge Injection for Low-Resource Knowledge-Intensive Language Tasks: A Unified Framework Integrating Retrieval-Augmented Generation, Parameter-Efficient Fine-Tuning, and Hybrid Adaptation

**Version:** 1.0

**Last Updated:** 2026-06-27

---

# Purpose

This document records every experiment conducted in this project.

Each experiment should be reproducible and linked to:

* Dataset
* Configuration
* Model
* Hyperparameters
* Metrics
* Output directory
* Git commit
* Notes

---

# Experiment Naming Convention

Every experiment should follow the format:

```
EXP-XXX
```

Example:

```
EXP-001
EXP-002
EXP-003
```

Output folders:

```
outputs/

20260701_153000_EXP-001/

20260701_171245_EXP-002/
```

---

# Experiment Lifecycle

```
Planned

↓

Running

↓

Completed

↓

Verified

↓

Included in Paper
```

Status labels:

* ⬜ Planned
* 🟡 Running
* ✅ Completed
* 📄 Included in Paper
* ❌ Failed
* 🔄 Repeated

---

# Standard Experiment Template

Every experiment should record:

| Field            | Value |
| ---------------- | ----- |
| Experiment ID    |       |
| Date             |       |
| Objective        |       |
| Task             |       |
| Dataset          |       |
| Model            |       |
| Method           |       |
| Configuration    |       |
| Random Seed      |       |
| Git Commit       |       |
| Hardware         |       |
| Runtime          |       |
| Output Directory |       |
| Notes            |       |

---

# Phase 1 — Baseline Experiments

## EXP-001

Objective

Evaluate Retrieval-Augmented Generation on Question Answering.

Status

⬜ Planned

Task

Question Answering

Dataset

PubMedQA

Method

RAG

Training Ratio

100%

Primary Metrics

* Exact Match
* F1
* BERTScore

---

## EXP-002

Objective

Evaluate PEFT on Question Answering.

Status

⬜ Planned

Method

LoRA

Dataset

PubMedQA

Training Ratio

100%

Primary Metrics

* Exact Match
* F1
* BERTScore

---

## EXP-003

Objective

Evaluate Hybrid Adaptation on Question Answering.

Status

⬜ Planned

Method

Hybrid

Dataset

PubMedQA

Training Ratio

100%

Primary Metrics

* Exact Match
* F1
* BERTScore

---

# Phase 2 — Summarization

## EXP-004

Objective

Evaluate RAG on Summarization.

Dataset

CNN/DailyMail

Status

⬜ Planned

---

## EXP-005

Objective

Evaluate PEFT on Summarization.

Dataset

CNN/DailyMail

Status

⬜ Planned

---

## EXP-006

Objective

Evaluate Hybrid Adaptation on Summarization.

Dataset

CNN/DailyMail

Status

⬜ Planned

---

# Phase 3 — Low-Resource Evaluation

Training ratios:

* 100%
* 50%
* 20%
* 10%
* 5%
* 1%

Experiments:

| ID      | Method | Status    |
| ------- | ------ | --------- |
| EXP-007 | RAG    | ⬜ Planned |
| EXP-008 | PEFT   | ⬜ Planned |
| EXP-009 | Hybrid | ⬜ Planned |

---

# Phase 4 — Retrieval Ablation

Objective

Compare retrieval strategies.

Configurations

* Dense Retrieval
* BM25
* Hybrid Retrieval

| ID      | Retrieval Strategy | Status    |
| ------- | ------------------ | --------- |
| EXP-010 | Dense              | ⬜ Planned |
| EXP-011 | BM25               | ⬜ Planned |
| EXP-012 | Hybrid             | ⬜ Planned |

---

# Phase 5 — Chunk Size Ablation

Configurations

| Chunk Size | Overlap |
| ---------- | ------- |
| 256        | 64      |
| 512        | 128     |
| 1024       | 256     |

| ID      | Configuration | Status    |
| ------- | ------------- | --------- |
| EXP-013 | 256/64        | ⬜ Planned |
| EXP-014 | 512/128       | ⬜ Planned |
| EXP-015 | 1024/256      | ⬜ Planned |

---

# Phase 6 — LoRA Ablation

Configurations

| Rank | Alpha |
| ---- | ----- |
| 8    | 16    |
| 16   | 32    |
| 32   | 64    |

| ID      | Rank | Status    |
| ------- | ---- | --------- |
| EXP-016 | 8    | ⬜ Planned |
| EXP-017 | 16   | ⬜ Planned |
| EXP-018 | 32   | ⬜ Planned |

---

# Phase 7 — Embedding Model Comparison

Models

* BGE Base
* E5 Base
* GTE Base

| ID      | Model | Status    |
| ------- | ----- | --------- |
| EXP-019 | BGE   | ⬜ Planned |
| EXP-020 | E5    | ⬜ Planned |
| EXP-021 | GTE   | ⬜ Planned |

---

# Phase 8 — Statistical Analysis

Objective

Validate whether observed performance differences are statistically significant.

Tests

* Paired t-test
* Wilcoxon Signed-Rank Test
* Bootstrap Confidence Interval
* Cohen's d

| ID      | Analysis               | Status    |
| ------- | ---------------------- | --------- |
| EXP-022 | Statistical Validation | ⬜ Planned |

---

# Phase 9 — Computational Efficiency

Metrics

* GPU Memory
* Training Time
* Inference Time
* Throughput
* Model Size
* Trainable Parameters

| ID      | Analysis             | Status    |
| ------- | -------------------- | --------- |
| EXP-023 | Efficiency Benchmark | ⬜ Planned |

---

# Final Benchmark

The final benchmark should compare:

| Method | QA | Summarization | Low Resource | Retrieval | Efficiency |
| ------ | -- | ------------- | ------------ | --------- | ---------- |
| RAG    | ⬜  | ⬜             | ⬜            | ⬜         | ⬜          |
| PEFT   | ⬜  | ⬜             | ⬜            | N/A       | ⬜          |
| Hybrid | ⬜  | ⬜             | ⬜            | ⬜         | ⬜          |

---

# Required Outputs

Each completed experiment must generate:

```
outputs/

logs/

metrics/

predictions/

tables/

figures/

reports/
```

Required artifacts:

* Configuration snapshot
* Evaluation metrics (JSON)
* Evaluation metrics (CSV)
* Predictions
* Runtime log
* Hardware information
* Random seed
* Model checkpoint (if applicable)

---

# Reproducibility Checklist

Every experiment must record:

* Dataset version
* Model version
* Configuration files
* Python version
* Package versions
* Git commit hash
* Random seed
* Hardware information

---

# Paper Figures

Planned figures:

* Overall pipeline
* RAG architecture
* PEFT architecture
* Hybrid architecture
* Low-resource performance curves
* Retrieval comparison
* Chunk size ablation
* LoRA ablation
* Efficiency comparison
* Statistical significance visualization

---

# Paper Tables

Planned tables:

1. Dataset statistics
2. Model configuration
3. Hyperparameters
4. QA benchmark results
5. Summarization benchmark results
6. Low-resource evaluation
7. Retrieval ablation
8. Chunk size ablation
9. LoRA ablation
10. Efficiency comparison
11. Statistical significance results

---

# Experiment Notes

Use this section to record:

* Unexpected behaviors
* Bugs
* Failed runs
* Reviewer-inspired analyses
* Follow-up experiments
* Ideas for future work

Every observation that may influence the paper should be documented here, even if it does not lead to a successful experiment.

---

# Publication Readiness Checklist

Before manuscript submission, verify that:

* All planned experiments are completed.
* All figures are reproducible.
* All tables are generated directly from experiment outputs.
* Statistical tests are complete.
* Hyperparameters are fully documented.
* Random seeds are recorded.
* Code reproduces published results from a clean environment.
* Repository is ready for public release.

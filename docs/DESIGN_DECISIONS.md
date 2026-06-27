# Design Decisions

**Project:** Adaptive Knowledge Injection for Low-Resource Knowledge-Intensive Language Tasks: A Unified Framework Integrating Retrieval-Augmented Generation, Parameter-Efficient Fine-Tuning, and Hybrid Adaptation

**Version:** 1.0

**Last Updated:** 2026-06-27

---

# Purpose

This document records all major technical and research decisions made during the development of this project.

It serves as the architectural memory of the repository and ensures that future modifications remain consistent with the original research objectives.

Whenever a major design choice changes, update this document.

---

# Research Objective

Develop and evaluate a unified framework for adaptive knowledge injection under low-resource settings by systematically comparing:

* Retrieval-Augmented Generation (RAG)
* Parameter-Efficient Fine-Tuning (PEFT)
* Hybrid Adaptation (RAG + PEFT)

across multiple knowledge-intensive language tasks.

---

# Research Tasks

Primary tasks:

* Question Answering
* Summarization

Future tasks (optional):

* Long-form Generation
* Information Extraction
* Report Generation

---

# Research Philosophy

The objective is not to maximize benchmark scores on a single dataset.

Instead, the framework should demonstrate:

* Robustness
* Generalization
* Efficiency
* Reproducibility
* Extensibility

The implementation should remain modular enough to support future research extensions.

---

# Overall System Architecture

```
Public Dataset

        │

        ▼

Dataset Preparation

        │

        ▼

Preprocessing

        │

        ▼

Low-Resource Sampling

        │

        ▼

────────────────────────────────────────────

RAG

PEFT

Hybrid

────────────────────────────────────────────

        │

        ▼

Evaluation

        │

        ▼

Statistical Analysis

        │

        ▼

Publication
```

---

# Low-Resource Definition

Low-resource conditions are simulated by reducing the available training data.

Training ratios:

* 100%
* 50%
* 20%
* 10%
* 5%
* 1%

These ratios are fixed across all experiments to ensure fair comparison.

---

# Public Datasets

## Question Answering

Primary:

* PubMedQA
* SciQ

Future candidates:

* BioASQ
* MedMCQA
* Natural Questions (domain-filtered)

---

## Summarization

Primary:

* CNN/DailyMail
* GovReport

Future candidates:

* XSum
* PubMed Summarization

---

# Internal Dataset Schema

Every dataset must be converted into a unified schema.

Required fields:

```
sample_id

dataset

task

domain

input

context

target

metadata
```

No downstream module should depend on the original dataset format.

---

# Knowledge Injection Paradigms

## Retrieval-Augmented Generation (RAG)

Characteristics:

* External knowledge retrieval
* No parameter updates
* Dynamic knowledge injection

Advantages:

* Up-to-date knowledge
* Lower training cost
* Better scalability

Limitations:

* Retrieval quality directly affects performance
* Retrieval latency

---

## Parameter-Efficient Fine-Tuning (PEFT)

Method:

* LoRA

Future extension:

* QLoRA

Characteristics:

* Internal knowledge adaptation
* Efficient parameter updates
* Compact checkpoints

Advantages:

* Low memory requirements
* Fast adaptation

Limitations:

* Static knowledge after training
* Requires retraining for new knowledge

---

## Hybrid Adaptation

Proposed contribution.

Combines:

* External retrieval
* Internal parameter adaptation

Expected advantages:

* Better robustness
* Higher factual accuracy
* Reduced hallucination
* Stronger performance in low-resource settings

---

# Generator Model

Primary model:

meta-llama/Llama-3.1-8B-Instruct

Selection criteria:

* Instruction tuned
* Strong reasoning capability
* Widely adopted
* Compatible with PEFT
* Suitable for Colab with quantization

Future comparison:

* Mistral
* Qwen
* Gemma

---

# Embedding Model

Primary model:

BAAI/bge-base-en-v1.5

Reason:

* Strong retrieval benchmark performance
* Efficient inference
* Open-source

Future comparison:

* BGE-large
* E5
* GTE

---

# Retrieval Strategy

Default:

Dense Retrieval

*

Cross-Encoder Reranking

Hybrid retrieval remains configurable.

---

# Vector Database

Primary backend:

FAISS

Reason:

* Fast
* Lightweight
* Easy integration
* Well-supported

Future comparison:

* ChromaDB
* Milvus

---

# Chunking Strategy

Default:

Recursive character chunking

Initial configuration:

* Chunk size: 512
* Overlap: 128

These values will be treated as experimental variables in ablation studies.

---

# PEFT Configuration

Primary method:

LoRA

Default configuration:

* Rank = 16
* Alpha = 32
* Dropout = 0.05

Hyperparameters remain configurable through YAML.

---

# Quantization

Default:

4-bit NF4

Reason:

* Google Colab compatibility
* Reduced GPU memory
* Efficient fine-tuning

---

# Evaluation Philosophy

Performance evaluation must include more than task accuracy.

Evaluation dimensions:

1. Task performance
2. Retrieval quality
3. Hallucination
4. Statistical significance
5. Computational efficiency

---

# Primary Evaluation Metrics

Question Answering:

* Exact Match
* F1
* BERTScore

Summarization:

* ROUGE-1
* ROUGE-2
* ROUGE-L
* BLEU
* BERTScore

Retrieval:

* Recall@k
* MRR
* MAP
* nDCG

Hallucination:

* Faithfulness
* Context Precision
* Context Recall

Efficiency:

* Inference latency
* GPU memory
* Throughput
* Model size

---

# Statistical Analysis

Required tests:

* Paired t-test
* Wilcoxon Signed-Rank Test
* Bootstrap Confidence Interval

Effect size:

* Cohen's d

Significance threshold:

* p < 0.05

---

# Experiment Design

Each experiment varies only one independent factor whenever possible.

Examples:

* Training ratio
* Retrieval strategy
* Chunk size
* LoRA rank
* Embedding model

This supports valid ablation studies.

---

# Configuration Management

All configurable values must originate from YAML files.

Python code should not contain hardcoded:

* model names
* learning rates
* paths
* retrieval parameters
* batch sizes
* evaluation settings

---

# Software Architecture

Business logic belongs exclusively in:

```
src/
```

Notebooks are reserved for:

* execution
* visualization
* analysis

---

# Reproducibility

Every experiment must record:

* Random seed
* Dataset
* Model
* Configuration
* Timestamp
* Metrics
* Hardware information

---

# Expected Contributions

1. Unified benchmark comparing RAG, PEFT, and Hybrid Adaptation.

2. Novel hybrid knowledge injection framework.

3. Comprehensive evaluation across QA and summarization.

4. Extensive low-resource analysis.

5. Open-source, reproducible research framework.

---

# Decisions Under Review

These choices may change after preliminary experiments:

* Generator model
* Embedding model
* Chunk size
* Retrieval backend
* Reranker
* LoRA rank
* Hybrid fusion strategy

Any modifications should be documented here before implementation changes are made.

---

# Decision Log

| Date       | Decision                                          | Reason                                             |
| ---------- | ------------------------------------------------- | -------------------------------------------------- |
| 2026-06-27 | Selected QA and Summarization as primary tasks    | Representative knowledge-intensive tasks           |
| 2026-06-27 | Chose RAG, PEFT, and Hybrid as comparison methods | Core research objective                            |
| 2026-06-27 | Selected FAISS as default vector store            | Efficient, lightweight, reproducible               |
| 2026-06-27 | Selected LoRA as default PEFT method              | Strong balance of efficiency and performance       |
| 2026-06-27 | Adopted YAML-driven configuration                 | Improves reproducibility and experiment management |

---

# Guiding Principle

Every implementation decision should satisfy the following criteria:

* Scientifically justified
* Reproducible
* Modular
* Extensible
* Appropriate for publication in a Q1 AI journal

If a proposed change conflicts with these principles, the rationale should be documented before the change is adopted.

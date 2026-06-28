# Adaptive Knowledge Injection

Adaptive Knowledge Injection for Low-Resource Knowledge-Intensive Language Tasks
is a research repository for comparing Retrieval-Augmented Generation (RAG),
Parameter-Efficient Fine-Tuning (PEFT), and Hybrid Adaptation.

The repository targets reproducible Q1-journal experiments for:

- Question Answering: PubMedQA and SciQ
- Summarization: CNN/DailyMail and GovReport

## Architecture

The architecture is documentation-driven and intentionally modular:

```text
configs/
src/utils/
src/datasets/
src/preprocessing/
src/retrieval/
src/models/
src/evaluation/
src/experiments/
notebooks/
```

Business logic belongs in `src/`. Notebooks are reserved for execution,
visualization, and analysis.

## Configuration

All configurable values are stored in YAML files under `configs/`.

- `datasets.yaml`: dataset registry, data paths, splits, low-resource ratios
- `preprocessing.yaml`: cleaning, filtering, tokenization, output validation
- `models.yaml`: generator model, quantization, generation settings
- `retrieval.yaml`: chunking, embedding, reranking, vector store, top-k
- `training.yaml`: seed, optimizer, scheduler, batch sizes, LoRA settings
- `evaluation.yaml`: task, retrieval, hallucination, efficiency, statistics metrics

## Current Status

The repository foundation is being prepared before implementation of dataset,
retrieval, model, evaluation, and experiment modules. See `docs/PROJECT_STATUS.md`
and `docs/TODO.md` for the active roadmap.

## Installation

For local Conda development:

```bash
conda env create -f environment.yml
conda activate adaptive-knowledge-injection
```

For pip-based environments:

```bash
pip install -r requirements.txt
```

## License

This project is released under the MIT License. See `LICENSE`.

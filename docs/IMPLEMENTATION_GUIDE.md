# IMPLEMENTATION_GUIDE

**Project:** Adaptive Knowledge Injection for Low-Resource Knowledge-Intensive Language Tasks

**Purpose:** Primary onboarding and implementation guide for human developers and
AI assistants.

**Status:** Utility foundation complete; dataset implementation pending.

**Last Updated:** 2026-06-28

---

# 1. Project Overview

This repository supports a Q1-journal research project on adaptive knowledge
injection for low-resource knowledge-intensive language tasks. The core research
objective is to compare three adaptation paradigms under controlled,
reproducible conditions:

- Retrieval-Augmented Generation (RAG)
- Parameter-Efficient Fine-Tuning (PEFT), primarily LoRA
- Hybrid Adaptation, combining retrieval with parameter-efficient adaptation

The supported tasks are Question Answering and Summarization. The active dataset
set is intentionally small and fixed for the initial benchmark: PubMedQA and
SciQ for Question Answering, CNN/DailyMail and GovReport for Summarization.

The benchmark strategy is comparative rather than single-score optimization.
The framework must make it possible to evaluate task performance, retrieval
quality, hallucination behavior, statistical significance, and computational
efficiency across low-resource data ratios.

This repository supports the paper by ensuring that every reported result can be
traced to a configuration file, an experiment ID, a logged runtime environment,
saved predictions, saved metrics, and reproducible analysis artifacts. The code
is not merely an implementation convenience; it is part of the scientific
evidence package.

The implementation philosophy is conservative: preserve the architecture, build
one layer at a time, keep business logic in `src/`, keep notebooks thin, and
avoid clever abstractions until repeated usage proves they are needed.

---

# 2. Repository Architecture

The repository is organized as a layered research software system:

```text
adaptive-knowledge-injection/

configs/       Centralized YAML configuration
data/          Raw, interim, processed, and split datasets
docs/          Architecture, standards, status, prompts, and research planning
notebooks/     Colab-oriented execution, analysis, and visualization
outputs/       Logs, metrics, predictions, figures, tables, and reports
checkpoints/   Model and vector-store artifacts generated during experiments
scripts/       Environment and automation scripts
src/           Core implementation
tests/         Unit, integration, and smoke tests
```

The package hierarchy under `src/` follows the research pipeline:

```text
src/
  utils/
  datasets/
  preprocessing/
  retrieval/
  models/
  evaluation/
  experiments/
```

The dependency direction is intentionally one-way:

```text
configs
  |
  v
utils
  |
  v
datasets
  |
  v
preprocessing
  |
  v
retrieval
  |
  v
models
  |
  v
evaluation
  |
  v
experiments
  |
  v
notebooks
```

Lower layers must not import higher layers. For example, `retrieval` may use
`utils`, but `utils` must never import `retrieval`. `models` may use retrieval
components for RAG and Hybrid inference, but retrieval code must not know about
model orchestration. This avoids circular imports, keeps modules independently
testable, and allows research components to be swapped without rewriting the
entire framework.

The architecture was designed this way because the paper requires separable
comparisons. RAG, PEFT, and Hybrid must share the same dataset preparation,
preprocessing, configuration, logging, and evaluation infrastructure. Any
shortcut that couples these layers will make the experiments harder to trust.

---

# 3. Development Philosophy

Every implementation must satisfy the following principles.

The repository must be modular. Each module should own one responsibility and
expose a small public API. If a module starts downloading data, cleaning text,
splitting datasets, and saving metrics, it is doing too much.

The repository must be configuration-driven. Model names, paths, seeds, LoRA
hyperparameters, chunk sizes, top-k values, batch sizes, and evaluation settings
belong in YAML files, not inline code.

The repository must be reproducible. Experiments must record seeds,
configuration snapshots, dataset names, model names, package versions, hardware
information, output paths, metrics, and timestamps.

The repository must separate research logic from execution surfaces. Business
logic belongs in `src/`; notebooks should call `src/` functions and display
results.

The repository must be deterministic wherever practical. Any randomized split,
low-resource sample, shuffle, model initialization, or bootstrap procedure must
derive from configured seeds.

The repository must remain extensible. Future datasets, retrievers, embedding
models, LLMs, PEFT methods, and tasks should extend existing interfaces rather
than introduce parallel architectures.

The repository must be publication-quality. Code should be readable, typed,
logged, documented, tested, and suitable for public release alongside the paper.

---

# 4. Package Responsibilities

## `src/utils`

Purpose:

`utils` contains repository-wide infrastructure. It is the foundation for every
other package.

Responsibilities:

- YAML configuration loading
- structured logging
- file I/O helpers
- seed management
- shared constants
- environment-independent path handling

Allowed dependencies:

- Python standard library
- lightweight dependencies listed in `requirements.txt`, such as PyYAML

Forbidden dependencies:

- datasets
- transformers
- torch-heavy model code
- retrieval, model, evaluation, or experiment packages

Expected public API:

- `load_config`
- `get_config`
- `get_logger`
- future I/O helpers
- future seed helpers
- future constants

Typical usage:

Downstream modules should load configuration through `utils.config`, initialize a
module logger through `utils.logger`, and use future I/O helpers for JSON, CSV,
Parquet, and directory creation.

Future extensions:

Add hardware inspection, configuration schema validation, reproducibility
snapshots, and output-directory management only if these are shared by multiple
packages.

## `src/datasets`

Purpose:

`datasets` owns public dataset acquisition, validation, loading, and conversion
into the repository's internal schema.

Responsibilities:

- download configured Hugging Face datasets
- validate expected columns and splits
- preserve raw data
- convert records into the unified schema
- expose loaded data to preprocessing

Allowed dependencies:

- `src.utils`
- Hugging Face Datasets
- pathlib-compatible I/O helpers

Forbidden dependencies:

- retrieval
- models
- evaluation
- experiments

Expected public API:

- dataset downloader functions or classes
- dataset validator functions or classes
- dataset loader functions returning standardized dataset objects

Typical usage:

The data preparation notebook or experiment runner calls dataset functions to
download and validate configured datasets, then passes standardized outputs to
preprocessing.

Future extensions:

Add new datasets by extending `configs/datasets.yaml` and implementing mapping
logic without changing downstream module contracts.

## `src/preprocessing`

Purpose:

`preprocessing` converts standardized dataset records into clean, validated,
split-ready artifacts.

Responsibilities:

- schema normalization
- text cleaning
- filtering
- train/validation/test splitting
- low-resource sampling
- preprocessing statistics

Allowed dependencies:

- `src.utils`
- `src.datasets` data objects or schema definitions
- pandas or Hugging Face Datasets where appropriate

Forbidden dependencies:

- retrieval index construction
- model loading
- evaluation metric computation

Expected public API:

- schema conversion helpers
- text cleaner
- deterministic splitter
- low-resource sampler

Typical usage:

Dataset outputs flow into preprocessing; preprocessing outputs are saved to
`data/processed/` and `data/splits/` for retrieval, training, and evaluation.

Future extensions:

Add language-specific cleaning, multilingual normalization, or task-specific
schema adapters while preserving the unified schema.

## `src/retrieval`

Purpose:

`retrieval` owns knowledge chunking, embedding, vector-store management,
retrieval, and reranking.

Responsibilities:

- chunk documents according to `retrieval.yaml`
- embed chunks
- build/load FAISS indexes
- retrieve top-k contexts
- optionally rerank retrieved candidates
- compute retrieval-specific artifacts for downstream evaluation

Allowed dependencies:

- `src.utils`
- processed/split data artifacts
- sentence-transformers
- FAISS
- optional reranker models

Forbidden dependencies:

- experiment orchestration
- PEFT training logic
- task metric aggregation

Expected public API:

- chunking utilities
- vector-store builder/loader
- retriever interface returning passages, scores, and metadata

Typical usage:

RAG and Hybrid model components call retrieval APIs to obtain context. Retrieval
evaluation uses retrieval outputs to compute recall, MRR, MAP, and nDCG.

Future extensions:

Add BM25, hybrid dense-sparse retrieval, alternative vector stores, and new
embedding models behind stable retrieval interfaces.

## `src/models`

Purpose:

`models` owns model loading and the three knowledge injection paradigms.

Responsibilities:

- base generator model loading
- automatic device selection
- RAG inference
- LoRA/PEFT setup and training logic
- Hybrid adaptation orchestration
- checkpoint save/load integration

Allowed dependencies:

- `src.utils`
- `src.retrieval` for RAG and Hybrid
- transformers
- torch
- PEFT
- optional GPU dependencies when available

Forbidden dependencies:

- experiment registry logic
- statistical analysis
- notebook-specific behavior

Expected public API:

- base model loader
- RAG pipeline class or function
- PEFT trainer/setup class or function
- Hybrid pipeline class or function

Typical usage:

Experiment runners instantiate model components from YAML configuration and pass
prepared datasets or retrieval contexts into them.

Future extensions:

Add new LLM families, QLoRA, AdaLoRA, model adapters, model ensembling, or
alternative generation strategies without changing dataset or evaluation code.

## `src/evaluation`

Purpose:

`evaluation` owns all metric computation, hallucination analysis, efficiency
measurement, and statistical testing.

Responsibilities:

- QA metrics
- summarization metrics
- retrieval metrics
- hallucination/faithfulness metrics
- efficiency metrics
- significance tests
- confidence intervals
- effect sizes

Allowed dependencies:

- `src.utils`
- saved predictions and metrics
- evaluate, rouge-score, sacrebleu, scipy, sklearn

Forbidden dependencies:

- model training
- dataset downloading
- notebook-only plotting logic

Expected public API:

- metric computation functions
- hallucination evaluator
- statistical test functions
- result aggregation helpers

Typical usage:

Experiment runners pass predictions and references to evaluation functions.
Analysis notebooks consume saved evaluation outputs.

Future extensions:

Add calibration metrics, robustness tests, adversarial perturbation metrics, or
new statistical corrections while preserving saved-output compatibility.

## `src/experiments`

Purpose:

`experiments` orchestrates full benchmark runs by connecting implemented layers.

Responsibilities:

- load configurations
- create timestamped experiment directories
- call dataset, preprocessing, retrieval, model, and evaluation modules
- save configuration snapshots
- save predictions, metrics, logs, and metadata
- maintain reproducible experiment execution

Allowed dependencies:

- all lower `src/` packages

Forbidden dependencies:

- notebook-only display code
- hardcoded experiment settings
- direct duplicated implementation from lower packages

Expected public API:

- `run_rag`
- `run_peft`
- `run_hybrid`
- `run_full_benchmark`

Typical usage:

Notebooks and command-line invocations call experiment runners. Experiment
runners do not contain core algorithmic logic; they coordinate existing modules.

Future extensions:

Add experiment registries, resumable runs, cloud execution wrappers, and result
aggregation while preserving the lower-layer APIs.

---

# 5. Module Dependency Graph

The foundational modules are `src/utils/config.py`, `src/utils/logger.py`,
`src/utils/io.py`, `src/utils/seed.py`, and `src/utils/constants.py`.

Shared utilities sit below all research modules:

```text
utils.config
utils.logger
utils.io
utils.seed
utils.constants
```

Independent layers should remain testable in isolation:

```text
datasets      depends on utils
preprocessing depends on utils + datasets schema/contracts
retrieval     depends on utils + processed data
models        depends on utils + retrieval where needed
evaluation    depends on utils + saved predictions/references
experiments   depends on all lower layers
```

The implementation order matters because each layer consumes artifacts from the
previous layer. Implementing `models` before `datasets` and `preprocessing`
would force fake data contracts that later need rewriting. Implementing
experiments before evaluation would create runners that cannot verify outputs.
Implementing notebooks before `src/` would violate the no-business-logic rule.

The correct order minimizes technical debt by allowing each package to be tested
against stable upstream contracts.

---

# 6. Configuration System

Configuration lives in `configs/` and is loaded through `src/utils/config.py`.
The current loader provides YAML loading, named config storage, and dot-notation
access.

Ownership is as follows:

- `datasets.yaml`: dataset names, dataset sources, dataset paths,
  train/validation/test splits, low-resource ratios
- `preprocessing.yaml`: cleaning, filtering, tokenization, preprocessing output,
  validation behavior
- `models.yaml`: generator model, quantization, generation parameters,
  inference batch size
- `retrieval.yaml`: embedding model, reranker, chunk size, overlap, vector store,
  retriever top-k and fetch-k
- `training.yaml`: random seed, optimizer, scheduler, epochs, learning rate,
  batch size, LoRA hyperparameters
- `evaluation.yaml`: evaluation metrics, hallucination metrics, efficiency
  metrics, statistical tests, confidence intervals, output formats

New parameters should be added to the file that owns their conceptual domain.
For example, a new LoRA dropout belongs in `training.yaml`; a new embedding
batch size belongs in `retrieval.yaml`; a new dataset column mapping belongs in
`datasets.yaml`.

Avoid duplication. If two modules need the same value, the value should still
have one source of truth. The consuming modules should receive that value through
configuration loading or explicit function parameters.

Configuration validation should be added before heavy implementation. At
minimum, validators should check required keys, value ranges, path types, known
task names, split totals, low-resource ratio bounds, and compatible model
settings.

---

# 7. Coding Patterns

Use `pathlib.Path` for all filesystem work. Avoid `os.path` unless a library
requires it.

Use structured logging through `src.utils.logger.get_logger`. Do not use
`print()` inside repository modules. Scripts may print human-facing diagnostics
when their purpose is command-line verification.

Use type hints for every public function and method. Prefer explicit return
types.

Use dataclasses for structured records such as dataset metadata, retrieval
results, experiment summaries, and metric bundles when a plain dictionary would
be ambiguous.

Use enums when a parameter has a constrained set of valid values, such as task
type, split name, retrieval strategy, or experiment status.

Use context managers for file handles, temporary directories, and managed
resources.

Use dependency injection for components that may vary by experiment. For
example, a retriever should be passed into a RAG pipeline instead of imported as
a hidden global.

Prefer small functions with clear inputs and outputs. Functions that mutate
global state or rely on implicit files are hard to test and should be avoided.

Anti-patterns that should never appear:

- hardcoded dataset paths
- hardcoded model names
- hardcoded CUDA assumptions
- wildcard imports
- silent `except: pass`
- notebooks containing business logic
- duplicated preprocessing logic in multiple modules
- hidden global mutable state
- experiment runners that reimplement lower-layer algorithms

---

# 8. Error Handling Strategy

Errors should be explicit, logged, and useful.

Configuration errors are fatal. Missing required keys, invalid ratios,
unsupported task names, or incompatible settings should fail early before a long
experiment starts.

Dataset errors should identify the dataset, split, expected field, and offending
record or file when possible. Raw download failures may be recoverable by retry,
but schema mismatch is fatal.

Preprocessing validation errors should distinguish between recoverable filtered
records and fatal schema failures. Dropped records should be counted and logged.

Retrieval errors should identify whether failure occurred in chunking,
embedding, FAISS index build/load, or reranking. Missing GPU should not be fatal;
retrieval should fall back to CPU unless the user explicitly requested GPU-only
execution.

Model errors should distinguish unavailable models, authentication issues,
device memory issues, optional GPU dependency issues, and generation failures.
GPU-only packages must be imported lazily and only when the selected runtime
needs them.

Evaluation errors should identify metric names, input lengths, missing
predictions, and incompatible task types.

Fatal errors should raise exceptions after logging. Recoverable errors should be
logged with enough context to audit them later.

---

# 9. Testing Strategy

Unit tests should be written for every public function once a module is
implemented. They should run on CPU-only Windows without requiring GPU,
bitsandbytes, large models, or network access.

Integration tests should verify interactions between adjacent layers:

- config + logger
- datasets + preprocessing
- preprocessing + retrieval input contracts
- retrieval + model context injection
- models + evaluation prediction format
- experiments + output directory creation

Smoke tests should run small, synthetic examples end to end. They should not use
large public datasets or train large models.

Notebook verification should confirm that notebooks import from `src/`, execute
the intended stage, and do not contain duplicated business logic.

Regression tests should be added when bugs affect reproducibility, saved output
formats, metrics, splitting, or experiment orchestration. Any bug that could
change a paper table deserves a regression test.

Testing checkpoints should occur after each package layer is implemented and
before moving to the next layer.

---

# 10. Google Colab Strategy

Local development is expected to happen on a CPU-only Windows machine with
Python 3.11 in Anaconda. This is the correct baseline for debugging, unit
testing, static validation, and repository maintenance.

Training, embedding generation, retrieval indexing, and full experiments are
expected to run on Google Colab GPU. Code must not require changes when moving
from local CPU development to Colab GPU execution.

Device selection should be automatic: use CUDA when `torch.cuda.is_available()`
is true, otherwise use CPU. Missing CUDA locally is expected and should not be
treated as a failure.

GPU-only packages such as bitsandbytes are optional for local development and
should be imported only when GPU quantization or GPU-specific training features
are requested. Missing bitsandbytes on Windows should produce a clear message or
skip, not a hard failure during ordinary imports.

No module should hardcode `cuda`. Configuration may request `auto`, `cpu`, or
`cuda`, but `cuda` should be validated against actual availability before use.

---

# 11. Environment Strategy

The repository maintains three environment surfaces:

- `requirements.txt` for pip and Colab-style setup
- `environment.yml` for local Conda development
- `pyproject.toml` for packaging and tool metadata

These files must remain synchronized. If a dependency is added to implementation
code, it must be added to the appropriate environment files in the same change.

Local Conda development should prioritize CPU-compatible packages. GPU-specific
packages should be optional or placed behind platform markers when possible.

`pyproject.toml` should capture project metadata and tool configuration such as
Black, isort, and pytest settings. It should not become a dumping ground for
experiment configuration; experiment configuration belongs in YAML.

The environment verification script should distinguish between local required
dependencies and optional Colab/GPU dependencies.

---

# 12. Experiment Workflow

The intended experiment lifecycle is:

```text
Repository setup
  |
  v
Dataset preparation
  |
  v
Preprocessing
  |
  v
RAG
  |
  v
PEFT
  |
  v
Hybrid
  |
  v
Evaluation
  |
  v
Statistics
  |
  v
Visualization
  |
  v
Paper tables
```

Each completed experiment must save configuration snapshots, logs, predictions,
metrics, runtime information, hardware information, and output artifacts.

Notebook roles:

- `01_environment.ipynb`: install dependencies, verify environment, check GPU
- `02_prepare_data.ipynb`: call dataset and preprocessing modules
- `03_build_rag.ipynb`: build retrieval artifacts and validate retrieval
- `04_train_peft.ipynb`: execute LoRA/PEFT training
- `05_build_hybrid.ipynb`: validate Hybrid integration
- `06_run_experiments.ipynb`: run benchmark experiments
- `07_analysis.ipynb`: statistics, visualization, and publication artifacts

Notebooks are execution surfaces. They should not contain implementations of
dataset loading, cleaning, retrieval, training, or metrics.

---

# 13. Coding Workflow

The expected workflow is:

```text
Confirm architecture
  |
  v
Implement one module
  |
  v
Write unit tests
  |
  v
Run manual verification
  |
  v
Integrate with notebook or runner
  |
  v
Update documentation
  |
  v
Commit
  |
  v
Move to next module
```

A module is not complete merely because it imports. It should have type hints,
Google-style docstrings, logging, deterministic behavior where relevant, tests,
and a clear integration path.

Avoid building several layers at once. A narrow, verified module is better than
a broad scaffold that hides broken contracts.

---

# 14. Git Workflow

Use small commits with clear scope. Recommended commit prefixes:

- `feat:` new implementation
- `fix:` bug fix
- `docs:` documentation-only change
- `config:` configuration change
- `test:` tests
- `refactor:` behavior-preserving code improvement
- `build:` dependency or environment metadata
- `research:` methodology or experiment change

Commit after each completed module and its tests. For example, `feat: implement
configuration validation` should include the implementation, tests, and any
documentation updates required by that module.

Use feature branches for substantial work. The default branch should remain
stable enough for other development sessions to start from.

Tagging should occur at meaningful repository milestones, such as completion of
the utility layer, dataset pipeline, retrieval pipeline, full benchmark runner,
and publication release.

---

# 15. Documentation Maintenance

Documentation is part of the repository contract.

Update `DESIGN_DECISIONS.md` when a research or architecture decision changes.
Examples: changing active datasets, changing default model families, changing
retrieval backend, or changing the hybrid strategy.

Update `REPOSITORY_MAP.md` when files or directories are added, removed, or
their responsibilities change.

Update `PROJECT_STATUS.md` when phase progress, current milestone, risks, or
next actions change.

Update `TODO.md` when implementation tasks are completed or reordered.

Update `EXPERIMENTS.md` when experiments are planned, run, failed, repeated, or
included in the paper.

Update `SESSION_CONTEXT.md` at handoff points so future sessions know what was
done, what remains, and what should not be touched.

Update `CHANGELOG.md` for meaningful implementation, configuration,
environment, documentation, or research changes.

Update `PAPER_PLAN.md` when repository artifacts affect manuscript structure,
figures, tables, or claims.

---

# 16. Common Mistakes to Avoid

Do not duplicate configuration values across YAML files. There should be one
source of truth for each parameter.

Do not create circular imports. If two modules need each other, the boundary is
wrong.

Do not hardcode paths. All paths should come from configuration or be derived
from the project root.

Do not hardcode CUDA. Local CPU-only development is expected.

Do not import GPU-only packages at module import time. Import them only inside
the code path that needs them.

Do not put business logic in notebooks. Notebooks should orchestrate and
visualize.

Do not duplicate preprocessing in dataset, retrieval, model, or experiment
modules.

Do not use global mutable state for experiment settings.

Do not silently overwrite experiment outputs. Use timestamped output
directories.

Do not implement a new parallel architecture for a future extension. Extend the
existing package boundary.

---

# 17. Future Extension Points

New datasets should be added through `configs/datasets.yaml` and dataset mapping
logic that emits the unified schema.

New retrievers should be implemented behind the retrieval interface, not inside
model code.

New embedding models should be configuration changes plus retrieval support,
not hardcoded branches.

New LLMs should be added through `models.yaml` and base model loading logic.

New PEFT methods should extend the PEFT module and training configuration while
preserving the RAG and Hybrid interfaces.

Multilingual datasets may require preprocessing extensions, language metadata,
and metric choices, but should still use the unified schema.

New language tasks should define schema expectations, metrics, and experiment
protocols before implementation.

Cloud execution should wrap experiment runners rather than replace them. The
core code should remain platform-independent.

---

# 18. AI Collaboration Guide

ChatGPT is responsible for research supervision, architecture review,
methodology, documentation, reviewer simulation, and high-level code review.

Codex is responsible for implementation, refactoring, bug fixing, tests, and
repository maintenance while preserving the documented architecture.

Google Colab is responsible for GPU execution, training, retrieval indexing,
large-scale experiments, evaluation runs, and figure/table production.

Every new AI session should first read:

1. `README.md`
2. `docs/DESIGN_DECISIONS.md`
3. `docs/CODING_STANDARD.md`
4. `docs/PROJECT_STATUS.md`
5. `docs/REPOSITORY_MAP.md`
6. `docs/TODO.md`
7. `docs/EXPERIMENTS.md`
8. `docs/SESSION_CONTEXT.md`
9. `docs/IMPLEMENTATION_GUIDE.md`

AI assistants should not redesign the repository unless explicitly instructed
and unless the relevant documentation is updated. They should make small,
auditable changes and avoid broad rewrites.

---

# 19. Implementation Order

Recommended implementation sequence:

```text
1. utils/config.py validation improvements
2. utils/logger.py verification
3. utils/io.py
4. utils/seed.py
5. utils/constants.py
6. utility tests
7. datasets/downloader.py
8. datasets/validator.py
9. datasets/loader.py
10. dataset tests and smoke checks
11. preprocessing/schema.py
12. preprocessing/cleaner.py
13. preprocessing/splitter.py
14. preprocessing tests and split reproducibility checks
15. retrieval/chunking.py
16. retrieval/vector_store.py
17. retrieval/retriever.py
18. retrieval tests and small FAISS smoke test
19. models/base_model.py
20. models/rag.py
21. models/peft.py
22. models/hybrid.py
23. model tests with tiny or mocked models
24. evaluation/metrics.py
25. evaluation/hallucination.py
26. evaluation/statistics.py
27. evaluation tests
28. experiments/run_rag.py
29. experiments/run_peft.py
30. experiments/run_hybrid.py
31. experiments/run_full_benchmark.py
32. experiment smoke tests
33. notebook integration
34. full Colab benchmark execution
35. analysis and paper artifact generation
```

This order minimizes technical debt because each layer has a stable upstream
contract before the next layer depends on it. It also creates natural testing
checkpoints and avoids building paper-facing experiment runners on unverified
infrastructure.

---

# 20. Repository Health Assessment

Current strengths:

The architecture is clear, layered, and aligned with the research methodology.
The documentation is unusually strong for an early-stage research repository.
The configuration ownership has been normalized. The local CPU and Colab GPU
execution strategy is now explicit. The active dataset scope is focused enough
to support a reproducible first benchmark.

Current weaknesses:

Most implementation modules are still empty. Tests have not yet been written.
Configuration schema validation is not complete. Environment verification needs
to distinguish local CPU requirements from optional Colab GPU requirements.
Notebook integration is not yet meaningful because the underlying modules are
not implemented.

Remaining work:

The utility layer is complete. Next, implement each package in the documented
order with tests and integration checkpoints. Add configuration validation
early. Build synthetic smoke tests before running large datasets. Keep
documentation updated as implementation decisions become concrete.

Implementation readiness:

The repository is ready to begin dataset-layer implementation after focused
utility tests are run from the verified local Anaconda environment. It is not
yet ready for retrieval, model, evaluation, or experiment implementation until
dataset and preprocessing contracts are stable.

Publication readiness:

The research plan and repository architecture support a publication-quality
workflow, but publication readiness depends on implementation, experiments,
statistical validation, and reproducible paper artifacts.

Scores:

| Dimension | Score | Assessment |
| --- | ---: | --- |
| Architecture | 9/10 | Clear, modular, and research-aligned |
| Maintainability | 8/10 | Utility foundation complete; research layers pending |
| Reproducibility | 8/10 | Good configuration plan; validation/logging still needed |
| Extensibility | 9/10 | Layered design supports future methods and datasets |
| Research Readiness | 7/10 | Methodology strong; empirical pipeline not implemented |

The most important near-term rule is simple: finish and test the foundation
before building research modules on top of it.

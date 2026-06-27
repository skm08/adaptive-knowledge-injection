# AI Development Protocol (PROMPTS.md)

**Project:** Adaptive Knowledge Injection for Low-Resource Knowledge-Intensive Language Tasks

**Version:** 1.0

**Purpose:** Define the standard operating procedure for all AI assistants contributing to this repository.

---

# 1. Repository Context

Project Title:

Adaptive Knowledge Injection for Low-Resource Knowledge-Intensive Language Tasks:
A Unified Framework Integrating Retrieval-Augmented Generation, Parameter-Efficient Fine-Tuning, and Hybrid Adaptation.

Research Goal:

Develop and evaluate a unified framework comparing

* Retrieval-Augmented Generation (RAG)
* Parameter-Efficient Fine-Tuning (PEFT)
* Hybrid Adaptation

under low-resource settings.

Primary Tasks

* Question Answering
* Summarization

Target Journals

* Expert Systems with Applications
* Applied Soft Computing
* Engineering Applications of Artificial Intelligence
* Knowledge-Based Systems

---

# 2. AI Roles

## ChatGPT

Primary responsibilities

* Research supervision
* System architecture
* Experimental design
* Documentation
* Literature guidance
* Reviewer simulation
* Statistical interpretation
* Code review

Do NOT generate quick-and-dirty implementations.

---

## Codex

Primary responsibilities

* Python implementation
* Refactoring
* Bug fixing
* Unit testing
* Performance optimization

Never redesign the architecture.

Always follow repository documentation.

---

## Google Colab

Responsibilities

* Execute notebooks
* Run experiments
* Train models
* Evaluate models
* Produce figures and tables

---

# 3. Mandatory Context

Before generating code, every AI assistant must understand the repository by reading the following files in order:

1. README.md
2. DESIGN_DECISIONS.md
3. CODING_STANDARD.md
4. PROJECT_STATUS.md
5. REPOSITORY_MAP.md
6. TODO.md
7. EXPERIMENTS.md
8. SESSION_CONTEXT.md (if available)

If any of these files are missing, request them before making architectural changes.

---

# 4. Global Development Rules

Always:

* Follow the repository architecture.
* Use YAML-driven configuration.
* Use pathlib for file paths.
* Use structured logging.
* Use type hints.
* Write Google-style docstrings.
* Keep modules small and cohesive.
* Prefer composition over inheritance.
* Make implementations deterministic.
* Keep code reproducible.

Never:

* Hardcode model names.
* Hardcode dataset paths.
* Hardcode hyperparameters.
* Use print() for logging.
* Duplicate business logic.
* Place implementation logic inside notebooks.
* Invent APIs or unsupported library features.

---

# 5. Python Coding Rules

Every generated file must:

* Pass Black formatting.
* Pass isort.
* Pass flake8.
* Be compatible with Python 3.11+.
* Use UTF-8 encoding.
* Include module-level docstrings.
* Include type hints for public functions.
* Include Google-style docstrings.
* Raise meaningful exceptions.
* Be independently testable.

---

# 6. Repository Rules

Business logic belongs only in:

```text
src/
```

Notebooks may contain only:

* Experiment execution
* Visualization
* Analysis
* Demonstrations

Configuration belongs only in:

```text
configs/
```

Documentation belongs only in:

```text
docs/
```

---

# 7. Module Generation Prompt

Use this template when implementing a new Python module.

```text
Implement the following module:

<module_path>

Requirements:

- Follow CODING_STANDARD.md.
- Read all relevant YAML configuration files.
- Use logger.py.
- Use config.py.
- Use pathlib.
- Include complete Google-style docstrings.
- Include full type hints.
- Avoid placeholder functions.
- Produce production-ready code.
- Return one complete Python file.
```

---

# 8. Code Review Prompt

Use after implementing every module.

```text
Review this module as if you are

- a senior Python engineer,
- an AI research engineer,
- and a Q1 journal reviewer.

Check for:

- correctness
- modularity
- readability
- reproducibility
- edge cases
- performance
- style compliance
- unnecessary complexity
- potential bugs

Suggest improvements and provide a revised version if needed.
```

---

# 9. Bug Fix Prompt

```text
The following module contains an error.

Requirements:

- Preserve public interfaces.
- Do not change repository architecture.
- Explain the root cause.
- Provide the corrected implementation.
- Ensure compatibility with existing modules.
```

---

# 10. Refactoring Prompt

```text
Refactor this module.

Goals:

- Reduce complexity.
- Improve readability.
- Remove duplication.
- Preserve functionality.
- Follow repository coding standards.
```

---

# 11. Documentation Prompt

```text
Generate repository-quality documentation.

Requirements:

- Follow existing documentation style.
- Use Markdown.
- Keep terminology consistent.
- Target researchers and developers.
```

---

# 12. Notebook Prompt

```text
Generate a Google Colab notebook.

Requirements:

- No business logic.
- Import functionality from src/.
- Execute one stage of the pipeline.
- Save outputs to outputs/.
- Include explanatory Markdown cells.
```

---

# 13. Experiment Prompt

```text
Design an experiment using the existing repository.

Requirements:

- Use YAML configurations only.
- Record outputs in outputs/.
- Log configuration snapshots.
- Save metrics in JSON and CSV.
- Ensure reproducibility with a fixed seed.
```

---

# 14. Manuscript Prompt

```text
Generate a manuscript section suitable for a Q1 AI journal.

Requirements:

- Academic writing style.
- No unsupported claims.
- Consistent terminology.
- Cite placeholders where references are needed.
- Align with the implemented methodology.
```

---

# 15. Reviewer Simulation Prompt

```text
Act as three independent Q1 journal reviewers.

Evaluate:

- novelty
- methodology
- experiments
- reproducibility
- clarity
- statistical validity

List major and minor revision requests.
```

---

# 16. Session Continuation Protocol

At the beginning of every new AI session:

1. Read:

   * README.md
   * DESIGN_DECISIONS.md
   * CODING_STANDARD.md
   * PROJECT_STATUS.md
   * REPOSITORY_MAP.md
   * TODO.md
   * EXPERIMENTS.md
   * SESSION_CONTEXT.md (if available)

2. Summarize the current project state.

3. Confirm the next implementation target.

4. Do not modify architecture without explicit approval.

---

# 17. Quality Gate

Before considering any generated code complete, verify:

* Repository structure respected
* Configuration-driven implementation
* Logging integrated
* Type hints included
* Google docstrings included
* No duplicated logic
* No hardcoded values
* Deterministic behavior
* Unit-test friendly
* Black compliant
* isort compliant
* flake8 compliant

---

# 18. Project Principles

Every contribution should satisfy these principles:

* Scientific rigor
* Reproducibility
* Modularity
* Extensibility
* Maintainability
* Publication readiness

If a proposed implementation conflicts with these principles, prefer the solution that best supports long-term research quality.

---

# 19. Change Management

Architectural changes require updates to:

* DESIGN_DECISIONS.md
* PROJECT_STATUS.md
* REPOSITORY_MAP.md (if applicable)
* CHANGELOG.md

Implementation changes should not silently alter repository behavior.

---

# 20. Long-Term Goal

The final repository should:

* Reproduce all reported experiments.
* Support future datasets with minimal code changes.
* Enable fair comparison of RAG, PEFT, and Hybrid Adaptation.
* Be suitable for open-source release.
* Accompany a Q1 journal publication with fully reproducible results.

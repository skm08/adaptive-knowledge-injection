# Coding Standard

Project:

Adaptive Knowledge Injection for Low-Resource Knowledge-Intensive Language Tasks

Version:

1.0

-------------------------------------------------------------------------------

## Purpose

This document defines the coding standards for the entire repository.

Every Python module MUST follow these rules.

Goals:

- Readability
- Maintainability
- Reproducibility
- Scalability
- Research-quality implementation
- Production-quality software engineering

-------------------------------------------------------------------------------

# Python Version

Python >= 3.11

-------------------------------------------------------------------------------

# Style Guide

Follow:

- PEP8
- PEP257
- Google Python Style Guide (Docstrings)

Maximum line length:

88 characters

-------------------------------------------------------------------------------

# Type Hints

Every public function MUST include type hints.

Example

```python
def load_dataset(path: Path) -> Dataset:
```

Avoid

```python
def load_dataset(path):
```

-------------------------------------------------------------------------------

# Docstrings

Every public class and function MUST contain Google-style docstrings.

Example

```python
def clean_text(text: str) -> str:
    """
    Clean raw input text.

    Args:
        text:
            Input document.

    Returns:
        Cleaned document.
    """
```

-------------------------------------------------------------------------------

# Imports

Order imports as follows.

1 Standard Library

2 Third-party Libraries

3 Local Project Modules

Example

```python
from pathlib import Path

import pandas as pd

from src.utils.logger import get_logger
```

Never use wildcard imports.

Incorrect

```python
from module import *
```

-------------------------------------------------------------------------------

# File Structure

Every module should follow this order.

1 Imports

2 Constants

3 Classes

4 Helper Functions

5 Main Functions

6 __main__

-------------------------------------------------------------------------------

# Naming Convention

Variables

snake_case

Functions

snake_case

Classes

PascalCase

Constants

UPPER_CASE

Private Functions

_prefix()

-------------------------------------------------------------------------------

# Paths

Never hardcode paths.

Incorrect

```python
data/raw/file.csv
```

Correct

```python
config.data.raw_dir
```

Use

```python
pathlib.Path
```

Never use

```python
os.path
```

unless absolutely necessary.

-------------------------------------------------------------------------------

# Configuration

All configurable values MUST come from YAML.

Never hardcode

- learning rate
- chunk size
- model names
- directories
- batch size
- epochs
- top-k
- LoRA parameters

-------------------------------------------------------------------------------

# Logging

Never use

```python
print()
```

Instead use

```python
logger.info()

logger.warning()

logger.error()
```

Every module should initialize a logger.

Example

```python
logger = get_logger(__name__)
```

-------------------------------------------------------------------------------

# Exceptions

Never suppress exceptions.

Incorrect

```python
except:
    pass
```

Correct

```python
except Exception as e:
    logger.exception(e)
    raise
```

-------------------------------------------------------------------------------

# Randomness

Every module must support reproducibility.

Always use

```python
set_seed()
```

Never generate random numbers without setting a seed.

-------------------------------------------------------------------------------

# DataFrames

Prefer

```python
pandas
```

Avoid unnecessary loops.

Vectorized operations are preferred.

-------------------------------------------------------------------------------

# Hugging Face Datasets

Always use

```python
Dataset

DatasetDict
```

Avoid converting to pandas unless necessary.

-------------------------------------------------------------------------------

# Model Loading

All models must be loaded through configuration.

Never write

```python
AutoModel.from_pretrained("model")
```

Instead

```python
config.generator.model
```

-------------------------------------------------------------------------------

# Device Handling

Never hardcode

cuda

cpu

Use

```python
device = config.device
```

-------------------------------------------------------------------------------

# Functions

Functions should perform ONE task.

Bad

```python
download()

clean()

split()

save()
```

inside one function.

Good

Separate functions.

-------------------------------------------------------------------------------

# Function Length

Target

20–40 lines

Maximum

60 lines

Longer functions should be refactored.

-------------------------------------------------------------------------------

# Class Design

Prefer composition over inheritance.

Keep classes focused.

-------------------------------------------------------------------------------

# Comments

Explain WHY.

Do not explain obvious code.

Bad

```python
i += 1
```

Good

```python
# Reserve one passage for the query itself.
```

-------------------------------------------------------------------------------

# TODO

Use

```python
TODO(username):
```

Example

```python
TODO(research):

Implement Hybrid Retrieval.
```

-------------------------------------------------------------------------------

# Notebook Rules

Notebooks should NOT contain business logic.

Allowed

- visualization

- experiments

- analysis

Not allowed

- preprocessing implementation

- retrieval implementation

- model implementation

These belong in

src/

-------------------------------------------------------------------------------

# Testing

Every module should be independently testable.

Avoid hidden dependencies.

-------------------------------------------------------------------------------

# Reproducibility

Every experiment must log

- seed

- dataset

- model

- hyperparameters

- metrics

- timestamp

-------------------------------------------------------------------------------

# Performance

Prefer

batch operations

Avoid

for-loops over tensors

Use

PyTorch vectorization whenever possible.

-------------------------------------------------------------------------------

# Documentation

Every public module must begin with

Project

Module

Purpose

Dependencies

Author

Version

-------------------------------------------------------------------------------

# Dependencies

Never import libraries that are not listed in

requirements.txt

-------------------------------------------------------------------------------

# Code Duplication

Never duplicate code.

If functionality is reused twice,

move it into

src/utils/

-------------------------------------------------------------------------------

# Output Files

Never overwrite previous experiments.

Always use timestamped output directories.

-------------------------------------------------------------------------------

# Experiment Naming

Use

YYYYMMDD_HHMMSS

Example

20260701_153010

-------------------------------------------------------------------------------

# Git

Commit after every completed module.

Commit message format

TYPE: Short description

Examples

feat: add dataset downloader

fix: improve retrieval pipeline

docs: update repository map

refactor: simplify logger

-------------------------------------------------------------------------------

# Pull Requests

One logical feature per pull request.

-------------------------------------------------------------------------------

# Linting

The code should pass

black

isort

flake8

without modification.

-------------------------------------------------------------------------------

# Research Philosophy

The objective is not merely to produce working code.

Every implementation should be:

- reproducible
- modular
- extensible
- well documented
- suitable for open-source release
- suitable for publication alongside a Q1 journal article

-------------------------------------------------------------------------------

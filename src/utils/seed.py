"""
Project: Adaptive Knowledge Injection
Module: src.utils.seed
Purpose: Provide deterministic seeding and automatic device selection helpers.
Dependencies: os, random, importlib
Author: Adaptive Knowledge Injection Research
Version: 1.0.0
"""

from __future__ import annotations

import importlib
import os
import random
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from src.utils.config import ConfigNode, load_config
from src.utils.constants import DEFAULT_RANDOM_SEED, TRAINING_CONFIG
from src.utils.logger import get_logger


logger = get_logger(__name__, log_to_file=False)


class SeedError(Exception):
    """Raised when seed configuration is invalid."""


@dataclass(frozen=True)
class SeedState:
    """Summary of applied seeding behavior.

    Attributes:
        seed:
            Seed value applied to available libraries.
        deterministic:
            Whether deterministic backend settings were requested.
        numpy_seeded:
            Whether NumPy was available and seeded.
        torch_seeded:
            Whether PyTorch was available and seeded.
        cuda_seeded:
            Whether CUDA devices were available and seeded.
    """

    seed: int
    deterministic: bool
    numpy_seeded: bool
    torch_seeded: bool
    cuda_seeded: bool


def _optional_import(module_name: str) -> Any | None:
    """Import an optional dependency without failing module import.

    Args:
        module_name:
            Module name to import.

    Returns:
        Imported module, or None when unavailable.
    """

    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None


def validate_seed(seed: int) -> int:
    """Validate and return a seed value.

    Args:
        seed:
            Candidate random seed.

    Returns:
        Validated seed.

    Raises:
        SeedError: If the seed is not a non-negative integer.
    """

    if not isinstance(seed, int):
        raise SeedError("Seed must be an integer.")

    if seed < 0:
        raise SeedError("Seed must be non-negative.")

    return seed


def set_seed(seed: int = DEFAULT_RANDOM_SEED, deterministic: bool = True) -> SeedState:
    """Seed Python, NumPy, and PyTorch when available.

    This function is safe on CPU-only Windows machines and Google Colab GPU
    runtimes. Optional libraries are imported lazily.

    Args:
        seed:
            Seed value to apply.
        deterministic:
            Whether to request deterministic PyTorch backend behavior.

    Returns:
        Summary of which libraries were seeded.
    """

    seed = validate_seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)

    numpy_seeded = False
    torch_seeded = False
    cuda_seeded = False

    numpy = _optional_import("numpy")

    if numpy is not None:
        numpy.random.seed(seed)
        numpy_seeded = True

    torch = _optional_import("torch")

    if torch is not None:
        torch.manual_seed(seed)
        torch_seeded = True

        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
            cuda_seeded = True

        if deterministic:
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False

    logger.info(
        "Seed set to %s (numpy=%s, torch=%s, cuda=%s)",
        seed,
        numpy_seeded,
        torch_seeded,
        cuda_seeded,
    )

    return SeedState(
        seed=seed,
        deterministic=deterministic,
        numpy_seeded=numpy_seeded,
        torch_seeded=torch_seeded,
        cuda_seeded=cuda_seeded,
    )


def get_seed_from_config(config: ConfigNode | Mapping[str, Any]) -> int:
    """Extract a seed value from a loaded configuration.

    Args:
        config:
            Configuration node or mapping containing a top-level `seed`.

    Returns:
        Validated seed value.
    """

    if isinstance(config, ConfigNode):
        seed = config.seed
    else:
        seed = config.get("seed", DEFAULT_RANDOM_SEED)

    return validate_seed(int(seed))


def set_seed_from_config(
    config_path: str = f"configs/{TRAINING_CONFIG}",
    deterministic: bool | None = None,
) -> SeedState:
    """Load training configuration and apply its seed settings.

    Args:
        config_path:
            Path to the training YAML configuration.
        deterministic:
            Optional override for deterministic backend behavior. When omitted,
            the value is read from the training configuration.

    Returns:
        Summary of applied seeding behavior.
    """

    config = load_config(config_path)
    seed = get_seed_from_config(config)

    if deterministic is None:
        deterministic = bool(getattr(config, "deterministic", True))

    return set_seed(seed=seed, deterministic=deterministic)


def get_device(preferred_device: str = "auto") -> str:
    """Resolve a runtime device without hard-coding CUDA assumptions.

    Args:
        preferred_device:
            `auto`, `cpu`, or `cuda`.

    Returns:
        Resolved device string.

    Raises:
        SeedError: If an unsupported device value is provided.
    """

    normalized = preferred_device.lower()

    if normalized not in {"auto", "cpu", "cuda"}:
        raise SeedError(f"Unsupported device: {preferred_device}")

    if normalized == "cpu":
        return "cpu"

    torch = _optional_import("torch")
    cuda_available = bool(torch is not None and torch.cuda.is_available())

    if normalized == "cuda":
        if cuda_available:
            return "cuda"

        logger.warning("CUDA requested but unavailable; falling back to CPU.")
        return "cpu"

    return "cuda" if cuda_available else "cpu"

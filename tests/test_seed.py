"""Tests for deterministic seed and device utilities."""

from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from src.utils.config import ConfigNode
from src.utils.seed import (
    SeedError,
    get_device,
    get_seed_from_config,
    set_seed,
    validate_seed,
)


def test_validate_seed_accepts_non_negative_integer() -> None:
    """Valid integer seeds should be returned unchanged."""

    assert validate_seed(42) == 42


@pytest.mark.parametrize("seed", [-1, "42"])
def test_validate_seed_rejects_invalid_values(seed: object) -> None:
    """Invalid seeds should raise SeedError."""

    with pytest.raises(SeedError):
        validate_seed(seed)  # type: ignore[arg-type]


def test_set_seed_without_optional_libraries(monkeypatch: pytest.MonkeyPatch) -> None:
    """set_seed should work when NumPy and PyTorch are unavailable."""

    monkeypatch.setattr("src.utils.seed._optional_import", lambda _: None)

    state = set_seed(seed=123, deterministic=True)
    first_value = random.random()

    set_seed(seed=123, deterministic=True)
    second_value = random.random()

    assert state.seed == 123
    assert state.numpy_seeded is False
    assert state.torch_seeded is False
    assert state.cuda_seeded is False
    assert first_value == second_value


def test_get_seed_from_config_node() -> None:
    """Seed extraction should support ConfigNode."""

    config = ConfigNode({"seed": 99})

    assert get_seed_from_config(config) == 99


def test_get_seed_from_mapping_defaults_when_missing() -> None:
    """Seed extraction should use the default seed when mapping omits seed."""

    assert get_seed_from_config({}) == 42


def test_get_device_returns_cpu_when_torch_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Automatic device selection should support CPU-only environments."""

    monkeypatch.setattr("src.utils.seed._optional_import", lambda _: None)

    assert get_device("auto") == "cpu"


def test_get_device_falls_back_when_cuda_requested_but_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Explicit CUDA requests should fall back to CPU when CUDA is unavailable."""

    fake_torch = SimpleNamespace(
        cuda=SimpleNamespace(is_available=lambda: False),
    )
    monkeypatch.setattr("src.utils.seed._optional_import", lambda _: fake_torch)

    assert get_device("cuda") == "cpu"


def test_get_device_uses_cuda_when_available(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Automatic and explicit CUDA selection should work when CUDA is available."""

    fake_torch = SimpleNamespace(
        cuda=SimpleNamespace(is_available=lambda: True),
    )
    monkeypatch.setattr("src.utils.seed._optional_import", lambda _: fake_torch)

    assert get_device("auto") == "cuda"
    assert get_device("cuda") == "cuda"


def test_get_device_rejects_unknown_device() -> None:
    """Unknown device strings should fail clearly."""

    with pytest.raises(SeedError):
        get_device("tpu")


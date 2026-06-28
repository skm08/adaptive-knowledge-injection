"""
Project: Adaptive Knowledge Injection
Module: scripts.verify_environment
Purpose: Verify local or Colab environment readiness before implementation.
Dependencies: importlib, pathlib, platform, sys
Author: Adaptive Knowledge Injection Research
Version: 1.0.0
"""

from __future__ import annotations

import importlib
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType


MIN_PYTHON_VERSION = (3, 11)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PACKAGES = {
    "accelerate": "accelerate",
    "bitsandbytes": "bitsandbytes",
    "datasets": "datasets",
    "evaluate": "evaluate",
    "faiss": "faiss",
    "huggingface_hub": "huggingface-hub",
    "langchain": "langchain",
    "langchain_text_splitters": "langchain-text-splitters",
    "matplotlib": "matplotlib",
    "nltk": "nltk",
    "numpy": "numpy",
    "pandas": "pandas",
    "peft": "peft",
    "pyarrow": "pyarrow",
    "yaml": "PyYAML",
    "rouge_score": "rouge-score",
    "sacrebleu": "sacrebleu",
    "scipy": "scipy",
    "sentence_transformers": "sentence-transformers",
    "sklearn": "scikit-learn",
    "tensorboard": "tensorboard",
    "torch": "torch",
    "tqdm": "tqdm",
    "transformers": "transformers",
}


@dataclass(frozen=True)
class CheckResult:
    """Result of one environment verification check."""

    name: str
    passed: bool
    detail: str


def _format_status(passed: bool) -> str:
    """Return a readable status label."""

    return "PASS" if passed else "FAIL"


def _import_module(module_name: str) -> tuple[ModuleType | None, str | None]:
    """Import a module and return the module or an error message."""

    try:
        return importlib.import_module(module_name), None
    except Exception as exc:  # noqa: BLE001 - diagnostics should catch all.
        return None, f"{type(exc).__name__}: {exc}"


def _get_version(module: ModuleType) -> str:
    """Return a module version when available."""

    return str(getattr(module, "__version__", "version unavailable"))


def check_python_version() -> CheckResult:
    """Verify the active Python version."""

    current = sys.version_info[:3]
    passed = current >= MIN_PYTHON_VERSION
    detail = (
        f"Python {platform.python_version()} "
        f"(required >= {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]})"
    )
    return CheckResult("Python version", passed, detail)


def check_package(module_name: str, package_name: str) -> CheckResult:
    """Verify one package import and version."""

    module, error = _import_module(module_name)

    if module is None:
        return CheckResult(package_name, False, f"import failed: {error}")

    return CheckResult(package_name, True, _get_version(module))


def check_cuda(torch_module: ModuleType | None) -> list[CheckResult]:
    """Verify CUDA visibility and PyTorch GPU support."""

    if torch_module is None:
        return [
            CheckResult("CUDA availability", False, "torch import unavailable"),
            CheckResult("PyTorch GPU support", False, "torch import unavailable"),
        ]

    cuda_available = bool(torch_module.cuda.is_available())
    cuda_detail = f"torch.cuda.is_available() = {cuda_available}"

    if not cuda_available:
        return [
            CheckResult("CUDA availability", False, cuda_detail),
            CheckResult("PyTorch GPU support", False, "no CUDA device visible"),
        ]

    device_count = torch_module.cuda.device_count()
    device_names = [
        torch_module.cuda.get_device_name(index) for index in range(device_count)
    ]
    gpu_detail = f"{device_count} CUDA device(s): {', '.join(device_names)}"

    return [
        CheckResult("CUDA availability", True, cuda_detail),
        CheckResult("PyTorch GPU support", True, gpu_detail),
    ]


def check_project_import() -> CheckResult:
    """Verify that the project root supports importing `src`."""

    project_root = str(PROJECT_ROOT)

    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    module, error = _import_module("src")

    if module is None:
        return CheckResult("Project import", False, f"import src failed: {error}")

    return CheckResult("Project import", True, f"imported src from {PROJECT_ROOT}")


def print_result(result: CheckResult) -> None:
    """Print a single check result."""

    print(f"[{_format_status(result.passed)}] {result.name}: {result.detail}")


def main() -> int:
    """Run all environment verification checks."""

    print("=" * 80)
    print("Adaptive Knowledge Injection - Environment Verification")
    print("=" * 80)
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Platform: {platform.platform()}")
    print("")

    results: list[CheckResult] = [check_python_version()]

    imported_modules: dict[str, ModuleType | None] = {}

    for module_name, package_name in REQUIRED_PACKAGES.items():
        module, error = _import_module(module_name)
        imported_modules[module_name] = module

        if module is None:
            results.append(
                CheckResult(package_name, False, f"import failed: {error}")
            )
        else:
            results.append(CheckResult(package_name, True, _get_version(module)))

    results.extend(check_cuda(imported_modules.get("torch")))
    results.append(check_project_import())

    for result in results:
        print_result(result)

    failed = [result for result in results if not result.passed]

    print("")
    print("=" * 80)
    print(f"Summary: {len(results) - len(failed)} passed, {len(failed)} failed")

    if failed:
        print("Final status: FAIL")
        print("Failed checks:")
        for result in failed:
            print(f"- {result.name}: {result.detail}")
        return 1

    print("Final status: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

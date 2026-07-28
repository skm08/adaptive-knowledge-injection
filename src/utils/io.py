"""
Project: Adaptive Knowledge Injection
Module: src.utils.io
Purpose: Provide pathlib-based file I/O helpers for repository modules.
Dependencies: json, pathlib, shutil, yaml
Author: Adaptive Knowledge Injection Research
Version: 1.0.0
"""

from __future__ import annotations

import json
import shutil
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

import yaml

from src.utils.config import ConfigNode, load_config
from src.utils.constants import DEFAULT_ENCODING, DEFAULT_JSON_INDENT, PROJECT_ROOT
from src.utils.logger import get_logger


logger = get_logger(__name__, log_to_file=False)


class IOErrorContextError(Exception):
    """Raised when repository file I/O cannot be completed."""


def resolve_path(path: str | Path, root: str | Path | None = None) -> Path:
    """Resolve a path relative to a root or the project root.

    Args:
        path:
            Absolute path or project-relative path.
        root:
            Optional root for relative paths. Defaults to the project root.

    Returns:
        Resolved absolute path.
    """

    candidate = Path(path)

    if candidate.is_absolute():
        return candidate.resolve()

    base = Path(root).resolve() if root is not None else PROJECT_ROOT
    return (base / candidate).resolve()


def ensure_directory(path: str | Path) -> Path:
    """Create a directory if it does not already exist.

    Args:
        path:
            Directory path.

    Returns:
        Resolved directory path.
    """

    directory = resolve_path(path)
    directory.mkdir(parents=True, exist_ok=True)
    logger.debug("Ensured directory exists: %s", directory)
    return directory


def ensure_parent_dir(path: str | Path) -> Path:
    """Create a file path's parent directory if needed.

    Args:
        path:
            File path whose parent directory should exist.

    Returns:
        Resolved file path.
    """

    file_path = resolve_path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    logger.debug("Ensured parent directory exists: %s", file_path.parent)
    return file_path


def path_exists(path: str | Path) -> bool:
    """Return whether a path exists.

    Args:
        path:
            Path to inspect.

    Returns:
        True when the path exists.
    """

    return resolve_path(path).exists()


def read_text(path: str | Path, encoding: str = DEFAULT_ENCODING) -> str:
    """Read a UTF-compatible text file.

    Args:
        path:
            Text file path.
        encoding:
            Text encoding.

    Returns:
        File contents.
    """

    file_path = resolve_path(path)
    return file_path.read_text(encoding=encoding)


def write_text(
    path: str | Path,
    content: str,
    encoding: str = DEFAULT_ENCODING,
) -> Path:
    """Write text to a file, creating parent directories as needed.

    Args:
        path:
            Output file path.
        content:
            Text content.
        encoding:
            Text encoding.

    Returns:
        Resolved output path.
    """

    file_path = ensure_parent_dir(path)
    file_path.write_text(content, encoding=encoding)
    logger.debug("Wrote text file: %s", file_path)
    return file_path


def read_json(path: str | Path, encoding: str = DEFAULT_ENCODING) -> Any:
    """Read a JSON file.

    Args:
        path:
            JSON file path.
        encoding:
            Text encoding.

    Returns:
        Parsed JSON content.
    """

    file_path = resolve_path(path)

    with file_path.open("r", encoding=encoding) as file:
        return json.load(file)


def write_json(
    path: str | Path,
    data: Any,
    encoding: str = DEFAULT_ENCODING,
    indent: int = DEFAULT_JSON_INDENT,
) -> Path:
    """Write JSON data to a file.

    Args:
        path:
            Output JSON file path.
        data:
            JSON-serializable data.
        encoding:
            Text encoding.
        indent:
            JSON indentation level.

    Returns:
        Resolved output path.
    """

    file_path = ensure_parent_dir(path)

    with file_path.open("w", encoding=encoding) as file:
        json.dump(data, file, indent=indent, ensure_ascii=False)
        file.write("\n")

    logger.debug("Wrote JSON file: %s", file_path)
    return file_path


def read_yaml(path: str | Path, encoding: str = DEFAULT_ENCODING) -> Any:
    """Read a YAML file.

    Args:
        path:
            YAML file path.
        encoding:
            Text encoding.

    Returns:
        Parsed YAML content.
    """

    file_path = resolve_path(path)

    with file_path.open("r", encoding=encoding) as file:
        return yaml.safe_load(file)


def write_yaml(
    path: str | Path,
    data: Any,
    encoding: str = DEFAULT_ENCODING,
) -> Path:
    """Write YAML data to a file.

    Args:
        path:
            Output YAML file path.
        data:
            YAML-serializable data.
        encoding:
            Text encoding.

    Returns:
        Resolved output path.
    """

    file_path = ensure_parent_dir(path)

    with file_path.open("w", encoding=encoding) as file:
        yaml.safe_dump(data, file, sort_keys=False, allow_unicode=True)

    logger.debug("Wrote YAML file: %s", file_path)
    return file_path


def load_yaml_config(
    path: str | Path,
    config_name: str | None = None,
) -> ConfigNode:
    """Load a YAML file through the shared configuration manager.

    Args:
        path:
            YAML configuration path.
        config_name:
            Optional configuration alias.

    Returns:
        Loaded configuration node.
    """

    return load_config(resolve_path(path), config_name=config_name)


def copy_file(source: str | Path, destination: str | Path) -> Path:
    """Copy one file to a destination path.

    Args:
        source:
            Source file path.
        destination:
            Destination file path.

    Returns:
        Resolved destination path.

    Raises:
        FileNotFoundError: If the source file does not exist.
    """

    source_path = resolve_path(source)

    if not source_path.is_file():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    destination_path = ensure_parent_dir(destination)
    shutil.copy2(source_path, destination_path)
    logger.debug("Copied file from %s to %s", source_path, destination_path)
    return destination_path


def list_files(
    directory: str | Path,
    pattern: str = "*",
    recursive: bool = False,
) -> list[Path]:
    """List files in a directory.

    Args:
        directory:
            Directory to inspect.
        pattern:
            Glob pattern.
        recursive:
            Whether to search recursively.

    Returns:
        Sorted list of matching files.
    """

    directory_path = resolve_path(directory)
    iterator: Iterable[Path]

    if recursive:
        iterator = directory_path.rglob(pattern)
    else:
        iterator = directory_path.glob(pattern)

    return sorted(path for path in iterator if path.is_file())


def save_config_snapshot(
    config_paths: Mapping[str, str | Path],
    output_dir: str | Path,
) -> dict[str, Path]:
    """Copy configuration files into an output directory.

    Args:
        config_paths:
            Mapping from snapshot name to config path.
        output_dir:
            Directory where snapshots should be copied.

    Returns:
        Mapping from snapshot name to copied file path.
    """

    snapshot_dir = ensure_directory(output_dir)
    copied_paths: dict[str, Path] = {}

    for name, config_path in config_paths.items():
        source_path = resolve_path(config_path)
        destination = snapshot_dir / source_path.name
        copied_paths[name] = copy_file(source_path, destination)

    return copied_paths

"""Tests for pathlib-based I/O utilities."""

from __future__ import annotations

from pathlib import Path

from src.utils import io
from src.utils.config import ConfigNode, config_manager


def test_resolve_path_uses_project_root_for_relative_paths(tmp_path: Path) -> None:
    """Relative paths should resolve under the provided root."""

    resolved = io.resolve_path("nested/file.txt", root=tmp_path)

    assert resolved == (tmp_path / "nested" / "file.txt").resolve()


def test_resolve_path_keeps_absolute_paths(tmp_path: Path) -> None:
    """Absolute paths should remain absolute after resolution."""

    absolute_path = tmp_path / "file.txt"

    assert io.resolve_path(absolute_path) == absolute_path.resolve()


def test_ensure_directory_creates_directory(tmp_path: Path) -> None:
    """ensure_directory should create missing directories."""

    directory = io.ensure_directory(tmp_path / "a" / "b")

    assert directory.is_dir()


def test_text_round_trip(tmp_path: Path) -> None:
    """Text helpers should write and read UTF-8 content."""

    path = tmp_path / "notes" / "sample.txt"

    written_path = io.write_text(path, "hello")

    assert written_path == path.resolve()
    assert io.read_text(path) == "hello"


def test_json_round_trip(tmp_path: Path) -> None:
    """JSON helpers should preserve structured data."""

    path = tmp_path / "data" / "sample.json"
    data = {"name": "aki", "scores": [1, 2, 3]}

    io.write_json(path, data)

    assert io.read_json(path) == data


def test_yaml_round_trip(tmp_path: Path) -> None:
    """YAML helpers should preserve simple mappings."""

    path = tmp_path / "config" / "sample.yaml"
    data = {"seed": 42, "nested": {"enabled": True}}

    io.write_yaml(path, data)

    assert io.read_yaml(path) == data


def test_load_yaml_config_uses_shared_config_manager(tmp_path: Path) -> None:
    """load_yaml_config should return a ConfigNode from config.py."""

    config_manager.clear()
    path = tmp_path / "training.yaml"
    io.write_yaml(path, {"seed": 123})

    config = io.load_yaml_config(path, config_name="test_training")

    assert isinstance(config, ConfigNode)
    assert config.seed == 123
    assert config_manager.get("test_training").seed == 123


def test_copy_file_copies_content(tmp_path: Path) -> None:
    """copy_file should copy source content and create parent directories."""

    source = tmp_path / "source.txt"
    destination = tmp_path / "nested" / "destination.txt"
    source.write_text("content", encoding="utf-8")

    copied_path = io.copy_file(source, destination)

    assert copied_path == destination.resolve()
    assert destination.read_text(encoding="utf-8") == "content"


def test_list_files_supports_patterns_and_recursion(tmp_path: Path) -> None:
    """list_files should filter by pattern and optionally recurse."""

    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "b.md").write_text("b", encoding="utf-8")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "c.txt").write_text("c", encoding="utf-8")

    shallow = io.list_files(tmp_path, pattern="*.txt")
    recursive = io.list_files(tmp_path, pattern="*.txt", recursive=True)

    assert shallow == [(tmp_path / "a.txt").resolve()]
    assert recursive == [
        (tmp_path / "a.txt").resolve(),
        (nested / "c.txt").resolve(),
    ]


def test_save_config_snapshot_copies_config_files(tmp_path: Path) -> None:
    """save_config_snapshot should copy each named config file."""

    config_path = tmp_path / "source" / "training.yaml"
    io.write_yaml(config_path, {"seed": 42})

    copied = io.save_config_snapshot(
        {"training": config_path},
        tmp_path / "snapshots",
    )

    assert copied["training"].is_file()
    assert copied["training"].name == "training.yaml"
    assert io.read_yaml(copied["training"]) == {"seed": 42}


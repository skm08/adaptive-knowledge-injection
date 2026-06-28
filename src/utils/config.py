"""
Project: Adaptive Knowledge Injection
Module: src.utils.config
Purpose: Load YAML configuration files with dot-notation access.
Dependencies: pathlib, yaml
Author: Adaptive Knowledge Injection Research
Version: 1.0.0
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class ConfigError(Exception):
    """Custom exception for configuration-related errors."""


class ConfigNode:
    """Dictionary wrapper that enables dot-notation configuration access."""

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    def __getattr__(self, item: str) -> Any:
        """Return nested configuration values as attributes.

        Args:
            item:
                Configuration key.

        Returns:
            Raw value or nested `ConfigNode`.

        Raises:
            AttributeError: If the key does not exist.
        """

        if item not in self._data:
            raise AttributeError(f"Configuration key '{item}' not found.")

        value = self._data[item]

        if isinstance(value, dict):
            return ConfigNode(value)

        return value

    def __getitem__(self, item: str) -> Any:
        """Return a configuration value by key."""

        return self._data[item]

    def to_dict(self) -> dict[str, Any]:
        """Return the underlying dictionary."""

        return self._data

    def __repr__(self) -> str:
        return f"ConfigNode({self._data})"


class ConfigManager:
    """Load and store named YAML configuration files."""

    def __init__(self) -> None:
        self._configs: dict[str, ConfigNode] = {}

    def load_yaml(
        self,
        config_path: str | Path,
        config_name: str | None = None,
    ) -> ConfigNode:
        """Load a YAML configuration file.

        Args:
            config_path:
                Path to the YAML file.
            config_name:
                Optional alias. Defaults to the file stem.

        Returns:
            Loaded configuration node.

        Raises:
            FileNotFoundError: If the configuration file is missing.
            ConfigError: If the YAML file is empty or not a mapping.
        """

        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with config_path.open("r", encoding="utf-8") as file:
            config_data = yaml.safe_load(file)

        if config_data is None:
            raise ConfigError(f"Empty configuration file: {config_path}")

        if not isinstance(config_data, dict):
            raise ConfigError(f"Configuration must be a mapping: {config_path}")

        config_node = ConfigNode(config_data)

        if config_name is None:
            config_name = config_path.stem

        self._configs[config_name] = config_node

        return config_node

    def get(self, name: str) -> ConfigNode:
        """Return a previously loaded configuration by name.

        Args:
            name:
                Configuration alias.

        Returns:
            Loaded configuration node.

        Raises:
            ConfigError: If the configuration has not been loaded.
        """

        if name not in self._configs:
            raise ConfigError(f"Configuration '{name}' has not been loaded.")

        return self._configs[name]

    def list_configs(self) -> list[str]:
        """Return names of loaded configurations."""

        return list(self._configs.keys())

    def clear(self) -> None:
        """Clear all loaded configurations."""

        self._configs.clear()

    def __repr__(self) -> str:
        return f"ConfigManager(loaded_configs={self.list_configs()})"


config_manager = ConfigManager()


def load_config(
    config_path: str | Path,
    config_name: str | None = None,
) -> ConfigNode:
    """Load a YAML configuration through the shared manager.

    Args:
        config_path:
            Path to the YAML file.
        config_name:
            Optional alias. Defaults to the file stem.

    Returns:
        Loaded configuration node.
    """

    return config_manager.load_yaml(config_path=config_path, config_name=config_name)


def get_config(config_name: str) -> ConfigNode:
    """Retrieve a previously loaded configuration.

    Args:
        config_name:
            Configuration alias.

    Returns:
        Loaded configuration node.
    """

    return config_manager.get(config_name)

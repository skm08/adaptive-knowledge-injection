"""
config.py

Centralized configuration management for the
Adaptive Knowledge Injection project.

Features
--------
- YAML configuration loading
- Dot-notation access
- Nested configuration support
- Validation
- Singleton-style access
- Reproducibility friendly

Author: Research Repository
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional
import yaml


class ConfigError(Exception):
    """Custom exception for configuration-related errors."""
    pass


class ConfigNode:
    """
    Enables dot notation access.

    Example
    -------
    config.datasets.pubmedqa.hf_name
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        self._data = data

    def __getattr__(self, item: str) -> Any:

        if item not in self._data:
            raise AttributeError(
                f"Configuration key '{item}' not found."
            )

        value = self._data[item]

        if isinstance(value, dict):
            return ConfigNode(value)

        return value

    def __getitem__(self, item: str) -> Any:
        return self._data[item]

    def to_dict(self) -> Dict[str, Any]:
        return self._data

    def __repr__(self) -> str:
        return f"ConfigNode({self._data})"


class ConfigManager:
    """
    Main configuration manager.

    Usage
    -----

    config = ConfigManager()

    config.load_yaml("configs/datasets.yaml")

    print(config.datasets.pubmedqa.hf_name)
    """

    def __init__(self) -> None:
        self._configs: Dict[str, ConfigNode] = {}

    def load_yaml(
        self,
        config_path: str | Path,
        config_name: Optional[str] = None
    ) -> ConfigNode:
        """
        Load YAML configuration file.

        Parameters
        ----------
        config_path : str | Path
            Path to YAML file.

        config_name : Optional[str]
            Alias name for configuration.

        Returns
        -------
        ConfigNode
        """

        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(
                f"Config file not found: {config_path}"
            )

        with open(config_path, "r", encoding="utf-8") as file:
            config_data = yaml.safe_load(file)

        if config_data is None:
            raise ConfigError(
                f"Empty configuration file: {config_path}"
            )

        config_node = ConfigNode(config_data)

        if config_name is None:
            config_name = config_path.stem

        self._configs[config_name] = config_node

        return config_node

    def get(self, name: str) -> ConfigNode:

        if name not in self._configs:
            raise ConfigError(
                f"Configuration '{name}' has not been loaded."
            )

        return self._configs[name]

    def list_configs(self) -> list[str]:
        return list(self._configs.keys())

    def clear(self) -> None:
        self._configs.clear()

    def __repr__(self) -> str:
        return (
            f"ConfigManager("
            f"loaded_configs={self.list_configs()})"
        )


config_manager = ConfigManager()


def load_config(
    config_path: str | Path,
    config_name: Optional[str] = None
) -> ConfigNode:
    """
    Convenience wrapper.

    Example
    -------

    cfg = load_config(
        "configs/datasets.yaml"
    )

    print(cfg.seed)
    """

    return config_manager.load_yaml(
        config_path=config_path,
        config_name=config_name
    )


def get_config(
    config_name: str
) -> ConfigNode:
    """
    Retrieve previously loaded configuration.
    """

    return config_manager.get(config_name)
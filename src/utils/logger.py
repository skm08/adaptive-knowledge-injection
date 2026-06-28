"""
Project: Adaptive Knowledge Injection
Module: src.utils.logger
Purpose: Provide centralized, reusable logging for repository modules.
Dependencies: logging, pathlib
Author: Adaptive Knowledge Injection Research
Version: 1.0.0
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path


LOG_FORMAT = "[%(asctime)s] [%(levelname)-8s] [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_DIR = Path("outputs/logs")


class LoggerError(Exception):
    """Raised when a logger cannot be configured."""


class LoggerFactory:
    """Factory for creating consistently configured project loggers."""

    @staticmethod
    def _resolve_level(level: int | str) -> int:
        """Resolve a logging level from an integer or string value.

        Args:
            level:
                Logging level as an integer or a standard logging level name.

        Returns:
            Numeric logging level.

        Raises:
            LoggerError: If the string level is not recognized.
        """

        if isinstance(level, int):
            return level

        level_name = level.upper()
        resolved_level = logging.getLevelName(level_name)

        if isinstance(resolved_level, int):
            return resolved_level

        raise LoggerError(f"Unknown logging level: {level}")

    @classmethod
    def get_logger(
        cls,
        name: str,
        log_dir: str | Path | None = None,
        level: int | str = logging.INFO,
        log_to_file: bool = True,
    ) -> logging.Logger:
        """Create or retrieve a configured logger.

        Args:
            name:
                Logger name, usually `__name__`.
            log_dir:
                Directory for log files. Defaults to `outputs/logs`.
            level:
                Logging level as an integer or string.
            log_to_file:
                Whether to attach a timestamped file handler.

        Returns:
            Configured logger instance.
        """

        resolved_level = cls._resolve_level(level)
        logger = logging.getLogger(name)
        logger.setLevel(resolved_level)
        logger.propagate = False

        if logger.handlers:
            for handler in logger.handlers:
                handler.setLevel(resolved_level)
            return logger

        formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(resolved_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if log_to_file:
            target_dir = Path(log_dir) if log_dir is not None else DEFAULT_LOG_DIR
            target_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = name.replace(".", "_")
            log_file = target_dir / f"{safe_name}_{timestamp}.log"

            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(resolved_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger


def get_logger(
    name: str,
    log_dir: str | Path | None = None,
    level: int | str = logging.INFO,
    log_to_file: bool = True,
) -> logging.Logger:
    """Return a configured project logger.

    Args:
        name:
            Logger name, usually `__name__`.
        log_dir:
            Directory for timestamped log files.
        level:
            Logging level as an integer or string.
        log_to_file:
            Whether to attach a timestamped file handler.

    Returns:
        Configured logger instance.
    """

    return LoggerFactory.get_logger(
        name=name,
        log_dir=log_dir,
        level=level,
        log_to_file=log_to_file,
    )


def log_exception(logger: logging.Logger, exception: Exception) -> None:
    """Log an exception with traceback.

    Args:
        logger:
            Logger used to emit the exception.
        exception:
            Exception instance to log.
    """

    logger.exception("Exception occurred: %s", exception)


def log_section(logger: logging.Logger, title: str) -> None:
    """Log a readable section separator.

    Args:
        logger:
            Logger used to emit the section.
        title:
            Section title.
    """

    line = "-" * 70
    logger.info(line)
    logger.info(title)
    logger.info(line)

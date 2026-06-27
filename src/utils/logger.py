"""
================================================================================
Project : Adaptive Knowledge Injection
File    : logger.py
Author  : Research Repository
Version : 1.0.0

Centralized logging utility.

Features
--------
✓ Console logging
✓ File logging
✓ Timestamped log files
✓ Automatic log directory creation
✓ Duplicate handler protection
✓ Custom logger names
✓ Multiple log levels
✓ Exception logging
✓ Thread-safe (Python logging module)

================================================================================
"""

from __future__ import annotations

import logging
import sys

from pathlib import Path
from datetime import datetime
from typing import Optional


class LoggerFactory:
    """
    Factory class for creating reusable loggers.

    Example
    -------
    >>> logger = LoggerFactory.get_logger(
            name="Downloader"
        )

    >>> logger.info("Downloading dataset...")
    """

    LOG_FORMAT = (
        "[%(asctime)s] "
        "[%(levelname)-8s] "
        "[%(name)s] "
        "%(message)s"
    )

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    DEFAULT_LEVEL = logging.INFO

    @classmethod
    def get_logger(
        cls,
        name: str,
        log_dir: Optional[str] = None,
        level: int = DEFAULT_LEVEL,
    ) -> logging.Logger:
        """
        Create or retrieve a configured logger.

        Parameters
        ----------
        name : str
            Logger name.

        log_dir : str
            Directory where log files are saved.

        level : int
            Logging level.

        Returns
        -------
        logging.Logger
        """

        logger = logging.getLogger(name)

        # Avoid duplicate handlers
        if logger.handlers:
            return logger

        logger.setLevel(level)

        formatter = logging.Formatter(
            cls.LOG_FORMAT,
            cls.DATE_FORMAT,
        )

        ####################################################
        # Console Handler
        ####################################################

        console_handler = logging.StreamHandler(sys.stdout)

        console_handler.setLevel(level)

        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

        ####################################################
        # File Handler
        ####################################################

        if log_dir is None:
            log_dir = "outputs/logs"

        log_directory = Path(log_dir)

        log_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        log_file = log_directory / f"{name}_{timestamp}.log"

        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8",
        )

        file_handler.setLevel(level)

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        logger.propagate = False

        logger.info("=" * 70)
        logger.info("Logger initialized")
        logger.info(f"Logger Name : {name}")
        logger.info(f"Log File    : {log_file}")
        logger.info("=" * 70)

        return logger


def get_logger(
    name: str,
    log_dir: Optional[str] = None,
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Convenience wrapper.

    Example
    -------
    >>> logger = get_logger("Downloader")
    """

    return LoggerFactory.get_logger(
        name=name,
        log_dir=log_dir,
        level=level,
    )


def log_exception(
    logger: logging.Logger,
    exception: Exception,
) -> None:
    """
    Log exception with traceback.

    Parameters
    ----------
    logger : logging.Logger

    exception : Exception
    """

    logger.exception(
        f"Exception occurred: {exception}"
    )


def banner(
    logger: logging.Logger,
    text: str,
) -> None:
    """
    Print a banner inside logs.

    Example
    -------
    ===============================
    DATA DOWNLOAD STARTED
    ===============================
    """

    line = "=" * 70

    logger.info(line)
    logger.info(text)
    logger.info(line)


def section(
    logger: logging.Logger,
    title: str,
) -> None:
    """
    Log section title.
    """

    logger.info("")
    logger.info("-" * 70)
    logger.info(title)
    logger.info("-" * 70)


if __name__ == "__main__":

    logger = get_logger("LoggerDemo")

    banner(
        logger,
        "LOGGER TEST",
    )

    logger.info("Information message.")

    logger.warning("Warning message.")

    logger.error("Error message.")

    section(
        logger,
        "Example Section",
    )

    logger.info("Logger is working correctly.")

    try:

        x = 10 / 0

    except Exception as e:

        log_exception(
            logger,
            e,
        )

    logger.info("Logger test finished.")
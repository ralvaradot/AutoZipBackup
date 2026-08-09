"""Tests for application logging."""

import logging
from pathlib import Path

from autozip.common.logging import LogManager


def test_log_manager_creates_log_file(
    tmp_path: Path,
) -> None:
    """LogManager must create the log file."""
    manager = LogManager(tmp_path)

    logger = manager.configure()

    logger.info("Test message.")

    for handler in logger.handlers:
        handler.flush()

    log_file = tmp_path / "autozip.log"

    assert log_file.exists()

    content = log_file.read_text(
        encoding="utf-8"
    )

    assert "Test message." in content

    manager.shutdown()


def test_log_manager_does_not_duplicate_handlers(
    tmp_path: Path,
) -> None:
    """Repeated configure calls must not duplicate handlers."""
    manager = LogManager(tmp_path)

    logger = manager.configure()

    first_handler_count = len(logger.handlers)

    manager.configure()

    second_handler_count = len(logger.handlers)

    assert first_handler_count == 1
    assert second_handler_count == 1

    manager.shutdown()


def test_log_manager_shutdown_removes_handlers(
    tmp_path: Path,
) -> None:
    """Shutdown must release configured handlers."""
    manager = LogManager(tmp_path)

    logger = manager.configure()

    assert len(logger.handlers) == 1

    manager.shutdown()

    assert len(logger.handlers) == 0


def test_log_level_is_configurable(
    tmp_path: Path,
) -> None:
    """LogManager must respect configured log level."""
    manager = LogManager(
        tmp_path,
        level=logging.DEBUG,
    )

    logger = manager.configure()

    assert logger.level == logging.DEBUG

    manager.shutdown()
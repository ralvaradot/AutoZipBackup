"""Application logging infrastructure."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class LogManager:
    """Configure and manage application logging."""

    LOGGER_NAME = "autozip"

    def __init__(
        self,
        log_directory: Path,
        *,
        max_bytes: int = 10 * 1024 * 1024,
        backup_count: int = 10,
        level: int = logging.INFO,
    ) -> None:
        self._log_directory = log_directory
        self._max_bytes = max_bytes
        self._backup_count = backup_count
        self._level = level
        self._logger = logging.getLogger(self.LOGGER_NAME)
        self._configured = False

    @property
    def logger(self) -> logging.Logger:
        """Return the application logger."""
        return self._logger

    def configure(self) -> logging.Logger:
        """Configure application logging."""
        if self._configured:
            return self._logger

        self._log_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        log_file = self._log_directory / "autozip.log"

        formatter = logging.Formatter(
            fmt=(
                "%(asctime)s | "
                "%(levelname)s | "
                "%(name)s | "
                "%(threadName)s | "
                "%(message)s"
            ),
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=self._max_bytes,
            backupCount=self._backup_count,
            encoding="utf-8",
        )

        file_handler.setLevel(self._level)
        file_handler.setFormatter(formatter)

        self._logger.setLevel(self._level)
        self._logger.propagate = False

        self._logger.addHandler(file_handler)

        self._configured = True

        return self._logger

    def shutdown(self) -> None:
        """Shutdown and release logging handlers."""
        handlers = self._logger.handlers[:]

        for handler in handlers:
            handler.flush()
            handler.close()
            self._logger.removeHandler(handler)

        self._configured = False
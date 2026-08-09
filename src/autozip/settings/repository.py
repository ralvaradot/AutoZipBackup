"""Persistence layer for application settings."""

import json
from pathlib import Path

from autozip.common.exceptions import ConfigurationError
from autozip.settings.models import AppSettings


class SettingsRepository:
    """Read and write application settings."""

    def __init__(self, settings_file: Path) -> None:
        self._settings_file = settings_file

    @property
    def settings_file(self) -> Path:
        """Return the settings file path."""
        return self._settings_file

    def load(self) -> AppSettings:
        """Load settings from disk.

        Missing or invalid settings are reported to the caller
        through ConfigurationError.
        """
        if not self._settings_file.exists():
            raise ConfigurationError(
                "Settings file does not exist.",
                code="SETTINGS_FILE_NOT_FOUND",
            )

        try:
            with self._settings_file.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

        except json.JSONDecodeError as exc:
            raise ConfigurationError(
                "Settings file contains invalid JSON.",
                code="SETTINGS_INVALID_JSON",
            ) from exc

        except OSError as exc:
            raise ConfigurationError(
                "Unable to read settings file.",
                code="SETTINGS_READ_FAILED",
            ) from exc

        if not isinstance(data, dict):
            raise ConfigurationError(
                "Settings root must be a JSON object.",
                code="SETTINGS_INVALID_STRUCTURE",
            )

        return AppSettings.from_dict(data)

    def save(self, settings: AppSettings) -> None:
        """Persist settings to disk."""
        try:
            self._settings_file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with self._settings_file.open(
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    settings.to_dict(),
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

        except OSError as exc:
            raise ConfigurationError(
                "Unable to save settings file.",
                code="SETTINGS_WRITE_FAILED",
            ) from exc
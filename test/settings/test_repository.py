"""Tests for the settings repository."""

import json
from pathlib import Path

import pytest

from autozip.common.exceptions import ConfigurationError
from autozip.settings.models import AppSettings
from autozip.settings.repository import SettingsRepository


def test_load_settings(
    tmp_path: Path,
) -> None:
    """Repository must load valid settings."""
    settings_file = tmp_path / "settings.json"

    settings_file.write_text(
        json.dumps(
            {
                "language": "en",
                "appearance": "light",
                "theme": "flatly",
            }
        ),
        encoding="utf-8",
    )

    repository = SettingsRepository(settings_file)

    settings = repository.load()

    assert settings.language == "en"
    assert settings.appearance == "light"
    assert settings.theme == "flatly"


def test_load_missing_file_raises_configuration_error(
    tmp_path: Path,
) -> None:
    """Missing settings file must raise ConfigurationError."""
    settings_file = tmp_path / "settings.json"

    repository = SettingsRepository(settings_file)

    with pytest.raises(ConfigurationError) as exc_info:
        repository.load()

    assert exc_info.value.code == "SETTINGS_FILE_NOT_FOUND"


def test_load_invalid_json_raises_configuration_error(
    tmp_path: Path,
) -> None:
    """Invalid JSON must raise ConfigurationError."""
    settings_file = tmp_path / "settings.json"

    settings_file.write_text(
        "{ invalid json",
        encoding="utf-8",
    )

    repository = SettingsRepository(settings_file)

    with pytest.raises(ConfigurationError) as exc_info:
        repository.load()

    assert exc_info.value.code == "SETTINGS_INVALID_JSON"


def test_save_settings(
    tmp_path: Path,
) -> None:
    """Repository must save settings as JSON."""
    settings_file = tmp_path / "settings.json"

    repository = SettingsRepository(settings_file)

    settings = AppSettings(
        language="en",
        appearance="light",
        theme="flatly",
    )

    repository.save(settings)

    assert settings_file.exists()

    data = json.loads(
        settings_file.read_text(encoding="utf-8")
    )

    assert data == {
        "language": "en",
        "appearance": "light",
        "theme": "flatly",
    }
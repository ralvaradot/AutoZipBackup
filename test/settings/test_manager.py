"""Tests for the settings manager."""

from pathlib import Path

import pytest

from autozip.common.exceptions import ConfigurationError
from autozip.settings.manager import SettingsManager
from autozip.settings.repository import SettingsRepository


def create_manager(
    tmp_path: Path,
) -> SettingsManager:
    """Create a settings manager using a temporary file."""
    repository = SettingsRepository(
        tmp_path / "settings.json"
    )

    return SettingsManager(repository)


def test_load_creates_default_settings_when_file_is_missing(
    tmp_path: Path,
) -> None:
    """Missing settings file must result in default settings."""
    manager = create_manager(tmp_path)

    settings = manager.load()

    assert settings.language == "es"
    assert settings.appearance == "dark"
    assert settings.theme == "darkly"

    assert (tmp_path / "settings.json").exists()


def test_set_language(
    tmp_path: Path,
) -> None:
    """Manager must allow supported languages."""
    manager = create_manager(tmp_path)

    manager.set_language("en")

    assert manager.settings.language == "en"


def test_set_invalid_language_raises_error(
    tmp_path: Path,
) -> None:
    """Unsupported language must raise ConfigurationError."""
    manager = create_manager(tmp_path)

    with pytest.raises(ConfigurationError) as exc_info:
        manager.set_language("fr")

    assert exc_info.value.code == "UNSUPPORTED_LANGUAGE"


def test_set_appearance(
    tmp_path: Path,
) -> None:
    """Manager must allow supported appearances."""
    manager = create_manager(tmp_path)

    manager.set_appearance("light")

    assert manager.settings.appearance == "light"


def test_set_invalid_appearance_raises_error(
    tmp_path: Path,
) -> None:
    """Unsupported appearance must raise ConfigurationError."""
    manager = create_manager(tmp_path)

    with pytest.raises(ConfigurationError) as exc_info:
        manager.set_appearance("blue")

    assert exc_info.value.code == "UNSUPPORTED_APPEARANCE"


def test_set_theme(
    tmp_path: Path,
) -> None:
    """Manager must allow supported themes."""
    manager = create_manager(tmp_path)

    manager.set_theme("flatly")

    assert manager.settings.theme == "flatly"


def test_set_invalid_theme_raises_error(
    tmp_path: Path,
) -> None:
    """Unsupported theme must raise ConfigurationError."""
    manager = create_manager(tmp_path)

    with pytest.raises(ConfigurationError) as exc_info:
        manager.set_theme("unknown_theme")

    assert exc_info.value.code == "UNSUPPORTED_THEME"


def test_save_persists_changes(
    tmp_path: Path,
) -> None:
    """Manager must persist configuration changes."""
    manager = create_manager(tmp_path)

    manager.load()

    manager.set_language("en")
    manager.set_appearance("light")
    manager.set_theme("flatly")

    manager.save()

    second_manager = create_manager(tmp_path)

    settings = second_manager.load()

    assert settings.language == "en"
    assert settings.appearance == "light"
    assert settings.theme == "flatly"
"""Tests for ttkbootstrap theme manager."""

import pytest

from autozip.common.exceptions import ConfigurationError
from autozip.ui.theme import ThemeManager


def test_default_theme() -> None:
    """Default theme must be darkly."""
    manager = ThemeManager()

    assert manager.theme == "darkly"
    assert manager.appearance == "dark"


def test_set_light_appearance() -> None:
    """Light appearance must select a light theme."""
    manager = ThemeManager()

    manager.set_appearance("light")

    assert manager.appearance == "light"
    assert manager.theme == "flatly"


def test_set_dark_appearance() -> None:
    """Dark appearance must select a dark theme."""
    manager = ThemeManager(
        theme="flatly",
        appearance="light",
    )

    manager.set_appearance("dark")

    assert manager.appearance == "dark"
    assert manager.theme == "darkly"


def test_set_theme() -> None:
    """Manager must allow supported themes."""
    manager = ThemeManager()

    manager.set_theme("superhero")

    assert manager.theme == "superhero"


def test_invalid_theme_raises_error() -> None:
    """Unsupported theme must raise ConfigurationError."""
    manager = ThemeManager()

    with pytest.raises(ConfigurationError) as exc_info:
        manager.set_theme("unknown")

    assert exc_info.value.code == "UNSUPPORTED_THEME"


def test_invalid_appearance_raises_error() -> None:
    """Unsupported appearance must raise ConfigurationError."""
    manager = ThemeManager()

    with pytest.raises(ConfigurationError) as exc_info:
        manager.set_appearance("blue")

    assert exc_info.value.code == "UNSUPPORTED_APPEARANCE"
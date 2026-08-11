"""Tests for ttkbootstrap theme manager."""

import pytest

from autozip.common.exceptions import ConfigurationError
from autozip.events import EventDispatcher, ThemeChanged
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


def test_theme_change_publishes_event() -> None:
    """Changing theme must publish ThemeChanged."""
    dispatcher = EventDispatcher()

    manager = ThemeManager(
        event_dispatcher=dispatcher,
    )

    received: list[ThemeChanged] = []

    dispatcher.subscribe(
        ThemeChanged,
        received.append,
    )

    manager.set_theme("superhero")

    assert len(received) == 1
    assert received[0].theme == "superhero"
    assert received[0].appearance == "dark"

def test_appearance_change_publishes_event() -> None:
    """Changing appearance must publish ThemeChanged."""
    dispatcher = EventDispatcher()

    manager = ThemeManager(
        event_dispatcher=dispatcher,
    )

    received: list[ThemeChanged] = []

    dispatcher.subscribe(
        ThemeChanged,
        received.append,
    )

    manager.set_appearance("light")

    assert len(received) == 1
    assert received[0].appearance == "light"
    assert received[0].theme == "flatly"

def test_same_theme_does_not_publish_event() -> None:
    """Setting the current theme must not publish an event."""
    dispatcher = EventDispatcher()

    manager = ThemeManager(
        event_dispatcher=dispatcher,
    )

    received: list[ThemeChanged] = []

    dispatcher.subscribe(
        ThemeChanged,
        received.append,
    )

    manager.set_theme("darkly")

    assert received == []

            
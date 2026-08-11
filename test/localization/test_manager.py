"""Tests for localization manager."""

from pathlib import Path

import pytest

from autozip.common.exceptions import LocalizationError
from autozip.events import EventDispatcher, LanguageChanged
from autozip.localization import (
    LocalizationManager,
    TranslationProvider,
)


def create_manager(
    tmp_path: Path,
) -> LocalizationManager:
    """Create a localization manager with test translations."""
    (tmp_path / "es.json").write_text(
        '{"hello": "Hola", "welcome": "Bienvenido {name}"}',
        encoding="utf-8",
    )

    (tmp_path / "en.json").write_text(
        '{"hello": "Hello", "welcome": "Welcome {name}"}',
        encoding="utf-8",
    )

    provider = TranslationProvider(tmp_path)

    return LocalizationManager(provider)


def test_default_language_is_spanish(
    tmp_path: Path,
) -> None:
    """Default language must be Spanish."""
    manager = create_manager(tmp_path)

    assert manager.language == "es"


def test_translate_spanish(
    tmp_path: Path,
) -> None:
    """Manager must translate Spanish keys."""
    manager = create_manager(tmp_path)

    assert manager.translate("hello") == "Hola"


def test_change_language(
    tmp_path: Path,
) -> None:
    """Manager must switch languages."""
    manager = create_manager(tmp_path)

    manager.set_language("en")

    assert manager.language == "en"
    assert manager.translate("hello") == "Hello"


def test_unsupported_language_raises_error(
    tmp_path: Path,
) -> None:
    """Unsupported language must raise LocalizationError."""
    manager = create_manager(tmp_path)

    with pytest.raises(LocalizationError) as exc_info:
        manager.set_language("fr")

    assert exc_info.value.code == "UNSUPPORTED_LANGUAGE"


def test_missing_key_returns_key(
    tmp_path: Path,
) -> None:
    """Missing translation must return the key."""
    manager = create_manager(tmp_path)

    assert manager.translate("missing.key") == "missing.key"


def test_has_key(
    tmp_path: Path,
) -> None:
    """Manager must report whether a key exists."""
    manager = create_manager(tmp_path)

    assert manager.has_key("hello")
    assert not manager.has_key("missing.key")


def test_translation_supports_parameters(
    tmp_path: Path,
) -> None:
    """Translations must support named parameters."""
    manager = create_manager(tmp_path)

    assert manager.translate(
        "welcome",
        name="Roberto",
    ) == "Bienvenido Roberto"


def test_missing_translation_parameter_raises_error(
    tmp_path: Path,
) -> None:
    """Missing translation parameter must raise an error."""
    manager = create_manager(tmp_path)

    with pytest.raises(LocalizationError) as exc_info:
        manager.translate("welcome")

    assert exc_info.value.code == "TRANSLATION_FORMAT_ERROR"

def test_language_change_publishes_event(
    tmp_path: Path,
) -> None:
    """Changing language must publish LanguageChanged."""
    manager = create_manager(tmp_path)

    dispatcher = EventDispatcher()

    manager = LocalizationManager(
        TranslationProvider(tmp_path),
        event_dispatcher=dispatcher,
    )

    received: list[LanguageChanged] = []

    def handler(event: LanguageChanged) -> None:
        received.append(event)

    dispatcher.subscribe(
        LanguageChanged,
        handler,
    )

    manager.set_language("en")

    assert len(received) == 1
    assert received[0].language == "en"    

def test_setting_same_language_does_not_publish_event(
    tmp_path: Path,
) -> None:
    """Setting the current language must not publish an event."""
    dispatcher = EventDispatcher()

    manager = LocalizationManager(
        TranslationProvider(tmp_path),
        event_dispatcher=dispatcher,
    )

    received: list[LanguageChanged] = []

    dispatcher.subscribe(
        LanguageChanged,
        received.append,
    )

    manager.set_language("es")

    assert received == []

        
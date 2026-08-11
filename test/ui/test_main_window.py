"""Tests for main application window."""

from pathlib import Path

import pytest

from autozip.events import EventDispatcher
from autozip.localization import (
    LocalizationManager,
    TranslationProvider,
)
from autozip.ui.main_window import MainWindow
from autozip.ui.theme import ThemeManager


def create_localization_manager(
    tmp_path: Path,
) -> LocalizationManager:
    """Create localization manager for UI tests."""
    (tmp_path / "es.json").write_text(
        (
            '{"app.name": "AutoZipBackup", '
            '"status.ready": "Listo"}'
        ),
        encoding="utf-8",
    )

    (tmp_path / "en.json").write_text(
        (
            '{"app.name": "AutoZipBackup", '
            '"status.ready": "Ready"}'
        ),
        encoding="utf-8",
    )

    provider = TranslationProvider(tmp_path)

    return LocalizationManager(
        provider
    )


@pytest.mark.skipif(
    not hasattr(__import__("tkinter"), "Tk"),
    reason="Tkinter is not available.",
)
def test_main_window_can_be_created(
    tmp_path: Path,
) -> None:
    """MainWindow must be constructible."""
    localization = create_localization_manager(
        tmp_path
    )

    theme = ThemeManager()

    dispatcher = EventDispatcher()

    closed = []

    window = MainWindow(
        localization_manager=localization,
        theme_manager=theme,
        event_dispatcher=dispatcher,
        on_close=lambda: closed.append(True),
    )

    assert window is not None

    window.destroy()

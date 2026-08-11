"""Tests for application events."""

from dataclasses import FrozenInstanceError
from datetime import datetime
from pathlib import Path

import pytest

from autozip.events import (
    BackupCompleted,
    BackupFailed,
    BackupStarted,
    LanguageChanged,
    SchedulerStarted,
    SchedulerStopped,
    ThemeChanged,
)


def test_language_changed_event() -> None:
    """LanguageChanged must contain the new language."""
    occurred_at = datetime.now()

    event = LanguageChanged(
        occurred_at=occurred_at,
        language="en",
    )

    assert event.occurred_at == occurred_at
    assert event.language == "en"


def test_theme_changed_event() -> None:
    """ThemeChanged must contain theme and appearance."""
    occurred_at = datetime.now()

    event = ThemeChanged(
        occurred_at=occurred_at,
        theme="darkly",
        appearance="dark",
    )

    assert event.occurred_at == occurred_at
    assert event.theme == "darkly"
    assert event.appearance == "dark"


def test_backup_started_event(
    tmp_path: Path,
) -> None:
    """BackupStarted must contain source and destination."""
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    event = BackupStarted(
        occurred_at=datetime.now(),
        source_folder=source,
        destination_folder=destination,
    )

    assert event.source_folder == source
    assert event.destination_folder == destination


def test_backup_completed_event(
    tmp_path: Path,
) -> None:
    """BackupCompleted must contain backup information."""
    source = tmp_path / "source"
    destination = tmp_path / "backup.zip"

    event = BackupCompleted(
        occurred_at=datetime.now(),
        source_folder=source,
        destination_file=destination,
        duration_seconds=3.42,
    )

    assert event.source_folder == source
    assert event.destination_file == destination
    assert event.duration_seconds == 3.42


def test_backup_failed_event(
    tmp_path: Path,
) -> None:
    """BackupFailed must contain the error information."""
    source = tmp_path / "source"

    event = BackupFailed(
        occurred_at=datetime.now(),
        source_folder=source,
        error_message="Unable to create ZIP.",
    )

    assert event.source_folder == source
    assert event.error_message == "Unable to create ZIP."


def test_scheduler_started_event() -> None:
    """SchedulerStarted must contain its timestamp."""
    event = SchedulerStarted(
        occurred_at=datetime.now(),
    )

    assert event.occurred_at is not None


def test_scheduler_stopped_event() -> None:
    """SchedulerStopped must contain its timestamp."""
    event = SchedulerStopped(
        occurred_at=datetime.now(),
    )

    assert event.occurred_at is not None


def test_events_are_immutable() -> None:
    """Events must be immutable."""
    event = LanguageChanged(
        occurred_at=datetime.now(),
        language="es",
    )

    with pytest.raises(FrozenInstanceError):
        event.language = "en"  # type: ignore[misc]
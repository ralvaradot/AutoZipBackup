"""Application event definitions."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class ApplicationEvent:
    """Base class for application events."""

    occurred_at: datetime


@dataclass(frozen=True)
class LanguageChanged(ApplicationEvent):
    """Raised when the application language changes."""

    language: str


@dataclass(frozen=True)
class ThemeChanged(ApplicationEvent):
    """Raised when the application theme changes."""

    theme: str
    appearance: str


@dataclass(frozen=True)
class BackupStarted(ApplicationEvent):
    """Raised when a backup operation starts."""

    source_folder: Path
    destination_folder: Path


@dataclass(frozen=True)
class BackupCompleted(ApplicationEvent):
    """Raised when a backup operation completes."""

    source_folder: Path
    destination_file: Path
    duration_seconds: float


@dataclass(frozen=True)
class BackupFailed(ApplicationEvent):
    """Raised when a backup operation fails."""

    source_folder: Path
    error_message: str


@dataclass(frozen=True)
class SchedulerStarted(ApplicationEvent):
    """Raised when the scheduler starts."""

    pass


@dataclass(frozen=True)
class SchedulerStopped(ApplicationEvent):
    """Raised when the scheduler stops."""

    pass
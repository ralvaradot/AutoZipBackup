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
class SchedulerStarted:
    """Published when the scheduler starts."""

    occurred_at: datetime


@dataclass(frozen=True)
class SchedulerStopped:
    """Published when the scheduler stops."""

    occurred_at: datetime


@dataclass(frozen=True)
class ScheduledBackupStarted:
    """Published when a scheduled backup starts."""

    occurred_at: datetime
    source_folder: Path
    destination_folder: Path


@dataclass(frozen=True)
class ScheduledBackupCompleted:
    """Published when a scheduled backup completes."""

    occurred_at: datetime
    destination_file: Path


@dataclass(frozen=True)
class ScheduledBackupFailed:
    """Published when a scheduled backup fails."""

    occurred_at: datetime
    source_folder: Path
    error_message: str
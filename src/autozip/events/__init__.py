"""Application event subsystem."""

from autozip.events.dispatcher import EventDispatcher
from autozip.events.events import (
    ApplicationEvent,
    BackupCompleted,
    BackupFailed,
    BackupStarted,
    LanguageChanged,
    ScheduledBackupCompleted,
    ScheduledBackupFailed,
    ScheduledBackupStarted,
    SchedulerStarted,
    SchedulerStopped,
    ThemeChanged,
)

__all__ = [
    "ApplicationEvent",
    "BackupCompleted",
    "BackupFailed",
    "BackupStarted",
    "EventDispatcher",
    "LanguageChanged",
    "ScheduledBackupCompleted",
    "ScheduledBackupFailed",
    "ScheduledBackupStarted",
    "SchedulerStarted",
    "SchedulerStopped",
    "ThemeChanged",
]
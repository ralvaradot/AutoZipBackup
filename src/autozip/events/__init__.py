"""Application event subsystem."""

from autozip.events.dispatcher import EventDispatcher
from autozip.events.events import (
    ApplicationEvent,
    BackupCompleted,
    BackupFailed,
    BackupStarted,
    LanguageChanged,
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
    "SchedulerStarted",
    "SchedulerStopped",
    "ThemeChanged",
]
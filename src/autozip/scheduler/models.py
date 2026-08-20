"""Scheduler domain models."""

from dataclasses import dataclass
from datetime import time
from pathlib import Path


@dataclass(frozen=True)
class ScheduleConfiguration:
    """Configuration for a daily backup schedule."""

    enabled: bool
    execution_time: time
    source_folder: Path
    destination_folder: Path


@dataclass(frozen=True)
class SchedulerStatus:
    """Current scheduler status."""

    running: bool
    configuration: ScheduleConfiguration
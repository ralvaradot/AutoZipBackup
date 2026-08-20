"""Tests for scheduler models."""

from datetime import time
from pathlib import Path

from autozip.scheduler import (
    ScheduleConfiguration,
    SchedulerStatus,
)


def test_schedule_configuration() -> None:
    """ScheduleConfiguration stores schedule information."""
    configuration = ScheduleConfiguration(
        enabled=True,
        execution_time=time(
            22,
            30,
        ),
        source_folder=Path(
            r"C:\Data"
        ),
        destination_folder=Path(
            r"C:\Backups"
        ),
    )

    assert configuration.enabled is True
    assert configuration.execution_time == time(
        22,
        30,
    )


def test_scheduler_status() -> None:
    """SchedulerStatus stores scheduler state."""
    configuration = ScheduleConfiguration(
        enabled=True,
        execution_time=time(
            22,
            30,
        ),
        source_folder=Path(
            r"C:\Data"
        ),
        destination_folder=Path(
            r"C:\Backups"
        ),
    )

    status = SchedulerStatus(
        running=True,
        configuration=configuration,
    )

    assert status.running is True
    assert status.configuration == configuration
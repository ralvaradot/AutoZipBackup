"""Tests for SchedulerService."""

from datetime import time
from pathlib import Path

import pytest

from autozip.backup import BackupResult
from autozip.common.exceptions import (
    SchedulerAlreadyRunningError,
)
from autozip.events import (
    EventDispatcher,
    ScheduledBackupCompleted,
    ScheduledBackupFailed,
    ScheduledBackupStarted,
    SchedulerStarted,
    SchedulerStopped,
)
from autozip.scheduler import (
    ScheduleConfiguration,
    SchedulerService,
)


class FakeBackupService:
    """Fake backup service for scheduler tests."""

    def __init__(self) -> None:
        self.calls: list[
            tuple[Path, Path]
        ] = []

        self.should_fail = False

    def create_backup(
        self,
        source_folder: Path,
        destination_folder: Path,
    ) -> BackupResult:
        """Record backup execution."""
        self.calls.append(
            (
                source_folder,
                destination_folder,
            )
        )

        if self.should_fail:
            raise RuntimeError(
                "Backup failed."
            )

        return BackupResult(
            source_folder=source_folder,
            destination_file=(
                destination_folder
                / "backup.zip"
            ),
            files_count=1,
            total_bytes=100,
            duration_seconds=0.1,
        )


def create_configuration() -> ScheduleConfiguration:
    """Create standard test configuration."""
    return ScheduleConfiguration(
        enabled=True,
        execution_time=time(
            0,
            0,
        ),
        source_folder=Path(
            "source"
        ),
        destination_folder=Path(
            "destination"
        ),
    )


def test_scheduler_can_be_configured() -> None:
    """Scheduler accepts a valid configuration."""
    backup_service = FakeBackupService()

    scheduler = SchedulerService(
        backup_service
    )

    configuration = create_configuration()

    scheduler.configure(
        configuration
    )

    assert (
        scheduler.configuration
        == configuration
    )


def test_scheduler_starts_and_stops() -> None:
    """Scheduler must start and stop."""
    backup_service = FakeBackupService()

    scheduler = SchedulerService(
        backup_service
    )

    scheduler.configure(
        create_configuration()
    )

    scheduler.start()

    assert scheduler.is_running is True

    scheduler.stop()

    assert scheduler.is_running is False


def test_starting_running_scheduler_raises_error() -> None:
    """Starting an already running scheduler must fail."""
    backup_service = FakeBackupService()

    scheduler = SchedulerService(
        backup_service
    )

    scheduler.configure(
        create_configuration()
    )

    scheduler.start()

    try:
        with pytest.raises(
            SchedulerAlreadyRunningError
        ):
            scheduler.start()

    finally:
        scheduler.stop()


def test_scheduler_publishes_start_and_stop_events() -> None:
    """Scheduler publishes lifecycle events."""
    backup_service = FakeBackupService()
    dispatcher = EventDispatcher()

    started: list[
        SchedulerStarted
    ] = []

    stopped: list[
        SchedulerStopped
    ] = []

    dispatcher.subscribe(
        SchedulerStarted,
        started.append,
    )

    dispatcher.subscribe(
        SchedulerStopped,
        stopped.append,
    )

    scheduler = SchedulerService(
        backup_service,
        dispatcher,
    )

    scheduler.configure(
        create_configuration()
    )

    scheduler.start()
    scheduler.stop()

    assert len(started) == 1
    assert len(stopped) == 1


def test_scheduler_executes_backup() -> None:
    """Scheduler executes configured backup."""
    backup_service = FakeBackupService()

    scheduler = SchedulerService(
        backup_service
    )

    configuration = create_configuration()

    scheduler.configure(
        configuration
    )

    scheduler._check_schedule()

    assert len(
        backup_service.calls
    ) == 1

    assert (
        backup_service.calls[0]
        == (
            configuration.source_folder,
            configuration.destination_folder,
        )
    )


def test_scheduler_executes_only_once_per_day() -> None:
    """Scheduler must execute only once per day."""
    backup_service = FakeBackupService()

    scheduler = SchedulerService(
        backup_service
    )

    scheduler.configure(
        create_configuration()
    )

    scheduler._check_schedule()
    scheduler._check_schedule()
    scheduler._check_schedule()

    assert len(
        backup_service.calls
    ) == 1


def test_disabled_schedule_does_not_execute() -> None:
    """Disabled schedule must not execute."""
    backup_service = FakeBackupService()

    scheduler = SchedulerService(
        backup_service
    )

    configuration = ScheduleConfiguration(
        enabled=False,
        execution_time=time(
            0,
            0,
        ),
        source_folder=Path(
            "source"
        ),
        destination_folder=Path(
            "destination"
        ),
    )

    scheduler.configure(
        configuration
    )

    scheduler._check_schedule()

    assert len(
        backup_service.calls
    ) == 0


def test_scheduler_publishes_backup_events() -> None:
    """Scheduled backup publishes lifecycle events."""
    backup_service = FakeBackupService()
    dispatcher = EventDispatcher()

    started: list[
        ScheduledBackupStarted
    ] = []

    completed: list[
        ScheduledBackupCompleted
    ] = []

    dispatcher.subscribe(
        ScheduledBackupStarted,
        started.append,
    )

    dispatcher.subscribe(
        ScheduledBackupCompleted,
        completed.append,
    )

    scheduler = SchedulerService(
        backup_service,
        dispatcher,
    )

    configuration = create_configuration()

    scheduler.configure(
        configuration
    )

    scheduler._check_schedule()

    assert len(started) == 1
    assert len(completed) == 1


def test_scheduler_publishes_failure_event() -> None:
    """Scheduled backup failure publishes event."""
    backup_service = FakeBackupService()
    backup_service.should_fail = True

    dispatcher = EventDispatcher()

    failed: list[
        ScheduledBackupFailed
    ] = []

    dispatcher.subscribe(
        ScheduledBackupFailed,
        failed.append,
    )

    scheduler = SchedulerService(
        backup_service,
        dispatcher,
    )

    scheduler.configure(
        create_configuration()
    )

    scheduler._check_schedule()

    assert len(failed) == 1

    assert (
        failed[0].error_message
        == "Backup failed."
    )


def test_scheduler_status() -> None:
    """Scheduler reports current status."""
    backup_service = FakeBackupService()

    scheduler = SchedulerService(
        backup_service
    )

    configuration = create_configuration()

    scheduler.configure(
        configuration
    )

    status = scheduler.get_status()

    assert status.running is False
    assert (
        status.configuration
        == configuration
    )
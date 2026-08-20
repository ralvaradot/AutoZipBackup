"""Daily backup scheduler implementation."""

from __future__ import annotations

import logging
import threading
from datetime import datetime, time
from pathlib import Path

from autozip.backup import BackupService
from autozip.common.exceptions import (
    InvalidScheduleTimeError,
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
from autozip.scheduler.models import (
    ScheduleConfiguration,
    SchedulerStatus,
)


class SchedulerService:
    """Execute backups according to a daily schedule."""

    CHECK_INTERVAL_SECONDS = 1.0

    def __init__(
        self,
        backup_service: BackupService,
        event_dispatcher: EventDispatcher | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self._backup_service = backup_service
        self._event_dispatcher = event_dispatcher
        self._logger = logger or logging.getLogger(
            __name__
        )

        self._configuration: (
            ScheduleConfiguration | None
        ) = None

        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._execution_lock = threading.Lock()

        self._last_execution_date: datetime.date | None = None

    @property
    def is_running(self) -> bool:
        """Return whether the scheduler is running."""
        return (
            self._thread is not None
            and self._thread.is_alive()
        )

    @property
    def configuration(
        self,
    ) -> ScheduleConfiguration | None:
        """Return current scheduler configuration."""
        return self._configuration

    def configure(
        self,
        configuration: ScheduleConfiguration,
    ) -> None:
        """Configure the scheduler."""
        self._validate_configuration(
            configuration
        )

        self._configuration = configuration

        self._logger.info(
            (
                "Scheduler configured. "
                "Enabled=%s, Time=%s, Source='%s', "
                "Destination='%s'."
            ),
            configuration.enabled,
            configuration.execution_time.strftime(
                "%H:%M"
            ),
            configuration.source_folder,
            configuration.destination_folder,
        )

    def start(self) -> None:
        """Start the scheduler background thread."""
        if self.is_running:
            raise SchedulerAlreadyRunningError(
                "Scheduler is already running.",
                code="SCHEDULER_ALREADY_RUNNING",
            )

        if self._configuration is None:
            raise InvalidScheduleTimeError(
                "Scheduler configuration is required.",
                code="SCHEDULER_NOT_CONFIGURED",
            )

        self._stop_event.clear()

        self._thread = threading.Thread(
            target=self._run,
            name="AutoZipScheduler",
            daemon=True,
        )

        self._thread.start()

        self._logger.info(
            "Scheduler started."
        )

        self._publish(
            SchedulerStarted(
                occurred_at=datetime.now()
            )
        )

    def stop(self) -> None:
        """Stop the scheduler."""
        if not self.is_running:
            return

        self._logger.info(
            "Stopping scheduler."
        )

        self._stop_event.set()

        if self._thread is not threading.current_thread():
            self._thread.join(
                timeout=5.0
            )

        self._thread = None

        self._logger.info(
            "Scheduler stopped."
        )

        self._publish(
            SchedulerStopped(
                occurred_at=datetime.now()
            )
        )

    def get_status(self) -> SchedulerStatus:
        """Return current scheduler status."""
        configuration = self._configuration

        if configuration is None:
            raise InvalidScheduleTimeError(
                "Scheduler has not been configured.",
                code="SCHEDULER_NOT_CONFIGURED",
            )

        return SchedulerStatus(
            running=self.is_running,
            configuration=configuration,
        )

    def _run(self) -> None:
        """Run the scheduler loop."""
        self._logger.info(
            "Scheduler worker started."
        )

        while not self._stop_event.is_set():
            try:
                self._check_schedule()

            except Exception:
                self._logger.exception(
                    "Unexpected error in scheduler loop."
                )

            self._stop_event.wait(
                self.CHECK_INTERVAL_SECONDS
            )

        self._logger.info(
            "Scheduler worker exited."
        )

    def _check_schedule(self) -> None:
        """Check whether a scheduled backup should run."""
        configuration = self._configuration

        if configuration is None:
            return

        if not configuration.enabled:
            return

        now = datetime.now()

        if now.time() < configuration.execution_time:
            return

        if (
            self._last_execution_date
            == now.date()
        ):
            return

        if not self._execution_lock.acquire(
            blocking=False
        ):
            self._logger.warning(
                "Scheduled backup is already running."
            )
            return

        try:
            self._last_execution_date = (
                now.date()
            )

            self._execute_scheduled_backup(
                configuration
            )

        finally:
            self._execution_lock.release()

    def _execute_scheduled_backup(
        self,
        configuration: ScheduleConfiguration,
    ) -> None:
        """Execute one scheduled backup."""
        self._logger.info(
            (
                "Executing scheduled backup. "
                "Source='%s', Destination='%s'."
            ),
            configuration.source_folder,
            configuration.destination_folder,
        )

        self._publish(
            ScheduledBackupStarted(
                occurred_at=datetime.now(),
                source_folder=configuration.source_folder,
                destination_folder=(
                    configuration.destination_folder
                ),
            )
        )

        try:
            result = (
                self._backup_service.create_backup(
                    configuration.source_folder,
                    configuration.destination_folder,
                )
            )

            self._logger.info(
                (
                    "Scheduled backup completed. "
                    "Destination='%s'."
                ),
                result.destination_file,
            )

            self._publish(
                ScheduledBackupCompleted(
                    occurred_at=datetime.now(),
                    destination_file=(
                        result.destination_file
                    ),
                )
            )

        except Exception as exc:
            self._logger.exception(
                "Scheduled backup failed."
            )

            self._publish(
                ScheduledBackupFailed(
                    occurred_at=datetime.now(),
                    source_folder=(
                        configuration.source_folder
                    ),
                    error_message=str(exc),
                )
            )

    @staticmethod
    def _validate_configuration(
        configuration: ScheduleConfiguration,
    ) -> None:
        """Validate scheduler configuration."""
        if not isinstance(
            configuration.execution_time,
            time,
        ):
            raise InvalidScheduleTimeError(
                "Execution time must be a datetime.time.",
                code="INVALID_SCHEDULE_TIME",
            )

        if not isinstance(
            configuration.source_folder,
            Path,
        ):
            raise InvalidScheduleTimeError(
                "Source folder must be a Path.",
                code="INVALID_SOURCE_PATH",
            )

        if not isinstance(
            configuration.destination_folder,
            Path,
        ):
            raise InvalidScheduleTimeError(
                "Destination folder must be a Path.",
                code="INVALID_DESTINATION_PATH",
            )

    def _publish(
        self,
        event: object,
    ) -> None:
        """Publish an event if dispatcher exists."""
        if self._event_dispatcher is None:
            return

        self._event_dispatcher.publish(
            event
        )
        
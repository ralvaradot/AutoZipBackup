"""AutoZipBackup application package."""

from autozip.common.version import (
    APPLICATION_NAME,
    APPLICATION_VERSION,
    BUILD_NUMBER,
    GIT_COMMIT,
)
from autozip.scheduler.service import SchedulerService

# self._scheduler_service: SchedulerService | None = None  # noqa: F821

__all__ = [
    "APPLICATION_NAME",
    "APPLICATION_VERSION",
    "BUILD_NUMBER",
    "GIT_COMMIT",
]

@property
def scheduler_service(self) -> SchedulerService:
    """Return the scheduler service."""
    if self._scheduler_service is None:
        raise RuntimeError(
            "Scheduler service has not been initialized."
        )

    return self._scheduler_service

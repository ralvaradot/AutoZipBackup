"""Backup service implementation."""

from __future__ import annotations

import logging
import shutil
import tempfile
import time
import zipfile
from datetime import datetime
from pathlib import Path

from autozip.backup.models import BackupResult
from autozip.common.exceptions import (
    BackupCompressionError,
    BackupDestinationError,
    BackupSourceInvalidError,
    BackupSourceNotFoundError,
)
from autozip.events import (
    BackupCompleted,
    BackupFailed,
    BackupStarted,
    EventDispatcher,
)


class BackupService:
    """Create ZIP backups from source directories."""

    DATE_FORMAT = "%Y-%m-%d"

    def __init__(
        self,
        event_dispatcher: EventDispatcher | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self._event_dispatcher = event_dispatcher
        self._logger = logger or logging.getLogger(
            __name__
        )

    def create_backup(
        self,
        source_folder: Path,
        destination_folder: Path,
    ) -> BackupResult:
        """
        Compress source_folder into a ZIP file.

        The resulting file is stored in destination_folder
        using the format:

            foldername_YYYY-MM-DD.zip
        """
        start_time = time.perf_counter()

        source_folder = source_folder.resolve()
        destination_folder = destination_folder.resolve()

        self._validate_source(source_folder)
        self._validate_destination(
            destination_folder
        )

        destination_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination_file = self._build_backup_name(
            source_folder,
            destination_folder,
        )

        self._publish_backup_started(
            source_folder,
            destination_folder,
        )

        self._logger.info(
            "Starting backup. Source='%s', Destination='%s'.",
            source_folder,
            destination_file,
        )

        try:
            result = self._create_zip(
                source_folder=source_folder,
                destination_file=destination_file,
                start_time=start_time,
            )

            self._publish_backup_completed(
                result
            )

            self._logger.info(
                (
                    "Backup completed. "
                    "Source='%s', Destination='%s', "
                    "Files=%d, Bytes=%d, Duration=%.3fs."
                ),
                result.source_folder,
                result.destination_file,
                result.files_count,
                result.total_bytes,
                result.duration_seconds,
            )

            return result

        except Exception as exc:
            duration = (
                time.perf_counter()
                - start_time
            )

            self._logger.exception(
                (
                    "Backup failed. "
                    "Source='%s', Duration=%.3fs."
                ),
                source_folder,
                duration,
            )

            self._publish_backup_failed(
                source_folder,
                str(exc),
            )

            if isinstance(exc, BackupCompressionError):
                raise

            raise BackupCompressionError(
                f"Unable to create backup: {exc}",
                code="BACKUP_COMPRESSION_ERROR",
            ) from exc

    def _create_zip(
        self,
        source_folder: Path,
        destination_file: Path,
        start_time: float,
    ) -> BackupResult:
        """Create ZIP file using a temporary file."""
        temp_file: Path | None = None

        files_count = 0
        total_bytes = 0

        try:
            with tempfile.NamedTemporaryFile(
                prefix=".autozip_",
                suffix=".tmp",
                dir=destination_file.parent,
                delete=False,
            ) as temp:
                temp_file = Path(temp.name)

            with zipfile.ZipFile(
                temp_file,
                mode="w",
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=6,
            ) as zip_file:

                for file_path in source_folder.rglob("*"):
                    if not file_path.is_file():
                        continue

                    if self._is_destination_file(
                        file_path,
                        destination_file,
                    ):
                        continue

                    relative_path = (
                        file_path.relative_to(
                            source_folder
                        )
                    )

                    zip_file.write(
                        file_path,
                        arcname=relative_path,
                    )

                    files_count += 1
                    total_bytes += file_path.stat().st_size

            self._move_completed_backup(
                temp_file,
                destination_file,
            )

            duration = (
                time.perf_counter()
                - start_time
            )

            return BackupResult(
                source_folder=source_folder,
                destination_file=destination_file,
                files_count=files_count,
                total_bytes=total_bytes,
                duration_seconds=duration,
            )

        except Exception as exc:
            if isinstance(
                exc,
                BackupCompressionError,
            ):
                raise

            raise BackupCompressionError(
                f"ZIP creation failed: {exc}",
                code="ZIP_CREATION_FAILED",
            ) from exc

        finally:
            if (
                temp_file is not None
                and temp_file.exists()
            ):
                try:
                    temp_file.unlink()
                except OSError:
                    self._logger.warning(
                        "Unable to remove temporary file '%s'.",
                        temp_file,
                    )

    def _move_completed_backup(
        self,
        temporary_file: Path,
        destination_file: Path,
    ) -> None:
        """Move completed temporary ZIP to final destination."""
        try:
            shutil.move(
                str(temporary_file),
                str(destination_file),
            )
        except OSError as exc:
            raise BackupDestinationError(
                (
                    "Unable to move completed backup "
                    f"to '{destination_file}'."
                ),
                code="BACKUP_MOVE_FAILED",
            ) from exc

    def _validate_source(
        self,
        source_folder: Path,
    ) -> None:
        """Validate source directory."""
        if not source_folder.exists():
            raise BackupSourceNotFoundError(
                f"Source folder does not exist: {source_folder}",
                code="SOURCE_NOT_FOUND",
            )

        if not source_folder.is_dir():
            raise BackupSourceInvalidError(
                f"Source path is not a directory: {source_folder}",
                code="SOURCE_NOT_DIRECTORY",
            )

    def _validate_destination(
        self,
        destination_folder: Path,
    ) -> None:
        """Validate destination directory."""
        if (
            destination_folder.exists()
            and not destination_folder.is_dir()
        ):
            raise BackupDestinationError(
                (
                    "Destination path is not a directory: "
                    f"{destination_folder}"
                ),
                code="DESTINATION_NOT_DIRECTORY",
            )

    def _build_backup_name(
        self,
        source_folder: Path,
        destination_folder: Path,
    ) -> Path:
        """Build an available backup filename."""
        current_date = datetime.now().strftime(
            self.DATE_FORMAT
        )

        base_name = (
            f"{source_folder.name}_{current_date}"
        )

        candidate = (
            destination_folder
            / f"{base_name}.zip"
        )

        counter = 1

        while candidate.exists():
            candidate = (
                destination_folder
                / f"{base_name}_{counter:02d}.zip"
            )

            counter += 1

        return candidate


    def _is_destination_file(
        self,
        file_path: Path,
        destination_file: Path,
    ) -> bool:
        """Return whether a file is the target ZIP."""
        try:
            return (
                file_path.resolve()
                == destination_file.resolve()
            )
        except OSError:
            return False

    def _publish_backup_started(
        self,
        source_folder: Path,
        destination_folder: Path,
    ) -> None:
        """Publish BackupStarted event."""
        if self._event_dispatcher is None:
            return

        self._event_dispatcher.publish(
            BackupStarted(
                occurred_at=datetime.now(),
                source_folder=source_folder,
                destination_folder=destination_folder,
            )
        )

    def _publish_backup_completed(
        self,
        result: BackupResult,
    ) -> None:
        """Publish BackupCompleted event."""
        if self._event_dispatcher is None:
            return

        self._event_dispatcher.publish(
            BackupCompleted(
                occurred_at=datetime.now(),
                source_folder=result.source_folder,
                destination_file=result.destination_file,
                duration_seconds=result.duration_seconds,
            )
        )

    def _publish_backup_failed(
        self,
        source_folder: Path,
        error_message: str,
    ) -> None:
        """Publish BackupFailed event."""
        if self._event_dispatcher is None:
            return

        self._event_dispatcher.publish(
            BackupFailed(
                occurred_at=datetime.now(),
                source_folder=source_folder,
                error_message=error_message,
            )
        )
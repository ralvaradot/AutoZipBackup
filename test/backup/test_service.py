"""Tests for BackupService."""

from pathlib import Path
from zipfile import ZipFile

import pytest

from autozip.backup import BackupService
from autozip.common.exceptions import (
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


def create_source_folder(
    tmp_path: Path,
) -> Path:
    """Create a test source directory."""
    source = tmp_path / "MyDocuments"

    source.mkdir()

    (source / "file1.txt").write_text(
        "Hello AutoZipBackup",
        encoding="utf-8",
    )

    (source / "file2.txt").write_text(
        "Second file",
        encoding="utf-8",
    )

    nested = source / "nested"
    nested.mkdir()

    (nested / "file3.txt").write_text(
        "Nested file",
        encoding="utf-8",
    )

    return source


def test_create_backup_creates_zip(
    tmp_path: Path,
) -> None:
    """BackupService must create a ZIP file."""
    source = create_source_folder(tmp_path)
    destination = tmp_path / "backups"

    service = BackupService()

    result = service.create_backup(
        source,
        destination,
    )

    assert result.destination_file.exists()
    assert result.destination_file.suffix == ".zip"


def test_backup_filename_contains_folder_and_date(
    tmp_path: Path,
) -> None:
    """Backup filename must contain source folder name and date."""
    source = create_source_folder(tmp_path)
    destination = tmp_path / "backups"

    service = BackupService()

    result = service.create_backup(
        source,
        destination,
    )

    assert (
        result.destination_file.name
        .startswith("MyDocuments_")
    )

    assert result.destination_file.suffix == ".zip"


def test_backup_contains_all_files(
    tmp_path: Path,
) -> None:
    """ZIP must contain all source files."""
    source = create_source_folder(tmp_path)
    destination = tmp_path / "backups"

    service = BackupService()

    result = service.create_backup(
        source,
        destination,
    )

    with ZipFile(
        result.destination_file,
        "r",
    ) as zip_file:
        names = set(zip_file.namelist())

    assert "file1.txt" in names
    assert "file2.txt" in names
    assert "nested/file3.txt" in names


def test_backup_reports_file_count(
    tmp_path: Path,
) -> None:
    """BackupResult must contain file count."""
    source = create_source_folder(tmp_path)
    destination = tmp_path / "backups"

    service = BackupService()

    result = service.create_backup(
        source,
        destination,
    )

    assert result.files_count == 3


def test_destination_directory_is_created(
    tmp_path: Path,
) -> None:
    """Destination directory must be created automatically."""
    source = create_source_folder(tmp_path)
    destination = tmp_path / "new" / "backups"

    service = BackupService()

    service.create_backup(
        source,
        destination,
    )

    assert destination.exists()
    assert destination.is_dir()


def test_nonexistent_source_raises_error(
    tmp_path: Path,
) -> None:
    """Missing source folder must raise an exception."""
    source = tmp_path / "does-not-exist"
    destination = tmp_path / "backups"

    service = BackupService()

    with pytest.raises(
        BackupSourceNotFoundError
    ):
        service.create_backup(
            source,
            destination,
        )


def test_file_as_source_raises_error(
    tmp_path: Path,
) -> None:
    """A file cannot be used as source folder."""
    source = tmp_path / "file.txt"
    source.write_text(
        "not a directory",
        encoding="utf-8",
    )

    destination = tmp_path / "backups"

    service = BackupService()

    with pytest.raises(
        BackupSourceInvalidError
    ):
        service.create_backup(
            source,
            destination,
        )


def test_file_as_destination_raises_error(
    tmp_path: Path,
) -> None:
    """A file cannot be used as destination."""
    source = create_source_folder(tmp_path)

    destination = tmp_path / "destination.txt"
    destination.write_text(
        "not a directory",
        encoding="utf-8",
    )

    service = BackupService()

    with pytest.raises(
        BackupDestinationError
    ):
        service.create_backup(
            source,
            destination,
        )


def test_backup_creates_unique_filename(
    tmp_path: Path,
) -> None:
    """Multiple backups on the same date must not overwrite."""
    source = create_source_folder(tmp_path)
    destination = tmp_path / "backups"

    service = BackupService()

    first = service.create_backup(
        source,
        destination,
    )

    second = service.create_backup(
        source,
        destination,
    )

    assert first.destination_file.exists()
    assert second.destination_file.exists()

    assert (
        first.destination_file
        != second.destination_file
    )

    assert second.destination_file.name.endswith(
        "_01.zip"
    )


def test_backup_publishes_events(
    tmp_path: Path,
) -> None:
    """Backup must publish started and completed events."""
    source = create_source_folder(tmp_path)
    destination = tmp_path / "backups"

    dispatcher = EventDispatcher()

    started: list[BackupStarted] = []
    completed: list[BackupCompleted] = []

    dispatcher.subscribe(
        BackupStarted,
        started.append,
    )

    dispatcher.subscribe(
        BackupCompleted,
        completed.append,
    )

    service = BackupService(
        event_dispatcher=dispatcher,
    )

    result = service.create_backup(
        source,
        destination,
    )

    assert len(started) == 1
    assert len(completed) == 1

    assert (
        started[0].source_folder
        == source.resolve()
    )

    assert (
        completed[0].destination_file
        == result.destination_file
    )


def test_backup_reports_size(
    tmp_path: Path,
) -> None:
    """BackupResult must report source bytes."""
    source = create_source_folder(tmp_path)
    destination = tmp_path / "backups"

    expected_size = sum(
        path.stat().st_size
        for path in source.rglob("*")
        if path.is_file()
    )

    service = BackupService()

    result = service.create_backup(
        source,
        destination,
    )

    assert result.total_bytes == expected_size


def test_backup_duration_is_reported(
    tmp_path: Path,
) -> None:
    """BackupResult must contain duration."""
    source = create_source_folder(tmp_path)
    destination = tmp_path / "backups"

    service = BackupService()

    result = service.create_backup(
        source,
        destination,
    )

    assert result.duration_seconds >= 0


def test_backup_failure_publishes_failed_event(
    tmp_path: Path,
) -> None:
    """Backup failure must publish BackupFailed."""
    source = tmp_path / "missing"
    destination = tmp_path / "backups"

    dispatcher = EventDispatcher()

    failed: list[BackupFailed] = []

    dispatcher.subscribe(
        BackupFailed,
        failed.append,
    )

    service = BackupService(
        event_dispatcher=dispatcher,
    )

    with pytest.raises(
        BackupSourceNotFoundError
    ):
        service.create_backup(
            source,
            destination,
        )

    assert len(failed) == 1
    assert (
        failed[0].source_folder
        == source.resolve()
    )
"""Tests for backup models."""

from pathlib import Path

from autozip.backup import BackupResult


def test_backup_result_contains_backup_information() -> None:
    """BackupResult must contain backup information."""
    result = BackupResult(
        source_folder=Path("source"),
        destination_file=Path("backup.zip"),
        files_count=10,
        total_bytes=2048,
        duration_seconds=1.25,
    )

    assert result.source_folder == Path("source")
    assert result.destination_file == Path("backup.zip")
    assert result.files_count == 10
    assert result.total_bytes == 2048
    assert result.duration_seconds == 1.25
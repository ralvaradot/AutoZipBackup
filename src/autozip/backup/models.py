"""Backup domain models."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BackupResult:
    """Result of a successful backup operation."""

    source_folder: Path
    destination_file: Path
    files_count: int
    total_bytes: int
    duration_seconds: float
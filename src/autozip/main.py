"""AutoZipBackup application entry point."""

from autozip.common.constants import (
    DEFAULT_LOG_BACKUP_COUNT,
    DEFAULT_LOG_MAX_BYTES,
)
from autozip.common.logging import LogManager
from autozip.common.paths import ApplicationPaths
from autozip.common.version import get_version_info
from autozip.settings import SettingsManager, SettingsRepository


def main() -> None:
    """Start the AutoZipBackup application."""
    paths = ApplicationPaths()

    log_manager = LogManager(
        paths.logs_directory,
        max_bytes=DEFAULT_LOG_MAX_BYTES,
        backup_count=DEFAULT_LOG_BACKUP_COUNT,
    )

    logger = log_manager.configure()

    version_info = get_version_info()

    logger.info(
        "Starting %s version %s.",
        version_info["application_name"],
        version_info["application_version"],
    )

    logger.info(
        "Build number: %s.",
        version_info["build_number"],
    )

    logger.info(
        "Git commit: %s.",
        version_info["git_commit"],
    )

    settings_file = paths.application_root / "settings.json"

    repository = SettingsRepository(settings_file)

    settings_manager = SettingsManager(repository)

    settings = settings_manager.load()

    logger.info(
        "Settings loaded successfully. "
        "Language=%s, Appearance=%s, Theme=%s.",
        settings.language,
        settings.appearance,
        settings.theme,
    )

    print(
        f"{version_info['application_name']} "
        f"{version_info['application_version']}"
    )

    print(
        f"Build: {version_info['build_number']}"
    )

    print(
        f"Git Commit: {version_info['git_commit']}"
    )

    print(
        f"Language: {settings.language}"
    )

    print(
        f"Appearance: {settings.appearance}"
    )

    print(
        f"Theme: {settings.theme}"
    )

    log_manager.shutdown()


if __name__ == "__main__":
    main()
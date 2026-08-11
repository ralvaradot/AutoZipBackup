"""AutoZipBackup application entry point."""

from autozip.common.constants import (
    DEFAULT_LOG_BACKUP_COUNT,
    DEFAULT_LOG_MAX_BYTES,
)
from autozip.common.logging import LogManager
from autozip.common.paths import ApplicationPaths
from autozip.common.version import get_version_info
from autozip.localization import (
    LocalizationManager,
    TranslationProvider,
)
from autozip.settings import (
    SettingsManager,
    SettingsRepository,
)
from autozip.ui.theme import ThemeManager


def main() -> None:
    """Start the AutoZipBackup application."""
    paths = ApplicationPaths()

    log_manager = LogManager(
        paths.logs_directory,
        max_bytes=DEFAULT_LOG_MAX_BYTES,
        backup_count=DEFAULT_LOG_BACKUP_COUNT,
    )

    logger = log_manager.configure()

    try:
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

        settings_file = (
            paths.application_root / "settings.json"
        )

        repository = SettingsRepository(
            settings_file
        )

        settings_manager = SettingsManager(
            repository
        )

        settings = settings_manager.load()

        translation_provider = TranslationProvider(
            paths.languages_directory
        )

        localization_manager = LocalizationManager(
            translation_provider,
            default_language=settings.language,
        )

        theme_manager = ThemeManager(
            theme=settings.theme,
            appearance=settings.appearance,
        )

        logger.info(
            "Localization initialized. Language=%s.",
            localization_manager.language,
        )

        logger.info(
            "Theme initialized. Appearance=%s, Theme=%s.",
            theme_manager.appearance,
            theme_manager.theme,
        )

        print(
            localization_manager.translate("app.name")
        )

        print(
            f"{localization_manager.translate('about.version')}: "
            f"{version_info['application_version']}"
        )

        print(
            f"{localization_manager.translate('about.build')}: "
            f"{version_info['build_number']}"
        )

        print(
            f"{localization_manager.translate('about.git_commit')}: "
            f"{version_info['git_commit']}"
        )

        print(
            f"{localization_manager.translate('settings.language')}: "
            f"{localization_manager.language}"
        )

        print(
            f"{localization_manager.translate('settings.appearance')}: "
            f"{theme_manager.appearance}"
        )

        print(
            f"{localization_manager.translate('settings.theme')}: "
            f"{theme_manager.theme}"
        )

    finally:
        log_manager.shutdown()


if __name__ == "__main__":
    main()
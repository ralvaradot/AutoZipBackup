"""Application bootstrap and composition root."""

from autozip.common.constants import (
    DEFAULT_LOG_BACKUP_COUNT,
    DEFAULT_LOG_MAX_BYTES,
)
from autozip.common.logging import LogManager
from autozip.common.paths import ApplicationPaths
from autozip.common.version import get_version_info
from autozip.events import (
    EventDispatcher,
    LanguageChanged,
    ThemeChanged,
)
from autozip.localization import (
    LocalizationManager,
    TranslationProvider,
)
from autozip.settings import (
    SettingsManager,
    SettingsRepository,
)
from autozip.ui.main_window import MainWindow
from autozip.ui.theme import ThemeManager


class Application:
    """Compose and run the AutoZipBackup application."""

    def __init__(
        self,
        paths: ApplicationPaths | None = None,
    ) -> None:
        self._paths = paths or ApplicationPaths()

        self._log_manager = LogManager(
            self._paths.logs_directory,
            max_bytes=DEFAULT_LOG_MAX_BYTES,
            backup_count=DEFAULT_LOG_BACKUP_COUNT,
        )

        self._logger = self._log_manager.configure()

        self._event_dispatcher = EventDispatcher()

        self._settings_manager: SettingsManager | None = None
        self._localization_manager: LocalizationManager | None = None
        self._theme_manager: ThemeManager | None = None
        self._main_window: MainWindow | None = None

        self._configure_services()

    @property
    def settings_manager(self) -> SettingsManager:
        """Return the settings manager."""
        if self._settings_manager is None:
            raise RuntimeError(
                "Settings manager has not been initialized."
            )

        return self._settings_manager

    @property
    def localization_manager(self) -> LocalizationManager:
        """Return the localization manager."""
        if self._localization_manager is None:
            raise RuntimeError(
                "Localization manager has not been initialized."
            )

        return self._localization_manager

    @property
    def theme_manager(self) -> ThemeManager:
        """Return the theme manager."""
        if self._theme_manager is None:
            raise RuntimeError(
                "Theme manager has not been initialized."
            )

        return self._theme_manager

    @property
    def event_dispatcher(self) -> EventDispatcher:
        """Return the application event dispatcher."""
        return self._event_dispatcher

    def run(self) -> None:
        """Start the graphical application."""
        self._log_startup_information()

        self._main_window = MainWindow(
            localization_manager=self.localization_manager,
            theme_manager=self.theme_manager,
            event_dispatcher=self.event_dispatcher,
            on_close=self.shutdown,
        )

        self._main_window.run()

    def shutdown(self) -> None:
        """Shutdown the application."""
        self._logger.info("Application shutdown requested.")

        if self._main_window is not None:
            self._main_window.destroy()
            self._main_window = None

        self._log_manager.shutdown()

    def _configure_services(self) -> None:
        """Create and configure application services."""
        settings_file = (
            self._paths.application_root / "settings.json"
        )

        settings_repository = SettingsRepository(
            settings_file
        )

        self._settings_manager = SettingsManager(
            settings_repository
        )

        settings = self._settings_manager.load()

        translation_provider = TranslationProvider(
            self._paths.languages_directory
        )

        self._localization_manager = LocalizationManager(
            translation_provider,
            default_language=settings.language,
            event_dispatcher=self._event_dispatcher,
        )

        self._theme_manager = ThemeManager(
            theme=settings.theme,
            appearance=settings.appearance,
            event_dispatcher=self._event_dispatcher,
        )

        self._event_dispatcher.subscribe(
            LanguageChanged,
            self._on_language_changed,
        )

        self._event_dispatcher.subscribe(
            ThemeChanged,
            self._on_theme_changed,
        )

    def _on_language_changed(
        self,
        event: LanguageChanged,
    ) -> None:
        """Persist language changes."""
        self.settings_manager.set_language(
            event.language
        )

        self.settings_manager.save()

        self._logger.info(
            "Language changed to '%s'.",
            event.language,
        )

    def _on_theme_changed(
        self,
        event: ThemeChanged,
    ) -> None:
        """Persist theme changes."""
        self.settings_manager.set_theme(
            event.theme
        )

        self.settings_manager.set_appearance(
            event.appearance
        )

        self.settings_manager.save()

        self._logger.info(
            "Theme changed to '%s' with appearance '%s'.",
            event.theme,
            event.appearance,
        )

    def _log_startup_information(self) -> None:
        """Write startup information to the application log."""
        version_info = get_version_info()

        self._logger.info(
            "Starting %s version %s.",
            version_info["application_name"],
            version_info["application_version"],
        )

        self._logger.info(
            "Build number: %s.",
            version_info["build_number"],
        )

        self._logger.info(
            "Git commit: %s.",
            version_info["git_commit"],
        )

        self._logger.info(
            "Language: %s.",
            self.localization_manager.language,
        )

        self._logger.info(
            "Appearance: %s.",
            self.theme_manager.appearance,
        )

        self._logger.info(
            "Theme: %s.",
            self.theme_manager.theme,
        )
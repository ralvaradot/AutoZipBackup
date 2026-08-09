"""Application settings manager."""

from autozip.common.constants import (
    DEFAULT_APPEARANCE,
    DEFAULT_LANGUAGE,
    DEFAULT_THEME,
    SUPPORTED_APPEARANCES,
    SUPPORTED_LANGUAGES,
    SUPPORTED_THEMES,
)
from autozip.common.exceptions import ConfigurationError
from autozip.settings.models import AppSettings
from autozip.settings.repository import SettingsRepository


class SettingsManager:
    """Manage application configuration."""

    def __init__(
        self,
        repository: SettingsRepository,
    ) -> None:
        self._repository = repository
        self._settings = AppSettings()

    @property
    def settings(self) -> AppSettings:
        """Return current settings."""
        return self._settings

    def load(self) -> AppSettings:
        """Load settings from repository.

        If the settings file does not exist, default settings are
        created and persisted.
        """
        try:
            settings = self._repository.load()

        except ConfigurationError as exc:
            if exc.code == "SETTINGS_FILE_NOT_FOUND":
                settings = AppSettings()

                self._repository.save(settings)

            else:
                raise

        self._validate(settings)

        self._settings = settings

        return self._settings

    def save(self) -> None:
        """Persist current settings."""
        self._validate(self._settings)
        self._repository.save(self._settings)

    def set_language(self, language: str) -> None:
        """Set application language."""
        if language not in SUPPORTED_LANGUAGES:
            raise ConfigurationError(
                f"Unsupported language: {language}",
                code="UNSUPPORTED_LANGUAGE",
            )

        self._settings.language = language

    def set_appearance(self, appearance: str) -> None:
        """Set application appearance."""
        if appearance not in SUPPORTED_APPEARANCES:
            raise ConfigurationError(
                f"Unsupported appearance: {appearance}",
                code="UNSUPPORTED_APPEARANCE",
            )

        self._settings.appearance = appearance

    def set_theme(self, theme: str) -> None:
        """Set application theme."""
        if theme not in SUPPORTED_THEMES:
            raise ConfigurationError(
                f"Unsupported theme: {theme}",
                code="UNSUPPORTED_THEME",
            )

        self._settings.theme = theme

    @staticmethod
    def _validate(settings: AppSettings) -> None:
        """Validate application settings."""
        if settings.language not in SUPPORTED_LANGUAGES:
            settings.language = DEFAULT_LANGUAGE

        if settings.appearance not in SUPPORTED_APPEARANCES:
            settings.appearance = DEFAULT_APPEARANCE

        if settings.theme not in SUPPORTED_THEMES:
            settings.theme = DEFAULT_THEME
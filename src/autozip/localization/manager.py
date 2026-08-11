"""Application localization manager."""

from datetime import datetime

from autozip.common.constants import (
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
)
from autozip.common.exceptions import LocalizationError
from autozip.events import EventDispatcher, LanguageChanged
from autozip.localization.provider import TranslationProvider


class LocalizationManager:
    """Manage application localization."""

    def __init__(
        self,
        provider: TranslationProvider,
        default_language: str = DEFAULT_LANGUAGE,
        event_dispatcher: EventDispatcher | None = None,
    ) -> None:
        self._provider = provider
        self._language = default_language
        self._translations: dict[str, str] = {}
        self._event_dispatcher = event_dispatcher

        self._load_language(default_language)

    @property
    def language(self) -> str:
        """Return current language."""
        return self._language

    def set_language(self, language: str) -> None:
        """Change the current language."""
        if language not in SUPPORTED_LANGUAGES:
            raise LocalizationError(
                f"Unsupported language: {language}",
                code="UNSUPPORTED_LANGUAGE",
            )

        if language == self._language:
            return

        self._load_language(language)

        if self._event_dispatcher is not None:
            self._event_dispatcher.publish(
                LanguageChanged(
                    occurred_at=datetime.now(),
                    language=language,
                )
            )

    def translate(
        self,
        key: str,
        **kwargs: object,
    ) -> str:
        """Translate a key."""
        value = self._translations.get(key, key)

        if kwargs:
            try:
                return value.format(**kwargs)
            except KeyError as exc:
                raise LocalizationError(
                    f"Missing translation parameter: {exc.args[0]}",
                    code="TRANSLATION_FORMAT_ERROR",
                ) from exc

        return value

    def has_key(self, key: str) -> bool:
        """Return whether the current language contains a key."""
        return key in self._translations

    def _load_language(self, language: str) -> None:
        """Load language translations."""
        self._translations = self._provider.load(language)
        self._language = language
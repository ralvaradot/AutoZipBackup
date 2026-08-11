"""Application localization manager."""

from autozip.common.constants import (
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
)
from autozip.common.exceptions import LocalizationError
from autozip.localization.provider import TranslationProvider


class LocalizationManager:
    """Manage application localization."""

    def __init__(
        self,
        provider: TranslationProvider,
        default_language: str = DEFAULT_LANGUAGE,
    ) -> None:
        self._provider = provider
        self._language = default_language
        self._translations: dict[str, str] = {}

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

        self._load_language(language)

    def translate(
        self,
        key: str,
        **kwargs: object,
    ) -> str:
        """Translate a key.

        If the key does not exist, the key itself is returned.
        This makes missing translations visible without crashing
        the application.
        """
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
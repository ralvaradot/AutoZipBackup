"""Localization resource provider."""

import json
from pathlib import Path

from autozip.common.exceptions import LocalizationError


class TranslationProvider:
    """Load and provide translation dictionaries."""

    def __init__(self, languages_directory: Path) -> None:
        self._languages_directory = languages_directory
        self._translations: dict[str, dict[str, str]] = {}

    def load(self, language: str) -> dict[str, str]:
        """Load translations for a language."""
        if language in self._translations:
            return self._translations[language]

        file_path = self._languages_directory / f"{language}.json"

        if not file_path.exists():
            raise LocalizationError(
                f"Translation file not found: {file_path}",
                code="TRANSLATION_FILE_NOT_FOUND",
            )

        try:
            with file_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

        except json.JSONDecodeError as exc:
            raise LocalizationError(
                f"Invalid translation file: {file_path}",
                code="TRANSLATION_INVALID_JSON",
            ) from exc

        except OSError as exc:
            raise LocalizationError(
                f"Unable to read translation file: {file_path}",
                code="TRANSLATION_READ_FAILED",
            ) from exc

        if not isinstance(data, dict):
            raise LocalizationError(
                "Translation root must be a JSON object.",
                code="TRANSLATION_INVALID_STRUCTURE",
            )

        translations: dict[str, str] = {}

        for key, value in data.items():
            if not isinstance(key, str):
                raise LocalizationError(
                    "Translation keys must be strings.",
                    code="TRANSLATION_INVALID_KEY",
                )

            if not isinstance(value, str):
                raise LocalizationError(
                    f"Translation value for '{key}' must be a string.",
                    code="TRANSLATION_INVALID_VALUE",
                )

            translations[key] = value

        self._translations[language] = translations

        return translations

    def clear_cache(self) -> None:
        """Clear loaded translations."""
        self._translations.clear()
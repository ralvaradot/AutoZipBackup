"""Tests for translation provider."""

import json
from pathlib import Path

import pytest

from autozip.common.exceptions import LocalizationError
from autozip.localization.provider import TranslationProvider


def test_load_translations(tmp_path: Path) -> None:
    """Provider must load valid translations."""
    language_file = tmp_path / "es.json"

    language_file.write_text(
        json.dumps(
            {
                "hello": "Hola",
                "goodbye": "Adiós",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    provider = TranslationProvider(tmp_path)

    translations = provider.load("es")

    assert translations["hello"] == "Hola"
    assert translations["goodbye"] == "Adiós"


def test_missing_language_file_raises_error(
    tmp_path: Path,
) -> None:
    """Missing language file must raise LocalizationError."""
    provider = TranslationProvider(tmp_path)

    with pytest.raises(LocalizationError) as exc_info:
        provider.load("es")

    assert exc_info.value.code == "TRANSLATION_FILE_NOT_FOUND"


def test_invalid_json_raises_error(
    tmp_path: Path,
) -> None:
    """Invalid JSON must raise LocalizationError."""
    language_file = tmp_path / "es.json"

    language_file.write_text(
        "{ invalid",
        encoding="utf-8",
    )

    provider = TranslationProvider(tmp_path)

    with pytest.raises(LocalizationError) as exc_info:
        provider.load("es")

    assert exc_info.value.code == "TRANSLATION_INVALID_JSON"


def test_invalid_translation_root_raises_error(
    tmp_path: Path,
) -> None:
    """Translation root must be a JSON object."""
    language_file = tmp_path / "es.json"

    language_file.write_text(
        json.dumps(["Hola"]),
        encoding="utf-8",
    )

    provider = TranslationProvider(tmp_path)

    with pytest.raises(LocalizationError) as exc_info:
        provider.load("es")

    assert exc_info.value.code == "TRANSLATION_INVALID_STRUCTURE"


def test_invalid_translation_value_raises_error(
    tmp_path: Path,
) -> None:
    """Translation values must be strings."""
    language_file = tmp_path / "es.json"

    language_file.write_text(
        json.dumps(
            {
                "hello": 123,
            }
        ),
        encoding="utf-8",
    )

    provider = TranslationProvider(tmp_path)

    with pytest.raises(LocalizationError) as exc_info:
        provider.load("es")

    assert exc_info.value.code == "TRANSLATION_INVALID_VALUE"


def test_provider_caches_loaded_language(
    tmp_path: Path,
) -> None:
    """Provider must cache loaded translations."""
    language_file = tmp_path / "es.json"

    language_file.write_text(
        json.dumps({"hello": "Hola"}),
        encoding="utf-8",
    )

    provider = TranslationProvider(tmp_path)

    first = provider.load("es")
    second = provider.load("es")

    assert first is second
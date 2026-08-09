"""Tests for application settings models."""

from autozip.settings.models import AppSettings


def test_default_settings() -> None:
    """Default settings must use application defaults."""
    settings = AppSettings()

    assert settings.language == "es"
    assert settings.appearance == "dark"
    assert settings.theme == "darkly"


def test_settings_to_dict() -> None:
    """Settings must serialize to a dictionary."""
    settings = AppSettings(
        language="en",
        appearance="light",
        theme="flatly",
    )

    assert settings.to_dict() == {
        "language": "en",
        "appearance": "light",
        "theme": "flatly",
    }


def test_settings_from_dict() -> None:
    """Settings must be created from a dictionary."""
    settings = AppSettings.from_dict(
        {
            "language": "en",
            "appearance": "light",
            "theme": "flatly",
        }
    )

    assert settings.language == "en"
    assert settings.appearance == "light"
    assert settings.theme == "flatly"


def test_settings_from_partial_dict_uses_defaults() -> None:
    """Missing values must use defaults."""
    settings = AppSettings.from_dict(
        {
            "language": "en",
        }
    )

    assert settings.language == "en"
    assert settings.appearance == "dark"
    assert settings.theme == "darkly"
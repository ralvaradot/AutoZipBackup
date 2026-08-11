"""Tests for application bootstrap."""

from pathlib import Path

from autozip.application import Application
from autozip.common.paths import ApplicationPaths


def create_application_root(
    tmp_path: Path,
) -> ApplicationPaths:
    """Create application paths for testing."""
    return ApplicationPaths(tmp_path)


def test_application_initializes_services(
    tmp_path: Path,
) -> None:
    """Application must initialize core services."""
    paths = create_application_root(tmp_path)

    application = Application(paths)

    assert application.settings_manager is not None
    assert application.localization_manager is not None
    assert application.theme_manager is not None
    assert application.event_dispatcher is not None

    application.shutdown()


def test_application_creates_settings_file(
    tmp_path: Path,
) -> None:
    """Application must initialize settings."""
    paths = create_application_root(tmp_path)

    Application(paths)

    assert (
        tmp_path / "settings.json"
    ).exists()


def test_application_creates_log_directory(
    tmp_path: Path,
) -> None:
    """Application must initialize logging."""
    paths = create_application_root(tmp_path)

    application = Application(paths)

    assert paths.logs_directory.exists()

    application.shutdown()


def test_application_uses_persisted_language(
    tmp_path: Path,
) -> None:
    """Application must use persisted language."""
    paths = create_application_root(tmp_path)

    application = Application(paths)

    application.settings_manager.set_language(
        "en"
    )

    application.settings_manager.save()

    application.shutdown()

    second_application = Application(paths)

    assert (
        second_application.localization_manager.language
        == "en"
    )

    second_application.shutdown()


def test_application_uses_persisted_theme(
    tmp_path: Path,
) -> None:
    """Application must use persisted theme."""
    paths = create_application_root(tmp_path)

    application = Application(paths)

    application.settings_manager.set_theme(
        "flatly"
    )

    application.settings_manager.set_appearance(
        "light"
    )

    application.settings_manager.save()

    application.shutdown()

    second_application = Application(paths)

    assert (
        second_application.theme_manager.theme
        == "flatly"
    )

    assert (
        second_application.theme_manager.appearance
        == "light"
    )

    second_application.shutdown()



def test_theme_change_is_persisted_through_event(
    tmp_path: Path,
) -> None:
    """ThemeChanged must be persisted by Application."""
    paths = create_application_root(tmp_path)

    application = Application(paths)

    application.theme_manager.set_appearance(
        "light"
    )

    application.shutdown()

    second_application = Application(paths)

    assert (
        second_application.theme_manager.appearance
        == "light"
    )

    assert (
        second_application.theme_manager.theme
        == "flatly"
    )

    second_application.shutdown()

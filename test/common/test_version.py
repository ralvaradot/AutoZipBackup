"""Tests for application version information."""

from autozip.common.version import (
    APPLICATION_NAME,
    APPLICATION_VERSION,
    BUILD_NUMBER,
    GIT_COMMIT,
    get_version_info,
)


def test_application_name_is_defined() -> None:
    """Application name must be defined and non-empty."""
    assert APPLICATION_NAME
    assert isinstance(APPLICATION_NAME, str)


def test_application_version_is_defined() -> None:
    """Application version must be defined."""
    assert APPLICATION_VERSION
    assert isinstance(APPLICATION_VERSION, str)


def test_build_number_is_defined() -> None:
    """Build number must be defined."""
    assert BUILD_NUMBER
    assert isinstance(BUILD_NUMBER, str)


def test_git_commit_is_defined() -> None:
    """Git commit metadata must be defined."""
    assert GIT_COMMIT
    assert isinstance(GIT_COMMIT, str)


def test_get_version_info_returns_expected_keys() -> None:
    """Version information must contain all required metadata."""
    version_info = get_version_info()

    assert version_info == {
        "application_name": APPLICATION_NAME,
        "application_version": APPLICATION_VERSION,
        "build_number": BUILD_NUMBER,
        "git_commit": GIT_COMMIT,
    }


def test_version_info_values_are_strings() -> None:
    """All version metadata values must be strings."""
    version_info = get_version_info()

    assert all(
        isinstance(value, str)
        for value in version_info.values()
    )
"""Tests for application path management."""

from pathlib import Path

from autozip.common.paths import ApplicationPaths


def test_application_root_uses_provided_path(
    tmp_path: Path,
) -> None:
    """ApplicationPaths must use the explicitly provided root."""
    paths = ApplicationPaths(tmp_path)

    assert paths.application_root == tmp_path


def test_src_directory_is_under_application_root(
    tmp_path: Path,
) -> None:
    """Source directory must be located under application root."""
    paths = ApplicationPaths(tmp_path)

    assert paths.src_directory == tmp_path / "src"


def test_logs_directory_is_under_application_root(
    tmp_path: Path,
) -> None:
    """Logs directory must be located under application root."""
    paths = ApplicationPaths(tmp_path)

    assert paths.logs_directory == tmp_path / "logs"


def test_resources_directory_is_correct(
    tmp_path: Path,
) -> None:
    """Resources directory must use the expected structure."""
    paths = ApplicationPaths(tmp_path)

    expected = (
        tmp_path
        / "src"
        / "autozip"
        / "resources"
    )

    assert paths.resources_directory == expected


def test_languages_directory_is_under_resources(
    tmp_path: Path,
) -> None:
    """Languages directory must be located under resources."""
    paths = ApplicationPaths(tmp_path)

    expected = (
        tmp_path
        / "src"
        / "autozip"
        / "resources"
        / "languages"
    )

    assert paths.languages_directory == expected


def test_paths_are_pathlib_objects(
    tmp_path: Path,
) -> None:
    """All exposed paths must be pathlib.Path instances."""
    paths = ApplicationPaths(tmp_path)

    assert isinstance(paths.application_root, Path)
    assert isinstance(paths.src_directory, Path)
    assert isinstance(paths.logs_directory, Path)
    assert isinstance(paths.resources_directory, Path)
    assert isinstance(paths.languages_directory, Path)
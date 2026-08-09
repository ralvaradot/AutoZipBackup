"""Application version and build information."""

APPLICATION_NAME = "AutoZipBackup"

APPLICATION_VERSION = "0.1.0"

BUILD_NUMBER = "20260809.1"

GIT_COMMIT = "development"

VERSION = APPLICATION_VERSION


def get_version_info() -> dict[str, str]:
    """Return application version metadata."""
    return {
        "application_name": APPLICATION_NAME,
        "application_version": APPLICATION_VERSION,
        "build_number": BUILD_NUMBER,
        "git_commit": GIT_COMMIT,
    }
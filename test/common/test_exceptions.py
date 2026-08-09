"""Tests for application exception hierarchy."""

import pytest

from autozip.common.exceptions import (
    ApplicationError,
    BackupError,
    CompressionError,
    ConfigurationError,
    LocalizationError,
    SchedulerError,
    UnexpectedApplicationError,
    ValidationError,
    VerificationError,
)


def test_application_error_contains_message() -> None:
    """ApplicationError must preserve its message."""
    error = ApplicationError("Something went wrong.")

    assert error.message == "Something went wrong."
    assert str(error) == "Something went wrong."


def test_application_error_supports_error_code() -> None:
    """ApplicationError must support an optional error code."""
    error = ApplicationError(
        "Something went wrong.",
        code="TEST_ERROR",
    )

    assert error.message == "Something went wrong."
    assert error.code == "TEST_ERROR"
    assert str(error) == "[TEST_ERROR] Something went wrong."


def test_application_error_without_code_has_clean_message() -> None:
    """String representation without a code must contain only the message."""
    error = ApplicationError("Something went wrong.")

    assert str(error) == "Something went wrong."


@pytest.mark.parametrize(
    "exception_type",
    [
        BackupError,
        SchedulerError,
        ConfigurationError,
        LocalizationError,
        ValidationError,
        UnexpectedApplicationError,
    ],
)
def test_domain_exceptions_inherit_from_application_error(
    exception_type: type[ApplicationError],
) -> None:
    """Domain exceptions must inherit from ApplicationError."""
    error = exception_type("Test error.")

    assert isinstance(error, ApplicationError)


@pytest.mark.parametrize(
    "exception_type",
    [
        CompressionError,
        VerificationError,
    ],
)
def test_backup_specific_exceptions_inherit_from_backup_error(
    exception_type: type[BackupError],
) -> None:
    """Backup-specific exceptions must inherit from BackupError."""
    error = exception_type("Backup error.")

    assert isinstance(error, BackupError)
    assert isinstance(error, ApplicationError)


def test_compression_error_preserves_code() -> None:
    """CompressionError must preserve its error code."""
    error = CompressionError(
        "Unable to create ZIP archive.",
        code="ZIP_CREATION_FAILED",
    )

    assert error.code == "ZIP_CREATION_FAILED"
    assert str(error) == (
        "[ZIP_CREATION_FAILED] "
        "Unable to create ZIP archive."
    )


def test_verification_error_is_application_error() -> None:
    """VerificationError must be part of the application hierarchy."""
    error = VerificationError(
        "The generated archive is invalid.",
    )

    assert isinstance(error, ApplicationError)
    assert isinstance(error, BackupError)


def test_application_error_can_be_raised() -> None:
    """ApplicationError must behave like a normal Python exception."""
    with pytest.raises(ApplicationError):
        raise ApplicationError("Test failure.")
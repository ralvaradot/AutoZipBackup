"""Application exception hierarchy."""


class ApplicationError(Exception):
    """Base exception for all application-specific errors."""

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"

        return self.message


class BackupError(ApplicationError):
    """Base exception for backup operations."""


class BackupSourceNotFoundError(BackupError):
    """Raised when the source folder does not exist."""


class BackupSourceInvalidError(BackupError):
    """Raised when the source path is not a directory."""


class BackupDestinationError(BackupError):
    """Raised when the destination cannot be used."""


class BackupCompressionError(BackupError):
    """Raised when ZIP compression fails."""
class SchedulerError(ApplicationError):
    """Base exception for scheduler-related errors."""


class ConfigurationError(ApplicationError):
    """Base exception for configuration-related errors."""


class LocalizationError(ApplicationError):
    """Base exception for localization-related errors."""


class ValidationError(ApplicationError):
    """Raised when application data fails validation."""


class CompressionError(BackupError):
    """Raised when archive compression fails."""


class VerificationError(BackupError):
    """Raised when archive verification fails."""


class UnexpectedApplicationError(ApplicationError):
    """Represents an unexpected application-level failure."""
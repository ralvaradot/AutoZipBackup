"""Application path management."""

from pathlib import Path


class ApplicationPaths:
    """Provides paths used by the application."""

    def __init__(self, application_root: Path | None = None) -> None:
        self._application_root = (
            application_root
            if application_root is not None
            else Path(__file__).resolve().parents[3]
        )

    @property
    def application_root(self) -> Path:
        """Return the application root directory."""
        return self._application_root

    @property
    def src_directory(self) -> Path:
        """Return the source directory."""
        return self.application_root / "src"

    @property
    def logs_directory(self) -> Path:
        """Return the logs directory."""
        return self.application_root / "logs"

    @property
    def resources_directory(self) -> Path:
        """Return the application resources directory."""
        return (
            self.application_root
            / "src"
            / "autozip"
            / "resources"
        )

    @property
    def languages_directory(self) -> Path:
        """Return the localization resources directory."""
        return self.resources_directory / "languages"
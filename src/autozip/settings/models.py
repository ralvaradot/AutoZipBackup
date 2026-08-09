"""Application settings models."""

from dataclasses import asdict, dataclass

from autozip.common.constants import (
    DEFAULT_APPEARANCE,
    DEFAULT_LANGUAGE,
    DEFAULT_THEME,
)


@dataclass
class AppSettings:
    """Application configuration."""

    language: str = DEFAULT_LANGUAGE
    appearance: str = DEFAULT_APPEARANCE
    theme: str = DEFAULT_THEME

    def to_dict(self) -> dict[str, object]:
        """Convert settings to a dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "AppSettings":
        """Create settings from a dictionary."""
        return cls(
            language=str(
                data.get("language", DEFAULT_LANGUAGE)
            ),
            appearance=str(
                data.get("appearance", DEFAULT_APPEARANCE)
            ),
            theme=str(
                data.get("theme", DEFAULT_THEME)
            ),
        )
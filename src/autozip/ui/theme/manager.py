"""ttkbootstrap theme management."""
from datetime import datetime
from typing import Final

import ttkbootstrap as ttk

from autozip.common.constants import (
    DEFAULT_APPEARANCE,
    DEFAULT_THEME,
    SUPPORTED_APPEARANCES,
    SUPPORTED_THEMES,
)
from autozip.common.exceptions import ConfigurationError
from autozip.events import EventDispatcher, ThemeChanged


class ThemeManager:
    """Manage ttkbootstrap application themes."""

    LIGHT_THEMES: Final[frozenset[str]] = frozenset(
        {
            "flatly",
            "cosmo",
            "litera",
        }
    )

    DARK_THEMES: Final[frozenset[str]] = frozenset(
        {
            "darkly",
            "superhero",
        }
    )

    def __init__(
        self,
        theme: str = DEFAULT_THEME,
        appearance: str = DEFAULT_APPEARANCE,
        event_dispatcher: EventDispatcher | None = None,
    ) -> None:
        self._theme = theme
        self._appearance = appearance
        self._event_dispatcher = event_dispatcher

        self._validate_theme(theme)
        self._validate_appearance(appearance)

    @property
    def theme(self) -> str:
        """Return current ttkbootstrap theme."""
        return self._theme

    @property
    def appearance(self) -> str:
        """Return current appearance."""
        return self._appearance

    def set_theme(self, theme: str) -> None:
        """Set the ttkbootstrap theme."""
        self._validate_theme(theme)

        if theme == self._theme:
            return

        self._theme = theme

        self._publish_change()

    def set_appearance(self, appearance: str) -> None:
        """Set the appearance mode."""
        self._validate_appearance(appearance)

        if appearance == self._appearance:
            return

        self._appearance = appearance

        if appearance == "light":
            if self._theme in self.DARK_THEMES:
                self._theme = "flatly"

        elif appearance == "dark":
            if self._theme in self.LIGHT_THEMES:
                self._theme = "darkly"

        self._publish_change()

    def apply(self, window: ttk.Window) -> None:
        """Apply the current theme to a ttkbootstrap window."""
        window.style.theme_use(self._theme)


    def _publish_change(self) -> None:
        """Publish a ThemeChanged event."""
        if self._event_dispatcher is None:
            return

        self._event_dispatcher.publish(
            ThemeChanged(
                occurred_at=datetime.now(),
                theme=self._theme,
                appearance=self._appearance,
            )
        )

    def _validate_theme(self, theme: str) -> None:
        """Validate theme."""
        if theme not in SUPPORTED_THEMES:
            raise ConfigurationError(
                f"Unsupported theme: {theme}",
                code="UNSUPPORTED_THEME",
            )

    def _validate_appearance(self, appearance: str) -> None:
        """Validate appearance."""
        if appearance not in SUPPORTED_APPEARANCES:
            raise ConfigurationError(
                f"Unsupported appearance: {appearance}",
                code="UNSUPPORTED_APPEARANCE",
            )
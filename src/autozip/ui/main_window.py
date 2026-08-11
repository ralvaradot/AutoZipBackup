"""Main application window."""

from collections.abc import Callable

import ttkbootstrap as ttk

from autozip.events import (
    EventDispatcher,
    LanguageChanged,
    ThemeChanged,
)
from autozip.localization import LocalizationManager
from autozip.ui.theme import ThemeManager


class MainWindow:
    """Main AutoZipBackup application window."""

    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 600

    def __init__(
        self,
        localization_manager: LocalizationManager,
        theme_manager: ThemeManager,
        event_dispatcher: EventDispatcher,
        on_close: Callable[[], None],
    ) -> None:
        self._localization_manager = localization_manager
        self._theme_manager = theme_manager
        self._event_dispatcher = event_dispatcher
        self._on_close = on_close

        self._window: ttk.Window | None = None

        self._title_label: ttk.Label | None = None
        self._status_label: ttk.Label | None = None

        self._create_window()
        self._create_widgets()
        self._subscribe_events()
        self._update_texts()

    def run(self) -> None:
        """Start the Tkinter event loop."""
        if self._window is None:
            raise RuntimeError(
                "Main window has not been initialized."
            )

        self._window.mainloop()

    def destroy(self) -> None:
        """Destroy the main window."""
        if self._window is None:
            return

        self._unsubscribe_events()

        self._window.destroy()
        self._window = None

    def _create_window(self) -> None:
        """Create the ttkbootstrap window."""
        self._window = ttk.Window(
            title=self._localization_manager.translate("app.name"),
            themename=self._theme_manager.theme,
        )

        self._window.geometry(
            f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}"
        )

        self._window.minsize(
            700,
            450,
        )

        self._window.protocol(
            "WM_DELETE_WINDOW",
            self._handle_close,
        )

        self._theme_manager.apply(
            self._window
        )

    def _create_widgets(self) -> None:
        """Create main window widgets."""
        if self._window is None:
            raise RuntimeError(
                "Window must exist before creating widgets."
            )

        main_frame = ttk.Frame(
            self._window,
            padding=30,
        )

        main_frame.pack(
            fill="both",
            expand=True,
        )

        self._title_label = ttk.Label(
            main_frame,
            font=(
                "TkDefaultFont",
                24,
                "bold",
            ),
        )

        self._title_label.pack(
            pady=(40, 20),
        )

        self._status_label = ttk.Label(
            main_frame,
            bootstyle="secondary",
        )

        self._status_label.pack(
            pady=10,
        )

        separator = ttk.Separator(
            main_frame,
            orient="horizontal",
        )

        separator.pack(
            fill="x",
            pady=30,
        )

        info_label = ttk.Label(
            main_frame,
            text="AutoZipBackup",
            font=(
                "TkDefaultFont",
                12,
            ),
        )

        info_label.pack()

    def _subscribe_events(self) -> None:
        """Subscribe to application events."""
        self._event_dispatcher.subscribe(
            LanguageChanged,
            self._on_language_changed,
        )

        self._event_dispatcher.subscribe(
            ThemeChanged,
            self._on_theme_changed,
        )

    def _unsubscribe_events(self) -> None:
        """Unsubscribe from application events."""
        self._event_dispatcher.unsubscribe(
            LanguageChanged,
            self._on_language_changed,
        )

        self._event_dispatcher.unsubscribe(
            ThemeChanged,
            self._on_theme_changed,
        )

    def _on_language_changed(
        self,
        event: LanguageChanged,
    ) -> None:
        """Refresh UI text after language change."""
        self._update_texts()

    def _on_theme_changed(
        self,
        event: ThemeChanged,
    ) -> None:
        """Apply theme changes to the window."""
        if self._window is None:
            return

        self._theme_manager.apply(
            self._window
        )

    def _update_texts(self) -> None:
        """Update localized UI text."""
        application_name = (
            self._localization_manager.translate(
                "app.name"
            )
        )

        if self._window is not None:
            self._window.title(
                application_name
            )

        if self._title_label is not None:
            self._title_label.configure(
                text=application_name
            )

        if self._status_label is not None:
            self._status_label.configure(
                text=self._localization_manager.translate(
                    "status.ready"
                )
            )


    def _handle_close(self) -> None:
        """Handle the window close request."""
        self._on_close()

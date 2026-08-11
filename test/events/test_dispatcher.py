"""Tests for event dispatcher."""

from datetime import datetime

from autozip.events import (
    BackupCompleted,
    EventDispatcher,
    LanguageChanged,
    ThemeChanged,
)


def test_subscribe_and_publish() -> None:
    """Subscribed handlers must receive published events."""
    dispatcher = EventDispatcher()

    received: list[LanguageChanged] = []

    def handler(event: LanguageChanged) -> None:
        received.append(event)

    dispatcher.subscribe(
        LanguageChanged,
        handler,
    )

    event = LanguageChanged(
        occurred_at=datetime.now(),
        language="en",
    )

    dispatcher.publish(event)

    assert received == [event]


def test_multiple_handlers_receive_event() -> None:
    """All subscribed handlers must receive the event."""
    dispatcher = EventDispatcher()

    first: list[LanguageChanged] = []
    second: list[LanguageChanged] = []

    def first_handler(event: LanguageChanged) -> None:
        first.append(event)

    def second_handler(event: LanguageChanged) -> None:
        second.append(event)

    dispatcher.subscribe(
        LanguageChanged,
        first_handler,
    )

    dispatcher.subscribe(
        LanguageChanged,
        second_handler,
    )

    event = LanguageChanged(
        occurred_at=datetime.now(),
        language="en",
    )

    dispatcher.publish(event)

    assert first == [event]
    assert second == [event]


def test_handler_only_receives_matching_event_type() -> None:
    """Handlers must only receive their subscribed event type."""
    dispatcher = EventDispatcher()

    language_events: list[LanguageChanged] = []
    theme_events: list[ThemeChanged] = []

    def language_handler(
        event: LanguageChanged,
    ) -> None:
        language_events.append(event)

    def theme_handler(
        event: ThemeChanged,
    ) -> None:
        theme_events.append(event)

    dispatcher.subscribe(
        LanguageChanged,
        language_handler,
    )

    dispatcher.subscribe(
        ThemeChanged,
        theme_handler,
    )

    language_event = LanguageChanged(
        occurred_at=datetime.now(),
        language="en",
    )

    theme_event = ThemeChanged(
        occurred_at=datetime.now(),
        theme="darkly",
        appearance="dark",
    )

    dispatcher.publish(language_event)
    dispatcher.publish(theme_event)

    assert language_events == [language_event]
    assert theme_events == [theme_event]


def test_unsubscribe_stops_notifications() -> None:
    """Unsubscribed handlers must no longer receive events."""
    dispatcher = EventDispatcher()

    received: list[LanguageChanged] = []

    def handler(event: LanguageChanged) -> None:
        received.append(event)

    dispatcher.subscribe(
        LanguageChanged,
        handler,
    )

    dispatcher.unsubscribe(
        LanguageChanged,
        handler,
    )

    dispatcher.publish(
        LanguageChanged(
            occurred_at=datetime.now(),
            language="en",
        )
    )

    assert received == []


def test_duplicate_subscription_is_ignored() -> None:
    """A handler must not be registered twice."""
    dispatcher = EventDispatcher()

    received: list[LanguageChanged] = []

    def handler(event: LanguageChanged) -> None:
        received.append(event)

    dispatcher.subscribe(
        LanguageChanged,
        handler,
    )

    dispatcher.subscribe(
        LanguageChanged,
        handler,
    )

    dispatcher.publish(
        LanguageChanged(
            occurred_at=datetime.now(),
            language="en",
        )
    )

    assert received == [
        received[0]
    ]

    assert dispatcher.handler_count(
        LanguageChanged
    ) == 1


def test_unsubscribe_unknown_handler_is_safe() -> None:
    """Unsubscribing an unknown handler must be safe."""
    dispatcher = EventDispatcher()

    def handler(event: LanguageChanged) -> None:
        pass

    dispatcher.unsubscribe(
        LanguageChanged,
        handler,
    )

    assert dispatcher.handler_count(
        LanguageChanged
    ) == 0


def test_clear_removes_all_handlers() -> None:
    """Clear must remove every subscription."""
    dispatcher = EventDispatcher()

    def language_handler(
        event: LanguageChanged,
    ) -> None:
        pass

    def theme_handler(
        event: ThemeChanged,
    ) -> None:
        pass

    dispatcher.subscribe(
        LanguageChanged,
        language_handler,
    )

    dispatcher.subscribe(
        ThemeChanged,
        theme_handler,
    )

    dispatcher.clear()

    assert dispatcher.handler_count(
        LanguageChanged
    ) == 0

    assert dispatcher.handler_count(
        ThemeChanged
    ) == 0

def test_handler_can_receive_backup_event(
    tmp_path,
) -> None:
    """Dispatcher must support backup events."""
    dispatcher = EventDispatcher()

    received: list[BackupCompleted] = []

    def handler(event: BackupCompleted) -> None:
        received.append(event)

    dispatcher.subscribe(
        BackupCompleted,
        handler,
    )

    event = BackupCompleted(
        occurred_at=datetime.now(),
        source_folder=tmp_path / "source",
        destination_file=tmp_path / "backup.zip",
        duration_seconds=1.5,
    )

    dispatcher.publish(event)

    assert received == [event]
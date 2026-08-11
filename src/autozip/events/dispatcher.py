"""Application event dispatcher."""

from collections import defaultdict
from collections.abc import Callable
from typing import TypeVar

from autozip.events.events import ApplicationEvent

EventType = TypeVar(
    "EventType",
    bound=ApplicationEvent,
)

EventHandler = Callable[[EventType], None]


class EventDispatcher:
    """Dispatch application events to registered handlers."""

    def __init__(self) -> None:
        self._handlers: defaultdict[
            type[ApplicationEvent],
            list[Callable[[ApplicationEvent], None]],
        ] = defaultdict(list)

    def subscribe(
        self,
        event_type: type[EventType],
        handler: EventHandler[EventType],
    ) -> None:
        """Subscribe a handler to an event type."""
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)

    def unsubscribe(
        self,
        event_type: type[EventType],
        handler: EventHandler[EventType],
    ) -> None:
        """Remove a handler from an event type."""
        handlers = self._handlers.get(event_type)

        if not handlers:
            return

        if handler in handlers:
            handlers.remove(handler)

        if not handlers:
            self._handlers.pop(event_type, None)

    def publish(
        self,
        event: ApplicationEvent,
    ) -> None:
        """Publish an event to all registered handlers."""
        handlers = list(
            self._handlers.get(type(event), [])
        )

        for handler in handlers:
            handler(event)

    def clear(self) -> None:
        """Remove all registered handlers."""
        self._handlers.clear()

    def handler_count(
        self,
        event_type: type[ApplicationEvent],
    ) -> int:
        """Return number of handlers for an event type."""
        return len(self._handlers.get(event_type, []))
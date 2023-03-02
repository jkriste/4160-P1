from typing import Callable

import pygame
from pygame.event import Event


class EventHandler:
    """
    Handles events sent to the window by PyGame.
    """

    def __init__(self):
        self._events: dict[int, Callable[[Event], None]] = {}

    def register(self, event_id: int, callback: Callable[[Event], None]) -> None:
        """
        Registers a new event with the given event id and callback.

        :param event_id: The ID of the event.
        :param callback: The callback to call when the event is sent by PyGame.
        :return: None.
        :raise EventError: Raised when the given event_id is already registered by the handler.
        """
        if event_id in self._events:
            raise EventError(f'Given event ID {event_id} already registered.')
        self._events[event_id] = callback
        print(f'Event with ID {event_id} registered.')

    def handle_events(self, events: list[Event]) -> None:
        """
        Called by the window to disperse all the events collecting since last tick.

        :param events: The list of events to handle.
        :return: None.
        """
        for event in events:
            if _callable := self._events.get(event.type, None):
                _callable(event)

    def clear(self) -> None:
        """
        Clears all registered events.

        :return: None.
        """
        self._events.clear()


def new_event() -> int:
    """
    Fetches a new user event ID for PyGame.

    :return: A new user event ID.
    """
    new_id = new_event.counter
    new_event.counter += 1
    return new_id


new_event.counter = pygame.USEREVENT


class EventError(Exception):

    def __init__(self, msg: str = '') -> None:
        super().__init__(msg)

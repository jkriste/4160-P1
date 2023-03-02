import sys
from typing import Union

import pygame
from pygame.color import Color
from pygame.time import Clock
from pymunk import Space

from engine.entity.entity import EntityHandler
from engine.event.events import EventHandler
from engine.window.resolution import Resolutions, Resolution

BLACK = Color(0, 0, 0)


class Window:

    def __init__(self, res: Union[Resolutions, Resolution],
                 *,
                 bg: Color = BLACK,
                 title: str = "PyGame",
                 fps: int = 30) -> None:
        self.res = res.value if isinstance(res, Resolutions) else res
        self._fps = fps
        self._bg = bg
        self._title = title
        self._running = False
        self.surface = pygame.display.set_mode(size=self.res.as_tuple())
        self.event_handler = EventHandler()
        self.entity_handler = EntityHandler()
        self.clock = Clock()
        self.space = Space()

    def start(self) -> None:
        """
        Starts the game loop and opens the window.
        Manages event, ticks and draws entities to the screen.

        :return: None.
        """
        pygame.display.set_caption(self._title)
        self._running = True

        while self._running:
            tick_count = self.clock.tick(self._fps) % self._fps
            self.space.step(1 / self._fps)
            self.surface.fill(self._bg)
            self.event_handler.handle_events(pygame.event.get())
            self.entity_handler.tick(tick_count)
            self.entity_handler.draw(self.surface)
            pygame.display.flip()

        self.event_handler.clear()
        self.entity_handler.remove_all()
        self.entity_handler.clear()
        pygame.quit()
        sys.exit()

    def stop(self) -> None:
        """
        Stops the game loop and subsequently the pygame window.
        The game loop will finish execution before stopping.

        :return: None.
        """
        self._running = False

from typing import Union

from pygame import Rect
from pygame.color import Color
from pygame.font import Font
from pygame.surface import Surface

from engine.entity.entity import Entity
from engine.utils import WHITE
from engine.window.location import Location


class String(Entity):

    def __init__(self, font: Font, text: str, *, color: Color = WHITE, loc: Location = Location(0, 0)):
        super().__init__(loc)
        self._font = font
        self._color = color
        self._surface = self._font.render(text, True, self._color)
        self._surface.get_rect().x = self._loc.x
        self._surface.get_rect().y = self._loc.y

    def tick(self, tick_count: int) -> None:
        # This method is empty since text is static.
        pass

    def draw(self, surface: Surface) -> None:
        surface.blit(self._surface, self._loc.as_tuple())

    def on_load(self) -> None:
        # This method is empty due to not needing to load any assets.
        pass

    def bounds(self) -> Rect:
        return self._surface.get_rect()

    def set_text(self, text: str) -> None:
        """
        Updates the text for the String.

        :param text: The text to set.
        :return: None.
        """
        self._surface = self._font.render(text, True, self._color)

    @Entity.loc.setter
    def loc(self, loc: Union[Location, tuple[int, int]]) -> None:
        self._loc = loc if isinstance(loc, Location) else Location(loc[0], loc[1])
        x = loc.x if isinstance(loc, Location) else loc[0]
        y = loc.y if isinstance(loc, Location) else loc[1]
        self._surface.get_rect().x = x
        self._surface.get_rect().y = y

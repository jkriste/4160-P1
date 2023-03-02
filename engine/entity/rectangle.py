import pygame
import pymunk
from pygame import Rect
from pygame.color import Color
from pygame.surface import Surface
from pymunk import Space

from engine.entity.entity import Entity
from engine.utils import BLACK
from engine.window.location import Location


class Rectangle(Entity):
    """
    Represents a rectangular static-body entity.
    """

    def __init__(self, w: int, h: int, color: Color = BLACK, loc: Location = Location(0, 0)) -> None:
        super().__init__(loc)
        self.w = w
        self.h = h
        self.color = color

    def tick(self, tick_count: int) -> None:
        # Method empty due to not needing to update the location.
        pass

    def draw(self, surface: Surface) -> None:
        pygame.draw.rect(surface, color=self.color, rect=self.bounds())

    def on_load(self) -> None:
        # Method empty due to not needing to load any resources.
        pass

    def bounds(self) -> Rect:
        return pygame.Rect(self.loc.x, self.loc.y, self.w, self.h)


class PymunkRectangle(Entity):
    """
    Represents a rectangular entity with a static body with elasticity and gravity.
    """

    def __init__(self,
                 p1: tuple[int, int],
                 p2: tuple[int, int],
                 r: int,
                 space: Space,
                 color: Color = BLACK):
        super().__init__(Location(p1[0], p1[1]))
        self.color = color
        self.r = r
        self.p1 = p1
        self.p2 = p2
        self._space = space
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, r)
        self.shape.elasticity = 0.9

    def tick(self, tick_count: int) -> None:
        # Method empty since Pymunk handles ticking in the window.
        pass

    def draw(self, surface: Surface) -> None:
        pygame.draw.line(surface, self.color, self.p1, self.p2, self.r)

    def on_load(self) -> None:
        # Method empty since
        pass

    def bounds(self) -> Rect:
        x = self.body.position.x
        y = self.body.position.y
        width = abs(self.p2[0] - x)
        height = abs(self.p2[1] - y)
        return Rect(x, y, width, height)

    def spawn(self) -> None:
        super().spawn()
        self._space.add(self.body, self.shape)

    def remove(self) -> None:
        super().remove()
        self._space.remove(self.body, self.shape)

    @Entity.loc.setter
    def loc(self, loc: Location) -> None:
        self._loc = loc
        self.body.position = loc.as_tuple()

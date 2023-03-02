import pygame.draw
import pymunk
from pygame import Rect, Color
from pygame.surface import Surface
from pymunk import Space

from engine.entity.entity import Entity
from engine.utils import BLACK
from engine.window.location import Location


class Circle(Entity):
    """
    Represents a circle entity.
    """

    def __init__(self, r: int, color: Color = BLACK, loc: Location = Location(0, 0)):
        super().__init__(loc)
        self.r = r
        self.color = color

    def tick(self, tick_count: int) -> None:
        # Method is empty as we do not need to update our location each tick - we're a static body.
        pass

    def draw(self, surface: Surface) -> None:
        pygame.draw.circle(surface, self.color, self.loc.as_tuple(), self.r)

    def on_load(self) -> None:
        # Method is empty as we do not need to load any resources beforehand.
        pass

    def bounds(self) -> Rect:
        return pygame.Rect(self.loc.x, self.loc.y, self.r, self.r)


class PymunkCircle(Entity):
    """
    Represents a circle entity with elasticity, gravity, and a dynamic body.
    """

    def __init__(self, r: int, space: Space, color: Color = BLACK, loc: Location = Location(0, 0)):
        super().__init__(loc)
        self.r = r
        self.color = color
        self._space = space
        self.body = pymunk.Body(1, 100, pymunk.Body.DYNAMIC)
        self.shape = pymunk.Circle(self.body, r)
        self.shape.elasticity = 1
        self.body.position = loc.as_tuple()

    def tick(self, tick_count: int) -> None:
        # Method is empty because our Window handles updating Pymunk objects.
        pass

    def draw(self, surface: Surface) -> None:
        pygame.draw.circle(surface, self.color, self.body.position, self.r)

    def on_load(self) -> None:
        # Method is empty as we do not need to load any resources beforehand.
        pass

    def bounds(self) -> Rect:
        return pygame.Rect(self.body.position.x, self.body.position.y, self.r, self.r)

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

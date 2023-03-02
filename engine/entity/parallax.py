import math
from typing import Union

import pygame.image
from pygame import Rect
from pygame.surface import Surface

from engine.entity.entity import Entity
from engine.entity.render_priority import Priority
from engine.window.resolution import Resolution, Resolutions


class Parallax(Entity):

    def __init__(self,
                 path: str,
                 layers: int,
                 res: Union[Resolution, Resolutions],
                 *,
                 scroll: int = 0,
                 speed: float = 0,
                 delta: float = 0):
        super().__init__(priority=Priority.LOWEST)
        self._path = path
        self._layers = layers
        self._images: dict[Surface, int] = {}
        self._width = 0
        self._height = 0
        self._scroll = scroll
        self._speed = speed
        self._delta = delta
        self._total_scroll = 0
        self._res = res if isinstance(res, Resolution) else res.value
        self._tiles = 0

    def tick(self, tick_count: int) -> None:
        pass

    def draw(self, surface: Surface) -> None:
        speed = self._speed
        for image, image_scroll in self._images.items():
            speed += self._delta
            if image_scroll + (self._scroll * speed) >= image.get_width():
                new_scroll = self._scroll * speed
            else:
                new_scroll = math.ceil(image_scroll + (self._scroll * speed))
            for x in range(self._tiles):
                surface.blit(image, ((x * image.get_width()) - new_scroll, 0))
                self._images[image] = new_scroll

    def on_load(self) -> None:
        for i in range(self._layers):
            image = pygame.image.load(f'{self._path}/{i}.png').convert_alpha()
            image = pygame.transform.scale(image, self._res.as_tuple())
            self._height = max(self._height, image.get_height())
            self._width = max(self._width, image.get_width())
            self._images[image] = 0
        self._tiles = math.ceil(self._res.width / self._width) + 1

    def bounds(self) -> Rect:
        pass

    @property
    def scroll(self) -> int:
        return self._scroll

    @scroll.setter
    def scroll(self, value: int) -> None:
        self._scroll = value

    @property
    def speed(self) -> float:
        return self._scroll

    @speed.setter
    def speed(self, value: float) -> None:
        self._speed = value

    @property
    def delta(self) -> float:
        return self._delta

    @delta.setter
    def delta(self, value: float) -> None:
        self._delta = value

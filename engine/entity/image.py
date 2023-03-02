import pygame.image
from pygame import Rect
from pygame.surface import Surface

from engine.entity.entity import Entity, EntityError
from engine.entity.render_priority import Priority


class Image(Entity):

    def __init__(self, path: str, count: int, *, scalar: float = 1):
        super().__init__(priority=Priority.HIGHEST)
        self._index = 0
        self._images: list[Surface] = []
        for i in range(count):
            image = pygame.image.load(f'{path}/{i}.png')
            new_width = image.get_width() * scalar
            new_height = image.get_height() * scalar
            image = pygame.transform.scale(image, (new_width, new_height))
            self._images.append(image)

    def tick(self, tick_count: int) -> None:
        # We do not need to tick the static image.
        pass

    def draw(self, surface: Surface) -> None:
        surface.blit(self._images[self._index], self.loc.as_tuple())

    def on_load(self) -> None:
        # Nothing to be loaded.
        pass

    def bounds(self) -> Rect:
        x, y = self.loc.as_tuple()
        image = self._images[0]
        return Rect(x, y, image.get_width(), image.get_height())

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        if 0 <= value <= len(self._images) - 1:
            self._index = value
        else:
            raise EntityError(f'Given index {value} out of range for size {len(self._images)}')

    def next(self) -> None:
        if self._index >= len(self._images) - 1:
            self._index = 0
        else:
            self._index += 1

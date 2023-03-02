from enum import Enum

import pygame.image
from pygame import Rect
from pygame.surface import Surface

from engine.entity.entity import Entity, EntityError
from engine.entity.render_priority import Priority
from engine.window.resolution import Resolution


class SpriteState(Enum):

    IDLE = 0,
    RUN = 1,
    JUMP = 2,
    MID_AIR = 3,
    LAND = 4


class Sprite(Entity):

    def __init__(self,
                 res: Resolution,
                 *,
                 speed: int = 1,
                 scalar: float = 1,
                 gravity: bool = True,
                 min_y: int = 0,
                 default_state: SpriteState = SpriteState.IDLE):
        super().__init__(priority=Priority.HIGHEST)
        self._animations: dict[SpriteState, list[Surface]] = {}
        self._states: dict[SpriteState, tuple[str, int]] = {}
        self._state = default_state
        self._speed = speed
        self._index = 0
        self._scalar = scalar
        self._max_y = res.height - min_y
        self._gravity = gravity
        self._velocity: tuple[int, int] = (0, 0)

    def tick(self, tick_count: int) -> None:
        if self.loc.y < self._max_y and self.state is SpriteState.RUN:
            self.state = SpriteState.MID_AIR
        elif self.loc.y >= self._max_y and self.state is SpriteState.MID_AIR:
            self.state = SpriteState.RUN
        vel_x, vel_y = self._velocity
        if self._gravity:
            self._velocity = (vel_x, min(30, vel_y + 1))
        self.loc.x -= vel_x
        self.loc.y = min(self.loc.y + vel_y, self._max_y)
        if tick_count % self._speed == 0:
            if self._index < len(self._animations[self._state]) - 1:
                self._index += 1
            else:
                self._index = 0

    def draw(self, surface: Surface) -> None:
        current_frame = self._animations[self._state][self._index]
        surface.blit(current_frame, self.loc.as_tuple())

    def bounds(self) -> Rect:
        x, y = self.loc.as_tuple()
        state_image = self._animations[self.state][0]
        return Rect(x, y, state_image.get_width(), state_image.get_height())

    def on_load(self) -> None:
        pass

    @property
    def state(self) -> SpriteState:
        return self._state

    @state.setter
    def state(self, value: SpriteState) -> None:
        self._state = value
        self._index = 0

    @property
    def velocity(self) -> tuple[int, int]:
        return self._velocity

    @velocity.setter
    def velocity(self, value: tuple[int, int]) -> None:
        self._velocity = value

    def min_y(self, res: Resolution, min_y: int):
        self._max_y = res.height - min_y - self._animations[self._state][0].get_height()

    def add_state(self, state: SpriteState, path: str, count: int) -> None:
        if state in self._states:
            raise EntityError(f'The sprite state {state.name} has already been set.')
        images = []
        for i in range(count):
            image = pygame.image.load(f'{path}/{i}.png')
            new_width = image.get_width() * self._scalar
            new_height = image.get_height() * self._scalar
            image = pygame.transform.scale(image, (new_width, new_height))
            images.append(image)
        self._animations[state] = images

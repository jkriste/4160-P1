from enum import Enum
from random import randint

import pygame
from pygame.color import Color
from pygame.event import Event

from engine.entity.parallax import Parallax
from engine.entity.sprite import Sprite, SpriteState
from engine.entity.string import String
from engine.window.location import Location
from engine.window.resolution import Resolutions
from engine.window.window import Window

RESOLUTION = Resolutions.P720
TITLE_FONT = pygame.font.Font('game/assets/font/kenvector_future.ttf', 40)
SUBTITLE_FONT = pygame.font.Font('game/assets/font/kenpixel_mini_square.ttf', 24)


class ParallexPreset:

    def __init__(self,
                 path: str,
                 layers: int,
                 *,
                 y_offset: int = 0,
                 color: Color = Color(0),
                 scroll: int = 2,
                 speed: float = 1,
                 delta: float = 2):
        self._path = path
        self._layers = layers
        self._y_offset = y_offset
        self._color = color
        self._scroll = scroll
        self._speed = speed
        self._delta = delta

    @property
    def path(self) -> str:
        return self._path

    @property
    def layers(self) -> int:
        return self._layers

    @property
    def y_offset(self) -> int:
        return self._y_offset

    @property
    def color(self) -> Color:
        return self._color

    @property
    def scroll(self) -> int:
        return self._scroll

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def delta(self) -> float:
        return self._delta


class Presets(Enum):

    COUNTRY = ParallexPreset(
        'game/assets/parallax/country',
        3,
        y_offset=100
    )
    FOREST = ParallexPreset(
        'game/assets/parallax/forest',
        4,
        color=Color(0xFFFFFFFF)
    )
    INDUSTRIAL = ParallexPreset(
        'game/assets/parallax/industrial',
        4,
        color=Color(0xFFFFFFFF)
    )
    JUNGLE = ParallexPreset(
        'game/assets/parallax/jungle',
        6,
        y_offset=150,
        color=Color(0xFFFFFFFF),
        scroll=2,
        speed=0.9,
        delta=1
    )

    @staticmethod
    def random() -> ParallexPreset:
        presets = [p.value for p in Presets]
        return presets[randint(0, len(presets) - 1)]


class Platformer:

    def __init__(self):
        self.window = Window(RESOLUTION, title='Runner', fps=25)
        self.register_events()
        self.color = Color(0xFFFFFFFF)
        self.preset = Presets.random()
        self.parallax = self.from_preset(self.preset)
        self.register_entities()
        self.window.entity_handler.spawn_all()
        self.window.start()

    def register_events(self) -> None:
        self.window.event_handler.register(pygame.QUIT, self.on_quit)
        self.window.event_handler.register(pygame.KEYDOWN, self.on_key_press)

    def register_entities(self) -> None:
        self.title = String(TITLE_FONT, 'RUNNER', color=self.color)
        self.subtitle = String(SUBTITLE_FONT, 'press space to start', color=self.color)
        self.title.loc = Location.center(RESOLUTION.value, self.title.bounds())
        self.subtitle.loc = Location.center(RESOLUTION.value, self.subtitle.bounds())
        self.subtitle.loc.add(y=50)
        self.character = Sprite(RESOLUTION.value, scalar=3.5, min_y=self.preset.y_offset)
        self.character.add_state(SpriteState.IDLE, 'game/assets/character/idle', 12)
        self.character.add_state(SpriteState.JUMP, 'game/assets/character/jump', 1)
        self.character.add_state(SpriteState.LAND, 'game/assets/character/land', 1)
        self.character.add_state(SpriteState.MID_AIR, 'game/assets/character/mid_air', 2)
        self.character.add_state(SpriteState.RUN, 'game/assets/character/run', 8)
        self.character.state = SpriteState.RUN
        self.character.loc = Location.bottom_left(RESOLUTION.value, self.character.bounds())
        self.character.loc.add(50, -self.preset.y_offset)
        self.window.entity_handler.register_entities(self.parallax, self.title, self.subtitle, self.character)

    def from_preset(self, pre: ParallexPreset) -> Parallax:
        self.color = pre.color
        return Parallax(pre.path, pre.layers, RESOLUTION, scroll=pre.scroll, speed=pre.speed, delta=pre.delta)

    def on_key_press(self, event: Event) -> None:
        if event.key == pygame.K_SPACE:
            print('Space pressed.')
            if self.title.visible or self.subtitle.visible:
                self.title.visible = False
                self.subtitle.visible = False
            if self.character.state is SpriteState.RUN:
                self.character.velocity = (0, -20)

    def on_quit(self, _: Event) -> None:
        print('Closing game...')
        self.window.stop()


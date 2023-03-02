from enum import Enum
from random import randint

from pygame import Color


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


class ParallaxPresets(Enum):

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
        color=Color(0xFFFFFFFF)
    )

    @staticmethod
    def random() -> ParallexPreset:
        presets = [p.value for p in ParallaxPresets]
        return presets[randint(0, len(presets) - 1)]


class SoundPresets(Enum):

    DEATH_0 = 'game/assets/sound/death_0.mp3'
    DEATH_1 = 'game/assets/sound/death_1.mp3'
    DEATH_2 = 'game/assets/sound/death_2.mp3'
    DEATH_3 = 'game/assets/sound/death_3.mp3'
    HURT_0 = 'game/assets/sound/hurt_0.mp3'
    HURT_1 = 'game/assets/sound/hurt_1.mp3'
    HURT_2 = 'game/assets/sound/hurt_2.mp3'

    @staticmethod
    def rand_death() -> str:
        death_sounds = [SoundPresets.DEATH_0, SoundPresets.DEATH_1, SoundPresets.DEATH_2, SoundPresets.DEATH_3]
        death_sounds = [p.value for p in death_sounds]
        return death_sounds[randint(0, len(death_sounds) - 1)]

    @staticmethod
    def rand_hurt() -> str:
        hurt_sounds = [SoundPresets.HURT_0, SoundPresets.HURT_1, SoundPresets.HURT_2]
        hurt_sounds = [p.value for p in hurt_sounds]
        return hurt_sounds[randint(0, len(hurt_sounds) - 1)]

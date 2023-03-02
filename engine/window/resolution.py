from enum import Enum


class Resolution:
    """
    A basic class for storing a specific resolution and scalar.
    """

    def __init__(self, w: int, h: int, scalar: float) -> None:
        self._w = w
        self._h = h
        self._scalar = scalar

    @property
    def width(self) -> int:
        return self._w

    @property
    def height(self) -> int:
        return self._h

    @property
    def scalar(self) -> float:
        return self._scalar

    def as_tuple(self) -> tuple[int, int]:
        """
        Gets the width and height as a tuple, formatted (width, height).

        :return: The width and height as a tuple.
        """
        return self._w, self._h


class Resolutions(Enum):
    """
    An enum for most, if not all, 16:9 ratio resolutions.
    """

    P576 = Resolution(1024, 576, 1.0)
    P648 = Resolution(1152, 648, 1.125)
    P720 = Resolution(1280, 720, 1.25)
    P900 = Resolution(1600, 900, 1.5625)
    P1080 = Resolution(1920, 1080, 1.875)
    P1440 = Resolution(2560, 1440, 2.5)
    P2160 = Resolution(3840, 2160, 3.75)

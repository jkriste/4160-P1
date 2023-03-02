from math import sqrt
from random import randint

from pygame import Rect

from engine.window.resolution import Resolution


class Location:
    """
    Class that represents a location on a 2D plane with x and y coordinates.
    """

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"

    @staticmethod
    def top_left() -> 'Location':
        """
        Corresponds to the top left of the window.
        The coordinate calculations can be summed by:
        (0, 0)

        :return: A location corresponding to the top left of the window.
        """
        return Location(0, 0)

    @staticmethod
    def top_center(res: Resolution, box: Rect) -> 'Location':
        """
        Corresponds to the top center of the window.
        The coordinate calculations can be summed by:
        ((WIDTH / 2) - (box.width / 2), 0)

        :param res: The resolution of the window.
        :param box: The bounding box of the object.
        :return: A location corresponding to the top center of the window.
        """
        return Location(int((res.width / 2) - (box.w / 2)), 0)

    @staticmethod
    def top_right(res: Resolution, box: Rect) -> 'Location':
        """
        Corresponds to the top right of the window.
        The coordinate calculations can be summed by:
        (WIDTH - box.width, 0)

        :param res: The resolution of the window.
        :param box: The bounding box of the object.
        :return: A location corresponding to the top right of the window.
        """
        return Location(res.width - box.w, 0)

    @staticmethod
    def center(res: Resolution, box: Rect) -> 'Location':
        """
        Corresponds to the center of the window.
        The coordinate calculations can be summed by:
        ((WIDTH / 2) - (box.width / 2), (HEIGHT / 2) - (box.height / 2))

        :param res: The resolution of the window.
        :param box: The bounding box of the object.
        :return: A location corresponding to the center of the window.
        """
        w = int((res.width / 2) - (box.w / 2))
        h = int((res.height / 2) - (box.h / 2))
        return Location(w, h)
    
    @staticmethod
    def center_left(res: Resolution, box: Rect) -> 'Location':
        """
        Corresponds to the center left of the window.
        The coordinate calculations can be summed by:
        (0, (HEIGHT / 2) - (box.height / 2))

        :param res: The resolution of the window.
        :param box: The bounding box of the object.
        :return: A location corresponding to the center left of the window.
        """
        return Location(0, int((res.height / 2) - (box.h / 2)))

    @staticmethod
    def center_right(res: Resolution, box: Rect) -> 'Location':
        """
        Corresponds to the center right of the window.
        The coordinate calculations can be summed by:
        (WIDTH - box.width, (HEIGHT / 2) - (box.height / 2))

        :param res: The resolution of the window.
        :param box: The bounding box of the object.
        :return: A location corresponding to the center right of the window.
        """
        w = res.width - box.w
        h = int((res.height / 2) - (box.h / 2))
        return Location(w, h)

    @staticmethod
    def bottom_left(res: Resolution, box: Rect) -> 'Location':
        """
        Corresponds to the bottom left of the window.
        The coordinate calculations can be summed by:
        (0, HEIGHT - box.height)

        :param res: The resolution of the window.
        :param box: The bounding box of the object.
        :return: A location corresponding to the bottom left of the window.
        """
        return Location(0, (res.height - box.h))

    @staticmethod
    def bottom_center(res: Resolution, box: Rect) -> 'Location':
        """
        Corresponds to the bottom center of the window.
        The coordinate calculations can be summed by:
        ((WIDTH / 2) - (box.width / 2), HEIGHT - box.height)

        :param res: The resolution of the window.
        :param box: The bounding box of the object.
        :return: A location corresponding to the bottom center of the window.
        """
        w = int((res.width / 2) - (box.w / 2))
        h = res.height - box.h
        return Location(w, h)

    @staticmethod
    def bottom_right(res: Resolution, box: Rect) -> 'Location':
        """
        Corresponds to the bottom right of the window.
        The coordinate calculations can be summed by:
        (WIDTH - box.width, HEIGHT - box.height)

        :param res: The resolution of the window.
        :param box: The bounding box of the object.
        :return: A location corresponding to the bottom right of the window.
        """
        return Location(res.width - box.w, res.height - box.h)

    @staticmethod
    def random(res: Resolution, box: Rect) -> 'Location':
        """
        Corresponds to a random location in the window.
        The coordinate calculations can be summed by:
        (RANDOM_W, RANDOM_H)

        where RANDOM_W is random(0, WIDTH - box.width)
        and RANDOM_H is random(0, HEIGHT - box.height)

        :param res: The resolution of the window.
        :param box: The bounding box of the object.
        :return: A random location in the window.
        """
        w = randint(0, res.width - box.w)
        h = randint(0, res.height - box.h)
        return Location(w, h)

    def add(self, x: int = 0, y: int = 0) -> None:
        """
        Adds the given x and y amounts to the location.

        :param x: The amount of width to add to the location.
        :param y: The amount of height to add to the location.
        :return: None.
        """
        self.x += x
        self.y += y

    def sub(self, x: int = 0, y: int = 0) -> None:
        """
        Subtracts the given x and y amounts from the location.

        :param x: The amount of width to remove from the location.
        :param y: The amount of height to remove from the location.
        :return: None.
        """
        self.x -= x
        self.y -= y

    def mul(self, scalar: float) -> None:
        """
        Multiplies the current location by the given scalar.

        :param scalar: The scalar to multiply the location by.
        :return: None.
        """
        self.x = int(self.x * scalar)
        self.y = int(self.y * scalar)

    def dist(self, loc: 'Location') -> float:
        """
        Gets the distance between this location instance and another.
        The given distance will always be positive.

        :param loc: The other location.
        :return: The distance between this location instance and another.
        """
        return sqrt(self.dist_sqr(loc))

    def dist_x(self, loc: 'Location') -> int:
        """
        Gets the width difference between this location and another.
        The given difference will always be positive.

        :param loc: The other location.
        :return: The width difference between this location and another.
        """
        return abs(self.x - loc.x)

    def dist_y(self, loc: 'Location') -> int:
        """
        Gets the height difference between this location and another.
        The given difference will always be positive.

        :param loc: The other location.
        :return: The height difference between this location and another.
        """
        return abs(self.y - loc.y)

    def dist_sqr(self, loc: 'Location') -> float:
        """
        Gets the distance^2 between this location instance and another.

        :param loc: The other location.
        :return: The approximate distance between this location instance and another.
        """
        x = self.x - loc.x
        y = self.y - loc.y
        return pow(x, 2) + pow(y, 2)

    def midpoint(self, loc: 'Location') -> 'Location':
        """
        Gets the midpoint between this location instance and another.

        :param loc: The other location.
        :return: A new location of the midpoint between this location instance and the given.
        """
        x = round((self.x + loc.x) / 2)
        y = round((self.y + loc.y) / 2)
        return Location(x, y)

    def as_tuple(self) -> tuple[int, int]:
        """
        Gets the current location as a tuple of two ints, the first being x and the second y.

        :return: The current location as a tuple.
        """
        return self.x, self.y

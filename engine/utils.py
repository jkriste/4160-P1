from random import randint

from pygame.color import Color

BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)


def random_color() -> Color:
    """
    Generates a random color.

    :return: A random color.
    """
    return Color(randint(0, 255), randint(0, 255), randint(0, 255))

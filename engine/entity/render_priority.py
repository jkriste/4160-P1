from enum import Enum

DEFAULT_PRIORITY = 10


class RenderPriority:
    """
    A simple class used to sort entities by when they should be rendered.
    """

    def __init__(self, priority: int = DEFAULT_PRIORITY):
        self._priority = priority
        self._dirty = True

    @property
    def priority(self) -> int:
        """
        Gets the render priority.
        Render priority is represented as a single int.
        The higher the priority, the later it will be rendered, making it look like it's on top of other entities.
        The lower the priority, the sooner it will be rendered, making it look like it's under other entities.

        :return: The render priority, as an int.
        """
        return self._priority

    @priority.setter
    def priority(self, value: int) -> None:
        """
        Sets the priority value of the Entity.
        Marks the render priority as "dirty" (`self.dirty`).

        :param value: The new render priority.
        :return: None.
        """
        self._priority = value
        self._dirty = True

    @property
    def dirty(self) -> bool:
        """
        Gets whether the RenderPriority has been changed since last tick, or if the render priority is "dirty".
        On next tick, it is expected that the EntityHandler will re-sort the Entities and call `RenderPriority.clean()`

        :return: True if the RenderPriority has been changed since last tick, false otherwise.
        """
        return self._dirty

    def clean(self) -> None:
        """
        Sets the RenderPriority as clean.
        Should only be called by the EntityHandler.

        :return: None.
        """
        self._dirty = False


class Priority(Enum):
    """
    A preset selection of render priorities.
    Each render priority is separated by 5 layers in case of self-made render priorities.
    """

    LOWEST = RenderPriority(0)
    LOW = RenderPriority(5)
    NORMAL = RenderPriority(10)
    HIGH = RenderPriority(15)
    HIGHEST = RenderPriority(20)

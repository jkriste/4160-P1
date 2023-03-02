from abc import ABC, abstractmethod
from typing import Union

import pygame.event
from pygame import Rect
from pygame.surface import Surface

from engine.entity.render_priority import RenderPriority, Priority
from engine.window.location import Location


class Entity(ABC):
    """
    An abstract class that represents an entity.
    An entity is anything that can be drawn to the screen or interacted with through the window.
    """

    def __init__(self, loc: Location = Location(0, 0), priority: Union[int, RenderPriority, Priority] = 10) -> None:
        self._loc = loc
        self._loaded = False
        self._visible = False
        self._removed = False
        self._should_remove = False
        if isinstance(priority, RenderPriority | Priority):
            self._priority = priority if isinstance(priority, RenderPriority) else priority.value
        else:
            self._priority = RenderPriority(priority)

    @abstractmethod
    def tick(self, tick_count: int) -> None:
        """
        Ticks the Entity, telling it to update its state.

        :param tick_count: The current tick represented as an integer.
        :return: None.
        """
        ...

    @abstractmethod
    def draw(self, surface: Surface) -> None:
        """
        Tells the Entity to draw itself to the given Surface.

        :param surface: The surface to draw to.
        :return: None.
        """
        ...

    @abstractmethod
    def on_load(self) -> None:
        """
        Used to load anything the Entity hasn't already loaded upon instantiation.

        :return: None.
        """
        ...

    @abstractmethod
    def bounds(self) -> Rect:
        """
        Gets the bounding box of the Entity.

        :return: The bounding box of the Entity.
        """
        ...

    @property
    def loc(self) -> Location:
        """
        Gets the current location of the Entity.

        :return: The location of the Entity.
        """
        return self._loc

    @loc.setter
    def loc(self, loc: Union[Location, tuple[int, int]]) -> None:
        """
        Sets the current location of the Entity.

        :param loc: The new location of the Entity.
        :return: None.
        """
        self._loc = loc if isinstance(loc, Location) else Location(loc[0], loc[1])

    @property
    def priority(self) -> RenderPriority:
        return self._priority

    @priority.setter
    def priority(self, priority: Union[int, RenderPriority, Priority]) -> None:
        """
        Sets the render priority of the entity instance.

        :param priority: The new render priority.
        :return: None.
        """
        if isinstance(priority, RenderPriority | Priority):
            self._priority = priority if isinstance(priority, RenderPriority) else priority.value
        else:
            self._priority = RenderPriority(priority)

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        self._visible = value

    def should_draw(self) -> bool:
        """
        Checks if the Entity should be drawn to the Surface.

        :return: True if the Entity should be drawn to the Window, False otherwise.
        """
        return self._visible and not self._removed and self._loaded

    def should_remove(self) -> bool:
        """
        Checks if the Entity should be removed by the EntityHandler.

        :return: True if the Entity should be removed by the Window, False otherwise.
        """
        if not self._loaded:
            return False
        return self._should_remove and not self._removed

    def dispose(self) -> None:
        """
        Marks the given Entity as disposable.
        This will tell the EntityHandler that it should remove this Entity.

        :return: None.
        """
        self._should_remove = True
        print(f"Entity '{type(self).__name__}' marked for disposal.")

    def remove(self) -> None:
        """
        Forcefully removes the Entity.
        Should not be called by anything but the EntityHandler.

        :return: None.
        :raise EntityError: Raised if the Entity was already removed or unloaded.
        """
        if self._removed or not self._loaded:
            raise EntityError(f"Tried to remove already-removed and/or unloaded entity '{type(self).__name__}'.")
        self._visible = False
        self._removed = True
        self._loaded = False
        print(f"Entity '{type(self).__name__}' removed.")

    def spawn(self) -> None:
        """
        Spawns the Entity.
        Calls on_load() and sets the entity's visibility to True.

        :return: None.
        """
        if not self._loaded:
            self.on_load()
            self._loaded = True
            self._visible = True

    def clicked_on(self, mouse_pos: tuple[int, int]) -> bool:
        """
        Checks if the Entity was clicked on, given the mouse position.

        :param mouse_pos: The coordinates of the mouse as a tuple (x, y)
        :return: True if the Entity collides with the given mouse position, false otherwise.
        """
        return self.bounds().collidepoint(mouse_pos)

    def collides_with(self, entity: 'Entity') -> bool:
        """
        Checks if the given Entity is colliding with the current Entity instance.

        :param entity: The other entity to check.
        :return: True if the Entity collides with the current instance, false otherwise.
        """
        return self.bounds().colliderect(entity.bounds())


class EntityHandler:
    """
    Represents an Entity registry and handles passive Entity states.
    """

    def __init__(self):
        self._entities: dict[int, list[Entity]] = {}
        self._collision_listeners: list[CollisionListener] = []

    def tick(self, tick_count: int) -> None:
        """
        Ticks all registered entities.
        Also checks:
        - If any entity's render priorities have changed, if true, will be re-sorted.
        - If any entity is marked as disposed, if true, will remove the entity.

        :param tick_count: The current tick count.
        :return: None.
        """
        for listener in self._collision_listeners:
            listener.collision_check()

        if self._check_dirty():
            self._clean()

        for _, entity_list in self._entities.items():
            for entity in entity_list:
                if entity.should_remove():
                    entity.remove()
                    entity_list.remove(entity)
                    continue
                entity.tick(tick_count)

    def draw(self, surface: Surface) -> None:
        """
        Draws all registered entities.
        If the entity is invisible or should not be drawn, it will be skipped over.

        :param surface: The surface to draw to.
        :return: None.
        """
        for _, entity_list in self._entities.items():
            for entity in entity_list:
                if entity.should_draw():
                    entity.draw(surface)

    def register_entities(self, *args: Entity) -> None:
        """
        Registers the given entities, sorted by their render priority.

        :param args: The entities to register.
        :return: None.
        """
        for entity in args:
            priority = entity.priority.priority
            entity_list = self._entities.get(priority, [])
            entity_list.append(entity)
            self._entities[priority] = entity_list

    def register_entity(self, entity: Entity) -> None:
        """
        Registers the given entity, sorted by their render priority.

        :param entity: The entity to register.
        :return: None.
        """
        priority = entity.priority.priority
        entity_list = self._entities.get(priority, [])
        entity_list.append(entity)
        self._entities[priority] = entity_list

    def spawn_all(self) -> None:
        """
        Spawns all registered entities, regardless if they're already spawned.

        :return: None.
        """
        for _, entity_list in self._entities.items():
            for entity in entity_list:
                entity.spawn()

    def dispose_all(self) -> None:
        """
        Disposes all registered entities, regardless if they're already marked for disposal.

        :return: None.
        """
        for _, entity_list in self._entities.items():
            for entity in entity_list:
                entity.dispose()

    def remove_all(self) -> None:
        """
        Removes all registered entities, regardless if they're marked for disposal.

        :return: None.
        """
        for _, entity_list in self._entities.items():
            for entity in entity_list:
                entity.remove()

    def clear(self) -> None:
        """
        Clears all entities. Does not call `Entity.dispose()` or `Entity.remove()`.

        :return: None.
        """
        self._entities.clear()

    def _check_dirty(self) -> bool:
        """
        Checks if any of the registered entities have been changed since last tick.

        :return: True if a registered entity has been changed since last tick, false otherwise.
        """
        for _, entities in self._entities.items():
            for entity in entities:
                if entity.priority.dirty:
                    return True
        return False

    def _clean(self) -> None:
        """
        Reorganizes any dirty entities.

        :return: None.
        """
        dirty = []
        for _, entities in self._entities.items():
            for entity in entities:
                if entity.priority.dirty:
                    dirty.append(entity)
                    entities.remove(entity)
        for entity in dirty:
            entity_list = self._entities.get(entity.priority.priority, [])
            entity_list.append(entity)
            self._entities[entity.priority.priority] = entity_list
            entity.priority.clean()

    def listen(self, entity: Entity, collides_with: list[Entity], event_id: int) -> None:
        self._collision_listeners.append(CollisionListener(entity, collides_with, event_id))


class CollisionListener:

    def __init__(self, entity: Entity, collides_with: list[Entity], event_id: int):
        self._entity = entity
        self._collides_with = collides_with
        self._event_id = event_id

    def collision_check(self) -> None:
        for entity in self._collides_with:
            if entity.collides_with(self._entity):
                pygame.event.post(pygame.event.Event(self._event_id))


class EntityError(Exception):

    def __init__(self, msg: str = ''):
        super().__init__(msg)

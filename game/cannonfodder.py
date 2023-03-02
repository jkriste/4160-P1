from random import randint

import pygame.font
from pygame.event import Event

from engine.entity.circle import PymunkCircle
from engine.entity.rectangle import PymunkRectangle
from engine.entity.string import String
from engine.utils import BLACK, new_user_event, spawn_all, random_color, WHITE
from engine.window.resolution import Resolutions
from engine.window.window import Window

RESOLUTION = Resolutions.P720
FONT = pygame.font.SysFont("comicsansms", 32, True)
UPDATE_FPS_EVENT = new_user_event()
CLOSE_GAP_EVENT = new_user_event()


class CannonFodder:

    def __init__(self):
        self.window = Window(RESOLUTION, BLACK, title="Cannon Fodder")
        self.window.space.gravity = (0, 200)
        self.fps_string = String(FONT, "FPS: 0")
        pygame.time.set_timer(UPDATE_FPS_EVENT, 500)
        self.register_events()
        self.spawn_boundaries()
        self.spawn_balls()
        pygame.time.set_timer(CLOSE_GAP_EVENT, 9000, 1)
        self.window.start()

    def register_events(self) -> None:
        """
        Registers the event that the window will listen for.

        :return: None.
        """
        self.window.register_event(pygame.QUIT, self.on_quit)
        self.window.register_event(pygame.KEYDOWN, self.on_key_press)
        self.window.register_event(CLOSE_GAP_EVENT, self.close_gap)
        self.window.register_event(UPDATE_FPS_EVENT, self.update_fps)

    def spawn_boundaries(self) -> None:
        """
        Spawns the boundaries for the collision of the window + barriers.

        :return: None.
        """
        top = PymunkRectangle((0, 0), (RESOLUTION.w, 0), 10, self.window.space)
        left = PymunkRectangle((0, 0), (0, RESOLUTION.h), 10, self.window.space)
        right = PymunkRectangle((RESOLUTION.w, 0), (RESOLUTION.w, RESOLUTION.h), 10, self.window.space)
        bottom = PymunkRectangle((0, RESOLUTION.h), (RESOLUTION.w, RESOLUTION.h), 10, self.window.space)
        top_wall = PymunkRectangle((900, 0), (900, 400), 50, self.window.space, color=WHITE)
        bottom_wall = PymunkRectangle((900, 600), (900, RESOLUTION.h), 50, self.window.space, color=WHITE)
        top_shelf = PymunkRectangle((1110, 600), (1230, 600), 10, self.window.space, color=WHITE)
        bottom_shelf = PymunkRectangle((1080, 650), (1200, 650), 10, self.window.space, color=WHITE)
        self.window.register_entities(top, left, right, bottom, top_wall, bottom_wall, top_shelf, bottom_shelf)
        spawn_all(top, left, right, bottom, top_wall, bottom_wall, top_shelf, bottom_shelf)

    def spawn_balls(self) -> None:
        """
        Spawns 100 balls on the left side, setting their velocity towards the right.

        :return: None.
        """
        for _ in range(100):
            circle = PymunkCircle(7, self.window.space, random_color())
            circle.loc.x = randint(100, 200)
            circle.loc.y = randint(200, 600)
            circle.body.velocity = (500, -20)
            self.window.register_entity(circle)
            circle.spawn()

    def close_gap(self, _: Event) -> None:
        """
        Programmed to close the gap after 9 seconds.

        :param _: The event, unused/ignored.
        :return: None.
        """
        print("Closed gap.")
        gap = PymunkRectangle((900, 400), (900, 600), 50, self.window.space, color=WHITE)
        self.window.register_entity(gap)
        gap.spawn()

    def update_fps(self, _: Event) -> None:
        """
        Updates the frames per second (fps) of the program.
        The FPS is currently capped at 30 frames per second.

        :param _: The event, unused/ignored.
        :return: None.
        """
        if not self.fps_string.visible:
            self.window.register_entity(self.fps_string)
            self.fps_string.spawn()
        self.fps_string.set_text(f"FPS: {int(self.window.clock.get_fps())}")

    def on_quit(self, _: Event) -> None:
        """
        A callable method for when a user closes the window or presses the ESCAPE key.

        :param _: The event, ignored/unused.
        :return: None.
        """
        self.window.stop()
        print("Game stopping...")

    def on_key_press(self, event: Event) -> None:
        """
        A callable method for when a user presses a key.

        :param event: The event information.
        :return: None.
        """
        if event.key is pygame.K_ESCAPE:
            self.on_quit(event)

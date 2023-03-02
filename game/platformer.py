from random import randint

import pygame
from pygame.event import Event

from engine.entity.image import Image
from engine.entity.parallax import Parallax
from engine.entity.sprite import Sprite, SpriteState
from engine.entity.string import String
from engine.event.events import new_event
from engine.window.location import Location
from engine.window.resolution import Resolutions
from engine.window.window import Window
from game.presets import ParallaxPresets, ParallexPreset, SoundPresets

RESOLUTION = Resolutions.P720
TITLE_FONT = pygame.font.Font('game/assets/font/kenvector_future.ttf', 40)
SUBTITLE_FONT = pygame.font.Font('game/assets/font/kenpixel_mini_square.ttf', 24)
COLLIDE_EVENT = new_event()
UPDATE_SCORE_EVENT = new_event()
INVINCIBLE_DISABLE_EVENT = new_event()
SPAWN_BAT_EVENT = new_event()


class Platformer:

    def __init__(self):
        self.window = Window(RESOLUTION, title='Runner', fps=24)
        self.register_events()
        self.bats: list[Sprite] = []
        self.init_entities()
        self.config_entities()
        self.new_game()
        self.register_entities()
        self.window.entity_handler.spawn_all()
        for bat in self.bats:
            bat.visible = False
        self.title.visible = True
        self.subtitle.visible = True
        self.game_over.visible = False
        self.score_str.visible = False
        self.window.start()

    def new_game(self) -> None:
        self.score = 0
        self.started = False
        self.invincible = False
        self.preset = ParallaxPresets.random()
        self.parallax = self.from_preset(self.preset)
        self.window.entity_handler.register_entity(self.parallax)
        self.parallax.spawn()
        self.character.min_y(RESOLUTION.value, self.preset.y_offset)
        self.character.state = SpriteState.IDLE
        self.set_entities()
        self.title.color = self.preset.color
        self.subtitle.color = self.preset.color
        self.game_over.color = self.preset.color
        self.score_str.color = self.preset.color
        self.health.index = 0
        for bat in self.bats:
            bat.visible = False
        self.title.visible = True
        self.subtitle.visible = True
        self.game_over.visible = False
        self.score_str.visible = False

    def register_events(self) -> None:
        self.window.event_handler.register(pygame.QUIT, self.on_quit)
        self.window.event_handler.register(pygame.KEYDOWN, self.on_key_press)
        self.window.event_handler.register(COLLIDE_EVENT, self.on_collide)
        self.window.event_handler.register(UPDATE_SCORE_EVENT, self.update_score)
        self.window.event_handler.register(INVINCIBLE_DISABLE_EVENT, self.disable_invincible)
        self.window.event_handler.register(SPAWN_BAT_EVENT, self.spawn_bat)
        pygame.time.set_timer(UPDATE_SCORE_EVENT, 1000, -1)
        pygame.time.set_timer(SPAWN_BAT_EVENT, 666, -1)

    def init_entities(self) -> None:
        self.title = String(TITLE_FONT, 'RUNNER')
        self.subtitle = String(SUBTITLE_FONT, 'press space to start')
        self.game_over = String(TITLE_FONT, 'GAME OVER')
        self.score_str = String(SUBTITLE_FONT, 'You lasted 0 seconds\npress space to restart')
        self.seconds = String(SUBTITLE_FONT, '0', loc=Location(10, 10))
        self.character = Sprite(RESOLUTION.value, scalar=3.5)
        self.health = Image('game/assets/health', 7, scalar=2.75)
        for i in range(4):
            self.bats.append(Sprite(RESOLUTION.value, scalar=3.5, gravity=False, default_state=SpriteState.MID_AIR))
            self.bats[i].loc.x = -250

    def set_entities(self) -> None:
        self.title.loc = Location.center(RESOLUTION.value, self.title.bounds())
        self.game_over.loc = Location.center(RESOLUTION.value, self.game_over.bounds())
        self.subtitle.loc = Location.center(RESOLUTION.value, self.subtitle.bounds())
        self.subtitle.loc.add(y=50)
        self.score_str.loc = Location.center(RESOLUTION.value, self.score_str.bounds())
        self.score_str.loc.add(y=50)
        self.health.loc = Location.top_right(RESOLUTION.value, self.health.bounds())
        self.character.loc = Location.bottom_left(RESOLUTION.value, self.character.bounds())
        self.character.loc.add(50, -self.preset.y_offset)

    def config_entities(self) -> None:
        self.character.add_state(SpriteState.IDLE, 'game/assets/character/idle', 12)
        self.character.add_state(SpriteState.JUMP, 'game/assets/character/jump', 1)
        self.character.add_state(SpriteState.LAND, 'game/assets/character/land', 1)
        self.character.add_state(SpriteState.MID_AIR, 'game/assets/character/mid_air', 2)
        self.character.add_state(SpriteState.RUN, 'game/assets/character/run', 8)
        for bat in self.bats:
            bat.add_state(SpriteState.MID_AIR, 'game/assets/bat/mid_air', 4)
        self.window.entity_handler.listen(self.character, self.bats, COLLIDE_EVENT)

    def register_entities(self) -> None:
        self.window.entity_handler.register_entities(self.title, self.game_over, self.subtitle, self.score_str,
                                                     self.seconds, self.character, self.health)
        for bat in self.bats:
            print('bat registered')
            self.window.entity_handler.register_entity(bat)

    def play_sound(self, path: str) -> None:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()

    def from_preset(self, pre: ParallexPreset) -> Parallax:
        return Parallax(pre.path, pre.layers, RESOLUTION)

    def spawn_bat(self, _: Event) -> None:
        if self.title.visible or self.game_over.visible:
            return
        i = 0
        for current_bat in self.bats:
            if current_bat.loc.x > -100:
                print(f'Bat {i} loc: {current_bat.loc.x}, {current_bat.loc.y}')
                i += 1
                continue
            current_bat.visible = True
            vel_x = randint(20, 50)
            current_bat.loc.x = RESOLUTION.value.width + 200
            current_bat.loc.y = randint(0, RESOLUTION.value.height - self.preset.y_offset - 100)
            current_bat.velocity = (vel_x, 0)
            print(f'Bat {i} spawned.')
            i += 1
            break
        print('No bat to spawn?')

    def on_key_press(self, event: Event) -> None:
        if event.key == pygame.K_SPACE:
            print('Space pressed.')
            if self.game_over.visible:
                self.parallax.dispose()
                self.new_game()
                return
            if self.title.visible:
                self.title.visible = False
                self.subtitle.visible = False
                self.parallax.scroll = self.preset.scroll
                self.parallax.speed = self.preset.speed
                self.parallax.delta = self.preset.delta
                self.character.state = SpriteState.RUN
                return
            if self.character.state is SpriteState.RUN:
                self.character.velocity = (0, -30)
        elif event.key == pygame.K_ESCAPE:
            self.on_quit(event)
        elif event.key == pygame.K_KP_ENTER:
            self.health.next()

    def on_collide(self, _: Event) -> None:
        if self.invincible:
            return
        self.health.next()
        if self.health.index == 6:
            self.on_death()
        else:
            self.play_sound(SoundPresets.rand_hurt())
            self.invincible = True
            pygame.time.set_timer(INVINCIBLE_DISABLE_EVENT, 2000)

    def disable_invincible(self, _: Event) -> None:
        self.invincible = False

    def update_score(self, _: Event) -> None:
        if self.game_over.visible or self.title.visible:
            return
        self.score += 1
        self.seconds.set_text(str(self.score))

    def on_death(self) -> None:
        self.play_sound(SoundPresets.rand_death())
        self.game_over.visible = True
        self.score_str.set_text(f'You lasted {self.score} seconds')
        self.score_str.loc = Location.center(RESOLUTION.value, self.score_str.bounds())
        self.score_str.loc.add(y=50)
        self.score_str.visible = True

    def on_quit(self, _: Event) -> None:
        print('Closing game...')
        self.window.stop()

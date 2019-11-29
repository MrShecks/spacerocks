import pygame
import random

from entities import entity
from gamelib import sprite
from gamelib import spritesheet
from gamelib import utils


class Factory(object):
    # --------------------------------------------------------------------------------------------------

    class Config(object):
        def __init__(self, powerup_type, sound, name, description, text_color=(255, 255, 255)):
            self._powerup_type = powerup_type
            self._sound = sound
            self._name = name
            self._description = description
            self._text_color = text_color

        @property
        def powerup_type(self):
            return self._powerup_type

        @property
        def sound(self):
            return self._sound

        @property
        def name(self):
            return self._name

        @property
        def description(self):
            return self._description

        @property
        def text_color(self):
            return self._text_color

    # --------------------------------------------------------------------------------------------------

    TYPE_POWER_YELLOW = 0
    TYPE_POWER_RED = 1
    TYPE_POWER_WHITE = 2

    TYPE_STAR_YELLOW = 3
    TYPE_STAR_RED = 4
    TYPE_STAR_WHITE = 5

    TYPE_ENERGY_YELLOW = 6
    TYPE_ENERGY_RED = 7
    TYPE_ENERGY_WHITE = 8

    TYPE_SHIELD_YELLOW = 9
    TYPE_SHIELD_RED = 10
    TYPE_SHIELD_WHITE = 11

    _TYPE_COUNT = 12

    _FRAME_COUNT = 11
    _FRAME_TIME = 150

    _WIDTH = 75
    _HEIGHT = 75

    _TIME_TO_LIVE = 10

    _COLOR_RED = (200, 0, 0)
    _COLOR_YELLOW = (200, 200, 0)
    _COLOR_WHITE = (255, 255, 255)

    _game = None
    _frames = []
    _sounds = []
    _powerup_config = {}

    @classmethod
    def init(cls, game):
        if cls._game is None:
            cls._frames = spritesheet.SpriteSheet(game.image_cache.get('powerup_set_01'), Factory._WIDTH, Factory._HEIGHT)

            cls._sounds.append(game.audio_cache.get('powerup_01'))
            cls._sounds.append(game.audio_cache.get('powerup_02'))
            cls._sounds.append(game.audio_cache.get('powerup_03'))
            cls._sounds.append(game.audio_cache.get('powerup_04'))
            cls._sounds.append(game.audio_cache.get('powerup_05'))

            # FIXME: Python must have a nicer way to do this
            cls._powerup_config[Factory.TYPE_POWER_YELLOW] = Factory.Config(Factory.TYPE_POWER_YELLOW, random.choice(cls._sounds), 'Yellow Power-up', '', Factory._COLOR_YELLOW)
            cls._powerup_config[Factory.TYPE_POWER_RED] = Factory.Config(Factory.TYPE_POWER_RED, random.choice(cls._sounds), 'Red Power-up', '', Factory._COLOR_RED)
            cls._powerup_config[Factory.TYPE_POWER_WHITE] = Factory.Config(Factory.TYPE_POWER_WHITE, random.choice(cls._sounds), 'White Power-up', '', Factory._COLOR_WHITE)

            cls._powerup_config[Factory.TYPE_STAR_YELLOW] = Factory.Config(Factory.TYPE_STAR_YELLOW, random.choice(cls._sounds), 'Yellow Star', '', Factory._COLOR_YELLOW)
            cls._powerup_config[Factory.TYPE_STAR_RED] = Factory.Config(Factory.TYPE_STAR_RED, random.choice(cls._sounds), 'Red Star', '', Factory._COLOR_RED)
            cls._powerup_config[Factory.TYPE_STAR_WHITE] = Factory.Config(Factory.TYPE_STAR_WHITE, random.choice(cls._sounds), 'White Star', '', Factory._COLOR_WHITE)

            cls._powerup_config[Factory.TYPE_ENERGY_YELLOW] = Factory.Config(Factory.TYPE_ENERGY_YELLOW, random.choice(cls._sounds), 'Yellow Energy', '', Factory._COLOR_YELLOW)
            cls._powerup_config[Factory.TYPE_ENERGY_RED] = Factory.Config(Factory.TYPE_ENERGY_RED, random.choice(cls._sounds), 'Red Energy', '', Factory._COLOR_RED)
            cls._powerup_config[Factory.TYPE_ENERGY_WHITE] = Factory.Config(Factory.TYPE_ENERGY_WHITE, random.choice(cls._sounds), 'White Energy', '', Factory._COLOR_WHITE)

            cls._powerup_config[Factory.TYPE_SHIELD_YELLOW] = Factory.Config(Factory.TYPE_SHIELD_YELLOW, random.choice(cls._sounds), 'Yellow Shield', '', Factory._COLOR_YELLOW)
            cls._powerup_config[Factory.TYPE_SHIELD_RED] = Factory.Config(Factory.TYPE_SHIELD_RED, random.choice(cls._sounds), 'Red Shield', '', Factory._COLOR_RED)
            cls._powerup_config[Factory.TYPE_SHIELD_WHITE] = Factory.Config(Factory.TYPE_SHIELD_WHITE, random.choice(cls._sounds), 'White Shield', '', Factory._COLOR_WHITE)

            cls._game = game

    @classmethod
    def create(cls, x, y, powerup_type=None):

        if powerup_type is None or powerup_type < 0 or powerup_type >= Factory._TYPE_COUNT:
            powerup_type = random.randrange(Factory._TYPE_COUNT)

        frames = cls._frames[powerup_type * Factory._FRAME_COUNT:(powerup_type + 1) * Factory._FRAME_COUNT]

        return PowerUp(x, y, cls._powerup_config[powerup_type], frames, Factory._FRAME_TIME, Factory._TIME_TO_LIVE)


class PowerUp(entity.Entity):
    _MIN_VELOCITY = 100
    _MAX_VELOCITY = 200

    _MIN_ROTATION_VELOCITY = 200
    _MAX_ROTATION_VELOCITY = 400

    _COLLISION_RADIUS = 38

    def __init__(self, x, y, config, frames, frame_speed, time_to_live):
        super().__init__(x, y, frames, 0, self.choose_velocity(PowerUp._MIN_VELOCITY, PowerUp._MAX_VELOCITY))

        self._config = config
        self._time_to_live = time_to_live

        self.set_frame_animator(sprite.LinearFrameAnimator(frame_speed, True))
        self.set_rotation_velocity(self.choose_range(PowerUp._MIN_ROTATION_VELOCITY, PowerUp._MAX_ROTATION_VELOCITY))

    @property
    def config(self):
        return self._config

    @property
    def entity_type(self):
        return entity.Entity.TYPE_POWERUP

    @property
    def powerup_type(self):
        return self._config.powerup_type

    @property
    def radius(self):
        return int(PowerUp._COLLISION_RADIUS * self.scale)

    def update(self, scene, dt):
        super().update(scene, dt)

        if self._time_to_live > 0:
            self._time_to_live -= dt
            self.rect.center = utils.clamp_point_to_rect(self.rect.center, scene.rect)

        else:
            self.kill()

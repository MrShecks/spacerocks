import pygame
import random

from entities import entity
from gamelib import sprite
from gamelib import spritesheet
from gamelib import utils

class Factory (object):

    TYPE_POWER_YELLOW       = 0
    TYPE_POWER_RED          = 1
    TYPE_POWER_WHITE        = 2

    TYPE_STAR_YELLOW        = 3
    TYPE_STAR_RED           = 4
    TYPE_STAR_WHITE         = 5

    TYPE_ENERGY_YELLOW      = 6
    TYPE_ENERGY_RED         = 7
    TYPE_ENERGY_WHITE       = 8

    TYPE_SHIELD_YELLOW      = 9
    TYPE_SHIELD_RED         = 10
    TYPE_SHIELD_WHITE       = 11

    _TYPE_COUNT             = 12

    _FRAME_COUNT            = 11
    _FRAME_TIME             = 150

    _WIDTH                  = 75
    _HEIGHT                 = 75

    _TIME_TO_LIVE           = 5

    _game                   = None
    _frames                 = []

    @classmethod
    def init (cls, game):
        if cls._game == None:

            cls._frames = spritesheet.SpriteSheet (game.image_cache.get ('powerup_set_01'), Factory._WIDTH, Factory._HEIGHT)
            cls._game = game

    @classmethod
    def create (cls, x, y, type = None):

        if type is None or type < 0 or type >= Factory._TYPE_COUNT:
            type = random.randrange (Factory._TYPE_COUNT)

        frames = cls._frames[type * Factory._FRAME_COUNT:(type + 1) * Factory._FRAME_COUNT]
        shield = PowerUp (x, y, type, frames, Factory._FRAME_TIME, Factory._TIME_TO_LIVE, cls._game.rect)

        return shield

class PowerUp (entity.Entity):

    _MIN_VELOCITY           = -200
    _MAX_VELOCITY           = 200

    _MAX_ROTATION_VELOCITY  = 200

    def __init__ (self, x, y, type, frames, frame_speed, time_to_live, screen_rect):
        super ().__init__ (x, y, frames, 0, self._get_velocity ())

        self._type = type
        self._time_to_live = time_to_live
        self._screen_rect = screen_rect

        self.set_frame_animator (sprite.LinearFrameAnimator (frame_speed, True))
        self.set_rotation_velocity (random.randrange (-PowerUp._MAX_ROTATION_VELOCITY, PowerUp._MAX_ROTATION_VELOCITY))

    @property
    def entity_type (self):
        return entity.Entity.TYPE_POWERUP

    def update (self, scene, dt):
        super ().update (scene, dt)

        if self._time_to_live > 0:
            self._time_to_live -= dt
            self.rect.center = utils.clamp_point_to_rect (self.rect.center, self._screen_rect)

        else:
            self.kill ()

    def _get_velocity (self):
        return pygame.math.Vector2 (random.randrange (PowerUp._MIN_VELOCITY, PowerUp._MAX_VELOCITY),
                                    random.randrange (PowerUp._MIN_VELOCITY, PowerUp._MAX_VELOCITY))
import pygame
import random

from entities import entity
from gamelib import sprite
from gamelib import spritesheet
from gamelib import utils

class Factory (object):

    _TILE_WIDTH      = 128
    _TILE_HEIGHT     = 128
    _TILE_SET        = 'asteroid_set_01'

    _game           = None
    _asteroid_tiles = None

    @classmethod
    def init (cls, game):
        if cls._game == None:

            cls._asteroid_tiles = spritesheet.SpriteSheet (game.image_cache.get (Factory._TILE_SET),
                                                           Factory._TILE_WIDTH, Factory._TILE_HEIGHT)
            cls._game = game

    @classmethod
    def create (cls, x, y, type = None):

        if type is None or not (Asteroid._TYPE_FIRST <= type <= Asteroid._TYPE_LAST):
            type = random.randrange (Asteroid._TYPE_FIRST, Asteroid._TYPE_LAST + 1)

        return Asteroid (x, y, cls._asteroid_tiles, type, cls._game.rect)


class Asteroid (entity.Entity):

    TYPE_TINY               = 0
    TYPE_SMALL              = 1
    TYPE_MEDIUM             = 2
    TYPE_LARGE              = 3

    _TYPE_FIRST             = TYPE_TINY
    _TYPE_LAST              = TYPE_LARGE

    _MIN_VELOCITY           = 100
    _MAX_VELOCITY           = 200

    _MIN_ROTATE_VELOCITY    = 50
    _MAX_ROTATE_VELOCITY    = 200

    _FRAME_SPEED            = 100

    _COLLISION_RADIUS       = 44

    _TYPE_TO_SCALE = {
        TYPE_LARGE:         1.00,
        TYPE_MEDIUM:        0.80,
        TYPE_SMALL:         0.60,
        TYPE_TINY:          0.40
    }


    def __init__ (self, x, y, frames, type, screen_rect):
        super ().__init__ (x, y, frames, 0, self.choose_velocity (Asteroid._MIN_VELOCITY, Asteroid._MAX_VELOCITY))

        self._type = type
        self._screen_rect = screen_rect
        self.set_rotation_velocity (self.choose_range (Asteroid._MIN_ROTATE_VELOCITY, Asteroid._MAX_ROTATE_VELOCITY))
        self.set_frame_animator (sprite.LinearFrameAnimator (Asteroid._FRAME_SPEED, True))
        self.set_scale (Asteroid._TYPE_TO_SCALE[type])

    @property
    def entity_type (self):
        # FIXME: Return the correct subtype
        return entity.Entity.TYPE_ASTEROID_SMALL

    @property
    def radius (self):
        return int (Asteroid._COLLISION_RADIUS * self.scale)

    def reflect (self):
        self.set_velocity (self.velocity.x * -1, self.velocity.y * -1)

    def update (self, scene, dt):
        super ().update (scene, dt)

        # If the asteroid runs off the edge of the screen it should warp to the opposite side
        self.rect.center = utils.clamp_point_to_rect (self.rect.center, scene.rect)

    def get_shards (self):

        shard_type = {
            Asteroid.TYPE_TINY:     (0, 0),
            Asteroid.TYPE_SMALL:    (2, Asteroid.TYPE_TINY),
            Asteroid.TYPE_MEDIUM:   (2, Asteroid.TYPE_SMALL),
            Asteroid.TYPE_LARGE:    (2, Asteroid.TYPE_MEDIUM)
        }[self._type]

        shards = []

        for n in range (shard_type[0]):
            shards.append (Factory.create (self.position.x, self.position.y, shard_type[1]))

        return shards
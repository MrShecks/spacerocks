import random

from entities import entity
from gamelib import sprite
from gamelib import spritesheet
from gamelib import utils


class Factory(object):
    # --------------------------------------------------------------------------------------------------

    class Config(object):
        def __init__(self, scale, max_hit_points, max_damage_points, max_shards, shard_type):
            self._scale = scale
            self._max_hit_points = max_hit_points
            self._max_damage_points = max_damage_points
            self._max_shards = max_shards
            self._shard_type = shard_type

        @property
        def scale(self):
            return self._scale

        @property
        def max_hit_points(self):
            return self._max_hit_points

        @property
        def max_damage_points(self):
            return self._max_damage_points

        @property
        def max_shards(self):
            return self._max_shards

        @property
        def shard_type(self):
            return self._shard_type

    # --------------------------------------------------------------------------------------------------

    _TILE_WIDTH = 128
    _TILE_HEIGHT = 128
    _TILE_SET = 'asteroid_set_01'

    _game = None
    _asteroid_tiles = None
    _asteroid_config = {}

    @classmethod
    def init(cls, game):
        if cls._game is None:
            cls._asteroid_tiles = spritesheet.SpriteSheet(game.image_cache.get(Factory._TILE_SET),
                                                          Factory._TILE_WIDTH, Factory._TILE_HEIGHT)

            cls._asteroid_config[Asteroid.TYPE_LARGE] = Factory.Config(1.00, 200, 60, 2, Asteroid.TYPE_MEDIUM)
            cls._asteroid_config[Asteroid.TYPE_MEDIUM] = Factory.Config(0.80, 150, 40, 2, Asteroid.TYPE_SMALL)
            cls._asteroid_config[Asteroid.TYPE_SMALL] = Factory.Config(0.60, 100, 20, 2, Asteroid.TYPE_TINY)
            cls._asteroid_config[Asteroid.TYPE_TINY] = Factory.Config(0.40, 50, 10, 0, 0)

            cls._game = game

    @classmethod
    def create(cls, x, y, asteroid_type=None):

        if asteroid_type is None or not (Asteroid.TYPE_FIRST <= asteroid_type <= Asteroid.TYPE_LAST):
            asteroid_type = random.randrange(Asteroid.TYPE_FIRST, Asteroid.TYPE_LAST + 1)

        return Asteroid(x, y, cls._asteroid_tiles, asteroid_type, cls._asteroid_config[asteroid_type])


class Asteroid(entity.Entity):
    TYPE_TINY = 0
    TYPE_SMALL = 1
    TYPE_MEDIUM = 2
    TYPE_LARGE = 3

    TYPE_FIRST = TYPE_TINY
    TYPE_LAST = TYPE_LARGE

    _MIN_VELOCITY = 100
    _MAX_VELOCITY = 200

    _MIN_ROTATE_VELOCITY = 50
    _MAX_ROTATE_VELOCITY = 200

    _FRAME_SPEED = 100

    _COLLISION_RADIUS = 44

    def __init__(self, x, y, frames, asteroid_type, config):
        super().__init__(x, y, frames, 0, self.choose_velocity(Asteroid._MIN_VELOCITY, Asteroid._MAX_VELOCITY))

        self._asteroid_type = asteroid_type
        self._config = config

        self.set_rotation_velocity(self.choose_range(Asteroid._MIN_ROTATE_VELOCITY, Asteroid._MAX_ROTATE_VELOCITY))
        self.set_frame_animator(sprite.LinearFrameAnimator(Asteroid._FRAME_SPEED, True))
        self.set_scale(config.scale)

    @property
    def entity_type(self):
        # FIXME: Return the correct subtype
        return entity.Entity.TYPE_ASTEROID_SMALL

    @property
    def radius(self):
        return int(Asteroid._COLLISION_RADIUS * self.scale)

    @property
    def score(self):
        return self._config.max_hit_points * (self._asteroid_type + 1)

    def reflect(self):
        self.set_velocity(self.velocity.x * -1, self.velocity.y * -1)

    def update(self, scene, dt):
        super().update(scene, dt)

        # If the asteroid runs off the edge of the screen it should warp to the opposite side
        self.rect.center = utils.clamp_point_to_rect(self.rect.center, scene.rect)

    def get_shards(self):
        shards = []

        for n in range(self._config.max_shards):
            shards.append(Factory.create(self.position.x, self.position.y, self._config.shard_type))

        return shards

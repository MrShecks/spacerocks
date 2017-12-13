import pygame
import random

from gamelib import sprite
from gamelib import tileset

class Factory (object):

    TYPE_SMALL      = 0
    TYPE_MEDIUM     = 1
    TYPE_LARGE      = 2
    TYPE_HUGE       = 3

    _TYPE_FIRST     = TYPE_SMALL
    _TYPE_LAST      = TYPE_HUGE

    _MIN_VELOCITY   = -400
    _MAX_VELOCITY   = 400

    _game           = None
    _asteroid_tiles = []

    @classmethod
    def init (cls, game):
        if cls._game == None:
            cls._asteroid_tiles.append (tileset.TileSet (game.image_cache.get ('asteroid_set_01'), 32, 32))
            cls._asteroid_tiles.append (tileset.TileSet (game.image_cache.get ('asteroid_set_02'), 64, 64))
            cls._asteroid_tiles.append (tileset.TileSet (game.image_cache.get ('asteroid_set_03'), 96, 96))
            cls._asteroid_tiles.append (tileset.TileSet (game.image_cache.get ('asteroid_set_04'), 128, 128))

            cls._game = game

    @classmethod
    def create (cls, x, y, type = None):

        if type is None or not (cls._TYPE_FIRST <= type <= cls._TYPE_LAST):
            type = random.randrange (cls._TYPE_FIRST, cls._TYPE_LAST + 1)

        asteroid = Asteroid (x, y, cls._asteroid_tiles[type], 100, cls._game.rect)

        return asteroid


class Asteroid (sprite.KinematicSprite):

    _MIN_VELOCITY   = -400
    _MAX_VELOCITY   = 400

    # TODO: Maybe add a factory method (class method) to create entities of different sizes?

    def __init__ (self, x, y, frames, frame_speed, screen_rect):
        super ().__init__ (x, y, frames, 0, self._get_velocity ())

        self._screen_rect = screen_rect

        self.set_rotation_velocity (-50)
        self.set_frame_animator (sprite.LinearFrameAnimator (frame_speed, True))

    def update (self, dt):
        super ().update (dt)

        # If the asteroid runs off the edge of the screen it should warp to the opposite side
        if self.rect.centerx <= 0:
            self.rect.centerx = self._screen_rect.width
        elif self.rect.centerx >= self._screen_rect.width:
            self.rect.centerx = 0

        if self.rect.centery <= 0:
            self.rect.centery = self._screen_rect.height
        elif self.rect.centery >= self._screen_rect.height:
            self.rect.centery = 0

    def _get_velocity (self):
        return pygame.math.Vector2 (random.uniform (Asteroid._MIN_VELOCITY, Asteroid._MAX_VELOCITY),
                                    random.uniform (Asteroid._MIN_VELOCITY, Asteroid._MAX_VELOCITY))
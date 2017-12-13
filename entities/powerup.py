import pygame
import random

from gamelib import sprite
from gamelib import tileset

class Factory (object):

    _TIME_TO_LIVE       = 5

    _game               = None
    _tiles              = None

    @classmethod
    def init (cls, game):
        if cls._game == None:

            cls._tiles = tileset.TileSet (game.image_cache.get ('small_powerup_set'), PowerUp.WIDTH, PowerUp.HEIGHT)
            cls._game = game

    @classmethod
    def create (cls, x, y, type = None):

        if type == None or type < 0 or type > len (cls._tiles):
            type = random.randrange (0, len (cls._tiles))

        return PowerUp (x, y, cls._tiles[type], Factory._TIME_TO_LIVE, cls._game.rect)


class PowerUp (sprite.KinematicSprite):

    WIDTH                   = 72
    HEIGHT                  = 72

    _MIN_VELOCITY           = -200
    _MAX_VELOCITY           = 200

    _MAX_ROTATION_VELOCITY  = 200

    def __init__ (self, x, y, image, time_to_live, screen_rect):
        super ().__init__ (x, y, [image], 0, self._get_velocity ())

        self._time_to_live = time_to_live
        self._screen_rect = screen_rect

        self.set_rotation_velocity (random.uniform (-PowerUp._MAX_ROTATION_VELOCITY, PowerUp._MAX_ROTATION_VELOCITY))

    def update (self, dt):
        super ().update (dt)

        if self._time_to_live > 0:
            self._time_to_live -= dt

            if self.rect.centerx <= 0:
                self.rect.centerx = self._screen_rect.width
            elif self.rect.centerx >= self._screen_rect.width:
                self.rect.centerx = 0

            if self.rect.centery <= 0:
                self.rect.centery = self._screen_rect.height
            elif self.rect.centery >= self._screen_rect.height:
                self.rect.centery = 0
        else:
            self.kill ()

    def _get_velocity (self):
        return pygame.math.Vector2 (random.uniform (PowerUp._MIN_VELOCITY, PowerUp._MAX_VELOCITY),
                                    random.uniform (PowerUp._MIN_VELOCITY, PowerUp._MAX_VELOCITY))
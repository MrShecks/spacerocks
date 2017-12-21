from gamelib import sprite
from gamelib import spritesheet
from random import choice

class Factory (object):

    TYPE_ONE            = 0
    TYPE_TWO            = 1

    _game               = None
    _explosion_tiles    = []

    @classmethod
    def init (cls, game):
        if cls._game == None:

            cls._explosion_tiles.append (spritesheet.SpriteSheet (game.image_cache.get ('explosion_set_01'), 192, 192))
            cls._explosion_tiles.append (spritesheet.SpriteSheet (game.image_cache.get ('explosion_set_02'), 256, 256))

            cls._game = game

    @classmethod
    def create (cls, x, y, type = None):

        if type not in [Factory.TYPE_ONE, Factory.TYPE_TWO]:
            type = choice ([Factory.TYPE_ONE, Factory.TYPE_TWO])

        explosion = Explosion (x, y, cls._explosion_tiles[type], 0.02)

        return explosion

class Explosion (sprite.SceneSprite):

    def __init__ (self, x, y, frames, frame_speed):
        super ().__init__ (x, y, frames, 0)

        self.set_frame_animator (sprite.LinearFrameAnimator (frame_speed, False, True))

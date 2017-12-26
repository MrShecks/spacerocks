from gamelib import sprite
from gamelib import spritesheet
from random import choice

class Factory (object):

    TYPE_ONE            = 0
    TYPE_TWO            = 1

    _game               = None
    _explosion_tiles    = []
    _explosion_sounds   = []

    @classmethod
    def init (cls, game):
        if cls._game is None:

            cls._explosion_tiles.append (spritesheet.SpriteSheet (game.image_cache.get ('explosion_set_01'), 192, 192))
            cls._explosion_tiles.append (spritesheet.SpriteSheet (game.image_cache.get ('explosion_set_02'), 256, 256))

            cls._explosion_sounds.append (game.audio_cache.get ('explosion1'))
            cls._explosion_sounds.append (game.audio_cache.get ('explosion2'))
            cls._explosion_sounds.append (game.audio_cache.get ('explosion3'))
            cls._explosion_sounds.append (game.audio_cache.get ('explosion4'))

            cls._game = game

    @classmethod
    def create (cls, x, y, type = None):

        if type not in [Factory.TYPE_ONE, Factory.TYPE_TWO]:
            type = choice ([Factory.TYPE_ONE, Factory.TYPE_TWO])

        return Explosion (x, y, cls._explosion_tiles[type], 0.02, choice (cls._explosion_sounds))

class Explosion (sprite.SceneSprite):

    def __init__ (self, x, y, frames, frame_speed, sound = None):
        super ().__init__ (x, y, frames, 0)

        self._sound = sound
        self.set_frame_animator (sprite.LinearFrameAnimator (frame_speed, False, True))

    @property
    def sound (self):
        return self._sound
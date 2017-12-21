from gamelib import sprite
from gamelib import spritesheet

class Shield (sprite.SceneSprite):
    _TILE_WIDTH     = 224
    _TILE_HEIGHT    = 224

    def __init__ (self, x, y, image_cache):
        super ().__init__ (x, y, spritesheet.SpriteSheet (image_cache.get ('shield_set_01'),
                                                          Shield._TILE_WIDTH, Shield._TILE_HEIGHT))

        self.set_frame_animator (sprite.LinearFrameAnimator (100, True))

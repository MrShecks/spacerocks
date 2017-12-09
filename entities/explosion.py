from gamelib import scene

class Explosion (scene.AnimatedSprite):

    def __init__ (self, x, y, frames, frame_speed):
        super ().__init__ (frames, frames.tile_width (), frames.tile_height (), frame_speed)

        self.rect.centerx = x
        self.rect.centery = y

    def animation_end (self):
        self.kill ()

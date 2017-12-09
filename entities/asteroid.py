import pygame
import random

from gamelib import scene

class Asteroid (scene.AnimatedSprite):

    # TODO: Maybe add a factory method (class method) to create entities of different sizes?

    def __init__ (self, x, y, frames, frame_speed, screen_rect):
        super ().__init__ (frames, frames.tile_width (), frames.tile_height (), frame_speed)

        self.rect.centerx = x
        self.rect.centery = y

        self._screen_rect = screen_rect

        self.velocity = pygame.math.Vector2 (random.randrange (-4, 4), random.randrange (-4, 4))

    def flip_direction (self):
        self.velocity *= -1

    def scene_update (self, dt):
        # If the asteroid runs off the edge of the screen it should warp to the opposite side
        self.rect.centerx = self.rect.centerx % self._screen_rect.width
        self.rect.centery = self.rect.centery % self._screen_rect.height

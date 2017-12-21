import math
import pygame

from gamelib import sprite

class ScrollingBackground (sprite.StaticSprite):

    def __init__ (self, x, y, width, height, tile):
        super ().__init__ (x, y, pygame.Surface ((width, height)))

        self._tile = tile
        self._x_offset = 0
        self._y_offset = 0
        self._velocity = pygame.math.Vector2 ()
        self._background = self._get_background_surface (tile, width, height)

    def set_velocity (self, x, y):
        self._velocity.x = x
        self._velocity.y = y

    def update (self, scene, dt):
        background_width = self._background.get_width ()
        background_height = self._background.get_height ()

        self._x_offset = (self._x_offset + (self._velocity.x * dt)) % background_width
        self._y_offset = (self._y_offset + (self._velocity.y * dt)) % background_height

        self.image.blit (self._background, (self._x_offset, self._y_offset))
        self.image.blit (self._background, (self._x_offset - background_width, self._y_offset))

        self.image.blit (self._background, (self._x_offset, self._y_offset - background_height))
        self.image.blit (self._background, (self._x_offset - background_width, self._y_offset - background_height))

        super ().update (scene, dt)

    def set_background (self, tile):
        self._background = self._get_background_surface (tile, self.rect.width, self.rect.height)

    def _get_background_surface (self, tile, width, height):
        rows = int (math.ceil (height / tile.get_height ()))
        cols = int (math.ceil (width / tile.get_width ()))

        background_width = tile.get_width () * cols
        background_height = tile.get_height () * rows
        background_surface = pygame.Surface ((background_width, background_height))

        for col in range (cols):
            for row in range (rows):
                background_surface.blit (tile, (col * tile.get_width (), row * tile.get_height ()))

        return background_surface
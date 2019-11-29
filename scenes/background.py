import math
import pygame

from gamelib import sprite

_DEBUG_BACKGROUND = False


class ParallaxScroller(sprite.StaticSprite):
    class Layer(object):

        def __init__(self, tile, speed, width, height, has_alpha):

            self._speed = speed
            self._x_offset = 0
            self._y_offset = 0
            self._velocity = pygame.math.Vector2()
            self._surface = self._create_layer_surface(tile, width, height, has_alpha)

        def set_velocity(self, velocity):
            self._velocity.x = velocity.x * self._speed
            self._velocity.y = velocity.y * self._speed

        def update(self, scene, dt):
            background_width = self._surface.get_width()
            background_height = self._surface.get_height()

            self._x_offset = (self._x_offset + (self._velocity.x * dt)) % background_width
            self._y_offset = (self._y_offset + (self._velocity.y * dt)) % background_height

        def draw(self, target_surface):
            background_width = self._surface.get_width()
            background_height = self._surface.get_height()

            # FIXME: This could be made more efficient, at the very least clip the rectangles to what's needed

            # print ('ParallaxScroller::Layer::draw (): X-offset=', self._x_offset, ', Y-offset=', self._y_offset)

            if target_surface.get_rect().collidepoint(self._x_offset, self._y_offset) or True:
                target_surface.blit(self._surface, (self._x_offset, self._y_offset))
            # else:
            #     print ('Skipping: X-Blit ', self._x_offset, self._y_offset)

            target_surface.blit(self._surface, (self._x_offset - background_width, self._y_offset))

            target_surface.blit(self._surface, (self._x_offset, self._y_offset - background_height))
            target_surface.blit(self._surface, (self._x_offset - background_width, self._y_offset - background_height))

        def _create_layer_surface(self, tile, width, height, has_alpha):
            rows = int(math.ceil(height / tile.get_height()))
            cols = int(math.ceil(width / tile.get_width()))

            layer_flags = pygame.HWSURFACE
            layer_width = tile.get_width() * cols
            layer_height = tile.get_height() * rows

            if has_alpha:
                layer_flags |= pygame.SRCALPHA

            layer_surface = pygame.Surface((layer_width, layer_height), layer_flags)

            print('ParallaxScroller::Layer::_create_layer_surface (): Tile=', tile.get_rect(),
                  ', Width=', layer_width, ', Height=', layer_height, ', Rows=', rows, ', Columns=', cols)

            for col in range(cols):
                for row in range(rows):
                    layer_surface.blit(tile, (col * tile.get_width(), row * tile.get_height()))

                    if _DEBUG_BACKGROUND:
                        rect = pygame.Rect(col * tile.get_width(),
                                           row * tile.get_height(),
                                           tile.get_width(),
                                           tile.get_height())

                        rect.inflate_ip(10, 10)
                        pygame.draw.rect(layer_surface, (200, 0, 0), rect, 1)

            return layer_surface

    def __init__(self, x, y, width, height):
        super().__init__(x, y, pygame.Surface((width, height), pygame.HWSURFACE))

        self._layers = []

    def set_velocity(self, velocity):
        for layer in self._layers:
            layer.set_velocity(velocity)

    def add_layer(self, tile, speed, has_alpha=True):
        self._layers.append(ParallaxScroller.Layer(tile, speed, self.rect.width, self.rect.height, has_alpha))

    def update(self, scene, dt):

        for layer in self._layers:
            layer.update(scene, dt)
            layer.draw(self.image)


class ScrollingBackground(sprite.StaticSprite):

    def __init__(self, x, y, width, height, tile):
        super().__init__(x, y, pygame.Surface((width, height)))

        self._tile = tile
        self._x_offset = 0
        self._y_offset = 0
        self._velocity = pygame.math.Vector2()
        self._background = self._get_background_surface(tile, width, height)

    def set_velocity(self, x, y):
        self._velocity.x = x
        self._velocity.y = y

    def update(self, scene, dt):
        background_width = self._background.get_width()
        background_height = self._background.get_height()

        self._x_offset = (self._x_offset + (self._velocity.x * dt)) % background_width
        self._y_offset = (self._y_offset + (self._velocity.y * dt)) % background_height

        self.image.blit(self._background, (self._x_offset, self._y_offset))
        self.image.blit(self._background, (self._x_offset - background_width, self._y_offset))

        self.image.blit(self._background, (self._x_offset, self._y_offset - background_height))
        self.image.blit(self._background, (self._x_offset - background_width, self._y_offset - background_height))

        super().update(scene, dt)

    def set_background(self, tile):
        self._background = self._get_background_surface(tile, self.rect.width, self.rect.height)

    def _get_background_surface(self, tile, width, height):
        rows = int(math.ceil(height / tile.get_height()))
        cols = int(math.ceil(width / tile.get_width()))

        background_width = tile.get_width() * cols
        background_height = tile.get_height() * rows
        background_surface = pygame.Surface((background_width, background_height))

        for col in range(cols):
            for row in range(rows):
                background_surface.blit(tile, (col * tile.get_width(), row * tile.get_height()))

        return background_surface

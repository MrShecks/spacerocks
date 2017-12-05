import pygame
import os

class ImageCache:

    _DEBUG = True

    def __init__ (self, path):
        self._images = dict ()
        self._path = path

    def add_image (self, tag, filename):
        image = pygame.image.load (os.path.join (self._path, filename))
        assert image is not None

        if image:
            self._images[tag] = image.convert_alpha ()

            if ImageCache._DEBUG:
                print ('DBG: ImageCache:add_image (): Filename=', filename)

        return image

    def get_image (self, tag):
        return self._images.get (tag)

    def draw_image (self, tag, canvas, x, y):
        image = self._images.get (tag)
        canvas.blit (image, (x, y))

import os
import random
import pygame

from gamelib import game
from gamelib import scene
from gamelib import imagecache

from player import PlayerShip

class Background (scene.SceneNode):

    SCROLL_SPEED = 50

    def __init__ (self, width, height):
        super ().__init__ (width, height, False)

        self._backgrounds = []
        self._current_index = 0
        self._scroll_offset = 0
        self._foreground = None

        self._image = pygame.Surface ((width, height))

    def add_background (self, image):
        self._backgrounds.append (image)

    def set_foreground (self, foreground):
        self._foreground = foreground

    def set_background (self, index):
        if 0 <= index < len (self._backgrounds):
            self._current_index = index

    def count (self):
        return len (self._backgrounds)

    def update (self, dt):
        self._scroll_offset = (self._scroll_offset + (Background.SCROLL_SPEED * dt)) % self._rect.width
        self._image.blit (self._backgrounds[self._current_index], (0, 0))

        if self._foreground is not None:
            y = (self._rect.height - self._foreground.get_height ()) // 2
            self._image.blit (self._foreground, (self._scroll_offset, y))
            self._image.blit (self._foreground, (self._scroll_offset - self._rect.width, y))

class Spacerocks (game.Game):

    WINDOW_TITLE                = 'Space Rocks'

    WINDOW_WIDTH                = 960
    WINDOW_HEIGHT               = 720
    WINDOW_RECT                 = pygame.Rect (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    FPS                         = 60

    SCENE_LAYER_BACKGROUND      = 0
    SCENE_LAYER_PLAYER_SHIP     = 1


    IMAGES = {
        'background_01'     : 'background_01.jpg',
        'background_02'     : 'background_02.jpg',
        'background_03'     : 'background_03.jpg',
        'background_04'     : 'background_04.jpg',
        'background_05'     : 'background_05.jpg',
        'background_06'     : 'background_06.jpg',
        'background_07'     : 'background_07.jpg',
        'background_08'     : 'background_08.jpg',
        'background_09'     : 'background_09.jpg',
        'background_10'     : 'background_10.jpg',
        'background_11'     : 'background_11.jpg',
        'background_12'     : 'background_12.jpg',

        'debris'            : 'debris.png',
        'player_ship'       : 'space_ship.png',
    }

    def __init__ (self):
        super ().__init__ (Spacerocks.WINDOW_WIDTH, Spacerocks.WINDOW_HEIGHT,
                           Spacerocks.WINDOW_TITLE, Spacerocks.FPS)

        assets_path = os.path.join (os.path.dirname (__file__), 'assets')

        self._scene = scene.SceneGraph ()
        self._images = imagecache.ImageCache (os.path.join (assets_path, 'images'))
        self._background = Background (Spacerocks.WINDOW_WIDTH, Spacerocks.WINDOW_HEIGHT)

        for tag, filename in self.IMAGES.items ():
            image = self._images.add_image (tag, filename)

            if tag.startswith ('background_'):
                self._background.add_background (image)

        self._scene.add_node (self._background, Spacerocks.SCENE_LAYER_BACKGROUND)

        self._playerShip = PlayerShip (self._images.get_image ('player_ship'), Spacerocks.WINDOW_RECT)
        self._scene.add_node (self._playerShip, Spacerocks.SCENE_LAYER_PLAYER_SHIP)

        self._background.set_foreground(self._images.get_image('debris'))
        self._background.set_background (random.randrange (self._background.count ()))

        self._playerShip.set_center (Spacerocks.WINDOW_RECT.centerx, Spacerocks.WINDOW_RECT.centery)

    def update (self, dt):
        self._scene.update (dt)

    def draw (self, canvas):
        self._scene.draw (canvas)

    def on_key_down(self, key, event):
        print ('Key Down: Key=', key)

        if key == pygame.K_UP:
            self._playerShip.set_thrust (True)
        elif key == pygame.K_LEFT:
            self._playerShip.rotate (PlayerShip.ROTATE_VELOCITY)
        elif key == pygame.K_RIGHT:
            self._playerShip.rotate (-PlayerShip.ROTATE_VELOCITY)

    def on_key_up(self, key, event):
        print ('Key Up: Key=', key)

        if key == pygame.K_UP:
            self._playerShip.set_thrust (False)
        elif key == pygame.K_LEFT:
            self._playerShip.rotate (-PlayerShip.ROTATE_VELOCITY)
        elif key == pygame.K_RIGHT:
            self._playerShip.rotate (PlayerShip.ROTATE_VELOCITY)
        elif key == pygame.K_b:
            self._background.set_background (random.randrange (self._background.count ()))

    def on_quit (self):
        return True


if __name__ == "__main__":
    app = Spacerocks ()
    app.run ()




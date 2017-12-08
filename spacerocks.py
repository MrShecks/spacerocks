"""
    Space Rocks a simple 'Asteroids' style space shooter

    Graphics Credits:

    Base Rice Rocks assets provided by Kim Lathrop and Rice University

    Additiional asset credits:

    Kenny		    - http://www.kenney.nl
    Rawdanitsu 	    - http://tinyurl.com/olbstsf, http://tinyurl.com/ogs94te
    Bart 		    - http://tinyurl.com/2vvf85p
    NenadSimic 	    - http://tinyurl.com/nf9ycac
    Julien 		    - http://tinyurl.com/nvt7ro5
    Mike Koenig	    - http://tinyurl.com/pm38lbo
    Skorpio 	    - http://tinyurl.com/ngkj7ch

    Assets used under Public Domain or Creative Commons License (http://tinyurl.com/2dkzmd)

"""


import os
import random
import pygame

from gamelib import game
from gamelib import scene

from gamelib import assets

from player.ship import PlayerShip


class Background (scene.Sprite):

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

    def scene_update (self, dt):
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


    BACKGROUNDS = {
        'background_01',
        'background_02',
        'background_03',
        'background_04',
        'background_05',
        'background_06',
        'background_07',
        'background_08',
        'background_09',
        'background_10',
        'background_11',
        'background_12'
    }

    def __init__ (self):
        super ().__init__ (Spacerocks.WINDOW_WIDTH, Spacerocks.WINDOW_HEIGHT,
                           Spacerocks.WINDOW_TITLE, Spacerocks.FPS)

        assets_path = os.path.join (os.path.dirname (__file__), 'assets')

        self._scene = scene.Scene ()

        self._image_cache = assets.ImageCache ()
        self._image_cache.load (os.path.join (assets_path, 'images'))

        self._background = Background (Spacerocks.WINDOW_WIDTH, Spacerocks.WINDOW_HEIGHT)

        for tag in Spacerocks.BACKGROUNDS:
            self._background.add_background (self._image_cache.get (tag))

        self._scene.add_node (self._background, Spacerocks.SCENE_LAYER_BACKGROUND)

        self._playerShip = PlayerShip (self._image_cache, Spacerocks.WINDOW_RECT, self._scene)
        self._scene.add_node (self._playerShip, Spacerocks.SCENE_LAYER_PLAYER_SHIP)

        self._background.set_foreground(self._image_cache.get ('debris'))

        #self._background.set_background (random.randrange (self._background.count ()))

        # DEBUG: Using background 11 for the moment, easier to see projectiles
        self._background.set_background (11)

        self._playerShip.set_center (Spacerocks.WINDOW_RECT.centerx, Spacerocks.WINDOW_RECT.centery)

        self.set_active_scene (self._scene)

    def on_key_down(self, key, event):

        if key == pygame.K_UP:
            self._playerShip.set_thrust (True)
        elif key == pygame.K_LEFT:
            self._playerShip.rotate (PlayerShip.DEFAULT_ROTATE_VELOCITY)
        elif key == pygame.K_RIGHT:
            self._playerShip.rotate (-PlayerShip.DEFAULT_ROTATE_VELOCITY)

    def on_key_up(self, key, event):

        if key == pygame.K_UP:
            self._playerShip.set_thrust (False)
        elif key == pygame.K_LEFT:
            self._playerShip.rotate (-PlayerShip.DEFAULT_ROTATE_VELOCITY)
        elif key == pygame.K_RIGHT:
            self._playerShip.rotate (PlayerShip.DEFAULT_ROTATE_VELOCITY)
        elif key == pygame.K_SPACE:
            self._playerShip.fire_weapon (PlayerShip.PRIMARY_WEAPON)



        #
        # DEBUGGING
        #

        elif key == pygame.K_x:
            self._playerShip.fire_weapon (PlayerShip.SECONDARY_WEAPON)
        elif key == pygame.K_b:
            self._background.set_background (random.randrange (self._background.count ()))
        elif key == pygame.K_f:
            self._playerShip.toggle_friction ()

    def on_quit (self):
        return True


if __name__ == "__main__":
    app = Spacerocks ()
    app.run ()




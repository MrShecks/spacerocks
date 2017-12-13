"""
    Space Rocks a simple 'Asteroids' style space shooter

    Graphics Credits:

    Base Rice Rocks assets provided by Kim Lathrop and Rice University

    Additional asset credits:

    Kenny		    - http://www.kenney.nl
    Bart 		    - http://tinyurl.com/2vvf85p
    NenadSimic 	    - http://tinyurl.com/nf9ycac
    Julien 		    - http://tinyurl.com/nvt7ro5
    Mike Koenig	    - http://tinyurl.com/pm38lbo
    Skorpio 	    - http://tinyurl.com/ngkj7ch

    Assets used under Public Domain or Creative Commons License (http://tinyurl.com/2dkzmd)

"""


import os
import pygame

from gamelib import game
from scenes import level


class Spacerocks (game.Game):

    WINDOW_TITLE                = 'Space Rocks'

    # WINDOW_WIDTH                = 960
    # WINDOW_HEIGHT               = 720

    SCREEN_WIDTH                = 1600 #1280 #1920
    SCREEN_HEIGHT               = 1280 #1080 #1080

    SCREEN_RECT                 = pygame.Rect (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    FPS                         = 60     # TODO: More research here

    def __init__ (self):
        super ().__init__ (Spacerocks.SCREEN_WIDTH, Spacerocks.SCREEN_HEIGHT,
                           Spacerocks.WINDOW_TITLE, Spacerocks.FPS)


        # ----------------------------------------------------------------
        # DEBUG
        # Figuring out how joysticks work with PyGame

        print ('Joysticks: ', pygame.joystick.get_count())

        joy = pygame.joystick.Joystick (0)
        joy.init ()

        # DEBUG
        # ----------------------------------------------------------------

        assets_path = os.path.join (os.path.dirname (__file__), 'assets')

        self.image_cache.load (os.path.join (assets_path, 'images'))
        self._scene = level.GameScene (self)

        self.set_active_scene (self._scene)

    def on_quit (self):
        return True


if __name__ == "__main__":
    app = Spacerocks ()
    app.run ()




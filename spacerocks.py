"""
    Space Rocks a simple 'Asteroids' style space shooter

    Credits:

    Graphics credits:

    Kenny		                - http://www.kenney.nl
    Skorpio 	                - https://opengameart.org/users/skorpio
    LuminousDragonGames         - https://opengameart.org/users/luminousdragongames

    Audio credits:

    Kenny                       - http://www.kenney.nl + https://opengameart.org/content/space-shooter-redux
    Michael Kurinnoy            - AstroMenace Artwork ver 1.2 Assets Copyright (c) 2006-2007 Michael Kurinnoy, Viewizard
                                  (https://opengameart.org/content/space-battle-game-sounds-astromenace)


    Assets used under Public Domain or Creative Commons License (http://tinyurl.com/2dkzmd)

"""


import os
import pygame

from gamelib import game
from scenes import level


class Spacerocks (game.Game):

    WINDOW_TITLE                = 'Space Rocks'

    # TODO: Scale all game objects based on resolution

    SCREEN_RESOLUTIONS          = [ (1920, 1080), (1280, 720), (854, 480) ]

    SCREEN_WIDTH                = SCREEN_RESOLUTIONS[0][0]
    SCREEN_HEIGHT               = SCREEN_RESOLUTIONS[0][1]

    SCREEN_RECT                 = pygame.Rect (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    FPS                         = 100

    def __init__ (self):
        super ().__init__ (Spacerocks.SCREEN_WIDTH, Spacerocks.SCREEN_HEIGHT,
                           Spacerocks.WINDOW_TITLE, Spacerocks.FPS)


        # ----------------------------------------------------------------
        # DEBUG
        # Figuring out how joysticks work with PyGame

        # print ('Joysticks: ', pygame.joystick.get_count())
        #
        # joy = pygame.joystick.Joystick (0)
        # joy.init ()

        # DEBUG
        # ----------------------------------------------------------------

        assets_path = os.path.join (os.path.dirname (__file__), 'assets')

        self.image_cache.load (os.path.join (assets_path, 'images'))
        self.audio_cache.load (os.path.join (assets_path, 'sounds'))

        self._scene = level.GameScene (self)

        self.set_active_scene (self._scene)

    def on_quit (self):
        return True


if __name__ == "__main__":
    app = Spacerocks ()
    app.run ()




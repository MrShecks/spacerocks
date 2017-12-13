import math
import random
import pygame

from gamelib import scene
from gamelib import sprite
from gamelib import tileset

from player import ship
from entities import asteroid
from entities import explosion
from entities import powerup

class Background (sprite.StaticSprite):

    def __init__ (self, width, height):
        super ().__init__ (0, 0, pygame.Surface ((width, height)))
        self._images = []

    def add_image (self, image):
        self._images.append (image)

    def set_image (self, index):

        if 0 <= index < len (self._images):
            rows = int (math.ceil (self.rect.height / self._images[index].get_height ()))
            cols = int (math.ceil (self.rect.width / self._images[index].get_width ()))

            print ('DBG: Background::set_background (): Rows=', rows, ', Cols=', cols)

            for col in range (0, cols):
                for row in range (0, rows):
                    # FIXME: Only blit what's needed
                    self.image.blit (self._images[index], (col * self._images[index].get_width (),
                                                           row * self._images[index].get_height ()))


class GameScene (scene.Scene):

    _SCENE_LAYER_BACKGROUND         = 0
    _SCENE_LAYER_PLAYER_SHIP        = 1
    _SCENE_LAYER_ASTEROID           = 2
    _SCENE_LAYER_POWERUP            = 3
    _SCENE_LAYER_EXPLOSION          = 4
    _SCENE_LAYER_HUD                = 5

    def __init__ (self, game):
        super ().__init__ (game)

        asteroid.Factory.init (game)
        explosion.Factory.init (game)
        powerup.Factory.init (game)

        self._background = Background (game.rect.width, game.rect.height)
        self._background.add_image (self.game.image_cache.get ('tiled_background_01'))
        self._background.add_image (self.game.image_cache.get ('tiled_background_02'))
        self._background.add_image (self.game.image_cache.get ('tiled_background_03'))
        self._background.add_image (self.game.image_cache.get ('tiled_background_04'))
        self._background.add_image (self.game.image_cache.get ('tiled_background_05'))
        self._background.add_image (self.game.image_cache.get ('tiled_background_06'))
        self._background.add_image (self.game.image_cache.get ('tiled_background_07'))

        self._background.set_image (0)

        self.add_node (self._background, GameScene._SCENE_LAYER_BACKGROUND)

        # FIXME: Pass the game object rather than all these params
        self._playerShip = ship.PlayerShip (game.rect.centerx, game.rect.centery,
                                            game.image_cache, game.rect, self)
        self.add_node (self._playerShip, GameScene._SCENE_LAYER_PLAYER_SHIP)

        self._asteroids = pygame.sprite.Group ()

        # DEBUG

        self.dbg_spawn_asteroids ()

        # DEBUG

        # DEBUG - Testing SceneText node

        self._fps_label = scene.SceneText (game.rect.right - 80, 5, 'FPS: ???', pygame.font.SysFont ('', 26))
        self.add_node (self._fps_label, GameScene._SCENE_LAYER_HUD)

        # DEBUG

    def update (self, dt):
        super ().update (dt)

        for projectile in self._playerShip.projectiles:
            destroyed_asteroids = pygame.sprite.spritecollide (projectile, self._asteroids, False)

            if destroyed_asteroids:
                projectile.kill ()

                for dead_asteroid in destroyed_asteroids:
                    exp = explosion.Factory.create (dead_asteroid.rect.centerx, dead_asteroid.rect.centery)
                    self.add_node (exp, GameScene._SCENE_LAYER_EXPLOSION)
                    dead_asteroid.kill ()

                    p = powerup.Factory.create (dead_asteroid.rect.centerx, dead_asteroid.rect.centery)
                    self.add_node (p, GameScene._SCENE_LAYER_POWERUP)

        self._fps_label.set_text ('FPS: {0:03d}'.format (int (self.game.fps)))

    def on_key_down (self, key, event):

        if key == pygame.K_UP:
            self._playerShip.set_thrust (True)
        elif key == pygame.K_LEFT:
            self._playerShip.rotate (ship.PlayerShip.ROTATE_LEFT)
        elif key == pygame.K_RIGHT:
            self._playerShip.rotate (ship.PlayerShip.ROTATE_RIGHT)

    def on_key_up (self, key, event):

        if key == pygame.K_UP:
            self._playerShip.set_thrust (False)
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self._playerShip.rotate (ship.PlayerShip.ROTATE_STOP)
        elif key == pygame.K_SPACE:
            self._playerShip.fire_weapon (ship.PlayerShip.PRIMARY_WEAPON)

        #
        # DEBUGGING
        #

        elif key == pygame.K_x:
            self._playerShip.fire_weapon (ship.PlayerShip.SECONDARY_WEAPON)
        elif key == pygame.K_f:
            self._playerShip.toggle_friction ()
        elif key == pygame.K_b:
            self._background.set_image (random.randrange (0, 7))
        elif key == pygame.K_F1:
            self.dbg_spawn_asteroids ()
        elif key == pygame.K_q:
            self.game.quit ()

    def on_joy_button_up (self, event):
        print ('GameLevel::on_joy_button_up (): Event=', event)

        if event.button == 0:
            self._playerShip.fire_weapon (ship.PlayerShip.PRIMARY_WEAPON)
        elif event.button == 1:
            self._playerShip.fire_weapon (ship.PlayerShip.SECONDARY_WEAPON)

    def on_joy_motion (self, event):
        joy = pygame.joystick.Joystick (event.joy)
        x = joy.get_axis (0)
        y = joy.get_axis (1)
        angle = math.atan2 (x, y)

        print ('GameLevel:on_joy_motion (): Event=', event, ', x=', x, ', y=', y, ', angle=', angle)

    def dbg_spawn_asteroids (self):
        # DEBUG - Create some random asteroids for testing

        types = [
            asteroid.Factory.TYPE_SMALL,
            asteroid.Factory.TYPE_MEDIUM,
            asteroid.Factory.TYPE_LARGE,
            asteroid.Factory.TYPE_HUGE,
        ]

        for type in types:
            for n in range (0, 4):
                x = random.randrange (self.game.rect.width)
                y = random.randrange (self.game.rect.height)

                a = asteroid.Factory.create (x, y, type)

                self.add_node (a, GameScene._SCENE_LAYER_ASTEROID)
                self._asteroids.add (a)

        # x = random.randrange (game.rect.width)
        # y = random.randrange (game.rect.height)
        #
        # a = asteroid.Factory.create (x, y, asteroid.Factory.TYPE_MEDIUM)
        #
        # self.add_node (a, GameScene._SCENE_LAYER_ASTEROID)
        # self._asteroids.add (a)

        # DEBUG

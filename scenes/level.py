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

        self._playerShip = ship.Factory.create (ship.Factory.TYPE_RED_VIPER, game.rect.centerx, game.rect.centery, game)
        self.add_node (self._playerShip, GameScene._SCENE_LAYER_PLAYER_SHIP)

        self._asteroids = pygame.sprite.Group ()

        # DEBUG

        self.dbg_spawn_asteroids ()

        # DEBUG

        # DEBUG - Testing SceneText node

        self._fps_label = scene.SceneText (game.rect.right - 180, 5, 'FPS: 000 OBJ: 0000', pygame.font.SysFont ('', 26))
        self.add_node (self._fps_label, GameScene._SCENE_LAYER_HUD)

        self._stat_label = scene.SceneText (5, game.rect.bottom - 26, '(D)rag: ?, (S)hield: ?',
                                            pygame.font.SysFont ('', 26))

        self.add_node (self._stat_label, GameScene._SCENE_LAYER_HUD)

        # DEBUG

    def update (self, dt):
        super ().update (dt)

        # FIXME: This is all temporary for debugging

        for projectile in self._playerShip.projectiles:
            destroyed_asteroids = pygame.sprite.spritecollide (projectile, self._asteroids, False)

            if destroyed_asteroids:
                projectile.kill ()

                for dead_asteroid in destroyed_asteroids:
                    exp = explosion.Factory.create (dead_asteroid.rect.centerx, dead_asteroid.rect.centery)
                    self.add_node (exp, GameScene._SCENE_LAYER_EXPLOSION)

                    if random.randint (1, 10) == 5:
                        p = powerup.Factory.create (dead_asteroid.rect.centerx, dead_asteroid.rect.centery)
                        self.add_node (p, GameScene._SCENE_LAYER_POWERUP)

                    shards = dead_asteroid.get_shards ()
                    if shards:
                        self.add_nodes (shards, GameScene._SCENE_LAYER_ASTEROID)
                        self._asteroids.add (shards)

                    dead_asteroid.kill ()

        self._fps_label.set_text ('FPS: {0:03d} OBJ: {1:04d}'.format (int (self.game.fps), self.object_count))
        self._stat_label.set_text ('(D)rag={0}, (S)hield={1}'.format (self._playerShip._has_drag, self._playerShip._has_shield))

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
        elif key == pygame.K_d:
            self._playerShip.toggle_drag ()
        elif key == pygame.K_s:
            self._playerShip.toggle_shield ()
        elif key == pygame.K_b:
            self._background.set_image (random.randrange (0, 7))
        elif key == pygame.K_F1:
            self.dbg_spawn_asteroids ()
        elif key == pygame.K_q:
            self.game.quit ()

    def on_joy_button_up (self, event):
        # print ('GameLevel::on_joy_button_up (): Event=', event)
        #
        # if event.button == 0:
        #     self._playerShip.fire_weapon (ship.PlayerShip.PRIMARY_WEAPON)
        # elif event.button == 1:
        #     self._playerShip.fire_weapon (ship.PlayerShip.SECONDARY_WEAPON)

        pass

    def on_joy_motion (self, event):
        # joy = pygame.joystick.Joystick (event.joy)
        # x = joy.get_axis (0)
        # y = joy.get_axis (1)
        # angle = math.atan2 (x, y)
        #
        # print ('GameLevel:on_joy_motion (): Event=', event, ', x=', x, ', y=', y, ', angle=', angle)

        pass

    def dbg_spawn_asteroids (self):
        # DEBUG - Create some random asteroids for testing

        types = [
            asteroid.Asteroid.TYPE_TINY,
            asteroid.Asteroid.TYPE_SMALL,
            asteroid.Asteroid.TYPE_MEDIUM,
            asteroid.Asteroid.TYPE_LARGE,
        ]

        for type in types:
            for n in range (0, 3):
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
import math
import random
import pygame

from gamelib import scene
from gamelib import tileset

from player import ship
from entities import asteroid
from entities import explosion

class Background (scene.Sprite):

    def __init__ (self, width, height):
        super ().__init__ (width, height, False)
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
    _SCENE_LAYER_EXPLOSION          = 3

    def __init__ (self, game):
        super ().__init__ (game)

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

        asteroid_tiles = []
        asteroid_tiles.append (tileset.TileSet (game.image_cache.get ('asteroid_set_01'), 32, 32))
        asteroid_tiles.append (tileset.TileSet (game.image_cache.get ('asteroid_set_02'), 64, 64))
        asteroid_tiles.append (tileset.TileSet (game.image_cache.get ('asteroid_set_03'), 96, 96))
        asteroid_tiles.append (tileset.TileSet (game.image_cache.get ('asteroid_set_04'), 128, 128))

        for frames in asteroid_tiles:
            for n in range (0, 4):
                x = random.randrange (game.rect.width)
                y = random.randrange (game.rect.height)

                a = asteroid.Asteroid (x, y, frames, 0.1, game.rect)
                self.add_node (a, GameScene._SCENE_LAYER_ASTEROID)

                self._asteroids.add (a)


        self._explosion_tiles = []
        self._explosion_tiles.append (tileset.TileSet (game.image_cache.get ('explosion_set_01'), 192, 192))
        self._explosion_tiles.append (tileset.TileSet (game.image_cache.get ('explosion_set_02'), 256, 256))

        # e1 = explosion.Explosion (500, 500, self._explosion_tiles[0], 0.05)
        # self.add_node (e1, GameScene._SCENE_LAYER_EXPLOSION)
        #
        # e2 = explosion.Explosion (game.rect.width - 500, game.rect.height - 500, self._explosion_tiles[1], 0.05)
        # self.add_node (e2, GameScene._SCENE_LAYER_EXPLOSION)

    def update (self, dt):
        super ().update (dt)

        # for asteroid1 in self._asteroids:
        #     colliding_asteroids = pygame.sprite.spritecollide (asteroid1, self._asteroids, False)
        #
        #     for a in colliding_asteroids:
        #         if a is not asteroid1:
        #             a.flip_direction ()

        for projectile in self._playerShip.projectiles:
            destroyed_asteroids = pygame.sprite.spritecollide (projectile, self._asteroids, False)

            if destroyed_asteroids:
                projectile.kill ()

                for dead_asteroid in destroyed_asteroids:
                    exp = explosion.Explosion (dead_asteroid.rect.centerx, dead_asteroid.rect.centery,
                                               self._explosion_tiles[1], 0.05)
                    self.add_node (exp, GameScene._SCENE_LAYER_EXPLOSION)
                    dead_asteroid.kill ()



    def on_key_down (self, key, event):

        if key == pygame.K_UP:
            self._playerShip.set_thrust (True)
        elif key == pygame.K_LEFT:
            self._playerShip.rotate (ship.PlayerShip.DEFAULT_ROTATE_VELOCITY)
        elif key == pygame.K_RIGHT:
            self._playerShip.rotate (-ship.PlayerShip.DEFAULT_ROTATE_VELOCITY)

    def on_key_up (self, key, event):

        if key == pygame.K_UP:
            self._playerShip.set_thrust (False)
        elif key == pygame.K_LEFT:
            self._playerShip.rotate (-ship.PlayerShip.DEFAULT_ROTATE_VELOCITY)
        elif key == pygame.K_RIGHT:
            self._playerShip.rotate (ship.PlayerShip.DEFAULT_ROTATE_VELOCITY)
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
        elif key == pygame.K_q:
            self.game.quit ()

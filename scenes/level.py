import random
import pygame

from gamelib import scene

from player import ship
from entities import asteroid
from entities import explosion
from entities import powerup
from scenes import background

from gamelib import sprite

class ShipStatsHud (sprite.StaticSprite):

    def __init__ (self, x, y, image):
        super ().__init__ (x, y, image)

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

        # self._background = background.ScrollingBackground (0, 0, game.rect.width, game.rect.height,
        #                                                    self.game.image_cache.get ('tiled_background_01'))

        self._background = background.ParallaxScroller (0, 0, game.rect.width, game.rect.height)
        self._background.add_layer (game.image_cache.get ('tiled_background_01'), 0.4, False)
        self._background.add_layer (game.image_cache.get ('parallax_layer_02'), 0.6)
        self._background.add_layer (game.image_cache.get ('parallax_layer_01'), 0.8)

        self.add_node (self._background, GameScene._SCENE_LAYER_BACKGROUND)

        self._playerShip = ship.Factory.create (ship.Factory.TYPE_RED_VIPER, game.rect.centerx, game.rect.centery, game)
        self.add_node (self._playerShip, GameScene._SCENE_LAYER_PLAYER_SHIP)

        self._asteroids = pygame.sprite.Group ()
        self._powerups = pygame.sprite.Group ()

        # DEBUG

        self.dbg_spawn_asteroids ()

        # s = shield.Shield (self.game.rect.centerx, self.game.rect.centery, self.game.image_cache)
        # self.add_node (s, GameScene._SCENE_LAYER_HUD)

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

        # Set the background scroll velocity based on the ships velocity
        self._background.set_velocity (self._playerShip.velocity * -1)

        self.check_collisions (dt)

        self._fps_label.set_text ('FPS: {0:03d} OBJ: {1:04d}'.format (int (self.game.fps), self.object_count))
        self._stat_label.set_text ('(D)rag={0}, (S)hield={1}'.format (self._playerShip._has_drag, self._playerShip._has_shield))

    def check_collisions (self, dt):
        #self.check_asteroid_collisions (dt)
        self.check_player_collisions (dt)
        self.check_projectile_collisions (dt)
        self.check_powerup_collisions (dt)

    def check_asteroid_collisions (self, dt):
        for asteroid in self._asteroids:
            collisions = pygame.sprite.spritecollide (asteroid, self._asteroids, False, pygame.sprite.collide_circle)
            for colliding_asteroid in collisions:
                if asteroid is not colliding_asteroid:
                    colliding_asteroid.reflect ()

    def check_player_collisions (self, dt):
        # TODO: Check for player + asteroid collisions
        # TODO: Check for player + powerup collisions here too instead of in check_powerup_collisions ()
        pass

    def check_projectile_collisions (self, dt):
        for projectile in self._playerShip.projectiles:
            colliding_asteroids = pygame.sprite.spritecollide (projectile, self._asteroids, False, pygame.sprite.collide_circle)

            if colliding_asteroids:
                projectile.kill ()

                for asteroid in colliding_asteroids:
                    exp = explosion.Factory.create (asteroid.rect.centerx, asteroid.rect.centery)
                    self.add_node (exp, GameScene._SCENE_LAYER_EXPLOSION)

                    asteroid_shards = asteroid.get_shards ()

                    if asteroid_shards:
                        self.add_nodes (asteroid_shards, GameScene._SCENE_LAYER_ASTEROID)
                        self._asteroids.add (asteroid_shards)

                    if random.randint (1, 10) == 5:
                        p = powerup.Factory.create (asteroid.rect.centerx, asteroid.rect.centery)
                        self.add_node (p, GameScene._SCENE_LAYER_POWERUP)
                        self._powerups.add (p)

                    exp.sound.play ()
                    asteroid.kill ()

    def check_powerup_collisions (self, dt):

        # TODO - Apply powerup to player
        collisions = pygame.sprite.spritecollide (self._playerShip, self._powerups, False, pygame.sprite.collide_circle)

        for powerup in collisions:
            powerup.sound.play ()
            powerup.kill ()

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
        elif key == pygame.K_ESCAPE:
            self.dbg_spawn_asteroids ()
        elif key == pygame.K_F1:
            self._playerShip.kill ()
            self._playerShip = ship.RedViper (self.game.rect.centerx, self.game.rect.centery, self.game)
            self.add_node (self._playerShip, GameScene._SCENE_LAYER_PLAYER_SHIP)
        elif key == pygame.K_F2:
            self._playerShip.kill ()
            self._playerShip = ship.YellowHawk (self.game.rect.centerx, self.game.rect.centery, self.game)
            self.add_node (self._playerShip, GameScene._SCENE_LAYER_PLAYER_SHIP)
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
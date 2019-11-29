import math
import pygame

from gamelib import sprite
from gamelib import spritesheet

from abc import ABC, abstractmethod


class PlayerWeapon(ABC):

    def __init__(self, game, ship):
        self.__game = game
        self.__ship = ship

    @abstractmethod
    def fire(self):
        """
            Fire the weapon creating one or more projectiles

            :return: Array of projectiles generated by firing the weapon

        """

    @property
    def game(self):
        return self.__game

    @property
    def ship(self):
        return self.__ship

    def can_fire(self):
        return True

    def update(self, scene, dt):
        pass


class Missile(sprite.KinematicSprite):
    MISSILE_WIDTH = 39
    MISSILE_HEIGHT = 39

    DEFAULT_VELOCITY = 3000         # Default velocity in pixels per second
    DEFAULT_TIME_TO_LIVE = 5        # Default TTL in seconds

    def __init__(self, x, y, image, velocity, angle, time_to_live=DEFAULT_TIME_TO_LIVE):
        super().__init__(x, y, [image], 0, velocity)

        self._time_to_live = time_to_live
        self.set_rotation(angle)
        self.set_max_velocity(5000, 5000)

    def update(self, scene, dt):
        super().update(scene, dt)

        self._time_to_live -= dt

        if self._time_to_live <= 0:
            self.kill()


class Photon(sprite.KinematicSprite):
    WIDTH = 42
    HEIGHT = 76

    COLOR_GREEN = 0
    COLOR_YELLOW = 1
    COLOR_RED = 2
    COLOR_WHITE = 3

    VELOCITY = 3000  # Default velocity in pixels per second
    TIME_TO_LIVE = 0.5  # Default TTL in seconds

    _COLLISION_RADIUS = 35

    def __init__(self, x, y, image, scale, velocity, angle, time_to_live=TIME_TO_LIVE):
        super().__init__(x, y, [image], 0, velocity)

        self._time_to_live = time_to_live

        self.set_scale(scale)
        self.set_rotation(angle)
        self.set_max_velocity(Photon.VELOCITY, Photon.VELOCITY)

    @property
    def radius(self):
        return int(Photon._COLLISION_RADIUS * self.scale)

    def update(self, scene, dt):
        super().update(scene, dt)

        # TODO: At some point might need to think about pooling projectiles for performance

        self._time_to_live -= dt

        if self._time_to_live <= 0 or scene.rect.colliderect(self.rect) == False:
            self.kill()

    @classmethod
    def get_tileset(cls, image_cache):
        return spritesheet.SpriteSheet(image_cache.get('photon_set_01'), Photon.WIDTH, Photon.HEIGHT)


class SingleShot(PlayerWeapon):
    """
        SingleShot - Fires a single missile from the from of the player ship

        Note: This should the basic primary weapon the player starts with. Variations could
        could be created by modifying the velocity, TTL and cool-down values

    """

    _COOL_DOWN_TIMER = 50

    def __init__(self, game, ship):
        super().__init__(game, ship)

        self._tiles = Photon.get_tileset(game.image_cache)
        self._last_update = pygame.time.get_ticks()
        self._can_fire = True

        self._sound = game.audio_cache.get('sfx_laser1')

    def can_fire(self):
        return self._can_fire

    def fire(self):
        player_ship = self.ship

        x = player_ship.rect.centerx
        y = player_ship.rect.centery

        velocity = player_ship.velocity + (player_ship.get_forward_vector() * Photon.VELOCITY)
        missile = Photon(x, y, self._tiles.get_tile(Photon.COLOR_GREEN), player_ship.scale,
                         velocity, player_ship.rotation)

        self._sound.play()

        return [missile]

    def update(self, scene, dt):
        now = pygame.time.get_ticks()

        if now - self._last_update >= SingleShot._COOL_DOWN_TIMER:
            self._last_update = now
            self._can_fire = True
        else:
            self._can_fire = False


class DoubleShot(PlayerWeapon):

    def __init__(self, game, ship):
        super().__init__(game, ship)

        self._tiles = Photon.get_tileset(game.image_cache)
        self._sound = game.audio_cache.get('sfx_laser2')

    def fire(self):
        player_ship = self.ship
        velocity = player_ship.velocity + (player_ship.get_forward_vector() * Photon.VELOCITY)

        # FIXME: Don't hardcode the gun positions, since we will have different ships it would be better
        # FIXME: to ask the ship (e.g ship.get_cannon_position (x) )

        mp1 = pygame.math.Vector2(-35, 0)
        mp1.rotate_ip(player_ship.rotation)

        mp1.x += player_ship.position.x
        mp1.y += player_ship.position.y

        missile1 = Photon(mp1.x, mp1.y, self._tiles.get_tile(Photon.COLOR_RED), player_ship.scale,
                          velocity, player_ship.rotation)

        mp2 = pygame.math.Vector2(35, 0)
        mp2.rotate_ip(player_ship.rotation)

        mp2.x += player_ship.position.x
        mp2.y += player_ship.position.y

        missile2 = Photon(mp2.x, mp2.y, self._tiles.get_tile(Photon.COLOR_RED), player_ship.scale,
                          velocity, player_ship.rotation)

        self._sound.play()

        return [missile1, missile2]


class RadialShot(PlayerWeapon):
    """
        RadialShot - Fires several missiles radiating from the center of the player ship in a circle

        Note: This might be a good secondary weapon obtained via a power up
    """

    DEFAULT_VELOCITY = 800          # Default velocity in pixels per second
    DEFAULT_TIME_TO_LIVE = 2        # Default TTL in seconds
    DEFAULT_MISSILE_COUNT = 20      # Default number of missiles to fire

    def __init__(self, game, ship):
        super().__init__(game, ship)

        self._tiles = Photon.get_tileset(game.image_cache)

        # self._tiles = spritesheet.SpriteSheet (game.image_cache.get ('missile_set'),
        #                                        Missile.MISSILE_WIDTH, Missile.MISSILE_HEIGHT)

    def fire(self):
        player_ship = self.ship
        missiles = []

        for angle in range(0, 360, 360 // RadialShot.DEFAULT_MISSILE_COUNT):
            radians = math.radians(angle)
            forward = pygame.math.Vector2(math.cos(radians), -math.sin(radians))

            missile_velocity = player_ship.velocity + (forward * RadialShot.DEFAULT_VELOCITY)

            x = player_ship.rect.centerx + (forward.x * player_ship.rect.width / 2)
            y = player_ship.rect.centery + (forward.y * player_ship.rect.width / 2)

            missile = Photon(x, y, self._tiles.get_tile(Photon.COLOR_YELLOW), player_ship.scale,
                             missile_velocity, angle)

            # missiles.append (Missile (x, y, self._tiles.get_tile (0),
            #                           missile_velocity, 0, RadialShot.DEFAULT_TIME_TO_LIVE))

            missiles.append(missile)

        return missiles

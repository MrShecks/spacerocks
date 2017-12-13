import math
import pygame

from gamelib import sprite
from gamelib import tileset

from abc import ABC, abstractmethod


class PlayerWeapon (ABC):

    def __init__ (self, player_ship):
        self.__player_ship = player_ship

    @abstractmethod
    def fire (self):

        """
            Fire the weapon creating one or more projectiles

            :return: Array of projectiles generated by firing the weapon

        """

    def can_fire (self):
        return True

    def _get_player_ship (self):
        return self.__player_ship

class Missile (sprite.KinimaticSprite):

    MISSILE_WIDTH           = 39
    MISSILE_HEIGHT          = 39

    DEFAULT_VELOCITY        = 800   # Default velocity in pixels per second
    DEFAULT_TIME_TO_LIVE    = 5     # Default TTL in seconds

    def __init__ (self, x, y, image, velocity, angle, time_to_live = DEFAULT_TIME_TO_LIVE):
        super ().__init__ (x, y, [image], 0, velocity)

        self._time_to_live = time_to_live

    def update (self, dt):
        super ().update (dt)

        self._time_to_live -= dt

        if self._time_to_live <= 0:
            self.kill ()


class SingleShot (PlayerWeapon):

    """
        SingleShot - Fires a single missile from the from of the player ship

        Note: This should the basic primary weapon the player starts with. Variations could
        could be created by modifying the velocity, TTL and cool-down values

    """

    def __init__ (self, player_ship, images):
        super ().__init__ (player_ship)
        self._tiles = tileset.TileSet (images.get ('missile_set'), Missile.MISSILE_WIDTH, Missile.MISSILE_HEIGHT)

    def fire (self):
        ship = self._get_player_ship ()

        x = ship.rect.centerx # + (ship.forward.x * ship.rect.width / 2)
        y = ship.rect.centery # + (ship.forward.y * ship.rect.width / 2)

        missile_velocity = ship.velocity + (ship.forward * Missile.DEFAULT_VELOCITY)
        missile = Missile (x, y, self._tiles.get_tile (1), missile_velocity, 0)

        return [ missile ]


class DoubleShot (PlayerWeapon):

    def __init__ (self, player_ship, images):
        super ().__init__ (player_ship)
        self._tiles = tileset.TileSet (images.get ('missile_set'), Missile.MISSILE_WIDTH, Missile.MISSILE_HEIGHT)

    def fire (self):
        ship = self._get_player_ship ()

        #missile_velocity = velocity + (forward * Missile.DEFAULT_VELOCITY)

        missile_velocity = pygame.math.Vector2 ()

        x = ship.rect.centerx + ship.forward.x
        y = ship.rect.centery + ship.forward.y

        missile1 = Missile (x, y, self._tiles.get_tile (0), missile_velocity, 0)

        # x = rect.centerx + (forward.x * rect.width / 2)
        # y = rect.centery + (forward.y * rect.width / 2)
        #
        # missile2 = Missile (x, y, self._tiles.get_tile (0), missile_velocity, 0)

        return [ missile1 ]


class RadialShot (PlayerWeapon):

    """
        RadialShot - Fires several missiles radiating from the center of the player ship in a circle

        Note: This might be a good secondary weapon obtained via a power up
    """

    DEFAULT_VELOCITY        = 800   # Default velocity in pixels per second
    DEFAULT_TIME_TO_LIVE    = 2     # Default TTL in seconds
    DEFAULT_MISSILE_COUNT   = 20    # Default number of missiles to fire

    def __init__ (self, player_ship, images):
        super ().__init__ (player_ship)
        self._tiles = tileset.TileSet (images.get ('missile_set'), Missile.MISSILE_WIDTH, Missile.MISSILE_HEIGHT)

    def fire (self):
        player_ship = self._get_player_ship ()
        missiles = []

        for angle in range (0, 360, 360 // RadialShot.DEFAULT_MISSILE_COUNT):
            radians = math.radians (angle)
            forward = pygame.math.Vector2 (math.cos (radians), -math.sin (radians))

            missile_velocity = player_ship.velocity + (forward * RadialShot.DEFAULT_VELOCITY)

            x = player_ship.rect.centerx + (forward.x * player_ship.rect.width / 2)
            y = player_ship.rect.centery + (forward.y * player_ship.rect.width / 2)

            missiles.append (Missile (x, y, self._tiles.get_tile (0),
                                      missile_velocity, 0, RadialShot.DEFAULT_TIME_TO_LIVE))

        return missiles
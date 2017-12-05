import pygame
import math

from gamelib.scene import SceneSprite
from gamelib.tileset import TileSet


class PlayerShip (SceneSprite):

    WIDTH               = 90
    HEIGHT              = 90

    TILE_SHIP           = 0
    TILE_SHIP_THRUST    = 1
    TILE_SHIP_SHIELD    = 2

    THRUST_VELOCITY     = 25        # Acceleration in pixels per second
    THRUST_FRICTION     = 2        # Deceleration in pixels per second
    ROTATE_VELOCITY     = 200       # Rotation speed in degrees per second

    def __init__ (self, image, screen_rect):
        super ().__init__ (PlayerShip.WIDTH, PlayerShip.HEIGHT)

        self._angle = 0
        self._thrust = False
        self._thrust_velocity = pygame.math.Vector2 ()
        self._rotate_velocity = 0
        self._screen_rect = screen_rect

        self._tiles = TileSet (image, PlayerShip.WIDTH, PlayerShip.HEIGHT)

    def rotate (self, rotate_velocity):
        self._rotate_velocity += rotate_velocity

    def set_thrust (self, thrust):
        self._thrust = thrust

    def update (self, dt):
        # Update the rotation angle, clamping to 2*PI radians (360 degrees)
        self._angle = (self._angle + (self._rotate_velocity * dt)) % 360

        # Update the ships position
        self._rect.centerx = (self._rect.centerx + self._thrust_velocity.x) % self._screen_rect.width
        self._rect.centery = (self._rect.centery + self._thrust_velocity.y) % self._screen_rect.height

        # FIXME: Drag/Friction integration not work right
        # Apply friction to the ships velocity
        # self._thrust_velocity.x *= (1.0 - (PlayerShip.THRUST_FRICTION * dt))
        # self._thrust_velocity.y *= (1.0 - (PlayerShip.THRUST_FRICTION * dt))

        # If the engines are running then apply thrust to the velocity
        if self._thrust:
            forward = self.__getForwardVector (math.radians (self._angle))
            self._thrust_velocity.x += (forward[0] * PlayerShip.THRUST_VELOCITY * dt)
            self._thrust_velocity.y += (forward[1] * PlayerShip.THRUST_VELOCITY * dt)

        # TODO: Will need to draw the ships shield if it's on

        frame = PlayerShip.TILE_SHIP_THRUST if self._thrust else PlayerShip.TILE_SHIP
        self._image = self.rot_center (self._tiles.get_tile (frame), self._angle)

        #self._image = pygame.transform.rotate (self._tiles.get_tile (self._frame), self._angle)
        #print ('Rect=', self._rect, 'Angle=', self._angle, 'Forward=', forward)

        print ('Velocity=', self._thrust_velocity)

    def __getForwardVector (self, angle):
        return [math.cos (angle), -math.sin (angle)]

    def rot_center (self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()

        return rot_image

    # def rot_center (self, image, angle):
    #     """rotate a Surface, maintaining position."""
    #
    #     loc = image.get_rect ().center  # rot_image is not defined
    #     rot_sprite = pygame.transform.rotate (image, angle)
    #     rot_sprite.get_rect ().center = loc
    #     return rot_sprite

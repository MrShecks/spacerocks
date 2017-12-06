import pygame
import math

from gamelib.scene import SceneSprite
from gamelib.tileset import TileSet
from weapons import SingleShot


class PlayerShip (SceneSprite):

    WIDTH               = 90
    HEIGHT              = 90

    TILE_SHIP           = 0
    TILE_SHIP_THRUST    = 1
    TILE_SHIP_SHIELD    = 2

    DEFAULT_THRUST_VELOCITY     = 25.0      # Acceleration in pixels per second
    DEFAULT_THRUST_FRICTION     = 2.0       # Deceleration in pixels per second
    DEFAULT_ROTATE_VELOCITY     = 200       # Rotation speed in degrees per second

    def __init__ (self, image_cache, screen_rect, scene):
        super ().__init__ (PlayerShip.WIDTH, PlayerShip.HEIGHT)

        self._scene = scene

        self._angle = 0
        self._thrust = False
        self._has_friction = True
        self._rotate_velocity = 0

        self._thrust_velocity = PlayerShip.DEFAULT_THRUST_VELOCITY
        self._thrust_friction = PlayerShip.DEFAULT_THRUST_FRICTION

        self._screen_rect = screen_rect

        self._tiles = TileSet (image_cache.get_image ('player_ship'), PlayerShip.WIDTH, PlayerShip.HEIGHT)
        self._bullets = TileSet (image_cache.get_image ('missile_set'), 39, 39)

        self._projectiles = pygame.sprite.Group ()
        self._primary_weapon = SingleShot (self, image_cache)

        # photon = Photon (100, 100, self._bullets.get_tile (0), 60)
        # photon.add (self._projectiles)

    def rotate (self, rotate_velocity):
        self._rotate_velocity += rotate_velocity

    def fire_weapon (self):
        print ('PlayerShip::fire_weapon ()')

        projectiles = []


        if self._primary_weapon.can_fire ():
            projectiles = self._primary_weapon.fire ()

        if projectiles:
            self._scene.add_nodes (projectiles, 5)


    def set_thrust (self, thrust):
        self._thrust = thrust

    def toggle_friction (self):
        self._has_friction = not self._has_friction

    def get_projectiles (self):
        return self._projectiles

    def get_forward_vector (self):
        return self.__get_forward_vector (math.radians (self._angle))

    def update (self, dt):

        # Update the rotation angle, clamping to 2*PI radians (360 degrees)
        self._angle = (self._angle + (self._rotate_velocity * dt)) % 360

        # If the engines are running then apply thrust to the velocity
        if self._thrust:
            forward = self.__get_forward_vector (math.radians (self._angle))
            self._velocity.x += (forward.x * self._thrust_velocity * dt)
            self._velocity.y += (forward.y * self._thrust_velocity * dt)

        # Update the ships position
        self._rect.centerx = (self._rect.centerx + self._velocity.x) % self._screen_rect.width
        self._rect.centery = (self._rect.centery + self._velocity.y) % self._screen_rect.height

        # FIXME: Friction should eventually bring the velocity down to 0 instead of continually decreasing

        # Apply friction to the ships velocity
        if self._has_friction:
            self._velocity.x *= (1.0 - (self._thrust_friction * dt))
            self._velocity.y *= (1.0 - (self._thrust_friction * dt))


        # TODO: Will need to draw the ships shield if it's on

        frame = PlayerShip.TILE_SHIP_THRUST if self._thrust else PlayerShip.TILE_SHIP
        self._image = self.__rotate_around_center (self._tiles.get_tile (frame), self._angle)

        # Update the sprite rectangle in case the width and height was change by the rotation
        # This should only be an issue if the sprite isn't exactly square
        self._rect.width = self._image.get_width ()
        self._rect.height = self._image.get_height ()


    def __get_forward_vector (self, angle):
        return pygame.math.Vector2 (math.cos (angle), -math.sin (angle))

    def __rotate_around_center (self, image, angle):
        # TODO: Review this, I don't like the idea of creating copies of the surface on each update

        orig_rect = image.get_rect ()
        rot_image = pygame.transform.rotate (image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect ().center
        rot_image = rot_image.subsurface (rot_rect).copy ()

        return rot_image
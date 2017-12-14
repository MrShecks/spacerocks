import pygame

from gamelib.tileset import TileSet
from player.weapons import SingleShot
from player.weapons import RadialShot

from gamelib import sprite
from gamelib import utils

class PlayerShip (sprite.KinematicSprite):

    ROTATE_STOP             = 0
    ROTATE_RIGHT            = 1
    ROTATE_LEFT             = -1


    PRIMARY_WEAPON          = 0
    SECONDARY_WEAPON        = 1

    _WIDTH                  = 90
    _HEIGHT                 = 90

    _TILE_SHEET             = 'player_ship'

    _TILE_SHIP              = 0
    _TILE_SHIP_THRUST       = 1
    _TILE_SHIP_SHIELD       = 2

    _THRUST_VELOCITY        = 400           # Acceleration in pixels per second
    _ROTATE_VELOCITY        = 200           # Rotation speed in degrees per second
    _SHIP_DRAG              = 100           # Deceleration in pixels per second

    def __init__ (self, x, y, image_cache, screen_rect):
        super ().__init__ (x, y, TileSet (image_cache.get (PlayerShip._TILE_SHEET),
                                          PlayerShip._WIDTH, PlayerShip._HEIGHT))

        self.set_rotation (0)

        self._thrust = False
        self._has_drag = False
        self._has_shield = False

        self._thrust_velocity = PlayerShip._THRUST_VELOCITY
        self._thrust_friction = PlayerShip._SHIP_DRAG

        self._screen_rect = screen_rect

        self._projectiles = pygame.sprite.Group ()

        self._primary_weapon = SingleShot (self, image_cache)
        #self._primary_weapon = DoubleShot (self, image_cache)
        self._secondary_weapon = RadialShot (self, image_cache)

    def rotate (self, type):
        self.set_rotation_velocity (PlayerShip._ROTATE_VELOCITY * type)

    def fire_weapon (self, type):
        print ('DBG: PlayerShip::fire_weapon (): Type=', type)

        weapon = self._primary_weapon if type == PlayerShip.PRIMARY_WEAPON else self._secondary_weapon

        if weapon.can_fire ():
            projectiles = weapon.fire ()

            if projectiles:
                self.scene.add_nodes (projectiles, self.scene_layer)
                self._projectiles.add (projectiles)


    def set_thrust (self, thrust):
        self._thrust = thrust

    def toggle_drag (self):

        if not self._has_drag:
            self.set_drag (PlayerShip._SHIP_DRAG, PlayerShip._SHIP_DRAG)
        else:
            self.set_drag (0, 0)

        self._has_drag = not self._has_drag

    def toggle_shield (self):
        self._has_shield = not self._has_shield

    @property
    def projectiles (self):
        return self._projectiles

    def update (self, dt):
        super ().update (dt)

        # self._primary_weapon.update (dt)

        if self._thrust == True:
            forward = self.get_forward_vector () * self._thrust_velocity
            self.set_acceleration (forward.x, forward.y)
        elif self.acceleration:
            self.set_acceleration (0, 0)

        # TODO: handle display of the ships shield
        frame = PlayerShip._TILE_SHIP_THRUST if self._thrust else PlayerShip._TILE_SHIP
        frame = frame if self._has_shield == False else frame + 2
        self.set_frame_index (frame)

        # If the ship runs off the edge of the screen it should warp to the opposite side
        self._rect.center = utils.clamp_point_to_rect (self._rect.center, self._screen_rect)

        # if self._primary_weapon.can_fire ():
        #     self.fire_weapon (PlayerShip.PRIMARY_WEAPON)

        #print ('PlayerShip::update (): Velocity=', self.velocity, ', Acceleration=', self.acceleration, ', Drag=', self.drag)
        #print ('PlayerShip::update (): Forward=', self.get_forward_vector (), ', Rotation=', self.rotation)
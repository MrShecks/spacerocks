import pygame

from gamelib.tileset import TileSet
from player.weapons import SingleShot
from player.weapons import RadialShot

from gamelib import sprite

class PlayerShip (sprite.KinimaticSprite):

    ROTATE_STOP             = 0
    ROTATE_LEFT             = 1
    ROTATE_RIGHT            = -1

    PRIMARY_WEAPON          = 0
    SECONDARY_WEAPON        = 1

    _WIDTH                  = 90
    _HEIGHT                 = 90

    _TILE_SHIP              = 0
    _TILE_SHIP_THRUST       = 1
    _TILE_SHIP_SHIELD       = 2

    _THRUST_VELOCITY        = 400           # Acceleration in pixels per second
    _ROTATE_VELOCITY        = 200           # Rotation speed in degrees per second
    _SHIP_DRAG              = 2.0           # Deceleration in pixels per second

    def __init__ (self, x, y, image_cache, screen_rect, scene):
        super ().__init__ (x, y, TileSet (image_cache.get ('player_ship'), PlayerShip._WIDTH, PlayerShip._HEIGHT))

        self.set_rotation (90)

        self._thrust = False
        self._has_drag = False

        self._thrust_velocity = PlayerShip._THRUST_VELOCITY
        self._thrust_friction = PlayerShip._SHIP_DRAG

        self._screen_rect = screen_rect

        self._bullets = TileSet (image_cache.get ('missile_set'), 39, 39)

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

    def toggle_friction (self):

        if not self._has_drag:
            self.set_drag (-1, -1)
        else:
            self.set_drag (0, 0)

        self._has_drag = not self._has_drag

    @property
    def projectiles (self):
        return self._projectiles

    @property
    def forward (self):
        return self.get_forward_vector ()

    def update (self, dt):
        super ().update (dt)

        #print ('Ship:', self)

        if self._thrust:
            forward = self.get_forward_vector () * self._thrust_velocity
            self.set_acceleration (forward.x, forward.y)
        else:
            self.set_acceleration (0, 0)

        # TODO: handle display of the ships shield
        frame = PlayerShip._TILE_SHIP_THRUST if self._thrust else PlayerShip._TILE_SHIP
        self.set_frame_index (frame)

        # If the ship runs off the edge of the screen it should warp to the opposite side

        if self.rect.centerx <= 0:
            self.rect.centerx = self._screen_rect.width
        elif self.rect.centerx >= self._screen_rect.width:
            self.rect.centerx = 0

        if self.rect.centery <= 0:
            self.rect.centery = self._screen_rect.height
        elif self.rect.centery >= self._screen_rect.height:
            self.rect.centery = 0
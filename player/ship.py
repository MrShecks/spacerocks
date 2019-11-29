import pygame

from gamelib import spritesheet
from gamelib import sprite
from gamelib import utils

from player import weapons


class Factory:
    TYPE_RED_VIPER = 0
    TYPE_YELLOW_HAWK = 1

    @classmethod
    def create(cls, ship_type, x, y, game):
        # TODO: Change this when more ships are added

        if ship_type == Factory.TYPE_RED_VIPER:
            ship = RedViper(x, y, game)
        else:
            ship = YellowHawk(x, y, game)

        return ship


class PlayerShip(sprite.KinematicSprite):
    ROTATE_STOP = 0
    ROTATE_RIGHT = 1
    ROTATE_LEFT = -1

    PRIMARY_WEAPON = 0
    SECONDARY_WEAPON = 1

    _TILE_SHIP = 0
    _TILE_SHIP_THRUST = 1
    _TILE_SHIP_SHIELD = 2

    _THRUST_VELOCITY = 400      # Acceleration in pixels per second
    _ROTATE_VELOCITY = 200      # Rotation speed in degrees per second
    _SHIP_DRAG = 100            # Deceleration in pixels per second

    _COLLISION_RADIUS = 80

    def __init__(self, x, y, tileset_name, tile_width, tile_height, scale, game):
        super().__init__(x, y, self._get_tileset(game.image_cache, tileset_name, tile_width, tile_height))

        self.set_rotation(0)
        self.set_scale(scale)

        self._thrust = False
        self._has_drag = False
        self._has_shield = False

        self._thrust_velocity = PlayerShip._THRUST_VELOCITY
        self._thrust_friction = PlayerShip._SHIP_DRAG

        self._screen_rect = game.rect

        self._projectiles = pygame.sprite.Group()

        self._primary_weapon = weapons.SingleShot(game, self)
        self._secondary_weapon = weapons.DoubleShot(game, self)

        # self._primary_weapon = weapons.DoubleShot (game, self)
        # self._secondary_weapon = weapons.RadialShot (game, self)

    @property
    def radius(self):
        return int(PlayerShip._COLLISION_RADIUS * self.scale)

    def rotate(self, type):
        self.set_rotation_velocity(PlayerShip._ROTATE_VELOCITY * type)

    def fire_weapon(self, type):
        print('DBG: PlayerShip::fire_weapon (): Type=', type)

        weapon = self._primary_weapon if type == PlayerShip.PRIMARY_WEAPON else self._secondary_weapon

        if weapon.can_fire():
            projectiles = weapon.fire()

            if projectiles:
                self.scene.add_nodes(projectiles, self.scene_layer)
                self._projectiles.add(projectiles)

    def set_thrust(self, thrust):
        self._thrust = thrust

    def toggle_drag(self):

        if not self._has_drag:
            self.set_drag(PlayerShip._SHIP_DRAG, PlayerShip._SHIP_DRAG)
        else:
            self.set_drag(0, 0)

        self._has_drag = not self._has_drag

    def toggle_shield(self):
        self._has_shield = not self._has_shield

    @property
    def projectiles(self):
        return self._projectiles

    @property
    def screen_rect(self):
        return self._screen_rect

    def update(self, scene, dt):
        super().update(scene, dt)

        # self._primary_weapon.update (scene, dt)

        if self._thrust:
            forward = self.get_forward_vector() * self._thrust_velocity
            self.set_acceleration(forward.x, forward.y)
        elif self.acceleration:
            self.set_acceleration(0, 0)

        # TODO: handle display of the ships shield
        frame = PlayerShip._TILE_SHIP_THRUST if self._thrust else PlayerShip._TILE_SHIP
        frame = frame if self._has_shield is False else frame + 2
        self.set_frame_index(frame)

        # If the ship runs off the edge of the screen it should warp to the opposite side
        self._rect.center = utils.clamp_point_to_rect(self._rect.center, self._screen_rect)

        # if self._primary_weapon.can_fire ():
        #     self.fire_weapon (PlayerShip.PRIMARY_WEAPON)

        # print ('PlayerShip::update (): Velocity=', self.velocity, ', Acceleration=', self.acceleration, ', Drag=', self.drag)
        # print ('PlayerShip::update (): Forward=', self.get_forward_vector (), ', Rotation=', self.rotation)

    @staticmethod
    def _get_tileset(image_cache, name, width, height):
        return spritesheet.SpriteSheet(image_cache.get(name), width, height)


class RedViper(PlayerShip):
    _TILE_WIDTH = 168
    _TILE_HEIGHT = 236
    _TILE_SCALE = 0.70

    _TILE_SET_NAME = 'playership_set_01'

    def __init__(self, x, y, game):
        super().__init__(x, y, RedViper._TILE_SET_NAME, RedViper._TILE_WIDTH,
                         RedViper._TILE_HEIGHT, RedViper._TILE_SCALE, game)


class YellowHawk(PlayerShip):
    _TILE_WIDTH = 186
    _TILE_HEIGHT = 296
    _TILE_SCALE = 0.50

    _TILE_SET_NAME = 'playership_set_02'

    def __init__(self, x, y, game):
        super().__init__(x, y, YellowHawk._TILE_SET_NAME, YellowHawk._TILE_WIDTH,
                         YellowHawk._TILE_HEIGHT, YellowHawk._TILE_SCALE, game)

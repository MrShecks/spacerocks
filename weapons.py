from abc import ABC, abstractmethod
from gamelib.scene import SceneSprite
from gamelib.tileset import TileSet


class PlayerWeapon (ABC):

    def __init__ (self, player_ship):
        self.__player_ship = player_ship

    @abstractmethod
    def fire (self):
        '''
            Fire the weapon creating one or more projectiles

            :return: Array of projectiles (SceneSprite based)

        '''

        pass

    def can_fire (self):
        return True

    def _get_player_ship (self):
        return self.__player_ship

class Missile (SceneSprite):

    _MISSILE_WIDTH = 39
    _MISSILE_HEIGHT = 39

    def __init__ (self, x, y, image, time_to_live):
        super ().__init__ (Missile._MISSILE_WIDTH, Missile._MISSILE_HEIGHT)
        self._image = image
        self._time_to_live = time_to_live
        self.set_center (x, y)

    def update (self, dt):
        #print ('Photon::update (): dt=', dt, 'TTL=', self._time_to_live, 'Pos=', self._rect, ', Sprite=', self)

        if self._time_to_live > 0:
            self._rect.centerx = (self._rect.centerx + self._velocity.x)
            self._rect.centery = (self._rect.centery + self._velocity.y)

            self._time_to_live -= dt
        else:
            self.kill ()


class SingleShot (PlayerWeapon):

    _MISSILE_WIDTH      = 39
    _MISSILE_HEIGHT     = 39

    _MISSILE_TTL        = 10
    _MISSILE_VELOCITY   = 8

    def __init__ (self, player_ship, images):
        super ().__init__ (player_ship)
        self._tiles = TileSet (images.get_image ('missile_set'), SingleShot._MISSILE_WIDTH, SingleShot._MISSILE_HEIGHT)

    def fire (self):
        player_ship = self._get_player_ship ()

        rect = player_ship.get_bounding_rect ()
        velocity = player_ship.get_velocity ()
        forward = player_ship.get_forward_vector ()

        x = rect.centerx + (forward.x * rect.width / 2)
        y = rect.centery + (forward.y * rect.width / 2)

        missile = Missile (x, y, self._tiles.get_tile (1), SingleShot._MISSILE_TTL)

        missile._velocity = velocity + (forward * SingleShot._MISSILE_VELOCITY)

        return [ missile ]




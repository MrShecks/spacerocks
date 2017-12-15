import abc

from gamelib import sprite

class Entity (sprite.KinematicSprite):

    TYPE_ASTEROID_SMALL     = 0
    TYPE_ASTEROID_MEDIUM    = 1
    TYPE_ASTEROID_LARGE     = 2
    TYPE_ASTEROID_HUGE      = 3

    TYPE_POWERUP            = 4

    TYPE_INVALID            = -1

    @property
    @abc.abstractmethod
    def entity_type (self):
        pass

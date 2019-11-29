import abc
import random
import pygame

from gamelib import sprite


class Entity(sprite.KinematicSprite):
    # FIXME: These should not be here!
    TYPE_ASTEROID_SMALL = 0
    TYPE_ASTEROID_MEDIUM = 1
    TYPE_ASTEROID_LARGE = 2
    TYPE_ASTEROID_HUGE = 3

    TYPE_POWERUP = 4
    TYPE_FLOATING_TEXT = 5

    TYPE_INVALID = -1

    @property
    @abc.abstractmethod
    def entity_type(self):
        pass

    @staticmethod
    def choose_velocity(min_velocity, max_velocity):
        vx = Entity.choose_range(min_velocity, max_velocity)
        vy = Entity.choose_range(min_velocity, max_velocity)

        return pygame.math.Vector2(vx, vy)

    @staticmethod
    def choose_range(min_range, max_range):
        return random.randrange(min_range, max_range) * random.choice([1, -1])

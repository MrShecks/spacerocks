import pygame

from entities import entity

class Factory (object):

    _DEFAULT_VELOCITY       = pygame.math.Vector2 (0, -20)
    _DEFAULT_TIME_TO_LIVE   = 1

    _game                   = None
    _font                   = None

    @classmethod
    def init (cls, game):
        if cls._game == None:
            cls._font = game.load_font ('kenvector_future_thin.ttf', 16)
            cls._game = game

    @classmethod
    def create (cls, x, y, text, color):

        return FloatingText (x, y, text, cls._font, color, Factory._DEFAULT_VELOCITY)

class FloatingText (entity.Entity):
    def __init__ (self, x, y, text, font, color, velocity, time_to_live = Factory._DEFAULT_TIME_TO_LIVE):
        super ().__init__ (x, y, [ self._get_frame (text, font, color) ], 0, velocity)

        self._time_to_live = time_to_live

    @property
    def entity_type (self):
        return entity.Entity.TYPE_FLOATING_TEXT

    def update (self, scene, dt):
        super ().update (scene, dt)

        if self._time_to_live > 0:
            self._time_to_live -= dt
        else:
            self.kill ()

    def _get_frame (self, text, font, color):
        return font.render (text, True, color)
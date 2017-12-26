import gamelib
import pygame
import abc

_DEBUG_SPRITE_BOUNDS        = gamelib._DEBUG_SCENE and True
_DEBUG_SPRITE_COLLISION     = gamelib._DEBUG_SCENE and True

class Scene (object):

    # --------------------------------------------------------------------------------------------------

    class Node (pygame.sprite.Sprite, abc.ABC):

        def __init__ (self):
            super ().__init__ ()
            self.__scene = None
            self.__scene_layer = -1

        @property
        def scene (self):
            return self.__scene

        @property
        def scene_layer (self):
            return self.__scene_layer

        def update (self, scene, dt):
            super ().update (scene, dt)

            if _DEBUG_SPRITE_BOUNDS:
                pygame.draw.rect (self.image, (0, 255, 0), [0, 0, self.rect.width, self.rect.height], 1)

            if _DEBUG_SPRITE_COLLISION and hasattr (self, 'radius'):
                pygame.draw.circle (self.image, (255, 0, 0),
                                    (self.rect.width // 2, self.rect.height // 2), self.radius, 1)


        def scene_add (self, scene, layer):
            self.__scene = scene
            self.__scene_layer = layer

        @property
        @abc.abstractmethod
        def image (self):
            pass

        @property
        @abc.abstractmethod
        def rect (self):
            pass

    # --------------------------------------------------------------------------------------------------

    def __init__ (self, game):
        self._game = game
        self._nodes = pygame.sprite.LayeredUpdates ()

    @property
    def game (self):
        return self._game

    @property
    def rect (self):
        return self._game.rect

    @property
    def object_count (self):
        return len (self._nodes)

    def add_node (self, node, scene_layer = -1):
        assert isinstance (node, Scene.Node)

        node.scene_add (self, scene_layer)
        self._nodes.add (node, layer=scene_layer)

    def add_nodes (self, nodes, scene_layer = -1):
        for node in nodes:
            self.add_node (node, scene_layer)

    def update (self, dt):
        self._nodes.update (self, dt)

    def draw (self, surface):
        self._nodes.draw (surface)

    def scene_activated (self):
        pass

    def scene_deactivated (self):
        pass

    def on_key_down (self, key, event):
        pass

    def on_key_up (self, key, event):
        pass

    def on_mouse_down (self, pos, event):
        pass

    def on_mouse_up (self, pos, event):
        pass

    def on_joy_motion (self, event):
        pass

    def on_joy_button_down (self, event):
        pass

    def on_joy_button_up (self, event):
        pass


class SceneText (Scene.Node):

    """
        Static scene node used to display a text string

    """

    def __init__ (self, x, y, text, font, color = (255, 255, 255)):
        super ().__init__ ()

        self.__image = font.render (text, True, color)
        self.__rect =  self.__image.get_rect ()

        self.__rect.x = x
        self.__rect.y = y

        self._text = text
        self._font = font
        self._color = color

        self._is_dirty = False

    def set_text (self, text):
        if self._text != text:
            self._text = text
            self._is_dirty = True

    def set_color (self, color):
        if self._color != color:
            self._color = color
            self._is_dirty = True

    def set_font (self, font):
        if self._font != font:
            self._font = font
            self._is_dirty = True

    def update (self, scene, dt):

        if self._is_dirty:
            pos = self.__rect.topleft

            self.__image = self._font.render (self._text, True, self._color)
            self.__rect = self.__image.get_rect ()
            self.__rect.topleft = pos

            self._is_dirty = False

        # Calling update () on the super class to allow any additional updates
        # to be performed on the sprite before it is drawn to the screen
        super ().update (scene, dt)

    @property
    def image (self):
        return self.__image

    @property
    def rect (self):
        return self.__rect

import gamelib
import pygame

_DEBUG_SPRITE_BOUNDS = gamelib._DEBUG_SCENE and True

class Sprite (pygame.sprite.Sprite):

    """
        Sprite

        This is the base class for all graphical objects managed buy a scene
        It's a simple subclass of PyGame.sprite.Sprite that adds some convenience and
        and debugging functionality to all scene objects
    """

    def __init__ (self, width, height, has_alpha = True):
        super ().__init__ ()

        flags = pygame.SRCALPHA if has_alpha else 0
        self._image = pygame.Surface ((width, height), flags)
        self._rect = self._image.get_rect ()

        self._scene_layer = -1
        self._scene = None

    def scene_update (self, dt):
        """
            Called to update the scene node before it is drawn to the scene.
            This method should be overridden by movable sprites or any sprites that
            need to update state or appearance between frames

            :param dt:              Time delta since last frame (in seconds)
            :return:                None
        """

        pass

    def scene_add (self, scene, scene_layer):
        """
            Called once by the scene when the node has been added to its sprite group

            :param scene:           The scene that the node has been added to
            :param scene_layer:     The layer that the node has been added too
            :return:                None
        """

        self._scene = scene
        self._scene_layer = scene_layer

    def update (self, dt):
        """
            Called by the scene manager (via PyGame) to update the sprite before it
            is drawn to the scene. The method will just delegate to Sprite.scene_update () for
            instance specific updating before performing some tasks useful for debugging (e.g. drawing
            the sprites bounding rect before it is rendered to the scene)

        :param dt:                  Time delta since the last frame (in seconds)
        :return:                    None

        """
        self.scene_update (dt)

        if _DEBUG_SPRITE_BOUNDS:
            pygame.draw.rect (self._image, (255, 0, 0), [0, 0, self._rect.width, self._rect.height ], 1)

    @property
    def image (self):
        """
            In order for PyGame to draw sprites it requires all classes inherited from PyGame.sprite.Sprite
            to have an surface attribute called 'image'. For the moment I've exposed the _image member as
            a property in case I ever want to change the implementation

            :return:                The sprites drawing surface
        """

        return self._image

    @property
    def rect (self):
        """
            In order for PyGame to draw sprites it requires all classes inherited from PyGame.sprite.Sprite
            to have an Rect attribute called 'rect'. For the moment I've exposed the _rect member as
            a property in case I ever want to change the implementation

            :return:                The sprites bounding rect
        """

        return self._rect

    @property
    def scene (self):
        """
            Returns the scene that the sprite belongs to

            :return:                Scene or None
        """

        return self._scene

    @property
    def scene_layer (self):
        """
            Returns the scene layer of the sprite within its scene

            :return:                Scene layer or -1
        """

        return self._scene_layer


class MovableSprite (Sprite):


    def __init__ (self, width, height, has_alpha = True):
        super ().__init__ (width, height, has_alpha)

        self._velocity = pygame.math.Vector2 ()

    def get_velocity (self):
        return self._velocity

    def get_bounding_rect (self):
        return self._rect

    def set_position (self, x, y):
        self._rect = self._rect.move (x, y)

    def set_center (self, x, y):
        self._rect.centerx = x
        self._rect.centery = y


class Scene (object):


    def __init__ (self):
        self._nodes = pygame.sprite.LayeredUpdates ()

    def add_node (self, node, scene_layer = -1):
        node.scene_add (self, scene_layer)
        self._nodes.add (node, layer=scene_layer)

    def add_nodes (self, nodes, scene_layer = -1):
        for node in nodes:
            self.add_node (node, scene_layer)

    def update (self, dt):
        self._nodes.update (dt)

    def draw (self, surface):
        self._nodes.draw (surface)

    def scene_activated (self):
        pass

    def scene_deactivated (self):
        pass
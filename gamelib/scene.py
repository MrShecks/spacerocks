import gamelib
import pygame

_DEBUG_SPRITE_BOUNDS        = gamelib._DEBUG_SCENE and True
_DEBUG_SPRITE_COLLISIONS    = gamelib._DEBUG_SCENE and True

class Sprite (pygame.sprite.Sprite):

    """
        Sprite

        This is the base class for all graphical objects managed buy a scene
        It's a simple subclass of PyGame.sprite.Sprite that adds some convenience and
        and debugging functionality to all scene objects
    """

    def __init__ (self, width, height, has_alpha = True):
        super ().__init__ ()

        flags = pygame.HWSURFACE
        flags |= pygame.SRCALPHA if has_alpha else 0

        self.__image = pygame.Surface ((width, height), flags)
        self.__rect = self.__image.get_rect ()

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
            pygame.draw.rect (self.image, (200, 0, 0), [0, 0, self.rect.width, self.rect.height ], 1)

        if _DEBUG_SPRITE_COLLISIONS:
            radius = max (self.rect.width, self.rect.height) // 2
            pygame.draw.circle ( self.image, (0, 200, 0), (self.rect.width // 2, self.rect.height // 2), radius, 1)


    @property
    def image (self):
        """
            In order for PyGame to draw sprites it requires all classes inherited from PyGame.sprite.Sprite
            to have an surface attribute called 'image'. For the moment I've exposed the _image member as
            a property in case I ever want to change the implementation

            :return:                The sprites drawing surface
        """

        return self.__image

    @image.setter
    def image (self, image):
        self.__image = image

    @property
    def rect (self):
        """
            In order for PyGame to draw sprites it requires all classes inherited from PyGame.sprite.Sprite
            to have an Rect attribute called 'rect'. For the moment I've exposed the _rect member as
            a property in case I ever want to change the implementation

            :return:                The sprites bounding rect
        """

        return self.__rect

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
        self._angle = 0

    def update (self, dt):
        super ().update (dt)

        self.rect.centerx = (self.rect.centerx + self.velocity.x)
        self.rect.centery = (self.rect.centery + self.velocity.y)

    @property
    def velocity (self):
        return self._velocity

    @velocity.setter
    def velocity (self, velocity):
        self._velocity = velocity

    @property
    def angle (self):
        return self._angle

    @angle.setter
    def angle (self, angle):
        self._angle = angle


class AnimatedSprite (MovableSprite):

    def __init__ (self, frames, frame_width, frame_height, frame_speed, has_alpha = True):
        super ().__init__ (frame_width, frame_height, has_alpha)

        self._frames = frames
        self._frame_speed = frame_speed

        self._current_frame = 0
        self._frame_timer = 0.0

        # TODO: Add support for specifying sub frames, sequence direction and loop control

#     def update (self, dt):
#         self._frame_timer = (self._frame_timer + ((1 / self._frame_speed) * dt)) % len (self._frames)
#
# #        print (self._frame_timer, self.frame_index)
#
#
#         super ().update (dt)

    def update (self, dt):
        self._frame_timer = (self._frame_timer + ((1 / self._frame_speed) * dt)) % len (self._frames)

        # FIXME: Temporary hack just to get explosions working for the moment

        if self._current_frame != self.frame_index:
            self._current_frame = self.frame_index

            if self._current_frame == 0:
                self.animation_start ()
            elif self._current_frame == len (self._frames) - 1:
                self.animation_end ()

        super ().update (dt)

    @property
    def frame_index (self):
        return int (self._frame_timer)

    @property
    def image (self):
        return self._frames[self.frame_index]

    def animation_start (self):
        pass

    def animation_end (self):
        pass


class Scene (object):


    def __init__ (self, game):
        self._game = game
        self._nodes = pygame.sprite.LayeredUpdates ()

    @property
    def game (self):
        return self._game

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

    def on_key_down (self, key, event):
        pass

    def on_key_up (self, key, event):
        pass

    def on_mouse_down (self, pos, event):
        pass

    def on_mouse_up (self, pos, event):
        pass


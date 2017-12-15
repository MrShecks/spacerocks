import pygame
import math
import abc

from gamelib import scene
from gamelib import utils


class SceneSprite (scene.Scene.Node):

    """
        Base class for all sprites drawn in the game scene. The base class supports displaying a sprite
        with one or more frames in a static position. By default only a single frame is displayed but
        an 'animator' can be applied to change frames on each update.
    """

    # --------------------------------------------------------------------------------------------------

    class Animator (abc.ABC):

        """
            Abstract base class for animators which can be used to animate the sprite on
            on each frame update
        """

        @abc.abstractmethod
        def update (self, sprite, dt):
            """
                Called once per frame to update the animators state

                :param sprite:  (SceneSprite) Sprite to animate
                :param dt:      (float) Time since last update

                :return:        None
            """
            pass

    # --------------------------------------------------------------------------------------------------

    _FLAG_UPDATE_NONE           = 0x00          # Sprite is up to date
    _FLAG_UPDATE_TRANSFORM      = 0x01          # Sprite transformation has changed
    _FLAG_UPDATE_FRAME          = 0x02          # Sprite image frame has changed

    def __init__ (self, x, y, frames, frame_index = 0):

        """
            :param x:               (int) Center position of sprite on x-axis
            :param y:               (int) Center position of sprite on y-axis
            :param frames:          (image[]) Array if image frames
            :param frame_index:     (int) Current frame index

        """

        super ().__init__ ()

        self.__frames = frames
        self.__frame_index = frame_index
        self.__frame_animator = None

        self._rect = frames[frame_index].get_rect ()

        self._rect.centerx = x
        self._rect.centery = y

        self._update_flags = SceneSprite._FLAG_UPDATE_NONE

    @property
    def frame_index (self):
        return self.__frame_index

    @property
    def frame_count (self):
        return len (self.__frames)

    def set_frame_animator (self, frame_animator):
        self.__frame_animator = frame_animator

    def set_frame_index (self, frame_index):
        if 0 <= frame_index < len (self.__frames) and self.__frame_index != frame_index:
            self._update_flags |= SceneSprite._FLAG_UPDATE_FRAME
            self.__frame_index = frame_index

    def update (self, dt):
        super ().update (dt)

        self._update_flags = SceneSprite._FLAG_UPDATE_NONE

        if self.__frame_animator:
            self.__frame_animator.update (self, dt)

    @property
    def image (self):
        return self.__frames[self.__frame_index]

    @property
    def rect (self):
        return self._rect


class StaticSprite (SceneSprite):

    """
        Helper class for single frame static sprites
        This should be used for sprites that do not move around the scene (e.g UI, HUD, Background)

        Note: For convenience StaticSprites are anchored relative to the top left corner
    """

    def __init__ (self, x, y, image, ):
        super ().__init__ (x + (image.get_width () // 2), y + (image.get_height () // 2), [image], 0)


class KinematicSprite (SceneSprite):

    """
        Base class for sprites that will move throughout the scene as forces are applied
    """

    _MAX_VELOCITY = 1000

    def __init__ (self, x, y, frames, frame_index = 0, velocity = None, max_velocity = None):

        """
            :param x:               (int) Center position of sprite on x-axis
            :param y:               (int) Center position of sprite on y-axis
            :param frames:          (image[]) Array if image frames
            :param frame_index:     (int) Current frame index
            :param velocity:        (Vector2) Initial velocity
            :param max_velocity:    (Vector2) Maximum velocity
        """

        super ().__init__ (x, y, frames, frame_index)

        if velocity is None:
            velocity = pygame.math.Vector2 ()

        if max_velocity is None:
            max_velocity = pygame.math.Vector2 (KinematicSprite._MAX_VELOCITY, KinematicSprite._MAX_VELOCITY)

        self.__frame_image = frames[frame_index].copy ()

        self.__velocity = velocity
        self.__max_velocity = max_velocity
        self.__acceleration = pygame.math.Vector2 ()
        self.__drag = pygame.math.Vector2 ()

        self.__rotation = 0
        self.__rotation_velocity = 0

        self.__scale = 1.0

    @property
    def position (self):
        return pygame.math.Vector2 (self._rect.centerx, self._rect.centery)

    @property
    def velocity (self):
        return pygame.math.Vector2 (self.__velocity)

    @property
    def acceleration (self):
        return pygame.math.Vector2 (self.__acceleration)

    @property
    def drag (self):
        return pygame.math.Vector2 (self.__drag)

    @property
    def scale (self):
        return self.__scale

    def set_position (self, x, y):
        self._rect.x = x
        self._rect.y = y

    def set_acceleration (self, x, y):
        self.__acceleration.x = x
        self.__acceleration.y = y

    def set_max_velocity (self, x, y):
        self.__max_velocity.x = x
        self.__max_velocity.y = y

    def set_drag (self, x, y):
        self.__drag.x = x
        self.__drag.y = y

    def set_scale (self, scale):
        if self.__scale != scale:
            self._update_flags |= SceneSprite._FLAG_UPDATE_TRANSFORM
            self.__scale = scale

    @property
    def rotation (self):
        return self.__rotation

    def set_rotation (self, rotation):
        if self.__rotation != rotation:
            self._update_flags |= SceneSprite._FLAG_UPDATE_TRANSFORM
            self.__rotation = rotation

    def set_rotation_velocity (self, rotation_velocity):
        if self.__rotation_velocity != rotation_velocity:
            self.__rotation_velocity = rotation_velocity

    def get_forward_vector (self):
        angle = math.radians (self.__rotation)

        return pygame.math.Vector2 (math.sin (angle), -math.cos (angle))

    def update (self, dt):

        # Recalculate the sprites angle of rotation if required
        if self.__rotation_velocity:
            self.__rotation_velocity = KinematicSprite.__get_velocity (dt, self.__rotation_velocity, 0, 0, 1000)
            self.__rotation = (self.__rotation + (self.__rotation_velocity * dt)) % 360
            self._update_flags |= SceneSprite._FLAG_UPDATE_TRANSFORM

        # Only update the sprites image if the rotation has changed or a new frame has been set
        if self._update_flags & (SceneSprite._FLAG_UPDATE_TRANSFORM | SceneSprite._FLAG_UPDATE_FRAME):

            # Note: Pygames transform.rotate () method expects negative values to rotate clockwise, all of our
            # math uses positive angles for clockwise rotation (e.g North=0, East=90, South= 180, West=270)
            # so we multiple the angle by -1

            self.__frame_image = pygame.transform.rotozoom (super ().image, self.__rotation * -1, self.__scale)

            current_position = self._rect.center

            self._rect = self.__frame_image.get_rect ()
            self._rect.center = current_position

        # Recalculate the sprites velocity
        self.__velocity.x = KinematicSprite.__get_velocity (dt, self.__velocity.x, self.__acceleration.x, self.__drag.x, self.__max_velocity.x)
        self.__velocity.y = KinematicSprite.__get_velocity (dt, self.__velocity.y, self.__acceleration.y, self.__drag.y, self.__max_velocity.y)

        # Apply velocity changes to the sprite position
        self._rect.x += self.__velocity.x * dt
        self._rect.y += self.__velocity.y * dt

        # Calling update () on the super class to allow any additional updates
        # to be performed on the sprite before it is drawn to the screen
        super ().update (dt)

    @property
    def image (self):
        return self.__frame_image

    @staticmethod
    def __get_velocity (dt, velocity, acceleration, drag, max_velocity):

        if acceleration:
            velocity += acceleration * dt
        elif drag:
            drag *= dt

            if velocity - drag > 0:
                velocity -= drag
            elif velocity + drag < 0:
                velocity += drag
            else:
                velocity = 0

        return utils.clamp (velocity, -max_velocity, max_velocity)

    # DEBUG - Review

    def __repr__ (self):
        return 'rect={0}, velocity={1}, acceleration={2}, rotation={3}, rotation_velocity={4}'\
            .format (self._rect, self.__velocity, self.__acceleration, self.__rotation, self.__rotation_velocity)

    # DEBUG - Review


class LinearFrameAnimator (SceneSprite.Animator):

    """
        Frame animator to cycle through each frame of a sprite at fixed intervals
    """

    def __init__ (self, frame_speed, frame_loop = False, kill_sprite = False):

        self._frame_speed = frame_speed
        self._frame_loop = frame_loop
        self._kill_sprite = kill_sprite

        self._last_update = pygame.time.get_ticks ()

    def update (self, sprite, dt):
        now = pygame.time.get_ticks ()

        if now - self._last_update > self._frame_speed:
            current_frame_index = sprite.frame_index

            if current_frame_index + 1 < sprite.frame_count:
                sprite.set_frame_index (current_frame_index + 1)
            elif self._frame_loop:
                sprite.set_frame_index (0)
            elif self._kill_sprite:
                sprite.kill ()

            self._last_update = now
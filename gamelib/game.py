import pygame
from gamelib import assets

class Game (object):

    def __init__ (self, width, height, title = '', fps_lock = 60):
        pygame.init ()

        flags = 0 #pygame.DOUBLEBUF|pygame.HWSURFACE

        self.__surface = pygame.display.set_mode ((width, height), flags)
        self.__fps_lock = fps_lock

        self.__is_running = False
        self.__active_scene = None

        self.__image_cache = assets.ImageCache ()

        pygame.display.set_caption (title)

    def run (self):
        self.__is_running = True
        clock = pygame.time.Clock ()

        while self.__is_running:
            dt = clock.tick (self.__fps_lock)

            if self.__active_scene:
                for event in pygame.event.get ():
                    if event.type == pygame.QUIT:
                        self.__is_running = not self.on_quit ()
                    elif event.type == pygame.KEYDOWN:
                        self.__active_scene.on_key_down(event.key, event)
                    elif event.type == pygame.KEYUP:
                        self.__active_scene.on_key_up (event.key, event)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.__active_scene.on_mouse_down (event.pos, event)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.__active_scene.on_mouse_up (event.pos, event)

                self.__active_scene.update (dt / 1000.0)
                self.__active_scene.draw (self.__surface)

                pygame.display.flip ()

                # print ('FPS=', clock.get_fps ())

        pygame.quit ()

    def set_active_scene (self, scene):

        if scene:
            if self.__active_scene:
                self.__active_scene.scene_deactivated ()

            self.__active_scene = scene
            self.__active_scene.scene_activated ()


    @property
    def rect (self):
        return self.__surface.get_rect ()

    @property
    def image_cache (self):
        return self.__image_cache

    def quit (self):
        self.__is_running = False

    def on_quit (self):
        return False

import pygame


class Game (object):

    def __init__ (self, width, height, title = '', fps_lock = 60):
        pygame.init ()

        self.__surface = pygame.display.set_mode ((width, height))
        self.__fps_lock = fps_lock

        self.__is_running = False
        self.__active_scene = None

        pygame.display.set_caption (title)

    def run (self):
        self.__is_running = True
        clock = pygame.time.Clock ()

        while self.__is_running:
            dt = clock.tick (self.__fps_lock)

            for event in pygame.event.get ():
                if event.type == pygame.QUIT:
                    self.__is_running = not self.on_quit ()
                elif event.type == pygame.KEYDOWN:
                    self.on_key_down(event.key, event)
                elif event.type == pygame.KEYUP:
                    self.on_key_up (event.key, event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_mouse_down (event.pos, event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.on_mouse_up (event.pos, event)

            if self.__active_scene:
                self.__active_scene.update (dt / 1000.0)
                self.__active_scene.draw (self.__surface)

            pygame.display.flip ()

        pygame.quit ()

    def set_active_scene (self, scene):

        if scene:
            if self.__active_scene:
                self.__active_scene.scene_deactivated ()

            self.__active_scene = scene
            self.__active_scene.scene_activated ()


    def on_quit (self):
        return False

    def on_key_down (self, key, event):
        pass

    def on_key_up (self, key, event):
        pass

    def on_mouse_down (self, pos, event):
        pass

    def on_mouse_up (self, pos, event):
        pass
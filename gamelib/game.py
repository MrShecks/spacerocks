from abc import ABC, abstractmethod
import pygame


class Game (ABC):

    _is_running = False

    def __init__ (self, width, height, title = '', fpslock = 60):
        pygame.init ()

        self._canvas = pygame.display.set_mode ((width, height))
        self._fpslock = fpslock

        pygame.display.set_caption (title)

    def run (self):
        self._is_running = True
        clock = pygame.time.Clock ()

        while self._is_running:
            dt = clock.tick (self._fpslock)

            for event in pygame.event.get ():
                if event.type == pygame.QUIT:
                    self._is_running = not self.on_quit ()
                elif event.type == pygame.KEYDOWN:
                    self.on_key_down(event.key, event)
                elif event.type == pygame.KEYUP:
                    self.on_key_up (event.key, event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_mouse_down (event.pos, event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.on_mouse_up (event.pos, event)

            self.update (dt / 1000.0)
            self.draw (self._canvas)

            pygame.display.flip ()

    @abstractmethod
    def update (self, dt):
        pass

    @abstractmethod
    def draw (self, canvas):
        pass

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
from abc import ABC, abstractmethod
import pygame


class Game (ABC):

    _is_running = False

    def __init__ (self, width, height):
        pygame.init ()

        self._screen = pygame.display.set_mode ((width, height))

    def run (self):
        self._is_running = True

        while self._is_running:
            for event in pygame.event.get ():
                if event.type == pygame.QUIT:
                    self._is_running = False


            self.update (0)
            self.draw ()

            self._screen.fill (( 0, 200, 0))

            pygame.display.flip ()

    @abstractmethod
    def update (self, dt):
        pass

    @abstractmethod
    def draw (self):
        pass
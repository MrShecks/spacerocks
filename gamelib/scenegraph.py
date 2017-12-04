from abc import ABC, abstractmethod


class Node (ABC):


    def __init__ (self):
        pass

    @abstractmethod
    def update (self, dt):
        pass

    def draw (self):
        pass

class SceneGraph:


    def __init__ (self):
        pass

    def update (self, dt):
        pass

    def draw (self):
        pass
import pygame

class SceneNode (pygame.sprite.Sprite):


    def __init__ (self, width, height, has_alpha = True):
        super ().__init__ ()

        flags = pygame.SRCALPHA if has_alpha else 0
        self._image = pygame.Surface ((width, height), flags)
        self._rect = self._image.get_rect ()

    @property
    def image (self):
        return self._image

    @property
    def rect (self):
        return self._rect



class SceneSprite (SceneNode):


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


class SceneGraph:


    def __init__ (self):
        self._nodes = pygame.sprite.LayeredUpdates ()

    def add_node (self, node, scene_layer = -1):
        self._nodes.add (node, layer=scene_layer)
        print ('SceneGraph::add_node (): Node=', node, ' Layer=', scene_layer)

    def add_nodes (self, nodes, scene_layer = -1):
        for node in nodes:
            self.add_node (node, scene_layer)

    def update (self, dt):
        self._nodes.update (dt)

    def draw (self, surface):
        self._nodes.draw (surface)
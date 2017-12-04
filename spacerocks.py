import os

from gamelib import game
from gamelib import scenegraph
from gamelib import imagecache
from gamelib import tileset

class Background (scenegraph.SceneNode):

    SCROLL_SPEED = 50

    def __init__ (self, debris, width, height):
        super ().__init__ ()
        self._debris = debris
        self._width = width
        self._height = height
        self._backgrounds = []
        self._current_index = 0
        self._scroll_offset = 0

    def add_background (self, image):
        self._backgrounds.append (image)

    def set_background (self, index):
        if 0 <= index < len (self._backgrounds):
            self._current_index = index

    def update (self, dt):
        self._scroll_offset = (self._scroll_offset + (Background.SCROLL_SPEED * dt)) % self._width

    def draw (self, canvas):
        canvas.blit (self._backgrounds[self._current_index], (0, 0))

        y = (self._height - self._debris.get_height ()) // 2

        canvas.blit (self._debris, (self._scroll_offset, y))
        canvas.blit (self._debris, (self._scroll_offset - self._width, y))


class Ship (scenegraph.SceneNode):


    def __init__ (self, image):
        super ().__init__ ()

        self._tiles = tileset.TileSet (image, 90, 90)
        self._frame = 0

    def draw (self, canvas):
        self._tiles.draw_tile (canvas, 0, 0, self._frame)


class Spacerocks (game.Game):

    WINDOW_TITLE                = 'Space Rocks'
    WINDOW_WIDTH                = 960
    WINDOW_HEIGHT               = 720

    FPS                         = 60

    SCENE_LAYER_BACKGROUND      = 0
    SCENE_LAYER_PLAYER_SHIP     = 1

    IMAGES = {
        'background_01'     : 'Background_01.jpg',
        'background_02'     : 'Background_02.jpg',
        'background_03'     : 'Background_03.jpg',
        'background_04'     : 'Background_04.jpg',
        'background_05'     : 'Background_05.jpg',
        'background_06'     : 'Background_06.jpg',
        'background_07'     : 'Background_07.jpg',
        'background_08'     : 'Background_08.jpg',
        'background_09'     : 'Background_09.jpg',
        'background_10'     : 'Background_10.jpg',
        'background_11'     : 'Background_11.jpg',
        'background_12'     : 'Background_12.jpg',

        'debris'            : 'debris.png',
        'ships'             : 'space_ship.png',
    }

    def __init__ (self):
        super ().__init__ (Spacerocks.WINDOW_WIDTH, Spacerocks.WINDOW_HEIGHT,
                           Spacerocks.WINDOW_TITLE, Spacerocks.FPS)

        assets_path = os.path.join (os.path.dirname (__file__), 'assets')

        self._scene = scenegraph.SceneGraph ()
        self._images = imagecache.ImageCache (os.path.join (assets_path, 'images'))

        for tag, filename in self.IMAGES.items ():
            self._images.add_image (tag, filename)

        self._background = Background (self._images.get_image ('debris'), Spacerocks.WINDOW_WIDTH, Spacerocks.WINDOW_HEIGHT)

        for n in range (1, 12 + 1):
            tag = 'background_%02d' % n
            self._background.add_background (self._images.get_image (tag))


        self._scene.add_node (self._background, Spacerocks.SCENE_LAYER_BACKGROUND)
        self._scene.add_node (Ship (self._images.get_image('ships')), Spacerocks.SCENE_LAYER_PLAYER_SHIP)


        self._background.set_background (6)

    def update (self, dt):
        self._scene.update (dt)

    def draw (self, canvas):
        self._scene.draw (canvas)

    def on_key_down(self, key, event):
        print ('Key Down: Key=', key)

    def on_key_up(self, key, event):
        print ('Key Up: Key=', key)

    def on_quit (self):
        print ('Quitting game')
        return True



if __name__ == "__main__":
    app = Spacerocks ()
    app.run ()




import os

from gamelib import game
from gamelib import scenegraph
from gamelib import imagecache
from gamelib import tileset

class Background (scenegraph.SceneNode):

    SCROLL_SPEED = 50

    def __init__ (self, width, height):
        super ().__init__ ()

        self._width = width
        self._height = height
        self._backgrounds = []
        self._current_index = 0
        self._scroll_offset = 0
        self._foreground = None

    def add_background (self, image):
        self._backgrounds.append (image)

    def set_foreground (self, foreground):
        self._foreground = foreground

    def set_background (self, index):
        if 0 <= index < len (self._backgrounds):
            self._current_index = index

    def update (self, dt):
        self._scroll_offset = (self._scroll_offset + (Background.SCROLL_SPEED * dt)) % self._width

    def draw (self, canvas):
        canvas.blit (self._backgrounds[self._current_index], (0, 0))

        if self._foreground is not None:
            y = (self._height - self._foreground.get_height ()) // 2
            canvas.blit (self._foreground, (self._scroll_offset, y))
            canvas.blit (self._foreground, (self._scroll_offset - self._width, y))


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
        'background_01'     : 'background_01.jpg',
        'background_02'     : 'background_02.jpg',
        'background_03'     : 'background_03.jpg',
        'background_04'     : 'background_04.jpg',
        'background_05'     : 'background_05.jpg',
        'background_06'     : 'background_06.jpg',
        'background_07'     : 'background_07.jpg',
        'background_08'     : 'background_08.jpg',
        'background_09'     : 'background_09.jpg',
        'background_10'     : 'background_10.jpg',
        'background_11'     : 'background_11.jpg',
        'background_12'     : 'background_12.jpg',

        'debris'            : 'debris.png',
        'ships'             : 'space_ship.png',
    }

    def __init__ (self):
        super ().__init__ (Spacerocks.WINDOW_WIDTH, Spacerocks.WINDOW_HEIGHT,
                           Spacerocks.WINDOW_TITLE, Spacerocks.FPS)

        assets_path = os.path.join (os.path.dirname (__file__), 'assets')

        self._scene = scenegraph.SceneGraph ()
        self._images = imagecache.ImageCache (os.path.join (assets_path, 'images'))
        self._background = Background (Spacerocks.WINDOW_WIDTH, Spacerocks.WINDOW_HEIGHT)

        for tag, filename in self.IMAGES.items ():
            image = self._images.add_image (tag, filename)

            if tag.startswith ('background_'):
                self._background.add_background (image)

        self._scene.add_node (self._background, Spacerocks.SCENE_LAYER_BACKGROUND)
        self._scene.add_node (Ship (self._images.get_image('ships')), Spacerocks.SCENE_LAYER_PLAYER_SHIP)

        self._background.set_foreground(self._images.get_image('debris'))
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




from gamelib import game
from gamelib import scenegraph


class Spacerocks (game.Game):

    WINDOW_WIDTH    = 960
    WINDOW_HEIGHT   = 720

    def __init__ (self):
        super ().__init__ (Spacerocks.WINDOW_WIDTH, Spacerocks.WINDOW_HEIGHT)
        self._scene = scenegraph.SceneGraph ()

    def update (self, dt):
        self._scene.update (dt)

        print ("Time =",  dt)

    def draw (self):
        self._scene.draw ()



if __name__ == "__main__":
    app = Spacerocks ()
    app.run ()




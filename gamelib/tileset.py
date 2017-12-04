
class TileSet:


    def __init__ (self, image, tile_width, tile_height):
        self._image = image
        self._tile_width = tile_width
        self._tile_height = tile_height

    def draw_tile (self, canvas, x, y, index):
        if index < self.tile_count ():
            row = index // (self._image.get_width () / self._tile_width)
            col = index % (self._image.get_width () / self._tile_width)

            #print ('Row=', row, 'Col=', col)

            cx = (col * self._tile_width)
            cy = (row * self._tile_height)

            canvas.blit (self._image, (x, y), (cx, cy, self._tile_width, self._tile_height))

            #print ('TileSet::draw_tile (): Index=', index, 'X=', x, 'Y=', y, 'Cx=', cx, 'Cy=', cy)

    def tile_width (self):
        return self._tile_width

    def tile_height (self):
        return self._tile_height

    def tile_count (self):
        return (self._image.get_width () // self._tile_width) * (self._image.get_height () // self._tile_height)
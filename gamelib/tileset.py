

class TileSet:


    def __init__ (self, image, tile_width, tile_height):
        self._tile_width = tile_width
        self._tile_height = tile_height
        self._tiles = []

        for row in range (0, image.get_height () // tile_height):
            for col in range (0, image.get_width () // tile_width):
                tile = image.subsurface ((col * tile_width, row * tile_height, tile_width, tile_height))
                self._tiles.append (tile)


    def draw_tile (self, surface, x, y, index, flags = 0):
        surface.blit (self.get_tile (index), (x, y), None, flags)

    def get_tile (self, index):
        return self.__getitem__ (index)

    def tile_width (self):
        return self._tile_width

    def tile_height (self):
        return self._tile_height

    def count (self):
        return self.__len__ ()

    def __getitem__ (self, index):
        if index < len (self._tiles):
            return self._tiles[index]
        else:
            raise IndexError ('Index is out of range')

    def __len__ (self):
        return len (self._tiles)

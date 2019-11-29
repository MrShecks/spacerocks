class SpriteSheet:

    def __init__(self, image, tile_width, tile_height):
        assert image is not None

        self._tile_width = tile_width
        self._tile_height = tile_height
        self._tiles = []

        for row in range(0, image.get_height() // tile_height):
            for col in range(0, image.get_width() // tile_width):
                tile = image.subsurface((col * tile_width, row * tile_height, tile_width, tile_height))
                self._tiles.append(tile)

    def get_tile(self, index):
        return self.__getitem__(index)

    def tile_width(self):
        return self._tile_width

    def tile_height(self):
        return self._tile_height

    def count(self):
        return self.__len__()

    def __getitem__(self, index):
        return self._tiles.__getitem__(index)

    def __len__(self):
        return self._tiles.__len__()

import os
import abc
import pygame
import gamelib

_DEBUG_ASSET_CACHE = gamelib._DEBUG_ASSETS and True

class AssetCache (abc.ABC):

    """
        AssetCache

        Base class for simple dictionary based asset cache and loading

    """
    def __init__ (self):
        self.__items = dict ()

    def get (self, tag):
        return self.__items.get (tag)

    def load (self, path):

        for filename in os.listdir (path):
            if os.path.isfile (os.path.join(path, filename)):
                item = self._loadfile (path, filename)

                if item:
                    tag = os.path.splitext (filename)[0].lower ()
                    self.__items[tag] = item

                    if _DEBUG_ASSET_CACHE:
                        print ('DBG: AssetCache::load (): Filename=', filename, 'Tag=', tag)

    @abc.abstractmethod
    def _loadfile (self, path, filename):
        """
            Called for each file found while loaded the asset cache. Sub classes must implement this
            method and return the loaded asset or None to skip

            :param path:            File path
            :param filename:        File name
            :return:                Asset (object) or None
        """

        pass


class ImageCache (AssetCache):

    """
        ImageCache

        Asset cache/loader for images (supports PNG and JPEG file types)

    """

    def __init__ (self):
        super ().__init__ ()

    def _loadfile (self, path, filename):
        file_extension = os.path.splitext (filename)[1]
        image = None

        if file_extension in ['.png', '.jpg', '.jpeg']:

            if file_extension == '.png':
                image = pygame.image.load (os.path.join (path, filename)).convert_alpha ()
            else:
                image = pygame.image.load (os.path.join (path, filename)).convert ()

        return image


class AudioCache (AssetCache):

    """
        AudioCache

        Asset cache/loader for audio files

    """

    def __init__ (self):
        super ().__init__ ()

    def _loadfile (self, path, filename):
        file_extension = os.path.splitext (filename)[1]
        sound = None

        if file_extension in ['.wav', '.ogg']:
            sound = pygame.mixer.Sound (os.path.join (path, filename))

        return sound


# TODO: Add TileSetCache (Maybe put all tileset in a sub director of 'images'
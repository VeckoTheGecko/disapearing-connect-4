import pygame
import os


class Model:
    pass


class View:
    """A class that represents the game window and assets"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        pygame.init()

        self.screen = pygame.display.set_mode((width, height))

        return self

    ASSET_FOLDER = "assets"
    asset_locations = {  # Specifying the location of assets in the ASSET_FOLDER
        "board": os.path.join(ASSET_FOLDER, "connect4.png"),
        "tokens": {
            "red": os.path.join(ASSET_FOLDER, "redtoken.png"),
            "yellow": os.path.join(ASSET_FOLDER, "yellowtoken.png"),
            "grey": os.path.join(ASSET_FOLDER, "greytoken.png"),
        },
        "dropclick": os.path.join(ASSET_FOLDER, "drop_click.wav"),
    }
    
    @staticmethod
    def _load_assets(item):
        """A function to turn the asset_locations into a dictionary of pygame assets.
        Takes in a dictionary (or nested dictionaries) containing asset file locations, and returns a dictionary of the same structure with the pygame assets loaded.
        Supports .pmg, .jpg, .wav, .mp3.
        """
        if type(item) == dict:  # Allowing for nested dictionaries using recursion
            asset_dict = {}
            for subitem_key in item.keys:
                asset_dict[subitem_key] = View._load_assets(
                    item[subitem_key]
                )  # recursion
            return asset_dict

        elif type(item) == str:
            if item.endswith(".png") or item.endswith(".jpg"):
                return pygame.image.load(item)  # Loading in image
            elif item.endswith(".mp3") or item.endswith(".wav"):
                pygame.mixer.Sound(item)  # Loading in
            else:
                raise Exception("Unexpected file extension passed to View._load_asset.")
        else:
            raise TypeError(
                "Unexpected type in View._load_asset , must be str or dict."
            )

    assets = _load_assets(asset_locations)


class Controller:
    pass

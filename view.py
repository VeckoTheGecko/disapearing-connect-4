import os
from typing_extensions import final
import pygame

# Helper function for converting asset paths to pygame assets
def load_assets(items):
    """A function to turn the asset_locations into a dictionary of pygame assets.
    Takes in a dictionary (or nested dictionaries) containing asset file locations, and returns a dictionary of the same structure with the pygame assets loaded.
    Supports .png, .jpg, .wav, .mp3.
    """
    if type(items) == dict:  # Allowing for nested dictionaries using recursion
        asset_dict = {}
        for item_key in items.keys():
            asset_dict[item_key] = load_assets(items[item_key])  # recursion
        return asset_dict

    elif type(items) == str:
        if items.endswith(".png") or items.endswith(".jpg"):
            return pygame.image.load(items)  # Loading in image
        elif items.endswith(".mp3") or items.endswith(".wav"):
            return pygame.mixer.Sound(items)  # Loading in
        else:
            raise Exception("Unexpected file extension passed to View._load_asset.")
    else:
        raise TypeError("Unexpected type in View._load_asset , must be str or dict.")


class View:
    """A class that represents the game window and assets"""

    default_font = pygame.font.get_default_font()
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

    # Storing the positions of the rows/cols relative to the original connect 4 board size
    # Going from the top left corner
    root_positions = {
        "col_positions": [24.5, 133, 240.5, 348, 456.5, 563.5, 671.5],
        "row_positions": [40, 153, 264, 377, 486.5, 600],
        "board_size": (800, 700),
        "token_height": 50,
        "header": 100,
        "gutter": 80,
    }

    def __init__(self, width: int = 800, height: int = 700):

        self.width = width
        self.height = height
        self.calculate_transformed_positions()
        pygame.init()
        pygame.display.init()
        pygame.mixer.init()

        self.assets = load_assets(self.asset_locations)
        self.assets["font"] = pygame.font.Font("freesansbold.ttf", 64)

        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE
        )
        pygame.display.set_caption("Disappearing Connect 4")
        pygame.display.set_icon(pygame.image.load("assets/four.png"))

    def update_screen_size(self, dimensions):
        """Updates the screen size."""
        self.width, self.height = dimensions
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE
        )
        self.calculate_transformed_positions()  # Updating the coordinates

    def calculate_transformed_positions(self):
        """Constructing the unscaled positioning of all assets and then scaling them to fit the window
        and be centred."""
        gutter, header = self.root_positions["gutter"], self.root_positions["header"]
        board_dimensions = (  # Dimensions of the current board
            2 * gutter + self.root_positions["board_size"][0],
            2 * gutter + header + self.root_positions["board_size"][1],
        )

        # Calculating the positions of the tokens etc. relative to the board
        transformed_positions = {}
        transformed_positions["col_positions"] = [
            gutter + x for x in self.root_positions["col_positions"]
        ]
        transformed_positions["row_positions"] = [
            gutter + header + y for y in self.root_positions["row_positions"]
        ]

        # Scaling and offseting the coordinates so that they are centred
        final_width = min(self.width, self.height)
        scaling_factor = final_width / board_dimensions[0]  # Aspect ratio is a square

        # Calculates the offset required to centre the object
        offset = (
            (self.width - final_width) / 2,
            (self.height - final_width) / 2,
        )

        transformed_positions["col_positions"] = [
            offset[0] + x * scaling_factor
            for x in transformed_positions["col_positions"]
        ]

        transformed_positions["row_positions"] = [
            offset[1] + y * scaling_factor
            for y in transformed_positions["row_positions"]
        ]

        transformed_positions["board_top_left"] = (
            offset[0] + gutter * scaling_factor,
            offset[1] + (gutter + header) * scaling_factor,
        )

        transformed_positions["token_height"] = (
            offset[1] + (gutter + self.root_positions["token_height"]) * scaling_factor
        )

        transformed_positions["scale"] = scaling_factor
        self.transformed_positions = transformed_positions
        return

    def render_outcome(self, win):
        """
        Renders winning text once the game is finished.
        """
        # Determining the end text
        if win is None:
            text_prerender = "It's a tie!"
        elif win in ["red", "yellow"]:
            text_prerender = f"{win.capitalize()} wins!"

        # Rendering and placing text
        text = self.assets["font"].render(text_prerender, True, (0, 0, 0))
        dimensions = self.assets["font"].size(
            text_prerender
        )  # Getting the dimensions of the text

        final_width = min(self.width, self.height) * 2 / 3
        scale = final_width / dimensions[0]
        final_height = dimensions[1] * scale

        self.render_with_scale(
            text,
            ((self.width - final_width) / 2, (self.height - final_height) / 2),
            scale,
        )
        return

    def play_click(self):
        """
        Plays the click sound of the token landing.
        """
        self.assets["dropclick"].play()
        return

    def render_with_scale(self, asset, pos, scale):
        """Renders an asset at a position with a scale factor applied to width and height"""
        # Calculating the transformed dimensions given the scale factor
        final_dim = (int(asset.get_width() * scale), int(asset.get_height() * scale))
        self.screen.blit(pygame.transform.scale(asset, final_dim), pos)

    def render_token(self, token_color, row, col):
        x = self.transformed_positions["col_positions"][col]
        y = self.transformed_positions["row_positions"][row]

        if token_color == "":
            return
        else:
            self.render_with_scale(
                self.assets["tokens"][token_color],
                (x, y),
                self.transformed_positions["scale"],
            )
            return

    def render_board(self, board, disappearing_mode, in_game, last_two):
        """
        Renders the board onto the screen
        """
        self.screen.fill((255, 255, 255))

        # Rendering all tokens
        for row in range(len(board)):
            for col in range(len(board[row])):
                token_color = board[row][col]
                if (disappearing_mode and in_game) and token_color != "":
                    # changing the color if in disappearing mode (and game is going on)
                    #  and slot is not empty
                    if (row, col) not in last_two:
                        token_color = "grey"
                self.render_token(token_color, row, col)

        # Rendering frame
        self.render_with_scale(
            self.assets["board"],
            self.transformed_positions["board_top_left"],
            self.transformed_positions["scale"],
        )
        return

    def render_placing_token(self, player_position, turn):
        scale = self.transformed_positions["scale"]
        token = self.assets["tokens"][turn]

        # No need to adjust x
        x = self.transformed_positions["col_positions"][player_position]
        y = self.transformed_positions["token_height"] - token.get_height() * scale / 2

        self.render_with_scale(token, (x, y), scale)

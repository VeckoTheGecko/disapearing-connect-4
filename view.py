import os
import pygame

# Helper function
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
    return


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
    col_positions = [24.5, 133, 240.5, 348, 456.5, 563.5, 671.5]
    row_positions = [40, 153, 264, 377, 486.5, 600]

    def __init__(self, width: int = 800, height: int = 700):

        self.width = width
        self.height = height
        pygame.init()
        pygame.display.init()
        pygame.mixer.init()

        self.assets = load_assets(self.asset_locations)
        self.assets["font"] = pygame.font.Font("freesansbold.ttf", 64)

        self.screen = pygame.display.set_mode((width, height))

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
        self.screen.blit(
            text, ((self.width - dimensions[0]) / 2, (self.height - dimensions[1]) / 2)
        )
        return

    def play_click(self):
        """
        Plays the click sound of the token landing.
        """
        self.assets["dropclick"].play()
        return

    def render_token(self, token_color, row, col):
        x = self.col_positions[col]
        y = self.row_positions[row]

        if token_color == "":
            return
        elif token_color == "red":
            self.screen.blit(self.assets["tokens"]["red"], (x, y))
            return
        elif token_color == "yellow":
            self.screen.blit(self.assets["tokens"]["yellow"], (x, y))
            return

    def render_board(self, board):
        """
        Renders the board onto the screen
        """
        self.screen.fill((255, 255, 255))

        # Rendering all tokens
        for row in range(len(board)):
            for col in range(len(board[row])):
                token_color = board[row][col]
                self.render_token(token_color, row, col)

        # Rendering frame
        self.screen.blit(self.assets["board"], (0, 0))
        return


if __name__ == "__main__":
    from model import Model

    v = View()
    m = Model()

    m.place_token("red", 0)
    m.place_token("red", 1)
    m.place_token("red", 2)
    m.place_token("red", 3)
    m.place_token("yellow", 0)
    m.place_token("yellow", 1)
    m.place_token("yellow", 2)
    m.place_token("yellow", 3)

    v.render_board(m.board)
    input()

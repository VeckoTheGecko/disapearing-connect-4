"""
A spin on connect 4 where the only tokens you can see are the last 2 placed, all other tokens are grey.
A game of simple strategy just got a new challenge: memory!

This code was originally written by me a couple years ago, however I wanted to refactor it using MVC architecture.
"""

import pygame
import os

# Helper functions
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
            pygame.mixer.Sound(items)  # Loading in
        else:
            raise Exception("Unexpected file extension passed to View._load_asset.")
    else:
        raise TypeError("Unexpected type in View._load_asset , must be str or dict.")
    return


class Model:
    def __init__(self):
        """
        Initialises the board, which is a 6rows*7cols array of strings.
        """
        self.nrows = 6
        self.ncols = 7
        self.board = [["" for i in range(self.ncols)] for i in range(self.nrows)]

        # Records the last 2 plays, so that they can be rendered properly
        # and everything else can be grey
        self.last_two = [None, None]

    def set_position(self, token, row, col):
        # Places a token in the specified spot
        self.board[row][col] = token
        return

    def record_history(self, row, col):
        self.last_two.pop(0)
        self.last_two.append((row, col))
        return

    def place_token(self, token: str, col: int) -> bool:
        col_is_full, row = self.col_is_full(col, get_row=True)

        if col_is_full:
            # Can't place token
            return False

        else:
            self.set_position(token, row, col)
            self.record_history(row, col)
            return True

    def is_win(self, turn_color, col):
        """
        Checks around the last token placed to see if there is a win.
        It traces back along each direction, then counts number of tokens placed by current player"
        """
        # Finding row of last placed token
        column_values = list(reversed([row[col] for row in self.board]))
        row = column_values.index("")

        # The possible directions connect 4 can occur
        step_directions = {
            "diagonal1": (1, 1),
            "diagonal2": (1, -1),
            "vertical": (1, 0),
            "horizontal": (0, 1),
        }

        for vector in step_directions.values():
            temp_row, temp_col = row, col
            # Trace back
            while True:
                # Check if the next token in the trace back is in range
                in_row_range = 0 <= (temp_row - vector[0]) <= self.nrows - 1
                in_col_range = 0 <= (temp_col - vector[1]) <= self.ncols - 1

                if not (in_row_range and in_col_range):
                    # We have reached the end of the board
                    break

                if self.board[temp_row - vector[0]][temp_col - vector[1]] == turn_color:
                    temp_row -= vector[0]
                    temp_col -= vector[1]
                else:
                    # We have reached the end of the colour chain
                    break

            # Now we count forwards
            connected = 0
            while True:
                # Check if the current token is in range
                in_row_range = 0 <= (temp_row) <= self.nrows - 1
                in_col_range = 0 <= (temp_col) <= self.ncols - 1

                if not (in_row_range and in_col_range):
                    # We have reached the end of the board
                    break

                if self.board[temp_row][temp_col] == turn_color:
                    connected += 1
                    temp_row += vector[0]
                    temp_col += vector[1]
                else:
                    # We have reached the other end of the chain
                    break

            if connected >= 4:
                return True

        # End of loop with no win
        return False

    def col_is_full(self, col: int, get_row: bool = False):
        """Checking from bottom to top of a column
        if there is a space for the token"""
        full_column = True
        for row in range(self.nrows - 1, -1, -1):
            if self.board[row][col] == "":
                full_column = False
                break

        # If the column is full, then the row is meaningless
        if full_column:
            row = None

        if get_row:
            return (full_column, row)
        else:
            return full_column

    def board_is_full(self):
        """
        Determines whether there are any spots on the board to place a token
        """
        full_columns = [self.col_is_full(col) for col in range(self.ncols)]
        return all(full_columns)  # True if all columns are full


class View:
    """A class that represents the game window and assets"""

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

    def __init__(self, width: int = 400, height: int = 400):

        self.width = width
        self.height = height
        pygame.init()
        pygame.mixer.init()

        self.assets = load_assets(self.asset_locations)

        self.screen = pygame.display.set_mode((width, height))


class Controller:
    def __init__(model: Model = Model(), view: View = View()):
        self.model = model
        self.view = view


if __name__ == "__main__":
    view = View(200, 400)
    input()

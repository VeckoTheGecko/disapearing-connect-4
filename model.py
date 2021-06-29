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

        self.player_position = int(self.ncols / 2)

    # Functions for moving around
    def get_position(self):
        """Gets the position of the players cursor"""
        return self.player_position

    def set_position(self, pos):
        """Sets the location of the token the player is about to place."""
        if 0 <= pos <= self.ncols - 1:
            self.player_position = pos
            return True
        return False

    def move_left(self):
        """Moves the players cursor to the left."""
        self.set_position(self.get_position() - 1)
        return

    def move_right(self):
        """Moves the players cursor to the right."""
        self.set_position(self.get_position() + 1)
        return

    # Functions for manipulating the board
    def set_token(self, token, row, col):
        """Places a token at the specified board coordinates"""
        self.board[row][col] = token
        return

    def record_history(self, row, col):
        """Records the last two positions that have been played"""
        self.last_two.pop(0)
        self.last_two.append((row, col))
        return

    def place_token(self, token: str, col: int) -> bool:
        """Places a token in the specified column"""
        if self.col_is_full(col):
            # Can't place token
            return False

        else:
            row = self.get_empty(col)
            self.set_token(token, row, col)
            self.record_history(row, col)
            return True

    def is_win(self, turn_color, col):
        """
        Checks around the last token placed to see if there is a win.
        It traces back along each direction, then counts number of tokens placed by current player"
        """
        # Finding row of last placed token
        row = self.get_top_token(col=col)

        if row is None:  # column must have a token
            raise Exception(
                "is_win expected a token in the column but no token was found"
            )

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

    def get_empty(self, col: int) -> int:
        """Returns the row of the empty spot. None if there is no empty spot"""
        row = None
        for test_row in range(self.nrows - 1, -1, -1):
            if self.board[test_row][col] == "":
                row = test_row
                break
        return row

    def get_top_token(self, col: int) -> int:
        """Returns the row of the topmost token in a column."""
        empty_row = self.get_empty(col)

        if empty_row == (self.nrows - 1):  # ie. the whole column is empty
            return None
        if empty_row is None:  # ie. the whole row is full
            return 0
        if empty_row is not None:  # ie. token is one row below the empty spot
            return empty_row + 1

    def col_is_full(self, col: int):
        """Checking if there is a space for the token"""

        if self.get_empty(col) is None:
            return True
        else:
            return False

    def board_is_full(self):
        """
        Determines whether there are any spots on the board to place a token
        """
        full_columns = [self.col_is_full(col) for col in range(self.ncols)]
        return all(full_columns)  # True if all columns are full


# if __name__ == "__main__":
#     model = Model()
#     model.place_token("yellow", 1)
#     model.place_token("yellow", 2)
#     model.place_token("yellow", 3)
#     model.place_token("yellow", 4)

#     model.is_win("yellow", 3)

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
        _, row = self.col_is_full(col=col, get_row=True)
        row += 1  # Row was the row of the empty spot, now its the full spot

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


# if __name__ == "__main__":
#     model = Model()
#     model.place_token("yellow", 1)
#     model.place_token("yellow", 2)
#     model.place_token("yellow", 3)
#     model.place_token("yellow", 4)

#     model.is_win("yellow", 3)

import unittest
from model import Model


class TestBoardLogic(unittest.TestCase):
    def setUp(self):
        self.model = Model()
        return

    def test_place_token(self):
        for column in (5, 4):
            # Tests placing tokens to capacity in two different columns
            for i in range(self.model.nrows):
                self.assertTrue(self.model.place_token("red", column))

            # Can't place anymore tokens
            self.assertFalse(self.model.place_token("red", column))
        return

    def test_get_empty(self):
        nrows = self.model.nrows

        for row_count in range(self.model.nrows):
            self.assertTrue(self.model.get_empty(0) == (nrows - 1) - row_count)
            self.model.place_token("yellow", 0)

        self.assertTrue(self.model.get_empty(0) is None)

        return

    def test_get_top_token(self):
        nrows = self.model.nrows
        self.assertTrue(self.model.get_top_token(0) is None)

        for row_count in range(self.model.nrows):
            self.model.place_token("yellow", 0)
            self.assertTrue(self.model.get_top_token(0) == (nrows - 1) - row_count)

        return

    def test_col_is_full(self):
        for _ in range(self.model.nrows - 1):
            self.model.place_token("yellow", 0)
            self.model.place_token("yellow", 1)

        self.assertFalse(self.model.col_is_full(0))
        self.assertFalse(self.model.col_is_full(0))

        self.model.place_token("yellow", 0)
        self.model.place_token("yellow", 1)
        self.assertTrue(self.model.col_is_full(0))
        self.assertTrue(self.model.col_is_full(1))

    def test_board_is_full(self):
        for _ in range(self.model.nrows):
            for col in range(self.model.ncols - 1):
                self.model.place_token("yellow", col)

        self.assertFalse(self.model.board_is_full())

        for _ in range(self.model.nrows):
            self.model.place_token("yellow", self.model.ncols - 1)

        self.assertTrue(self.model.board_is_full())

    def test_is_win(self):
        # self.model.place_token("yellow", 0)
        # self.model.place_token("yellow", 0)
        # self.model.place_token("yellow", 0)

        # self.model.place_token("red", 1)
        # self.model.place_token("red", 1)
        # self.model.place_token("red", 1)

        # self.model.place_token("yellow", 0)
        # self.assertTrue(self.model.is_win("yellow", 0))

        # self.model.place_token("yellow", 1)
        # self.assertFalse(self.model.is_win("yellow", 1))

        # Checking horizontal win detection
        self.setUp()
        self.model.place_token("yellow", 1)
        self.model.place_token("yellow", 2)
        self.model.place_token("yellow", 3)
        self.assertFalse(self.model.is_win("yellow", 3))
        self.model.place_token("yellow", 4)

        self.assertTrue(self.model.is_win("yellow", 1))
        self.assertTrue(self.model.is_win("yellow", 2))
        self.assertTrue(self.model.is_win("yellow", 3))
        self.assertTrue(self.model.is_win("yellow", 4))

        return

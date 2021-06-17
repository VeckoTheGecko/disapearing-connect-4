import unittest
from main import Model


class TestBoardLogic(unittest.TestCase):
    def setUp(self):
        self.model = Model()

        self.model.place_token("yellow", 0)
        self.model.place_token("yellow", 0)
        self.model.place_token("yellow", 0)

        self.model.place_token("red", 1)
        self.model.place_token("red", 1)
        self.model.place_token("red", 1)
        return

    def test_place_token(self):
        for column in (5, 4):
            # Tests placing tokens to capacity in two different columns
            for i in range(self.model.nrows):
                self.assertTrue(self.model.place_token("red", column))

            # Can't place anymore tokens
            self.assertFalse(self.model.place_token("red", column))
        return

    def test_is_win(self):

        self.model.place_token("yellow", 0)
        self.assertTrue(self.model.is_win("yellow", 0))

        self.model.place_token("yellow", 1)
        self.assertFalse(self.model.is_win("yellow", 1))

        # Checking horizontal win detection
        self.setUp()
        self.model.place_token("yellow", 1)
        self.model.place_token("yellow", 2)
        self.model.place_token("yellow", 3)
        self.assertFalse(self.model.is_win("yellow", 3))
        self.model.place_token("yellow", 4)
        self.assertTrue(self.model.is_win("yellow", 4))

        return

import unittest
from copy import deepcopy

from ai import new_find_move
from logic import build_game, draw, move

game = build_game(False)


class Test(unittest.TestCase):
    def test_new_find_move_new_game(self):
        self.assertEqual(new_find_move(game), -1)

    def test_new_find_move_tableau_to_foundation(self):
        _game = deepcopy(game)
        _game.stock, _game.pile = draw(_game.stock, _game.pile)
        self.assertTupleEqual(new_find_move(_game), (2, 1, 2, 1))

    # def test_new_find_move_big_boi(self):
    #     _game = deepcopy(game)
    #     self.assertEqual(new_find_move(_game), -1)
    #     _game.stock, _game.pile = draw(_game.stock, _game.pile)
    #     self.assertTupleEqual(new_find_move(_game), (2, 1, 2, 1))


if __name__ == "__main__":
    unittest.main()

import unittest
from logic import Card, build_game, draw, move, check_move, SUITS


_SUITS = {'h': SUITS[0], 'd': SUITS[1], 's': SUITS[2], 'c': SUITS[3]}


class CardTest(unittest.TestCase):

    def test_card_repr(self):
        card = Card(1, 'h')
        self.assertEqual(str(card), ' 1h')


class KlondikeTest(unittest.TestCase):

    def test_build_game(self):
        pass

    def test_draw(self):
        stock = [Card(1, 'h'), Card(2, 'h'), Card(3, 'h'), Card(4, 'h')]
        pile = [Card(5, 'h')]
        _stock, _pile = draw(stock, pile)
        self.assertEqual((len(stock), len(pile)), (len(_pile), len(_stock)))

    def test_check_move(self):
        h1 = Card(1, _SUITS['h'])
        h2 = Card(2, _SUITS['h'])
        s1 = Card(1, _SUITS['s'])
        s2 = Card(2, _SUITS['s'])
        self.assertTrue(check_move(h1, [s2]))
        self.assertTrue(check_move(s1, [h2]))
        self.assertFalse(check_move(h1, [s1]))
        self.assertFalse(check_move(h1, [h2]))
        self.assertTrue(check_move(h1, [], to_foundation=True))
        self.assertTrue(check_move(h2, [h1], to_foundation=True))


if __name__ == "__main__":
    unittest.main()

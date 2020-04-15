import unittest
from logic import Card, Klondike, build_game, draw, move


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


if __name__ == "__main__":
    unittest.main()

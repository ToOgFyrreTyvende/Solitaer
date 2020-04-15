import unittest
from logic import Card, Klondike, build_game, draw, move


class CardTest(unittest.TestCase):

    def test_repr(self):
        card = Card(1, 'h')
        self.assertEqual(str(card), '| 1h|')


class KlondikeTest(unittest.TestCase):

    def draw_test(self):
        stock = [Card(1, 'h'), Card(2, 'h'), Card(3, 'h'), Card(4, 'h')]
        pile = [Card(5, 'h')]
        result = draw(stock, pile)
        self.assertEqual((stock[:1], pile.append(stock[1:])), result)

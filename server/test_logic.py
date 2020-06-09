from functools import partial
from typing import List, Dict, Tuple

import pytest

from logic import Card, Klondike, draw, move, check_move, SUITS

FlippedCard = partial(Card, flipped=True)

# cards = {
#     'h1': Card(1, SUITS['h']),
#     'h2': Card(2, SUITS['h']),
#     'h3': Card(3, SUITS['h']),
#     'h4': Card(4, SUITS['h']),
#     'h5': Card(5, SUITS['h']),
#     'hk': Card(13, SUITS['h']),
#     's1': Card(1, SUITS['s']),
#     's2': Card(2, SUITS['s'])
# }

h1 = Card(1, SUITS['h'])
h2 = Card(2, SUITS['h'])
h3 = Card(3, SUITS['h'])
h4 = Card(4, SUITS['h'])
h5 = Card(5, SUITS['h'])
hk = Card(13, SUITS['h'])
s1 = Card(1, SUITS['s'])
s2 = Card(2, SUITS['s'])


@pytest.mark.parametrize('card, expected', [
    (Card(1, SUITS['h']), f" 1{SUITS['h']}"),
    (Card(10, SUITS['d']), f"10{SUITS['d']}"),
    (Card(13, SUITS['s']), f"13{SUITS['s']}"),
    (Card(9, SUITS['c']), f" 9{SUITS['c']}")
])
def test_card_repr(card: Card, expected: str):
    assert repr(card) == expected


@pytest.mark.parametrize('exp_stock, exp_pile_len, exp_tableaus, exp_found_lens', [
    (Card(1, SUITS['h'], True),
     0,
     [FlippedCard(7, SUITS['h']), Card(7, SUITS['d']), Card(7, SUITS['c']), Card(8, SUITS['s']), Card(9, SUITS['s']), Card(10, SUITS['c']), Card(12, SUITS['d'])],
     0)
])
def test_build_game(exp_stock: Card, exp_pile_len: int, exp_tableaus: list, exp_found_lens: int):  # 'exp' short for 'expected'
    game_no_shuffle = Klondike.new_game(False)

    assert game_no_shuffle.stock[0] == exp_stock
    assert len(game_no_shuffle.pile) == exp_pile_len
    for i, card in enumerate(exp_tableaus):
        assert game_no_shuffle.tableaus[i][0] == card
    for foundation in game_no_shuffle.foundations:
        assert len(foundation) == exp_found_lens

    assert isinstance(game_no_shuffle.stock, list)
    assert isinstance(game_no_shuffle.pile, list)
    assert isinstance(game_no_shuffle.tableaus, list)
    assert isinstance(game_no_shuffle.foundations, list)


@pytest.mark.parametrize('exp_stock_len, exp_pile_len, exp_tableau_lens, exp_found_lens', [
    (24, 0, list(range(1, 8)), 0)
])
def test_klondike_new_game(exp_stock_len: int, exp_pile_len: int, exp_tableau_lens: List[int], exp_found_lens: int):  # 'exp' short for 'expected'
    game_no_shuffle = Klondike.new_game(False)

    assert len(game_no_shuffle.stock) == exp_stock_len
    assert len(game_no_shuffle.pile) == exp_pile_len
    for i, tableau in enumerate(game_no_shuffle.tableaus):
        assert len(tableau) == exp_tableau_lens[i]
    for foundation in game_no_shuffle.foundations:
        assert len(foundation) == exp_found_lens

    assert isinstance(game_no_shuffle.stock, list)
    assert isinstance(game_no_shuffle.pile, list)
    assert isinstance(game_no_shuffle.tableaus, list)
    assert isinstance(game_no_shuffle.foundations, list)


@pytest.mark.parametrize('stock, pile, exp_lens', [
    ([Card(1, 'h'), Card(2, 'h'), Card(3, 'h'), Card(4, 'h')], [Card(5, 'h')], {'stock': 1, 'pile': 4}),
    ([Card(1, 'h'), Card(2, 'h')], [Card(3, 'h')], {'stock': 0, 'pile': 3}),
    ([], [Card(1, 'h'), Card(2, 'h'), Card(3, 'h'), Card(4, 'h')], {'stock': 4, 'pile': 0})
])
def test_draw(stock: List[Card], pile: List[Card], exp_lens: Dict[str, int]):
    _stock, _pile = draw(stock, pile, nb_cards=3)

    assert len(_stock) == exp_lens['stock']
    assert len(_pile) == exp_lens['pile']


@pytest.mark.parametrize('card_from, card_to, to_foundation, expected', [
    (h1, [s2], False, True),
    (s1, [h2], False, True),
    (h1, [s1], False, False),
    (h1, [h2], False, False),
    (h2, [h1], True, True),
    (h1, [], True, True),
    (hk, [], False, True)
])
def test_check_move(card_from: Card, card_to: List[Card], to_foundation: bool, expected: bool):
    assert check_move(card_from, card_to, to_foundation=to_foundation) == expected


@pytest.mark.parametrize('card_pos, pile_from, pile_to, expected', [
    (1, [h1, h2, h3, h4], [h5], ([h1, h2, h3], [h5, h4])),
    (1, [s2, h1], [], ([s2], [h1]))
])
def test_move(card_pos: int, pile_from: List[Card], pile_to: List[Card], expected: Tuple[List[Card], List[Card]]):
    assert expected == move(card_pos, pile_from, pile_to)


if __name__ == "__main__":
    pytest.main()

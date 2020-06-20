from copy import deepcopy
from typing import Union, Tuple

import pytest

from ai import MOVE_CODE, new_find_move, find_move_wrapper
from logic import draw, move, Klondike, get_card_at, Card


def build_test_games() -> Tuple[Klondike, Klondike, Klondike, Klondike]:
    # No games are shuffled, to avoid random stuff
    game2 = Klondike.new_game(False)
    game2.stock, game2.pile = draw(game2.stock, game2.pile)

    game4 = deepcopy(game2)
    game4.tableaus[1], game4.tableaus[2] = move(1, game4.tableaus[1], game4.tableaus[2])
    game4.tableaus[3], game4.tableaus[4] = move(1, game4.tableaus[3], game4.tableaus[4])
    game4.tableaus[5], game4.tableaus[6] = move(1, game4.tableaus[5], game4.tableaus[6])
    game4.tableaus[5], game4.tableaus[6] = move(1, game4.tableaus[5], game4.tableaus[6])

    game3 = deepcopy(game4)
    game3.pile, game3.tableaus[2] = move(1, game3.pile, game3.tableaus[2])
    game3.pile, game3.tableaus[0] = move(1, game3.pile, game3.tableaus[0])
    game3.pile, game3.tableaus[1] = move(1, game3.pile, game3.tableaus[1])
    game3.stock, game3.pile = draw(game3.stock, game3.pile)
    game3.pile, game3.tableaus[2] = move(1, game3.pile, game3.tableaus[2])
    game3.stock, game3.pile = draw(game3.stock, game3.pile)
    game3.stock, game3.pile = draw(game3.stock, game3.pile)
    game3.pile, game3.tableaus[2] = move(1, game3.pile, game3.tableaus[2])
    game3.stock, game3.pile = draw(game3.stock, game3.pile)
    game3.stock, game3.pile = draw(game3.stock, game3.pile)
    game3.stock, game3.pile = draw(game3.stock, game3.pile)

    game1 = deepcopy(game3)
    game1.pile, game1.foundations[0] = move(1, game1.pile, game1.foundations[0])
    game1.stock, game1.pile = draw(game1.stock, game1.pile)
    game1.pile, game1.foundations[1] = move(1, game1.pile, game1.foundations[1])
    game1.pile, game1.foundations[2] = move(1, game1.pile, game1.foundations[2])
    game1.pile, game1.foundations[3] = move(1, game1.pile, game1.foundations[3])
    game1.pile, game1.foundations[1] = move(1, game1.pile, game1.foundations[1])
    game1.pile, game1.foundations[2] = move(1, game1.pile, game1.foundations[2])
    game1.pile, game1.foundations[3] = move(1, game1.pile, game1.foundations[3])
    game1.pile, game1.foundations[0] = move(1, game1.pile, game1.foundations[0])
    game1.pile, game1.foundations[1] = move(1, game1.pile, game1.foundations[1])

    return game2, game4, game3, game1


game_after_draw, g_move4, g_move3, g_move1 = build_test_games()

game5 = Klondike()
game5.tableaus[0] = [Card.from_str('As')]

@pytest.mark.parametrize('game, expected', [
    (Klondike.new_game(), (MOVE_CODE.DRAW,)),
    (game_after_draw, (MOVE_CODE.T_TO_T, 1, 2, 1)),
    (g_move4, (MOVE_CODE.P_TO_T, 2)),
    (g_move3, (MOVE_CODE.P_TO_F, 0)),
    (g_move1, (MOVE_CODE.T_TO_F, 2, 1)),
    (game5, (MOVE_CODE.T_TO_F, 0, 0))
])
def test_new_find_move(game: Klondike, expected: Union[int, Tuple[int, int], Tuple[int, int, int], Tuple[int, int, int, int]]):
    assert new_find_move(game) == expected


def wrapper_dict_builder(kind: str = 'MOVE', move_to: str = None, move_from: str = None):
    return {'kind': kind, 'move': {'to': move_to, 'from': move_from}}


@pytest.mark.parametrize('game, expected', [
    (Klondike.new_game(), wrapper_dict_builder(kind='DRAW')),
    (game_after_draw, wrapper_dict_builder(move_from=get_card_at(game_after_draw.tableaus[1]),
                                           move_to=get_card_at(game_after_draw.tableaus[2]))),
    (g_move4, wrapper_dict_builder(move_from=get_card_at(g_move4.pile),
                                   move_to=get_card_at(g_move4.tableaus[2]))),
    (g_move3, wrapper_dict_builder(move_from=get_card_at(g_move3.pile),
                                   move_to=get_card_at(g_move3.foundations[0]))),
    (g_move1, wrapper_dict_builder(move_from=get_card_at(g_move1.tableaus[2]),
                                   move_to=get_card_at(g_move1.foundations[1])))
])
def test_find_move_wrapper(game: Klondike, expected: Union[int, Tuple[int, int], Tuple[int, int, int], Tuple[int, int, int, int]]):
    assert find_move_wrapper(game) == expected


if __name__ == "__main__":
    pytest.main()

import random
from copy import deepcopy
from typing import Union, Tuple, Dict, Optional

import pytest

from ai import MOVE_CODE, new_find_move, find_move_wrapper, game_won
from logic import draw, move, Klondike, get_card_at, Card

# Custom types
Move = Union[int, Tuple[int, int], Tuple[int, int, int], Tuple[int, int, int, int]]
WrappedMove = Dict[str, Union[str, Dict[str, Optional[str]]]]


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


g_move_tt, g_move_pt, g_move_pf, g_move_tf = build_test_games()

g_ace_to_f = Klondike()
g_ace_to_f.tableaus[0].append(Card.from_str('As'))

complete_game = Klondike()
for foundation in complete_game.foundations:
    foundation.append(Card(13, '_'))


@pytest.mark.parametrize('game, expected', [
    (Klondike.new_game(), False),
    (complete_game, True),
])
def test_game_won(game: Klondike, expected: bool):
    assert game_won(game) == expected


@pytest.mark.parametrize('game, expected', [
    (Klondike.new_game(), (MOVE_CODE.DRAW,)),
    (g_move_tt, (MOVE_CODE.T_TO_T, 1, 2, 1)),
    (g_move_pt, (MOVE_CODE.P_TO_T, 2)),
    (g_move_pf, (MOVE_CODE.P_TO_F, 0)),
    (g_move_tf, (MOVE_CODE.T_TO_F, 2, 1)),
    (g_ace_to_f, (MOVE_CODE.T_TO_F, 0, 0))
])
def test_new_find_move(game: Klondike, expected: Move):
    assert new_find_move(game) == expected


def wrapper_dict_builder(kind: str = 'MOVE', move_to: str = None, move_from: str = None) -> WrappedMove:
    return {'kind': kind, 'move': {'to': move_to, 'from': move_from}}


@pytest.mark.parametrize('game, expected', [
    (Klondike.new_game(), wrapper_dict_builder(kind='DRAW')),
    (g_move_tt, wrapper_dict_builder(kind='TT',
                                     move_from=get_card_at(g_move_tt.tableaus[1]),
                                     move_to=get_card_at(g_move_tt.tableaus[2]))),
    (g_move_pt, wrapper_dict_builder(kind='PT',
                                     move_from=get_card_at(g_move_pt.pile),
                                     move_to=get_card_at(g_move_pt.tableaus[2]))),
    (g_move_pf, wrapper_dict_builder(kind='PF',
                                     move_from=get_card_at(g_move_pf.pile),
                                     move_to=get_card_at(g_move_pf.foundations[0]))),
    (g_move_tf, wrapper_dict_builder(kind='TF',
                                     move_from=get_card_at(g_move_tf.tableaus[2]),
                                     move_to=get_card_at(g_move_tf.foundations[1]))),
    (g_ace_to_f, wrapper_dict_builder(kind='TF',
                                      move_from=get_card_at(g_ace_to_f.tableaus[0]),
                                      move_to=get_card_at(g_ace_to_f.foundations[0])))
])
def test_find_move_wrapper(game: Klondike, expected: WrappedMove):
    assert find_move_wrapper(game) == expected


def test_winrate():
    wins: int = 0
    random.seed(21522)

    for i in range(1000):
        g = Klondike.new_game()
        consecutive_draws = 0
        while not game_won(g) and consecutive_draws < 24:
            code, *instr = new_find_move(g)
            if code == MOVE_CODE.DRAW:
                consecutive_draws += 1
                g.stock, g.pile = draw(g.stock, g.pile, nb_cards=1)
            elif code == MOVE_CODE.T_TO_F:
                consecutive_draws = 0
                g.tableaus[instr[0]], g.foundations[instr[1]] = move(1, g.tableaus[instr[0]], g.foundations[instr[1]])
            elif code == MOVE_CODE.T_TO_T:
                consecutive_draws = 0
                g.tableaus[instr[0]], g.tableaus[instr[1]] = move(instr[2], g.tableaus[instr[0]], g.tableaus[instr[1]])
            elif code == MOVE_CODE.P_TO_F:
                consecutive_draws = 0
                g.pile, g.foundations[instr[0]] = move(1, g.pile, g.foundations[instr[0]])
            elif code == MOVE_CODE.P_TO_T:
                consecutive_draws = 0
                g.pile, g.tableaus[instr[0]] = move(1, g.pile, g.tableaus[instr[0]])
        if game_won(g): wins += 1
    assert wins > 290


if __name__ == "__main__":
    pytest.main(args=['test_ai.py', '-vv'])


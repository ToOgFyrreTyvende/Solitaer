from typing import List, Tuple, Union, Dict
from enum import IntEnum

from logic import print_game, move, draw, Klondike, check_move, Card, get_card_at


class MOVE_CODE(IntEnum):
    ERROR:  int = -1
    DRAW:   int = 0
    T_TO_F: int = 1
    T_TO_T: int = 2
    P_TO_F: int = 3
    P_TO_T: int = 4


def get_nr_of_flipped(tableau: List[Card]) -> int:
    result = 0
    for card in tableau:
        if card.flipped:
            result += 1
    return result


def game_won(g: Klondike):
    for foundation in g.foundations:
        if not len(foundation) or foundation[-1].value != 13: return False
    return True


def new_find_move(g: Klondike) -> Union[Tuple[int], Tuple[int, int], Tuple[int, int, int], Tuple[int, int, int, int]]:
    """Finds a valid move in the given game

    Return value is dynamic, first int is a code:
     0: draw
     1: tableau -> foundation => (code, tableau_id   , foundation_id)
     2: tableau -> tableau    => (code, tableau_id   , tableau_id   , number of cards)
     3: pile    -> foundation => (code, foundation_id)
     4: pile    -> tableau    => (code, tableau_id)

    If a valid move exists, it returns an int and two card piles.
    The int specifies the index from the first list to move to the other list
    If no valid move is found, it returns a tuple with the draw code (int): 0
    """

    # Draw cards if the pile is empty and there are cards in the stock
    if len(g.pile) == 0 and len(g.stock) != 0:
        return MOVE_CODE.DRAW,

    # Check tableaus for possible moves
    for from_id, from_tableau in enumerate(g.tableaus):
        if len(from_tableau) == 0: continue  # Skip
        for f_id, foundation in enumerate(g.foundations):
            if check_move(from_tableau[-1], foundation, to_foundation=True):
                return MOVE_CODE.T_TO_F, from_id, f_id  # code 1
        for to_id, to_tableau in enumerate(g.tableaus):
            nb_flipped = get_nr_of_flipped(from_tableau)
            if from_tableau[-nb_flipped] == from_tableau[0] and from_tableau[0].value == 13: continue
            if check_move(from_tableau[-nb_flipped], to_tableau):
                return MOVE_CODE.T_TO_T, from_id, to_id, nb_flipped  # code 2

    # Check pile for possible moves
    if len(g.pile):
        for f_id, foundation in enumerate(g.foundations):
            if check_move(g.pile[-1], foundation, to_foundation=True):
                return MOVE_CODE.P_TO_F, f_id  # code 3
        for to_id, tableau in enumerate(g.tableaus):
            if check_move(g.pile[-1], tableau):
                return MOVE_CODE.P_TO_T, to_id  # code 4

    return MOVE_CODE.DRAW,  # No other options matched, give up


def find_move_wrapper(g: Klondike) -> Dict[str, Union[str, Dict[str, Union[str, None]]]]:
    """Translates the 'new_find_move' functions results to something the client side understands!

    returns a dict such as this:
    >>> find_move_wrapper(Klondike.new_game())
    {'kind': 'MOVE', 'move': {'to': 'Ks', 'from': 'Qh'}}
    (If the function recommends moving a red queen to a black king that is...)
    """
    response: Dict[str, Union[str, Dict[str, Union[str, None]]]]
    response = {'kind': None, 'move': {'to': None, 'from': None}}

    code, *instr = new_find_move(g)
    if code == MOVE_CODE.ERROR:
        response['kind'] = 'ERROR'
    elif code == MOVE_CODE.DRAW:
        response['kind'] = 'DRAW'
    elif code == MOVE_CODE.T_TO_F:
        response['kind'] = 'TF'
        response['move']['from'] = get_card_at(g.tableaus[instr[0]])
        response['move']['to'] = get_card_at(g.foundations[instr[1]])
    elif code == MOVE_CODE.T_TO_T:
        response['kind'] = 'TT'
        response['move']['from'] = get_card_at(g.tableaus[instr[0]], index=-instr[2])
        response['move']['to'] = get_card_at(g.tableaus[instr[1]])
    elif code == MOVE_CODE.P_TO_F or code == MOVE_CODE.P_TO_T:
        response['kind'] = 'PF' if code == MOVE_CODE.P_TO_F else 'PT'
        response['move']['from'] = get_card_at(g.pile)
        response['move']['to'] = get_card_at(g.foundations[instr[0]]) if code == MOVE_CODE.P_TO_F else get_card_at(g.tableaus[instr[0]])

    return response


def main():
    g = Klondike.new_game(False)
    print_game(g); print()
    game_state = 'Won'

    while not game_won(g):
        code, *instr = new_find_move(g)
        print(f'Code: {code!s}, instr: {instr}')
        if code == MOVE_CODE.DRAW:
            g.stock, g.pile = draw(g.stock, g.pile)
        elif code == MOVE_CODE.T_TO_F:
            g.tableaus[instr[0]], g.foundations[instr[1]] = move(1, g.tableaus[instr[0]], g.foundations[instr[1]])
        elif code == MOVE_CODE.T_TO_T:
            g.tableaus[instr[0]], g.tableaus[instr[1]] = move(instr[2], g.tableaus[instr[0]], g.tableaus[instr[1]])
        elif code == MOVE_CODE.P_TO_F:
            g.pile, g.foundations[instr[0]] = move(1, g.pile, g.foundations[instr[0]])
        elif code == MOVE_CODE.P_TO_T:
            g.pile, g.tableaus[instr[0]] = move(1, g.pile, g.tableaus[instr[0]])
        elif code == MOVE_CODE.ERROR:
            print('Cannot find any valid moves!')
            game_state = 'Over'
            break
        print_game(g)
        print()
    print(f'Game {game_state}')


if __name__ == "__main__":
    main()

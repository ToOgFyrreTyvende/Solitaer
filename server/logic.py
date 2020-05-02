from __future__ import annotations

import random
from dataclasses import dataclass, field
from itertools import zip_longest
from typing import List, Tuple

# Constants
# SUITS = ['hearts', 'diamonds', 'spades', 'clubs']
# SUITS = ['h', 'd', 's', 'c']
SUITS = ['♡', '♢', '♠', '♣']


@dataclass
class Card:
    value: int
    suit: str
    flipped: bool = False

    @property
    def is_black(self):
        return self.suit in SUITS[2:]

    def __repr__(self):
        """Card representation"""
        return f'{self.value:2}{self.suit}'

    @staticmethod
    def from_str(string: str) -> Card:
        name_values = {'K': 13, 'Q': 12, 'J': 11, 'A': 1}
        if len(string) == 3:
            return Card(value=10, suit=string[-1])
        elif string[0] in name_values.keys():
            return Card(value=name_values[string[0]], suit=string[-1])
        else:
            return Card(value=int(string[0]), suit=string[-1])


@dataclass
class Klondike:
    stock: List[Card] = None
    pile: List[Card] = None
    tableau1: List[Card] = None
    tableau2: List[Card] = None
    tableau3: List[Card] = None
    tableau4: List[Card] = None
    tableau5: List[Card] = None
    tableau6: List[Card] = None
    tableau7: List[Card] = None
    foundation1: List[Card] = field(default_factory=list)
    foundation2: List[Card] = field(default_factory=list)
    foundation3: List[Card] = field(default_factory=list)
    foundation4: List[Card] = field(default_factory=list)
    tableaus: List[List[Card]] = None
    foundations: List[List[Card]] = None


DEFAULT_DECK = [Card(value, suit) for value in range(1, 14) for suit in SUITS]


def build_game(shuffle: bool = True) -> Klondike:
    _deck = [Card(value, suit) for value in range(1, 14) for suit in SUITS]
    if shuffle: random.shuffle(_deck)
    game = Klondike()
    game.stock = _deck[:24]
    for card in game.stock: card.flipped = True
    game.pile = []

    game.tableau1 = _deck[24:25]; game.tableau1[-1].flipped = True
    game.tableau2 = _deck[25:27]; game.tableau2[-1].flipped = True
    game.tableau3 = _deck[27:30]; game.tableau3[-1].flipped = True
    game.tableau4 = _deck[30:34]; game.tableau4[-1].flipped = True
    game.tableau5 = _deck[34:39]; game.tableau5[-1].flipped = True
    game.tableau6 = _deck[39:45]; game.tableau6[-1].flipped = True
    game.tableau7 = _deck[45:52]; game.tableau7[-1].flipped = True

    game.foundations = [game.foundation1, game.foundation2, game.foundation3, game.foundation4]
    game.tableaus = [game.tableau1, game.tableau2, game.tableau3, game.tableau4, game.tableau5, game.tableau6, game.tableau7]

    return game


def draw(stock: List[Card], pile: List[Card], nb_cards: int = 3) -> Tuple[List[Card], List[Card]]:
    _stock = [card for card in stock]
    _pile = [card for card in pile]

    if len(stock) == 0:
        _stock = list(reversed(pile))
        _pile = []
    elif len(stock) >= 3:
        for i in range(3):
            _pile.append(_stock.pop(-1))
    else:
        for i in range(len(stock)):
            _pile.append(_stock.pop(-1))

    return _stock, _pile


def move(card_pos: int, stack_from: List[Card], stack_to: List[Card]) -> Tuple[List[Card], List[Card]]:
    _from = [card for card in stack_from]
    _to = [card for card in stack_to]

    for i in range(-card_pos, 0):
        _to.append(_from.pop(i))
        if len(_from) > 0:
            _from[-1].flipped = True

    return _from, _to


def check_move(card: Card, target: List[Card], to_foundation: bool = False) -> bool:
    """Checks if it is legal to move 'card' to 'target'."""
    if not isinstance(card, Card) and not isinstance(target, List): raise TypeError
    if len(target) == 0:
        if to_foundation: return card.value == 1
        else: return card.value == 13

    if to_foundation: return card.suit == target[-1].suit and card.value == target[-1].value + 1
    else: return card.is_black != target[-1].is_black and card.value == target[-1].value - 1


def _print_helper(base_stack: List[Card], tableau: List[Card]) -> str:
    return f''


def _foundation_str(foundation: List[Card]) -> str:
    return f'|{foundation[-1]}|' if len(foundation) > 0 else '|   |'


def _tableau_str(tableau: List[Card]) -> str:
    result = ''
    for card in tableau:
        result += f'|{card}' if card.flipped else '|###'
    return result + '|'


def print_game(game: Klondike) -> None:
    for i, (foundation, tableau) in enumerate(zip_longest(game.foundations, reversed(game.tableaus))):
        left = _foundation_str(foundation) if foundation is not None else '     '
        right = _tableau_str(tableau)
        if i == 5 and len(game.pile) != 0:
            left = f'|{game.pile[-1]}|'
        elif i == 6:
            left = '|###|' if len(game.stock) > 0 else '|   |'
        print(f'{left}\t{right}')

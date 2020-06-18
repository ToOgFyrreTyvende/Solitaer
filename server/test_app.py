import os
from typing import Dict

import cv2
import numpy as np
import pytest

from ai import find_move_wrapper
from card_detector.yolodetector import new_extract_cards_from_image
from logic import Klondike, Card, print_game

dirname = os.path.dirname(__file__)
card_detector_dir = os.path.join(dirname, 'card_detector')
images = ['dui.png', 'cards2.jpg', 'cards3.jpg', 'cards4.jpg', 'cards5.jpg']
images = [os.path.join(card_detector_dir, item) for item in images]


@pytest.mark.parametrize('img, expected', [
    (cv2.imread(images[0]), {'kind': 'MOVE', 'move': {'to': None, 'from': None}})
])
def test_find_move_wrapper(img: np.ndarray, expected: Dict):
    (img_pile, img_founds, img_tableaus) = new_extract_cards_from_image(img)
    img_pile = img_pile[0]

    game = Klondike()
    game.pile = [Card.from_str(card) for card in img_pile]
    game.foundations = [[Card.from_str(card) for card in lst] for lst in img_founds]
    game.tableaus = [[Card.from_str(card) for card in lst] for lst in img_tableaus]
    print_game(game)

    next_move = find_move_wrapper(game)

    assert next_move == expected


if __name__ == '__main__':
    pytest.main()
    # test_find_move_wrapper(cv2.imread(images[0]), {'kind': 'MOVE', 'move': {'to': None, 'from': None}})

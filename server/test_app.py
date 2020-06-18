import os
from typing import Dict

import cv2
import numpy as np
import pytest

from ai import find_move_wrapper
from app import get_move_from_img
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
    assert get_move_from_img(img) == expected


if __name__ == '__main__':
    pytest.main()
    # test_find_move_wrapper(cv2.imread(images[0]), {'kind': 'MOVE', 'move': {'to': None, 'from': None}})

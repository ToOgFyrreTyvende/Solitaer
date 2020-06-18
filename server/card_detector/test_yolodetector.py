import os
from typing import Tuple, List
from itertools import chain

import cv2
import numpy as np
import pytest

from card_detector.yolodetector import scale_up_img, scale_down_img, new_extract_cards_from_image

GamePile = List[List[str]]

dirname = os.path.dirname(__file__)
images = ['dui.png', 'cards2.jpg', 'cards3.jpg', 'cards4.jpg', 'cards5.jpg', 'egg.jpg']
images = [os.path.join(dirname, item) for item in images]


@pytest.mark.parametrize('img', [cv2.imread(images[-1])])
def test_scale_up_img(img: np.ndarray):
    h, w, _ = img.shape
    scaled = scale_up_img(img)
    sh, sw, _ = scaled.shape
    # print(f'{h} -> {sh}, {w} -> {sw}')
    assert h < sh or w < sw


@pytest.mark.parametrize('img', [cv2.imread(images[0])])
def test_scale_down_img(img: np.ndarray):
    h, w, _ = img.shape
    scaled = scale_down_img(img)
    sh, sw, _ = scaled.shape
    assert h > sh or w > sw


@pytest.mark.parametrize('img, expected', [
    (cv2.imread(images[0]),
     ([['10c']],
      [['Ad']],
      [['6h', '5c'], ['8s'], ['5h'], ['Qd', 'Jc'], ['Jd', '9h', '8c'], ['10d', '9c', '8h', '6d', '5s', '2h']]))
])
def test_extract_cards_from_image(img: np.ndarray, expected: Tuple[GamePile, GamePile, GamePile]):
    (img_pile, img_founds, img_tableaus) = new_extract_cards_from_image(img)
    assert isinstance(img_pile, list)
    assert isinstance(img_founds, list)
    assert isinstance(img_tableaus, list)

    # We use the `set.issuperset` function so that the test hopefully passes as our program gets better at recognition
    assert set(chain(*img_pile)).issuperset(set(chain(*expected[0])))
    assert set(chain(*img_founds)).issuperset(set(chain(*expected[1])))
    assert set(chain(*img_tableaus)).issuperset(set(chain(*expected[2])))


if __name__ == '__main__':
    pytest.main(args=['-vv'])

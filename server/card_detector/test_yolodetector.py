import cv2
import numpy as np
import pytest
from typing import Tuple, List

from card_detector.yolodetector import scale_up_img, scale_down_img, new_extract_cards_from_image

GamePile = List[List[str]]

images = ['dui.png', 'cards2.jpg', 'cards3.jpg', 'cards4.jpg', 'cards5.jpg', 'egg.jpg']


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
    (cv2.imread(images[0]), ([['10c']],
                             [['Ad']],
                             [['6h', '5c'], ['8s', '8c'], ['5h'], ['Qd', 'Jc'], ['Jd', '9h', '8c']]))
])
def test_extract_cards_from_image(img: np.ndarray, expected: Tuple[GamePile, GamePile, GamePile]):
    (img_pile, img_founds, img_tableaus) = new_extract_cards_from_image(img)
    assert img_pile == expected[0]
    assert img_founds == expected[1]
    assert img_tableaus == expected[2]


if __name__ == '__main__':
    pytest.main()

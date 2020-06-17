import cv2
import numpy as np
import pytest

from card_detector.yolodetector import scale_up_img, scale_down_img

dui = cv2.imread('dui.png')
egg = cv2.imread('egg.jpg')


@pytest.mark.parametrize('img', [
    egg
])
def test_scale_up_img(img: np.ndarray):
    h, w, _ = img.shape
    scaled = scale_up_img(img)
    sh, sw, _ = scaled.shape
    # print(f'{h} -> {sh}, {w} -> {sw}')
    assert h < sh or w < sw


@pytest.mark.parametrize('img', [
    dui
])
def test_scale_down_img(img: np.ndarray):
    h, w, _ = img.shape
    scaled = scale_down_img(img)
    sh, sw, _ = scaled.shape
    assert h > sh or w > sw


if __name__ == '__main__':
    pytest.main()

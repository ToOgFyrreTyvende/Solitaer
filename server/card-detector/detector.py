import cv2
import numpy as np
import time
import os
from helpers import *

IMAGE_W = 1280
IMAGE_H = 720

image_test = cv2.imread('test.jpg')
processed_img = preprocess_image(image_test)


cv2.imshow('result', processed_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
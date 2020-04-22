import cv2
import numpy as np
import time
import os
from helpers import *

IMAGE_W = 1280
IMAGE_H = 720

image_test = cv2.imread('cards2.jpg')
processed_img = threshold_image(image_test)
cnts = find_number_suit(processed_img)
cv2.drawContours(image_test, cnts, -1, (0,255,0), 3)

cv2.imshow('result', image_test)
cv2.waitKey(0)
cv2.destroyAllWindows()
import numpy as np
import cv2
import time

font = cv2.FONT_HERSHEY_SIMPLEX

BG_THRESHOLD = 110


def get_background_reference(gray_image):
    image_w, image_h  = np.shape(gray_image)[:2]
    # Select random pixel at the bottom left as background reference point
    background_pixel = gray_image[int(image_w/100)][int(image_h-image_h/100)]
    return background_pixel + BG_THRESHOLD

def threshold_image(image):
    grayed  = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayed,(5,5),0)

    thresh_level   = get_background_reference(grayed)
    _, thresholded = cv2.threshold(blurred,thresh_level,255,cv2.THRESH_BINARY)
    
    return thresholded

def find_number_suit(thresholded_image):
    cnts, hier = cv2.findContours(thresholded_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    return cnts
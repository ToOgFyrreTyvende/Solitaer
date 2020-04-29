import numpy as np
import cv2
import time

font = cv2.FONT_HERSHEY_SIMPLEX

BG_THRESHOLD = 130

kernel = np.ones((5,5), np.uint8) 

def get_background_reference(gray_image):
    image_w, image_h  = np.shape(gray_image)[:2]
    # Select random pixel at the bottom left as background reference point
    background_pixel = gray_image[int(image_w/100)][int(image_h-image_h/100)]
    return background_pixel + BG_THRESHOLD

def threshold_image(image):
    grayed  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayed, (1,1), 1000)

    thresh_level   = get_background_reference(grayed)
    _, thresholded = cv2.threshold(blurred, thresh_level, 255, cv2.THRESH_BINARY)
    
    return thresholded

def find_number_suit(thresholded_image, img):
    #thresholded_image = cv2.erode(thresholded_image, kernel, iterations=1)
    cnts, hier = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #numcards = len(cnts)-1
    #contours = sorted(cnts, key=cv2.contourArea, reverse=True)[:numcards]
    contor_img = None
    for c in cnts:
        # Idea: Create approximation trapezoid
        # Use trapezoid corners as homography or warpperspective
        # https://stackoverflow.com/a/44156317

        #hull = cv2.convexHull(c)
        #cv2.drawContours(img,[hull],0,(0,255,0),2)
        x,y,w,h = cv2.boundingRect(c)
        contor_img = img[y:y+h, x:x+w]
        #h, status = cv2.findHomography(pts_src, pts_dst)
        #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.imshow('convex hull',contor_img)
    return cnts
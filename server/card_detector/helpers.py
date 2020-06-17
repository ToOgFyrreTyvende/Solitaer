import numpy as np
import cv2
import time

font = cv2.FONT_HERSHEY_SIMPLEX

BG_THRESHOLD = 130

kernel = np.ones((5, 5), np.uint8)


def get_background_reference(gray_image):
    image_w, image_h = np.shape(gray_image)[:2]
    # Select random pixel at the bottom left as background reference point
    background_pixel = gray_image[int(image_w/100)][int(image_h/100)]
    return 170


def threshold_image(image):
    grayed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayed, (1, 1), 1000)

    thresh_level = get_background_reference(grayed)
    _, thresholded = cv2.threshold(
        blurred, thresh_level, 255, cv2.THRESH_BINARY)
    thresholded = cv2.dilate(thresholded, kernel)

    return thresholded


def find_number_suit(thresholded_image, img):
    #thresholded_image = cv2.erode(thresholded_image, kernel, iterations=1)
    cnts, hier = cv2.findContours(
        thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #numcards = len(cnts)-1
    #contours = sorted(cnts, key=cv2.contourArea, reverse=True)[:numcards]
    rects = []
    img_slices = []
    contor_img = None
    cutoff = img.shape[0]*img.shape[1]*0.009
    for c in cnts:
        if cv2.contourArea(c) < cutoff:
            continue
        # Idea: Create approximation trapezoid
        # Use trapezoid corners as homography or warpperspective
        # https://stackoverflow.com/a/44156317
        box = cv2.minAreaRect(c)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        img_slices.append(warp_bboxes(img, box))
        cv2.drawContours(img, [box], -1, (0, 255, 0), 2)
        rects.append(box)

        #h, status = cv2.findHomography(pts_src, pts_dst)
        # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    #cv2.imshow('convex hull',contor_img)
    return img_slices


def warp_bboxes(img, box):
    rotated_contour = np.zeros((4, 2), dtype="float32")
    s = box.sum(axis=1)
    # Top left has smallest sum
    rotated_contour[0] = box[np.argmin(s)]
    # Bottom right has largest sum
    rotated_contour[2] = box[np.argmax(s)]
    diff = np.diff(box, axis=1)
    # Top right has smallest diff
    rotated_contour[1] = box[np.argmin(diff)]
    # Bottom left has largest diff
    rotated_contour[3] = box[np.argmax(diff)]

    [tl, tr, br, bl] = rotated_contour
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rotated_contour, dst)
    return cv2.warpPerspective(img, M, (maxWidth, maxHeight))

import logging
import os
from itertools import groupby
from typing import Tuple, List, Union
import configparser

import cv2
import numpy as np
from numpy.linalg import norm

from card_detector.helpers import threshold_image, find_slices

Detection = Tuple[int, float, List[int]]

dirname = os.path.dirname(__file__)
config_file = os.path.join(dirname, '../config.cfg')

config = configparser.ConfigParser()
config.read(config_file)
yolo_cfg = config['YOLO']
sep_cfg = config['SEPERATORS']

DEBUG = False
CONFIDENCE_CUTOFF = yolo_cfg.getfloat('confidence', fallback=0.3)
PROBABILITY_CUTOFF = yolo_cfg.getfloat('probability', fallback=0.5)
HORIZONTAL_LINE_CUTOFF = sep_cfg.getfloat('horizontal', fallback=0.25)
VERTICAL_LINE_CUTOFF = sep_cfg.getfloat('vertical', fallback=0.35)
CLASS_IDS: List[str]

weights = os.path.join(dirname, "reanchored.weights")
names = os.path.join(dirname, "cards.names")
cfg = os.path.join(dirname, "cards.cfg")
# load neural network from YOLO weights and config
nnet = cv2.dnn.readNet(weights, cfg)

# Read all object classes (card number + suit names) into an array
with open(names, "r") as f:
    CLASS_IDS = [line.strip() for line in f.readlines()]

# extract darknet layers from model
layer_names = nnet.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in nnet.getUnconnectedOutLayers()]


def detect_cards(outputs, real_w, real_h):
    bounding_boxes = []
    confidence_scores = []
    datected_classes = []
    detected_classes_set = set()
    for output in outputs:
        for detection in output:
            # Confidences are extracted from the output, to determine how precise algorithm is of detection
            # The scores are the remaining values after 5. index. The first elements are x y w h pc (confidence probability) values
            # The confidences will be a confidence of a card being either of the 52 possible card suit + number combos.
            # The remaining elements of this array will have a value from 0.0 - 1.0
            if detection[4] < PROBABILITY_CUTOFF: continue
            scores = detection[5:]
            # The class_id can be found from the INDEX of the highest value of these scores (the scores of each class)
            # argmax returns index of highest value
            detection_class = np.argmax(scores)
            # After this is found, the confidence score can be found at that index
            confidence = scores[detection_class]
            # We want to reject predictions with a low confidence, here we choose 40% percent confidence as the cutoff
            # found through trial and error
            # Only unique identifications are wanted here, so this is checked against a set
            if confidence > CONFIDENCE_CUTOFF and detection_class not in detected_classes_set:
                detected_classes_set.add(detection_class)
                # The detection position can now be found
                center_x = int(detection[0] * real_w)
                center_y = int(detection[1] * real_h)
                w = int(detection[2] * real_w)
                h = int(detection[3] * real_h)
                # x and y of the detection can be found too
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # now we have a proper prediction with coordinates and confidence, along with its class id.
                # We add this to a resulting array. Also we keep a set of detected class ids to remove duplicate card detections.
                bounding_boxes.append([x, y, w, h])
                confidence_scores.append(float(confidence))
                datected_classes.append(detection_class)

    return (bounding_boxes, confidence_scores, datected_classes)


def clean_detections(detections) -> List[Detection]:
    # We need to run the data through non maximum suppression.
    # This removes boxes around the same detection.
    (bounding_boxes, confidence_scores, detected_classes) = detections
    if not bounding_boxes:
        return []

    indices = cv2.dnn.NMSBoxes(
        bounding_boxes, confidence_scores, CONFIDENCE_CUTOFF, 0.4).flatten()

    # This will result in array of form
    # [(class_id, confidence, [x,y,w,h])
    return [(detected_classes[i], confidence_scores[i], bounding_boxes[i]) for i in indices]


def draw_cards(img, detections):
    for class_id, confidence, pos in detections:
        [x, y, w, h] = pos
        label = str(CLASS_IDS[class_id])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, label, (x, y + 30),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)


def scale_down_img(raw_img: np.ndarray) -> np.ndarray:
    height, width, _ = raw_img.shape
    w_scale = h_scale = 1
    if height > 605:
        h_scale = 605 / height
    if width > 605:
        w_scale = 605 / width

    if w_scale != 1 or h_scale != 1:
        raw_img = cv2.resize(raw_img, None, fx=w_scale, fy=h_scale)

    return raw_img


def scale_up_img(raw_img: np.ndarray) -> np.ndarray:
    height, width, _ = raw_img.shape
    w_scale = h_scale = 1
    if height < 550:
        h_scale = 550 / height
    if width < 550:
        w_scale = 550 / width

    if w_scale != 1 or h_scale != 1:
        raw_img = cv2.resize(raw_img, None, fx=h_scale, fy=h_scale)

    return raw_img


def infer_from_image(raw_img: np.ndarray) -> List[Detection]:

    def sort_detections(detections: List[Detection]) -> List[Detection]:
        return list(sorted(detections, key=lambda x: x[2][1]))

    # Scale image to be only 40% of width and height
    # img = cv2.resize(raw_img, None, fx=1, fy=1)

    # Scale image down/up the right way (cv2.resize(img, 608, 608) stretches the image, so we do it by scale)
    # scaled = scale_down_img(scale_up_img(raw_img))
    # scaled = scale_up_img(scale_down_img(raw_img))
    logging.info(f'current img shape: {raw_img.shape}')
    scaled = scale_down_img(raw_img)

    height, width, _ = scaled.shape
    top_bot = int((608 - height) / 2)
    left_right = int((608 - width) / 2)

    image = cv2.copyMakeBorder(
        scaled, top_bot, top_bot, left_right, left_right, cv2.BORDER_CONSTANT)

    # Detecting the objects
    # https://docs.opencv.org/master/d6/d0f/group__dnn.html#ga29f34df9376379a603acd8df581ac8d7
    # The first argument after img is the scale factor, then size, mean and swrapRB
    # Scale factor is a multiplyer to scale. It is suggested to let this be 1/255, same as 0.00392
    # https://www.learnopencv.com/deep-learning-based-object-detection-using-yolov3-with-opencv-python-c/
    # Size given as the target resolution, YOLO takes 416x416 images
    # Mean is scalar values subtracted from channels. We do not change any color values.
    # SwapRB indicates swapping first and last channels in 3 channel images
    blob = cv2.dnn.blobFromImage(
        image=image, scalefactor=1 / 255, size=(608, 608), mean=(0, 0, 0), swapRB=True, crop=False)
    # Load binary image data into our neural network and infer
    nnet.setInput(blob)
    outputs = nnet.forward(output_layers)
    detections = detect_cards(outputs, 608, 608)
    clean_detect = clean_detections(detections)
    logging.info(clean_detect)
    if DEBUG:
        draw_cards(image, clean_detect)
        cv2.imshow("bombie", image)
        cv2.waitKey(0)
    return sort_detections(clean_detect)


def area(a, b, c):
    return 0.5 * norm(np.cross(b - a, c - a))


def create_stacks(bboxes: List[np.ndarray], detections: List[tuple], img_height: int, img_width: int) -> Tuple:
    pile: list = []
    foundations: list = []
    tableaus: list = []
    cutoff_y: int = int(img_height * 0.3)
    cutoff_x: int = int(img_width * 0.35)

    for i, [A, B, C, D] in enumerate(bboxes):
        ABC = area(A, B, C)
        CDA = area(C, D, A)
        rect_area = ABC + CDA
        if C[1] > cutoff_y:  # Cards are under the 30% line
            cards: list = []
            for class_id, confidence, pos in detections:
                [cx, cy, cw, ch] = pos
                P = [cx + cw/2, cy + ch/2]
                # https://math.stackexchange.com/a/190117
                """
                A-------------B
                |\           /|
                | \         / |
                |  \  PBA  /  |
                |   \     /   |
                |    \   /    |
                |     \ /     |
                | APD  P  CPB |
                |     / \     |
                |    /   \    |
                |   /     \   |
                |  /  DPC  \  |
                | /         \ |
                |/           \|
                D-------------C
                If the APD + DPC + CPB + PBA > ABC + CDA, then the point P is not within the rectangle ABCD
                """
                area_check = area(A, P, D) + area(D, P, C) + area(C, P, B) + area(P, B, A)
                if area_check == rect_area:
                    cards.append((P[1], str(CLASS_IDS[class_id])))
            tableaus.append([x[1] for x in sorted(cards, key=lambda x: x[0])])
        else:
            if C[0] > cutoff_x:  # Cards are over the 30% line and right of the 35% line
                for class_id, confidence, pos in detections:
                    cx, cy, cw, ch = pos
                    P = [cx + cw/2, cy + ch/2]
                    area_check = area(A, P, D) + area(D, P, C) + area(C, P, B) + area(P, B, A)
                    if area_check == rect_area:
                        foundations.append(str(CLASS_IDS[class_id]))
            else:  # Cards are over the 30% line and left of the 35% line
                for class_id, confidence, pos in detections:
                    cx, cy, cw, ch = pos
                    P = [cx + cw / 2, cy + ch / 2]
                    area_check = area(A, P, D) + area(D, P, C) + area(C, P, B) + area(P, B, A)
                    if area_check == rect_area:
                        pile.append(str(CLASS_IDS[class_id]))

    return pile, foundations, tableaus


def new_create_stacks(boxes_and_slices: List[Tuple[np.ndarray, List[Detection]]], img_height: int, img_width: int) -> Tuple[List[Tuple[np.ndarray, List[Detection]]], List[Tuple[np.ndarray, List[Detection]]], List[Tuple[np.ndarray, List[Detection]]]]:
    cutoff_y: int = int(img_height * HORIZONTAL_LINE_CUTOFF)
    cutoff_x: int = int(img_width * VERTICAL_LINE_CUTOFF)

    upper_cards = {True: [], False: []}
    for key, group in groupby(boxes_and_slices, lambda x: x[0][2][1] < cutoff_y):
        upper_cards[key].extend(list(group))

    pile: list = list(filter(lambda x: x[0][2][0] < cutoff_x, upper_cards[True]))
    foundations: list = list(filter(lambda x: x[0][2][0] > cutoff_x, upper_cards[True]))
    tableaus: list = upper_cards[False]

    return pile, foundations, tableaus


def extract_cards_from_image(img: np.ndarray):
    # detections = infer_from_image(img)
    processed_img = threshold_image(img)
    img_slices = find_slices(processed_img, img)
    [infer_from_image(x) for x in img_slices]
    return "oke"


def get_clean_card_stacks(card_stack: List[Tuple[np.ndarray, List[Detection]]]) -> Union[List[str], List[List[str]]]:
    result: List[List[str]] = []
    for _, detections in card_stack:
        cards = []
        for cls_id, _, _ in detections:
            cards.append(CLASS_IDS[cls_id])
        result.append(cards)
    return result


def new_extract_cards_from_image(img: np.ndarray) -> Tuple[List[str], List[List[str]], List[List[str]]]:
    processed_img = threshold_image(img)
    img_slices = find_slices(processed_img, img)

    # Slice detection: (np.ndarray, [class: int, confidence: float, [x, y, w, h]])
    slice_detections: List[Tuple[np.ndarray, List[Tuple[int, float, List[int]]]]]

    logging.info('List of detections for each slice:')
    slice_detections = [(box, infer_from_image(_img)) for box, _img in img_slices]
    slice_detections = [item for item in slice_detections if len(item[1])]  # Remove elements with no detections
    logging.info('End of detection list\n')

    sorted_stacks = new_create_stacks(slice_detections, img_width=img.shape[1], img_height=img.shape[0])

    pile, foundation, tableaus = [get_clean_card_stacks(stack) for stack in sorted_stacks]

    return pile, foundation, tableaus


def get_card_classes(detections):
    res = []
    for class_id, confidence, pos in detections:
        label = str(CLASS_IDS[class_id])
        res.append(label)
    return res


if __name__ == "__main__":
    from pprint import pprint
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.debug(f'YOLO cutoffs:\nProbability: {PROBABILITY_CUTOFF}\nConfidence: {CONFIDENCE_CUTOFF}\n')
    logging.debug(f'SEPERATORS cutoffs:\nHorizontal: {HORIZONTAL_LINE_CUTOFF}\nVertical: {VERTICAL_LINE_CUTOFF}\n')
    img = cv2.imread("dui.png")
    logging.info(f'img shape: {img.shape}\n')
    pprint(new_extract_cards_from_image(img))
    # cv2.imshow("Image", img)
    # cv2.waitKey(0)

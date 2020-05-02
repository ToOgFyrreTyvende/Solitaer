import cv2
import numpy as np
from helpers import *
from numpy.linalg import norm

DEBUG = True
CONFIDENCE_CUTOFF = 0.3
CLASS_IDS = []

# load neural network from YOLO weights and config
nnet = cv2.dnn.readNet("yolocards_608.weights", "cards.cfg")

# Read all object classes (card number + suit names) into an array
with open("cards.names", "r") as f:
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
            # The scores are the remaining values after 5. index. The first elements are x y w h values
            # The confidences will be a confidence of a card being either of the 52 possible card suit + number combos.
            # The remaining elements of this array will have a value from 0.0 - 1.0
            scores = detection[5:]
            # The class_id can be found from the INDEX of the highest value of these scores (the scores of each class)
            detection_class = np.argmax(scores) # argmax returns index of highest value
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

def clean_detections(detections):
    # We need to run the data through non maximum suppression.
    # This removes boxes around the same detection.
    (bounding_boxes, confidence_scores, detected_classes) = detections
    indices = cv2.dnn.NMSBoxes(bounding_boxes, confidence_scores, CONFIDENCE_CUTOFF, 0.4).flatten()

    # This will result in array of form 
    # [(class_id, confidence, [x,y,w,h])
    return [(detected_classes[i], confidence_scores[i], bounding_boxes[i]) for i in indices]
    

def draw_cards(img, detections):
    for class_id, confidence, pos in detections:
        [x, y, w, h] = pos
        label = str(CLASS_IDS[class_id])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)


def infer_from_image(raw_img):
    # Scale image to be only 40% of width and height
    img = cv2.resize(raw_img, None, fx=0.4, fy=0.4)
    height, width, channels = raw_img.shape

    # Detecting the objects
    # https://docs.opencv.org/master/d6/d0f/group__dnn.html#ga29f34df9376379a603acd8df581ac8d7
    # The first argument after img is the scale factor, then size, mean and swrapRB
    # Scale factor is a multiplyer to scale. It is suggested to let this be 1/255, same as 0.00392
        # https://www.learnopencv.com/deep-learning-based-object-detection-using-yolov3-with-opencv-python-c/
    # Size given as the target resolution, YOLO takes 416x416 images
    # Mean is scalar values subtracted from channels. We do not change any color values.
    # SwapRB indicates swapping first and last channels in 3 channel images
    blob = cv2.dnn.blobFromImage(img, 1/255, (608, 608), (0, 0, 0), True, crop=False)
    # Load binary image data into our neural network and infer
    nnet.setInput(blob)
    outputs = nnet.forward(output_layers)
    detections = detect_cards(outputs, width, height)
    clean_detect = clean_detections(detections)
    if DEBUG:
        draw_cards(raw_img, clean_detect)
    return clean_detect


def area(a, b, c) :
    return 0.5 * norm( np.cross( b-a, c-a ) )

def create_stacks(bboxes, detections):
    tableaus = []
    print(bboxes)
    for [A, B, C, D] in bboxes:
        """
        A------B
        |\ ABC |
        | \    |
        |  \   |
        |   \  |
        |    \ |
        | CDA \|
        D------C
        """
        ABC = area(A, B, C)
        CDA = area(C, D, A)
        rect_area = ABC + CDA
        if C[1] > 170:
            cards = []
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
                    cards.append(str(CLASS_IDS[class_id]))

        tableaus.append((A[0], cards))
    return [x[1] for x in sorted(tableaus, key=lambda x: x[0])]

def extract_cards_from_image(img):
    detections = infer_from_image(img)
    processed_img = threshold_image(img)
    bboxes = find_number_suit(processed_img, img)
    return create_stacks(bboxes, detections)

if __name__ == "__main__":
    img = cv2.resize(cv2.imread("cards5.jpg"), (1280,720))
    print(extract_cards_from_image(img))
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    
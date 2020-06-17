import base64

import pytest
import numpy as np
import cv2

from ai import new_find_move, MOVE_CODE
from card_detector.yolodetector import extract_cards_from_image, new_extract_cards_from_image, get_card_classes, create_stacks
from logic import Klondike, Card, print_game
from test_app_helper import *

test_json_data = json_img_four()


@pytest.mark.parametrize('request_json', [
    (test_json_data,)
])
def test_boardAnalyse(request_json: dict):
    img_data = request_json['data'][23:]
    np_arr = np.fromstring(base64.b64decode(img_data), np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    detections = extract_cards_from_image(img)
    retval, buffer = cv2.imencode('.jpeg', img)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    response = {'cards': get_card_classes(detections), 'img_data': jpg_as_text}

    return response


@pytest.mark.parametrize('request_json', [
    (test_json_data,)
])
def test_get_move(request_json: dict):
    img_data = request_json['data'][23:]
    np_arr = np.fromstring(base64.b64decode(img_data), np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    (img_pile, img_founds, img_tableaus) = new_extract_cards_from_image(img)
    game = Klondike()
    game.pile = [Card.from_str(card) for card in img_pile]
    for foundation in img_founds:
        game.foundations.append(foundation)
    for tableau in img_tableaus:
        game.tableaus.append([Card.from_str(card) for card in tableau])
    print_game(game)
    code, *instr = new_find_move(game)
    shown_move = str(code)[10:]
    response = {'code': code, 'from': None, 'to': None, 'error': False}
    if code == MOVE_CODE.DRAW:
        pass
    elif code == MOVE_CODE.T_TO_F:
        response['from'] = game.tableaus[instr[0]][-1].to_json()
        response['to'] = game.foundations[instr[1]][-1].to_json()
    elif code == MOVE_CODE.T_TO_T:
        response['from'] = game.tableaus[instr[0]][-1].to_json()
        response['to'] = game.tableaus[instr[1]][-instr[2]].to_json()
    elif code == MOVE_CODE.P_TO_F:
        response['from'] = game.pile[-1].to_json()
        response['to'] = game.foundations[instr[0]][-1].to_json()
    elif code == MOVE_CODE.P_TO_T:
        response['from'] = game.pile[-1].to_json()
        response['to'] = game.tableaus[instr[0]][-1].to_json()
    elif code == MOVE_CODE.ERROR:
        response['error'] = True
    return True


if __name__ == '__main__':
    test_boardAnalyse(test_json_data)
    test_get_move(test_json_data)

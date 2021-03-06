import base64
from itertools import chain
from typing import Union, Dict

import cv2
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS

from ai import find_move_wrapper
from card_detector.yolodetector import new_extract_cards_from_image
from logic import Klondike, Card

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__, static_folder='app', static_url_path="/")
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/api/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


def get_move_from_img(img: np.ndarray) -> Dict[str, Union[str, Dict[str, Union[str, None]]]]:
    result = new_extract_cards_from_image(img)
    (img_pile, img_founds, img_tableaus) = result
    img_pile = chain(*img_pile)

    game = Klondike()
    game.pile = [Card.from_str(card) for card in img_pile]
    for real_foundation, detected_foundation in zip(game.foundations, img_founds):
        real_foundation.extend([Card.from_str(card) for card in detected_foundation])
    for real_tableau, detected_tableau in zip(game.tableaus, img_tableaus):
        real_tableau.extend([Card.from_str(card) for card in detected_tableau])

    return find_move_wrapper(game)


@app.route('/api/getMove', methods=['POST'])
def get_next_klondike_move():
    img_data = request.json['data'][23:]
    np_arr = np.fromstring(base64.b64decode(img_data), np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    return jsonify(get_move_from_img(img))


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")


if __name__ == '__main__':
    app.run()

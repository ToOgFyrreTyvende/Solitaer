import base64
import uuid
from typing import Union, Dict
from itertools import chain

import cv2
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS

from ai import find_move_wrapper
from card_detector.yolodetector import extract_cards_from_image, get_card_classes, new_extract_cards_from_image
from logic import Klondike, Card

BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/boardAnalyse', methods=['POST'])
def boardAnalyse():
    img_data = request.json['data'][23:]
    np_arr = np.fromstring(base64.b64decode(img_data), np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    detections = extract_cards_from_image(img)
    retval, buffer = cv2.imencode('.jpeg', img)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    json = {'cards': get_card_classes(detections), 'img_data': jpg_as_text}
    return jsonify(json)


def get_move_from_img(img: np.ndarray) -> Dict[str, Union[str, Dict[str, Union[str, None]]]]:
    result = new_extract_cards_from_image(img)
    (img_pile, img_founds, img_tableaus) = result
    img_pile = chain(*img_pile)

    game = Klondike()
    game.pile = [Card.from_str(card) for card in img_pile]
    game.foundations = [[Card.from_str(card) for card in lst] for lst in img_founds]
    game.tableaus = [[Card.from_str(card) for card in lst] for lst in img_tableaus]

    return find_move_wrapper(game)


@app.route('/getMove', methods=['POST'])
def get_next_klondike_move():
    img_data = request.json['data'][23:]
    np_arr = np.fromstring(base64.b64decode(img_data), np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    return jsonify(get_move_from_img(img))


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()

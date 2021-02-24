from flask import Blueprint, request, jsonify
from models import songs
from routes import api
from helpers.convert_object_ids import convert_model_ids

import sys
import logging

_logger = logging.getLogger(__name__)

songs_bp = Blueprint('songs', __name__)


@songs_bp.route(api.route['get_all_songs'], methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def get_songs():
    '''
    Get songs
    '''
    if request.method == 'GET':
        lang = request.args.get('lang')
        model = songs.Songs(lang)
        if not lang:
            return jsonify(
                {
                    "message": "please specify the language. Refer to the API documentation for details.",
                    "success": False
                }), 400
        documents = model.get_all_songs()
        converted_documents = convert_model_ids(documents)
        response = dict(message="get songs query successful",
                        data=converted_documents)
        return jsonify(response), 200
    else:
        return jsonify(
            {
                "message": "Invalid request method. Please refer to the API documentation",
                "success": False
            }), 400

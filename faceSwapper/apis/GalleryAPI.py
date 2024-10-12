# -*- coding: utf-8 -*-
from __future__ import annotations

import logging

from flask import Blueprint, request, jsonify, Response
from typing import Tuple

from visuals.facial.analyzer.Analyzer import Analyzer as Analyzer
from visuals.facial.swapper.Swapper import Swapper as Swapper

from flask_cors import CORS  # Import CORS

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a Blueprint for the SwapperAPI
galleryAPI_routes = Blueprint('galleryAPI_routes', __name__)

CORS(galleryAPI_routes)  # Enable CORS for all routes

# Route to upload file (images)
@galleryAPI_routes.route('/extractFaces', methods=['POST'])
def extract_faces() -> Tuple[Response, int]:

    # Get the image URL from the request body
    data = request.get_json()
    image_url = data.get('imageUrl')

    if not image_url:
        return jsonify({'error': 'Image URL is required'}), 400
    
    return  jsonify({'message': 'Image URL is required'}), 400


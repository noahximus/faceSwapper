# -*- coding: utf-8 -*-
from __future__ import annotations

import logging

from flask import Blueprint, request, jsonify, Response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from typing import Tuple
from flask_cors import CORS  # Import CORS

from faceSwapper.commons.config import CommonConfig
from faceSwapper.commons.utils import FileUtils
from faceSwapper.commons.utils import MediaUtils

from faceSwapper.services import UploadsService
from faceSwapper.services import GalleryService

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a Blueprint for the SwapperAPI
galleryAPI_routes = Blueprint('galleryAPI_routes', __name__)

CORS(galleryAPI_routes)  # Enable CORS for all routes

def extract(file: FileStorage, uploadType: str|None) -> Tuple[Response, int]:

    if not UploadsService.is_upload_valid(file):
        return jsonify({'error': 'No valid file.'}), 400

    try:
        logger.debug(f'Reading image from file.')
        
        # Convert the uploaded file to an OpenCV image
        img = GalleryService.read_image_from_file(file)
        logger.debug(f'Extracting faces from image.')
        
        # Extract faces using the reusable extract_faces method
        faces = GalleryService.extract_faces(img)
        logger.debug(f'There are {len(faces)} faces in the image.')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "filename": secure_filename(str(file.filename)),
        "uploadType": uploadType,
        "image_url": f'{CommonConfig.UPLOADS_URL}/{secure_filename(str(file.filename))}',
        "faces": faces,
    }), 200

# Route to extract faces from file (images)
@galleryAPI_routes.route('/extractFaces', methods=['POST'])
def extract_faces() -> Tuple[Response, int]:

    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    uploadType = request.form.get('uploadType')
    
    return extract(file, uploadType)

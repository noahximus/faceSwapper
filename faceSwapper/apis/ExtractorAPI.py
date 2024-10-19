# -*- coding: utf-8 -*-
from __future__ import annotations
import logging

from typing import Dict, Any, Tuple

from flask import request
from flask_restx import Namespace, Resource

from werkzeug.utils import secure_filename

from faceSwapper.commons.config import CommonConfig
from faceSwapper.services import GalleryService
from faceSwapper.services import UploadService

# Define the namespace
extractorAPI_routes = Namespace('extractor', description='Face Extractor operations')

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# Route to extract faces from file (images)
@extractorAPI_routes.route('/extract')
class FaceExtractResource(Resource):
    def post(self) -> Tuple[Dict[str, Any], int]:

        # Check if the post request has the file part
        if 'file' not in request.files:
            return {"error": "No file part"}, 400

        file = request.files['file']
        uploadType = request.form.get('uploadType')
        if not UploadService.is_upload_valid(file):
            return {'error': 'No valid file.'}, 400

        try:
            logger.debug(f'Reading image from file.')

            # Convert the uploaded file to an OpenCV image
            img = GalleryService.read_image_from_file(file)
            logger.debug(f'Extracting faces from image.')

            # Extract faces using the reusable extract_faces method
            faces = GalleryService.extract_faces(img)
            logger.debug(f'There are {len(faces)} faces in the image.')
        except Exception as e:
            return {"error": str(e)}, 500

        return {
            "filename": secure_filename(str(file.filename)),
            "uploadType": uploadType,
            "image_url": f'{CommonConfig.UPLOADS_URL}/{secure_filename(str(file.filename))}',
            "faces": faces,
        }, 200

# -*- coding: utf-8 -*-
from __future__ import annotations
import logging

from typing import Dict, Any, Tuple

from flask import request
from flask_restx import Namespace, Resource

from werkzeug.utils import secure_filename

from faceSwapper.commons.config import CommonConfig
from faceSwapper.commons.utils import MediaUtils

from faceSwapper.services import GalleryService
from faceSwapper.services import UploadService

# Define the namespace
extractorAPI_routes = Namespace('extractor', description='Face Extractor operations')

logger = logging.getLogger(__name__)

# Route to extract faces from file (images)
@extractorAPI_routes.route('/extract')
class FaceExtractResource(Resource):
    def post(self) -> Tuple[Dict[str, Any], int]:
        # Check if the post request has the file part
        if 'file' not in request.files:
            logger.error(f'No file part.')
            return {"error": "No file part."}, 400

        file = request.files['file']
        uploadType = request.form.get('uploadType')

        if not UploadService.is_upload_valid(file):
            logger.error(f'No valid file.')
            return {'error': 'No valid file.'}, 400

        faces = []
        try:
            if MediaUtils.is_image(file):

                logger.debug(f'Reading image from file.')
                img = GalleryService.read_image_from_file(file) # Convert the uploaded file to an OpenCV image
                faces = GalleryService.extract_faces_from_image(img)
                logger.debug(f'There are {len(faces)} faces in the image.')

            elif MediaUtils.is_video(file):

                logger.debug(f'Reading video from file.')
                video_file_path = f"/tmp/{secure_filename(str(file.filename))}"
                file.save(video_file_path)
                faces = GalleryService.extract_faces_from_video(str(video_file_path))
                logger.debug(f'There are {len(faces)} faces in the video.')

            else:
                logger.error(f'Unsupported file type.')
                return {"error": "Unsupported file type."}, 400

        except Exception as e:
            logger.error(f'Error: {str(e)}')
            return {"error": str(e)}, 500

        return {
            "filename": secure_filename(str(file.filename)),
            "uploadType": uploadType,
            "image_url": f'{CommonConfig.UPLOADS_URL}/{secure_filename(str(file.filename))}',
            "faces": faces,
        }, 200


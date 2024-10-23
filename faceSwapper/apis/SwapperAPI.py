import json
import logging
import time

from typing import Dict, Tuple

from flask import request
from flask_restx import Namespace, Resource

from faceSwapper.services import SwapperService

# logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# Define the namespace
swapperAPI_routes = Namespace('swapper', description='Face Swapper operations')

# Route to handle the face swap image upload and processing
@swapperAPI_routes.route('/swap')
class FaceSwapResource(Resource):
    def post(self) -> Tuple[Dict[str, str], int]:
        # logger = logging.getLogger(__name__)
        start_time = time.time()
        logger.debug(f'FaceSwap START')

        response = None
        try:
            # Access the uploaded files
            source_file = request.files.get('sourceFile')
            target_file = request.files.get('targetFile')

            if not source_file or not target_file:
                logger.error(f'Source and target files are required!')
                response = {'error': 'Source and target files are required!'}, 400

            # Access the gallery faces data (sent as JSON strings)
            source_gallery_order = request.form.get('sourceGalleryOrder')
            target_gallery_order = request.form.get('targetGalleryOrder')

            # Convert JSON strings to Python objects (arrays)
            try:
                if source_gallery_order:
                    source_gallery_order = json.loads(source_gallery_order)
                if target_gallery_order:
                    target_gallery_order = json.loads(target_gallery_order)
            except json.JSONDecodeError as e:
                logger.error(f'Source and target files are required!')
                response = {'error': f'Invalid JSON in gallery faces: {str(e)}'}, 400

            # Log received files and data for debugging
            logger.debug(f"Received source file: {source_file.filename if source_file else ''}")
            logger.debug(f"Received target file: {target_file.filename if target_file else ''}")

            # Perform face swapping using the files and faces
            try:
                result = SwapperService.swap_faces_sync(
                    source_file, source_gallery_order,
                    target_file, target_gallery_order
                )
                logger.debug(f"Done with SWAPPING")
                
                response = { 'image': f'{result}' }, 200
            except Exception as e:
                logger.error(f'Face swapping failed: {str(e)}')
                response = {'error': f'Face swapping failed: {str(e)}'}, 500

        except Exception as e:
            logger.error(f'{str(e)}')
            response = {'error': str(e)}, 500

        logger.debug(f'FaceSwap DONE: ({time.time() - start_time} secs)')
        return response


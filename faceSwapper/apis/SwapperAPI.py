import json
import logging
import time

from flask import Blueprint, jsonify, request, Response
from flask_cors import CORS  # Import CORS
from typing import Tuple

from faceSwapper.services import SwapperService
from faceSwapper.services import EnhancerService

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a Blueprint for the SwapperAPI
swapperAPI_routes = Blueprint('swapperAPI_routes', __name__)

CORS(swapperAPI_routes)  # Enable CORS for all routes

# Route to handle the face swap image upload and processing
@swapperAPI_routes.route('/faceSwap', methods=['POST'])
def faceSwap() -> Tuple[Response, int]:
    # logger = logging.getLogger(__name__)
    start_time = time.time()
    logger.debug(f'FaceSwap START')

    returned_result = ''
    try:
        # Access the uploaded files
        source_file = request.files.get('sourceFile')
        target_file = request.files.get('targetFile')

        if not source_file or not target_file:
            logger.error(f'Source and target files are required!')
            returned_result = jsonify({'error': 'Source and target files are required!'}), 400

        source_file_Name = request.form.get('sourceFileName')
        target_file_Name = request.form.get('targetFileName')

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
            returned_result = jsonify({'error': f'Invalid JSON in gallery faces: {str(e)}'}), 400

        # Log received files and data for debugging
        logger.debug(f"Received source file: {source_file.filename if source_file else ''}")
        logger.debug(f"Received target file: {target_file.filename if target_file else ''}")

        # Perform face swapping using the files and faces
        try:
            result = SwapperService.swap_faces(
                source_file, source_file_Name, source_gallery_order,
                target_file, target_file_Name, target_gallery_order)
            logger.debug(f"Done with SWAPPING")
            
            result = EnhancerService.enhance_image(result)
            logger.debug(f"Done with ENHANCING")

            returned_result = jsonify({ 'swapped_image': f'{result}' }), 200
        except Exception as e:
            logger.error(f'Face swapping failed: {str(e)}')
            returned_result = jsonify({'error': f'Face swapping failed: {str(e)}'}), 500

    except Exception as e:
        logger.error(f'{str(e)}')
        returned_result = jsonify({'error': str(e)}), 500

    logger.debug(f'FaceSwap DONE: ({time.time() - start_time} secs)')
    return returned_result


import json
import logging
import time

from flask import Blueprint, jsonify, request, Response
from flask_cors import CORS  # Import CORS
from typing import Tuple

from faceSwapper.services import EnhancerService

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a Blueprint for the EnhancerAPI
enhancerAPI_routes = Blueprint('enhancerAPI_routes', __name__)

CORS(enhancerAPI_routes)  # Enable CORS for all routes

# Route to handle the face swap image upload and processing
@enhancerAPI_routes.route('/enhance', methods=['POST'])
def enhance() -> Tuple[Response, int]:
    start_time = time.time()
    logger.debug(f'Enhancement START')

    returned_result = None
    try:
        # Get the image from the request body
        images = request.form.get('images')

        # Convert JSON strings to Python objects (arrays)
        try:
            if images:
                images = json.loads(images)
        except json.JSONDecodeError as e:
            logger.error(f'At least one image is required!: {str(e)}')
            returned_result = jsonify({'error': f'At least one image is required!: {str(e)}'}), 400

        if not images or not isinstance(images, list):
            returned_result = jsonify({'message': 'Invalid request. Please provide an array of image URLs.'}), 400
            return returned_result

        logger.debug(f'There are {len(images)} images present')
        result = None
        for i in range(len(images)):
            image = images[i]

            if image:
                try:
                    result = EnhancerService.enhance_image(image)
                    logger.debug(f"Done with ENHANCING")
                    returned_result = jsonify({ 'image': f'{result}' }), 200
                except Exception as e:
                    logger.error(f'Enhancement failed: {str(e)}')
                    returned_result = jsonify({'error': f'Enhancement failed: {str(e)}'}), 500
            if result:
                break

    except Exception as e:
        logger.error(f'{str(e)}')
        returned_result = jsonify({'error': str(e)}), 500

    logger.debug(f'Enhancement DONE: ({time.time() - start_time} secs)')
    return returned_result


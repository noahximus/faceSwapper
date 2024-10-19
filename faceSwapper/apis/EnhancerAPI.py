import json
import logging
import time

from typing import Dict, Tuple
from flask import request
from flask_restx import Namespace, Resource

from faceSwapper.services import EnhancerService

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# Define the namespace
enhancerAPI_routes = Namespace('enhancer', description='Face Enhance operations')

# Route to handle the face swap image upload and processing
@enhancerAPI_routes.route('/enhance')
class FaceEnhanceResource(Resource):
    def post(self) -> Tuple[Dict[str, str], int]:
        start_time = time.time()
        logger.debug(f'Enhancement START')

        try:
            # Get the image from the request body
            images = request.form.get('images')

            # Convert JSON strings to Python objects (arrays)
            if images:
                try:
                    images = json.loads(images)
                except json.JSONDecodeError as e:
                    logger.error(f'At least one image is required!: {str(e)}')
                    return {'error': f'At least one image is required!: {str(e)}'}, 400

            if not images or not isinstance(images, list):
                return {'message': 'Invalid request. Please provide an array of image URLs.'}, 400

            logger.debug(f'There are {len(images)} images present')
            result = None

            for image in images:
                if image:
                    try:
                        result = EnhancerService.enhance_image(image)
                        logger.debug(f"Done with ENHANCING")
                        return { 'image': f'{result}' }, 200
                    except Exception as e:
                        logger.error(f'Enhancement failed: {str(e)}')
                        return {'error': f'Enhancement failed: {str(e)}'}, 500

        except Exception as e:
            logger.error(f'{str(e)}')
            return {'error': str(e)}, 500

        logger.debug(f'Enhancement DONE: ({time.time() - start_time} secs)')

        # If no result was returned in the loop, return an error
        return {'error': 'No valid image found for enhancement.'}, 400


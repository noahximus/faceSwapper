import os
import logging

from flask import request, jsonify, send_from_directory, Response, abort
from flask_restx import Namespace, Resource

from werkzeug.utils import secure_filename
from typing import Tuple

from faceSwapper.commons.config import CommonConfig
from faceSwapper.commons.utils import FileUtils
from faceSwapper.commons.utils import MediaUtils

from faceSwapper.services import UploadService
from faceSwapper.services import GalleryService

# logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# Define the namespace
uploaderAPI_routes = Namespace('uploader', description='Image Uploader operations')

# Route to upload file (images)
@uploaderAPI_routes.route('/upload')
class ImageUploadResource(Resource):
    def post(self) -> Tuple[Response, int]:

        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        uploadType = request.form.get('uploadType')
        

        if not UploadService.is_upload_valid(file):
            return jsonify({'error': 'No valid file.'}), 400

        try:
            logger.debug(f'Upload filename: {file.filename}')
            file_path = FileUtils.save_file(file, CommonConfig.TARGETS_UPLOADS_DIR)

            logger.debug(f'Reading image from file. Saved files is in {file_path}')
            
            # Convert the uploaded file to an OpenCV image
            img = GalleryService.read_image_from_file_path(file_path)

            logger.debug(f'Extracting faces from image.')
            
            # Extract faces using the reusable extract_faces method
            faces = GalleryService.extract_faces_from_image(img)

            logger.debug(f'There are {len(faces)} faces in the image.')
                    
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        if not MediaUtils.is_image_file(file_path):
            return jsonify({"error": "Uploaded file is not a valid image"}), 400

        return jsonify({
            "filename": secure_filename(str(file.filename)),
            "filepath": str(file_path),
            "content_type": FileUtils.file_type(str(file_path)),
            "uploadType": uploadType,
            "image_url": f'{CommonConfig.UPLOADS_URL}/{secure_filename(str(file.filename))}',
            "faces": faces,
        }), 200


# Define the uploader route
@uploaderAPI_routes.route('/uploads/<path:filename>')
class ImageFromDirectory(Resource):
    def get(self, filename: str) -> Response:

        # Check if the file exists
        if not os.path.isfile(CommonConfig.TARGETS_UPLOADS_DIR.joinpath(filename)):
            abort(404, description="File not found")  # Return 404 if the file doesn't exist

        # Serve the file using send_from_directory
        return send_from_directory(CommonConfig.TARGETS_UPLOADS_DIR, filename, as_attachment=False)



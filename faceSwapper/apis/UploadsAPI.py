import logging

from flask import Blueprint, request, jsonify, send_from_directory, Response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from typing import Tuple

from faceSwapper.commons.config import CommonConfig
from faceSwapper.commons.utils import FileUtils
from faceSwapper.commons.utils import MediaUtils

from faceSwapper.services import UploadsService
from faceSwapper.services import GalleryService

from flask_cors import CORS  # Import CORS

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a Blueprint for the SwapperAPI
uploadsAPI_routes = Blueprint('uploadsAPI_routes', __name__)

CORS(uploadsAPI_routes)  # Enable CORS for all routes

def upload(file: FileStorage, uploadType: str|None) -> Tuple[Response, int]:

    if not UploadsService.is_upload_valid(file):
        return jsonify({'error': 'No valid file.'}), 400

    try:
        logger.debug(f'Upload filename: {file.filename}')
        file_path = FileUtils.save_file(file, CommonConfig.TARGETS_UPLOADS_DIR)

        logger.debug(f'Reading image from file. Saved files is in {file_path}')
        
        # Convert the uploaded file to an OpenCV image
        img = GalleryService.read_image_from_file_path(file_path)

        logger.debug(f'Extracting faces from image.')
        
        # Extract faces using the reusable extract_faces method
        faces = GalleryService.extract_faces(img)

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

# Route to upload file (images)
@uploadsAPI_routes.route('/upload', methods=['POST'])
def upload_file() -> Tuple[Response, int]:

    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    uploadType = request.form.get('uploadType')
    
    return upload(file, uploadType)

# Route to serve uploaded file (images)
@uploadsAPI_routes.route('/uploads/<path:filename>', methods=['GET'])
def get_file(filename:str) -> Response:
    return send_from_directory(CommonConfig.TARGETS_UPLOADS_DIR, filename)


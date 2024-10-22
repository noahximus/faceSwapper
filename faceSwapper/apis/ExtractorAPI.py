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

logging.root.setLevel(logging.DEBUG)
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

        fileType = MediaUtils.is_image_or_video(file)
        faces = []

        try:
            if fileType == 'image':
                logger.debug(f'Reading image from file.')

                # Convert the uploaded file to an OpenCV image
                img = GalleryService.read_image_from_file(file)

                logger.debug(f'Extracting faces from image.')
                faces = GalleryService.extract_faces_from_image(img)

                logger.debug(f'There are {len(faces)} faces in the image.')

            elif fileType == 'video':
                logger.debug(f'Reading video from file.')

                # Save the uploaded video temporarily for processing
                video_filename = secure_filename(str(file.filename))
                video_file_path = f"/tmp/{video_filename}"  # Path to save the video temporarily
                file.save(video_file_path)

                logger.debug(f'Extracting faces from video.')
                faces = GalleryService.extract_faces_from_video(video_file_path)

                # Encode each face as base64 for JSON serialization
                faces = [MediaUtils.encode_face_as_base64(face) for face in faces]

                logger.debug(f'There are {len(faces)} faces in the video.')
                # Optionally, delete the video file after processing if not needed

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


# from flask import request, jsonify
#
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'videoFile' not in request.files:
#         return jsonify({'error': 'No video file uploaded'})
#
#     video_file = request.files['videoFile']
#
#     if video_file and allowed_file(video_file.filename, ['video']):
#         video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
#         video_file.save(video_path)
#
#         # Call your face extraction function
#         output_dir = "extracted_faces"
#         extract_faces_from_video(video_path, output_dir)
#
#         return jsonify({'success': 'Video processed and faces extracted'})
#     return jsonify({'error': 'Invalid file type'})
#
# def allowed_file(filename, file_type):
#     return filename.rsplit('.', 1)[1].lower() in ['mp4', 'mov', 'avi']  # Add other video formats if needed

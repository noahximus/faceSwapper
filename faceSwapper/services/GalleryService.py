
import requests
import numpy as np
import cv2
import os
from io import BytesIO
import base64
import logging

from typing import Dict, Any, Tuple
from faceSwapper.model.Analyzer import Analyzer
from faceSwapper.model.Swapper import Swapper

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from faceSwapper.commons.config import CommonConfig

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

ANALYZER = Analyzer.FACE_ANALYZER
SWAPPER = Swapper.get_face_swapper()

def download_image_from_url(image_url):
    """Download an image from a given URL."""
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = np.asarray(bytearray(response.content), dtype="uint8")
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        return image
    else:
        raise ValueError("Failed to download image from URL")

def read_image_from_file(file):
    """Convert an uploaded file to an OpenCV image."""
    image_stream = BytesIO(file.read())
    image_array = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

def read_image_from_file_path(file_path):
    """Convert an image from a file path to an OpenCV image."""
    # Read the image from the file path as binary data
    with open(file_path, 'rb') as f:
        image_data = f.read()

    # Convert the image data to a NumPy array
    image_array = np.asarray(bytearray(image_data), dtype=np.uint8)

    # Decode the NumPy array into an OpenCV image
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Check if the image was successfully loaded
    if image is None:
        raise ValueError(f"Could not load image from file: {file_path}")

    return image

def extract_faces_from_image(image):
    """Extract faces from the provided image and return them as a list of base64-encoded images."""
    faces = ANALYZER.get(image)
    faces = sorted(faces, key = lambda x : x.bbox[0])
    extracted_faces = []
    
    # Extract and return each face in the image
    for face in faces:
        # Crop the face from the original image using the face bounding box
        x1, y1, x2, y2 = map(int, face.bbox)
        cropped_face = image[y1:y2, x1:x2]

        # Encode the cropped face to base64
        _, buffer = cv2.imencode('.jpg', cropped_face)
        face_base64 = base64.b64encode(buffer).decode('utf-8')

        # Append the base64-encoded face to the result list
        extracted_faces.append(face_base64)

    return extracted_faces

def extract(file: FileStorage, uploadType: str|None) -> Tuple[Dict[str, Any], int]:

    try:
        logger.debug(f'Reading image from file.')

        # Convert the uploaded file to an OpenCV image
        img = read_image_from_file(file)
        logger.debug(f'Extracting faces from image.')

        # Extract faces using the reusable extract_faces method
        faces = extract_faces(img)
        logger.debug(f'There are {len(faces)} faces in the image.')
    except Exception as e:
        return {"error": str(e)}, 500

    return {
        "filename": secure_filename(str(file.filename)),
        "uploadType": uploadType,
        "image_url": f'{CommonConfig.UPLOADS_URL}/{secure_filename(str(file.filename))}',
        "faces": faces,
    }, 200



def extract_faces_from_video(video_file_path: str):
    video_path = video_file_path
    cap = cv2.VideoCapture(video_path)

    # Initialize the face detector (can be dlib or OpenCV's CascadeClassifier)
    face_cascade = cv2.CascadeClassifier(str(CommonConfig.TARGETS_MODELS_DIR.joinpath('haarcascade_frontalface_default.xml')))

    frame_number = 0
    extracted_faces = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Exit when the video ends

        frame_number += 1
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_image = frame[y:y + h, x:x + w]
            extracted_faces.append(face_image)

    cap.release()
    cv2.destroyAllWindows()
    return extracted_faces


def reassemble_video(processed_frames_dir, output_video_path, frame_size, fps=24):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

    # List the processed frames in order
    frame_files = sorted([f for f in os.listdir(processed_frames_dir) if f.endswith(".jpg")])

    for frame_file in frame_files:
        frame = cv2.imread(os.path.join(processed_frames_dir, frame_file))
        video_writer.write(frame)

    video_writer.release()
    print(f"Video saved to {output_video_path}")



# # Example usage:
# video_path = "path/to/your/video.mp4"
# output_dir = "extracted_faces"
# extract_faces_from_video(video_path, output_dir)

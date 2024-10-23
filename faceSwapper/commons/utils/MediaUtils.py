
import os
import logging
import numpy as np
import cv2
import base64
import mimetypes

from faceSwapper.commons.config import CommonConfig
from faceSwapper.commons.utils import FileUtils as FileUtils


logger = logging.getLogger(__name__)


# Function to check if the file extension is allowed
def is_allowed_filename_ext(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in CommonConfig.ALLOWED_UPLOAD_FILE_EXTENSIONS


def is_file_in_path_image(path: str) -> bool:
    return is_file_in_path_of_type(path,'image/')


def is_file_in_path_video(path: str) -> bool:
    return is_file_in_path_of_type(path,'video/')


def is_file_in_path_of_type(file_path: str, file_type_prefix: str) -> bool:
    if file_path and os.path.isfile(file_path):
        mimetype, _ = mimetypes.guess_type(file_path)
        return bool(mimetype and mimetype.startswith(file_type_prefix))
    return False


def is_image(file):
    mime_type = file.mimetype
    return mime_type.startswith('image')


def is_video(file):
    mime_type = file.mimetype
    return mime_type.startswith('video')


# Function to encode an OpenCV image back to base64
# def encode_face_as_base64(face):
def convert_cv2_image_to_base64_URI_string(image):
    """
    Encode a face image (NumPy array) as a base64 string.
    Ensure the image is a valid NumPy array and has type uint8.
    """
    base64_image = convert_cv2_image_to_base64(image)
    return f"data:image/jpeg;base64,{base64_image}"
    # return base64_image

def convert_cv2_image_to_base64(image):
    """
    Encode a face image (NumPy array) as a base64 string.
    Ensure the image is a valid NumPy array and has type uint8.
    """
    if image is None or image.size == 0:
        raise ValueError("Cannot encode an empty or invalid image.")
    
    # Ensure the image is of type uint8
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)

    success, buffer = cv2.imencode('.jpg', image) # Encode the image into a base64 string
    if not success:
        raise ValueError("Failed to encode image using imencode.")
    
    base64_image = base64.b64encode(buffer).decode('utf-8')
    # return f"data:image/jpeg;base64,{base64_image}"
    return base64_image



# def encode_face_as_base64_old(face):
#     """
#     Encode a face image (NumPy array) as a base64 string.
#     Ensure the image is a valid NumPy array and has type uint8.
#     """
#     if face is None or face.size == 0:
#         raise ValueError("Cannot encode an empty or invalid image.")
#
#     # Ensure the image is of type uint8
#     if face.dtype != np.uint8:
#         face = face.astype(np.uint8)
#
#     # Encode the face image into a base64 string
#     success, buffer = cv2.imencode('.jpg', face)
#
#     if not success:
#         raise ValueError("Failed to encode image using imencode.")
#
#     face_base64 = base64.b64encode(buffer).decode('utf-8')
#     return face_base64


# Function to convert file or base64 string to OpenCV image
def convert_base64_to_cv2_image(file_data):
    """Convert an uploaded file to an OpenCV image."""
    if isinstance(file_data, str) and file_data.startswith("data:image"):
        # Base64 string handling
        image_data = base64.b64decode(file_data.split(",")[1]) # Decode the base64 string to bytes
        np_array = np.frombuffer(image_data, np.uint8) # Convert bytes to a NumPy array (image)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR) # Decode the image
    else:
        # File handling (assuming file_data is a binary file-like object)
        np_array = np.frombuffer(file_data.read(), np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return image


def get_frame_count(video_file_path):
    # Open the video file
    cap = cv2.VideoCapture(video_file_path)

    # Check if the video was successfully opened
    if not cap.isOpened():
        raise ValueError(f"Error: Could not open video file {video_file_path}")

    # Get the total number of frames in the video
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Release the video capture object
    cap.release()

    return frame_count


def jump_to_frame_by_time(video_file_path, time):
    # Open the video file
    cap = cv2.VideoCapture(video_file_path)

    logger.debug(f'time: {time}')
    
    if not cap.isOpened():
        raise ValueError(f"Error: Could not open video file {video_file_path}")

    # Set the position to the halfway time
    cap.set(cv2.CAP_PROP_POS_MSEC, time)

    # Read the frame at the halfway point
    ret, frame = cap.read()
    
    # Release the video capture object and close display window
    cap.release()
    cv2.destroyAllWindows()

    return ret, frame

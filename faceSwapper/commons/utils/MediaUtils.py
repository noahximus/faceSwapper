
import os
import logging
import numpy as np
import cv2
import base64

from PIL import Image

from faceSwapper.commons.config import CommonConfig
from faceSwapper.commons.utils import FileUtils as FileUtils

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# Function to check if the file extension is allowed
def is_allowed_image_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in CommonConfig.ALLOWED_UPLOAD_FILE_EXTENSIONS

def is_image(image_path: str) -> bool:
    return FileUtils.is_file_type(image_path,'image/')

def is_video(video_path: str) -> bool:
    return FileUtils.is_file_type(video_path,'video/')

# Verify that the file is indeed an image
def is_image_file(file):
    is_true_image = False
    file_path = os.path.abspath(file)

    logger.debug(f'file_path: {file_path}')
    try:
        img = Image.open(file_path)
        img.verify()  # Verify that this is an actual image
        is_true_image = True
    except (IOError, SyntaxError):
        os.remove(file_path)

    return is_true_image

# Function to convert the file to an OpenCV image
def convert_file_to_opencv_image(file):
    # Read the file into a NumPy array
    np_array = np.frombuffer(file.read(), np.uint8)
    
    # Decode the NumPy array to an OpenCV image
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    return img

# Function to decode base64 string into an OpenCV image
def base64_to_cv2_image(base64_string):
    # Remove the data:image/jpeg;base64, or data:image/png;base64, part if it's present
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]
    
    # Decode the base64 string to bytes
    image_data = base64.b64decode(base64_string)

    # Convert the bytes data to a NumPy array
    np_array = np.frombuffer(image_data, np.uint8)

    # Decode the NumPy array to an OpenCV image
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    return img

# Function to encode an OpenCV image back to base64
def cv2_image_to_base64(cv2_image):
    _, buffer = cv2.imencode('.jpg', cv2_image)
    base64_image = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{base64_image}"

# Function to convert file or base64 string to OpenCV image
def convert_file_to_cv2_image(file_data):
    """Convert an uploaded file to an OpenCV image."""
    if isinstance(file_data, str) and file_data.startswith("data:image"):
        # Base64 string handling
        image_data = base64.b64decode(file_data.split(",")[1])
        np_array = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    else:
        # File handling (assuming file_data is a binary file-like object)
        np_array = np.frombuffer(file_data.read(), np.uint8)
        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return img

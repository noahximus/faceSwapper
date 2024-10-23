
import os
import logging
import numpy as np
import cv2
import base64

from PIL import Image

from faceSwapper.commons.config import CommonConfig
from faceSwapper.commons.utils import FileUtils as FileUtils

# logging.root.setLevel(logging.DEBUG)
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

def is_image_or_video(file):
    mime_type = file.mimetype
    if mime_type.startswith('image'):
        return 'image'
    elif mime_type.startswith('video'):
        return 'video'
    else:
        return 'unknown'

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


def convert_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{img_base64}"


def base64_to_numpy(base64_string):
    # Remove header if present
    if "base64," in base64_string:
        base64_string = base64_string.split(",")[1]
    
    # Decode the base64 string to bytes
    image_bytes = base64.b64decode(base64_string)
    
    # Convert bytes to a NumPy array (image)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    
    # Decode the image
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise ValueError("Image decoding failed")
    
    return image


def encode_face_as_base64_old(face):
    _, buffer = cv2.imencode('.jpg', face)  # Encode face as a JPEG image
    face_base64 = base64.b64encode(buffer).decode('utf-8')  # Convert to base64 string
    return face_base64

def encode_face_as_base64(face):
    """
    Encode a face image (NumPy array) as a base64 string.
    Ensure the image is a valid NumPy array and has type uint8.
    """
    if face is None or face.size == 0:
        raise ValueError("Cannot encode an empty or invalid image.")
    
    # Ensure the image is of type uint8
    if face.dtype != np.uint8:
        face = face.astype(np.uint8)

    # Encode the face image into a base64 string
    success, buffer = cv2.imencode('.jpg', face)
    
    if not success:
        raise ValueError("Failed to encode image using imencode.")
    
    face_base64 = base64.b64encode(buffer).decode('utf-8')
    return face_base64

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


def jump_to_frame(video_file_path, position):
    # Open the video file
    cap = cv2.VideoCapture(video_file_path)
    
    if not cap.isOpened():
        raise ValueError(f"Error: Could not open video file {video_file_path}")

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate the halfway point
    # halfway_frame = total_frames // 2

    # Set the position to the halfway frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, position)

    # Read the frame at the halfway point
    ret, frame = cap.read()
    
    if ret:
        # Display the halfway frame
        cv2.imshow('Halfway Frame', frame)
        cv2.waitKey(0)  # Wait until a key is pressed
    else:
        print("Error: Could not retrieve the frame.")
    
    # Release the video capture object and close display window
    cap.release()
    cv2.destroyAllWindows()

def jump_to_frame_by_time(video_file_path, time_slice):
    # Open the video file
    cap = cv2.VideoCapture(video_file_path)

    logger.debug(f'time_slice: {time_slice}')
    
    if not cap.isOpened():
        raise ValueError(f"Error: Could not open video file {video_file_path}")

    # Get the total duration of the video (in milliseconds)
    total_duration = cap.get(cv2.CAP_PROP_POS_MSEC)
    
    # Calculate the halfway time (in milliseconds)
    # target_time = total_duration * time_slice

    # Set the position to the halfway time
    cap.set(cv2.CAP_PROP_POS_MSEC, time_slice)

    # Read the frame at the halfway point
    ret, frame = cap.read()
    
    # if ret:
    #     # Display the halfway frame
    #     cv2.imshow('Halfway Frame by Time', frame)
    #     cv2.waitKey(0)  # Wait until a key is pressed
    # else:
    #     print("Error: Could not retrieve the frame.")
    
    # Release the video capture object and close display window
    cap.release()
    cv2.destroyAllWindows()

    return ret, frame


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
from faceSwapper.commons.utils import MediaUtils

# logging.root.setLevel(logging.DEBUG)
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
        faces = extract_faces_from_image(img)
        logger.debug(f'There are {len(faces)} faces in the image.')
    except Exception as e:
        return {"error": str(e)}, 500

    return {
        "filename": secure_filename(str(file.filename)),
        "uploadType": uploadType,
        "image_url": f'{CommonConfig.UPLOADS_URL}/{secure_filename(str(file.filename))}',
        "faces": faces,
    }, 200



# def extract_faces_from_video(video_file_path: str):
#     video_path = video_file_path
#     cap = cv2.VideoCapture(video_path)
#
#     # Initialize the face detector (can be dlib or OpenCV's CascadeClassifier)
#     face_cascade = cv2.CascadeClassifier(str(CommonConfig.TARGETS_MODELS_DIR.joinpath('haarcascade_frontalface_default.xml')))
#
#     frame_number = 0
#     extracted_faces = []
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break  # Exit when the video ends
#
#         frame_number += 1
#         gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
#
#         for (x, y, w, h) in faces:
#             face_image = frame[y:y + h, x:x + w]
#             extracted_faces.append(face_image)
#
#     cap.release()
#     cv2.destroyAllWindows()
#     return extracted_faces


# def reassemble_video(processed_frames_dir, output_video_path, frame_size, fps=24):
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)
#
#     # List the processed frames in order
#     frame_files = sorted([f for f in os.listdir(processed_frames_dir) if f.endswith(".jpg")])
#
#     for frame_file in frame_files:
#         frame = cv2.imread(os.path.join(processed_frames_dir, frame_file))
#         video_writer.write(frame)
#
#     video_writer.release()
#     print(f"Video saved to {output_video_path}")



# # Example usage:
# video_path = "path/to/your/video.mp4"
# output_dir = "extracted_faces"
# extract_faces_from_video(video_path, output_dir)

import cv2
import dlib
import base64
import numpy as np

from sklearn.cluster import KMeans

# Initialize dlib's face detector (HOG-based) and facial embedding model
face_detector = dlib.get_frontal_face_detector()
face_recognizer = dlib.face_recognition_model_v1(str(CommonConfig.TARGETS_MODELS_DIR.joinpath("dlib_face_recognition_resnet_model_v1.dat")))
shape_predictor = dlib.shape_predictor(str(CommonConfig.TARGETS_MODELS_DIR.joinpath('shape_predictor_68_face_landmarks.dat')))


# def encode_face_as_base64(face):
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

def get_face_embedding(img, face):
    """
    Extract the facial embedding from the given face.
    """
    landmarks = shape_predictor(img, face)  # Get the facial landmarks
    embedding = face_recognizer.compute_face_descriptor(img, landmarks)  # Compute embedding
    return np.array(embedding)

def extract_faces_from_video(video_file_path):
    """
    Extract unique faces from a video, encode them in base64, and return the list.
    """
    cap = cv2.VideoCapture(video_file_path)
    
    if not cap.isOpened():
        raise ValueError(f"Error: Could not open video file {video_file_path}")

    face_embeddings = []  # To store facial embeddings (for uniqueness check)
    face_base64_images = []  # To store unique face images as base64 strings

    # frame_count = MediaUtils.get_frame_count(video_file_path)
    logger.debug(f'Frame Count: {cap.get(cv2.CAP_PROP_FRAME_COUNT)}')

    # Alternatively, you can get the duration using cv2.CAP_PROP_POS_MSEC
    # cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)  # Move to the end of the video
    # total_duration_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))  # Total duration in milliseconds
    # duration_seconds_msec = total_duration_ms / 1000  # Convert milliseconds to seconds
   


    frame_number = 0
    # for time_slice in range(0, total_duration_ms, CommonConfig.VIDEO_SLICES):

    # Get the total number of frames and FPS
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # Calculate the duration in milliseconds
    duration_ms = (total_frames / fps) * 1000
    logger.debug(f'total_duration_ms: {duration_ms}')
    logger.debug(f'total_duration_s: {duration_ms/1000}')

    skips_in_ms = CommonConfig.SKIPS_IN_SECS * 1000

    if duration_ms < skips_in_ms:
        skips_in_ms = int(duration_ms / 3)

    
    logger.debug(f'skips in ms: {skips_in_ms}')

    # Generate x evenly spaced numbers between 0 and 1
    # for time_slice in np.linspace(0, 1, int(video_slices)):
    # Iterate from 0 to max_milliseconds with a step of 5000 milliseconds (5 seconds)
    for time_slice in range(0, int(duration_ms) + 1, skips_in_ms):

        ret, frame = MediaUtils.jump_to_frame_by_time(video_file_path, time_slice)

        logger.debug(f"###### {frame_number}/{time_slice} Current face count: {len(face_base64_images)}")

        # Check if frame is properly loaded
        if not ret or frame is None or frame.size == 0:
            logger.error("Error: Empty frame captured or end of video.")
            break
        
        # Detect faces in the frame
        faces = face_detector(frame)

        for face in faces:
            # Extract the face region from the frame
            x, y, w, h = (face.left(), face.top(), face.width(), face.height())
            
            # Check if face dimensions are valid
            if w <= 0 or h <= 0 or x < 0 or y < 0 or (x + w) > frame.shape[1] or (y + h) > frame.shape[0]:
                logger.debug(f"Invalid face region detected at (x={x}, y={y}, w={w}, h={h}). Skipping...")
                continue
            
            face_image = frame[y:y + h, x:x + w]

            # Ensure the extracted face region is valid
            if face_image is None or face_image.size == 0:
                logger.debug(f"Invalid face extracted at (x={x}, y={y}, w={w}, h={h}). Skipping...")
                continue

            # Get the face embedding
            embedding = get_face_embedding(frame, face)

            # Check if this face is unique based on the embeddings
            if not is_duplicate(embedding, face_embeddings):
                face_embeddings.append(embedding)
                
                # Encode the face as base64
                face_base64 = MediaUtils.encode_face_as_base64(face_image)
                face_base64_images.append(face_base64)

        # logger.debug(f"Current face count: {len(face_base64_images)}")

        # if len(face_base64_images) >= CommonConfig.EXTRACT_COUNT:
        #     logger.info("Reached desired face count")
        #     break

        frame_number = frame_number + 1

    cap.release()
    cv2.destroyAllWindows()

    # Return unique faces encoded in base64
    return face_base64_images

def is_duplicate(new_embedding, existing_embeddings, threshold=0.6):
    """
    Check if a new face embedding is a duplicate based on Euclidean distance.
    """
    from scipy.spatial.distance import euclidean
    
    for existing_embedding in existing_embeddings:
        if euclidean(new_embedding, existing_embedding) < threshold:
            return True  # Found a duplicate
    
    return False  # No duplicates found


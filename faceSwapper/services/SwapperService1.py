import logging
import cv2
import base64
import os

import concurrent.futures

from faceSwapper.model.Analyzer import Analyzer as Analyzer
from faceSwapper.model.Swapper import Swapper as Swapper
from faceSwapper.commons.utils import MediaUtils as MediaUtils

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

ANALYZER = Analyzer.FACE_ANALYZER
SWAPPER = Swapper.get_face_swapper()

sampleSourceImages = [
    "data:image/jpeg;base64,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",
    "data:image/jpeg;base64,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",
]

sampleTargetImages = [
    "data:image/jpeg;base64,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",
    "data:image/jpeg;base64,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",
]

# Function for swapping faces using the InsightFace swapper model
def swap_faces1(source_file , target_file, sourceGalleryOrder, targetGalleryOrder) -> str:
    """Perform face swapping between source and target image."""
    # Convert files to OpenCV images
    source_img = MediaUtils.convert_file_to_cv2_image(source_file)
    target_img = MediaUtils.convert_file_to_cv2_image(target_file)


    # Detect faces in both source and target images
    source_faces = ANALYZER.get(source_img)
    source_faces = sorted(source_faces, key = lambda x : x.bbox[0])
    target_faces = ANALYZER.get(target_img)
    target_faces = sorted(target_faces, key = lambda x : x.bbox[0])

    if not source_faces or not target_faces:
        raise ValueError("No faces detected in one or both images.")

    faceCountToSwap = min(len(sourceGalleryOrder), len(targetGalleryOrder))
    logger.debug(f'faceCountToSwap is {faceCountToSwap}')
    logger.debug(f'sourceGalleryOrder is {sourceGalleryOrder}')
    logger.debug(f'targetGalleryOrder is {targetGalleryOrder}')

    result = target_img
    for i in range(faceCountToSwap):
        logger.debug(f'sourceGalleryOrder[{i}] is {sourceGalleryOrder[i]}')
        logger.debug(f'targetGalleryOrder[{i}] is {targetGalleryOrder[i]}')

        # Use the first face from both the source and target for swapping
        source_face = source_faces[int(sourceGalleryOrder[i])]
        target_face = target_faces[int(targetGalleryOrder[i])]

        # if source_face is None:
        #     logger.debug(f'source_face is {source_face}')

        try:
            logger.debug(f'About to swap [{i}] : {sourceGalleryOrder[i]} --> {targetGalleryOrder[i]}')
            result = SWAPPER.get(result, target_face, source_face, paste_back=True)
            logger.debug(f'Done swapping [{i}] : {sourceGalleryOrder[i]} --> {targetGalleryOrder[i]}')
        except Exception as e:
            logger.error(f'Face swapping failed: {str(e)}')
            return ''

    # Optionally return a base64-encoded string for frontend rendering
    _, buffer = cv2.imencode('.jpg', result)
    result_base64 = base64.b64encode(buffer).decode('utf-8')

    return f"data:image/jpeg;base64,{result_base64}"

# Externalized function to swap a single pair of faces
def swap_single_face(i, source_faces, target_faces, sourceGalleryOrder, targetGalleryOrder, result):
    """Swaps a single pair of faces between the source and target."""
    source_face = source_faces[int(sourceGalleryOrder[i])]
    target_face = target_faces[int(targetGalleryOrder[i])]
    logger.debug(f'About to swap [{i}] : {sourceGalleryOrder[i]} --> {targetGalleryOrder[i]}')

    try:
        # Since we're working in parallel, make sure to copy the result image
        swapped_result = SWAPPER.get(result.copy(), target_face, source_face, paste_back=True)
        logger.debug(f'Done swapping [{i}] : {sourceGalleryOrder[i]} --> {targetGalleryOrder[i]}')
        return swapped_result
    except Exception as e:
        logger.error(f'Face swapping failed for [{i}]: {str(e)}')
        return None

# Function for swapping faces using the InsightFace swapper model
def swap_faces(source_file, target_file, sourceGalleryOrder, targetGalleryOrder) -> str:
    """Perform face swapping between source and target image."""
    # Convert files to OpenCV images
    source_img = MediaUtils.convert_file_to_cv2_image(source_file)
    target_img = MediaUtils.convert_file_to_cv2_image(target_file)

    # Detect faces in both source and target images
    source_faces = ANALYZER.get(source_img)
    source_faces = sorted(source_faces, key=lambda x: x.bbox[0])
    target_faces = ANALYZER.get(target_img)
    target_faces = sorted(target_faces, key=lambda x: x.bbox[0])

    if not source_faces or not target_faces:
        raise ValueError("No faces detected in one or both images.")

    faceCountToSwap = min(len(sourceGalleryOrder), len(targetGalleryOrder))
    logger.debug(f'faceCountToSwap is {faceCountToSwap}')
    logger.debug(f'sourceGalleryOrder is {sourceGalleryOrder}')
    logger.debug(f'targetGalleryOrder is {targetGalleryOrder}')

    result = target_img

    # Use ProcessPoolExecutor to take advantage of multiple CPU cores
    cpu_cores = os.cpu_count()  # Get the number of available CPU cores
    logger.debug(f'Available CPU cores: {cpu_cores}')

    # Process each face swap in parallel using ProcessPoolExecutor
    with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_cores) as executor:
        futures = [executor.submit(swap_single_face, i, source_faces, target_faces, sourceGalleryOrder, targetGalleryOrder, result) for i in range(faceCountToSwap)]

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            swapped_result = future.result()
            if swapped_result is not None:
                result = swapped_result  # Update the result image with the latest swap
            else:
                logger.error(f'Skipping update for face [{i}] due to error')

    # Optionally return a base64-encoded string for frontend rendering
    _, buffer = cv2.imencode('.jpg', result)
    result_base64 = base64.b64encode(buffer).decode('utf-8')

    return f"data:image/jpeg;base64,{result_base64}"

# Function for swapping faces using the InsightFace swapper model
def swap_faces_2(source_file, target_file, sourceGalleryOrder, targetGalleryOrder) -> str:
    """Perform face swapping between source and target image."""
    # Convert files to OpenCV images
    source_img = MediaUtils.convert_file_to_cv2_image(source_file)
    target_img = MediaUtils.convert_file_to_cv2_image(target_file)

    # Detect faces in both source and target images
    source_faces = ANALYZER.get(source_img)
    source_faces = sorted(source_faces, key=lambda x: x.bbox[0])
    target_faces = ANALYZER.get(target_img)
    target_faces = sorted(target_faces, key=lambda x: x.bbox[0])

    if not source_faces or not target_faces:
        raise ValueError("No faces detected in one or both images.")

    faceCountToSwap = min(len(sourceGalleryOrder), len(targetGalleryOrder))
    logger.debug(f'faceCountToSwap is {faceCountToSwap}')
    logger.debug(f'sourceGalleryOrder is {sourceGalleryOrder}')
    logger.debug(f'targetGalleryOrder is {targetGalleryOrder}')

    result = target_img

    # Process each face swap in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(swap_single_face, i, source_faces, target_faces, sourceGalleryOrder, targetGalleryOrder, result) for i in range(faceCountToSwap)]
        
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            swapped_result = future.result()
            if swapped_result is not None:
                result = swapped_result
            else:
                logger.error(f'Skipping update for face [{i}] due to error')

    # Optionally return a base64-encoded string for frontend rendering
    _, buffer = cv2.imencode('.jpg', result)
    result_base64 = base64.b64encode(buffer).decode('utf-8')

    return f"data:image/jpeg;base64,{result_base64}"

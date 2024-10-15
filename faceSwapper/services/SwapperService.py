import os
import cv2
import base64
import logging
import traceback

import concurrent.futures
import numpy as np

from typing import Tuple, List

from faceSwapper.commons.config import CommonConfig
from faceSwapper.model.Analyzer import Analyzer
from faceSwapper.model.Swapper import Swapper
from faceSwapper.commons.utils import MediaUtils

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

ANALYZER = Analyzer.FACE_ANALYZER
SWAPPER = Swapper.get_face_swapper()

# Externalized function to swap a single pair of faces
def swap_single_face(
    i, source_faces, target_faces, sourceGalleryOrder, targetGalleryOrder, result
):
    """Swaps a single pair of faces between the source and target."""
    source_face = source_faces[int(sourceGalleryOrder[i])]
    target_face = target_faces[int(targetGalleryOrder[i])]

    try:
        logger.debug(f'About to swap [{i}] : {sourceGalleryOrder[i]} --> {targetGalleryOrder[i]}')
        # Since we're working in parallel, make sure to copy the result image
        swapped_result = SWAPPER.get(result, target_face, source_face, paste_back=True)
        logger.debug(f'Done swapping [{i}] : {sourceGalleryOrder[i]} --> {targetGalleryOrder[i]}')
        return swapped_result
    except Exception as e:
        logger.error(f'Face swapping failed for [{i}]: {str(e)}')
        logger.error(f'Traceback: {traceback.format_exc()}')
        logger.debug(f"Target face landmarks: {target_face.kps}")
        logger.debug(f"Landmarks shape: {target_face.kps.shape}")
        return None


def process_face_swap(
    source_file, target_file, source_file_name, target_file_name, source_gallery_order, target_gallery_order,
) -> Tuple[np.ndarray, List[int], List[int], int]:

    """Common logic for face swapping between source and target images."""

    # Convert files to OpenCV images
    source_img = MediaUtils.convert_file_to_cv2_image(source_file)
    target_img = MediaUtils.convert_file_to_cv2_image(target_file)

    # source_file_path = CommonConfig.TARGETS_UPLOADS_DIR.joinpath(source_file_name)
    # target_file_path = CommonConfig.TARGETS_UPLOADS_DIR.joinpath(target_file_name)
    # source_img = cv2.imread(str(source_file_path))
    # target_img = cv2.imread(str(target_file_path))

    # Detect faces in both source and target images
    source_faces = ANALYZER.get(source_img)
    source_faces = sorted(source_faces, key=lambda x: x.bbox[0])
    target_faces = ANALYZER.get(target_img)
    target_faces = sorted(target_faces, key=lambda x: x.bbox[0])

    if not source_faces or not target_faces:
        raise ValueError("No faces detected in one or both images.")

    face_count_to_swap = min(len(source_gallery_order), len(target_gallery_order))
    logger.debug(f'faceCountToSwap is {face_count_to_swap}')
    logger.debug(f'sourceGalleryOrder is {source_gallery_order}')
    logger.debug(f'targetGalleryOrder is {target_gallery_order}')

    return target_img, source_faces, target_faces, face_count_to_swap


# Function for swapping faces using the InsightFace swapper model
def swap_faces_sync(
    source_file, source_file_name, source_gallery_order,
    target_file, target_file_name, target_gallery_order,
) -> str:

    """Perform face swapping between source and target image."""

    target_img, source_faces, target_faces, face_count_to_swap = process_face_swap(
        source_file, target_file, source_file_name, target_file_name, source_gallery_order, target_gallery_order
    )
    result = target_img
    for i in range(face_count_to_swap):
        logger.debug(f'sourceGalleryOrder[{i}] is {source_gallery_order[i]}')
        logger.debug(f'targetGalleryOrder[{i}] is {target_gallery_order[i]}')

        # Call the externalized swap_single_face function for each pair of faces
        swapped_result = swap_single_face(i, source_faces, target_faces, source_gallery_order, target_gallery_order, result)
        
        if swapped_result is not None:
            result = swapped_result  # Update the result image with the latest swap
        else:
            logger.error(f'Skipping face [{i}] due to error during face swapping')

    return MediaUtils.convert_to_base64(result)


def choose_executor(use_process_pool):
    """Helper function to choose the appropriate executor."""
    if use_process_pool:
        cpu_cores = os.cpu_count()  # Get the number of available CPU cores
        logger.debug(f'Using ProcessPoolExecutor with {cpu_cores} cores')
        return concurrent.futures.ProcessPoolExecutor, {'max_workers': cpu_cores}
    else:
        logger.debug(f'Using ThreadPoolExecutor')
        return concurrent.futures.ThreadPoolExecutor, {}


def swap_faces_async(
    source_file_name, source_gallery_order,
    target_file_name, target_gallery_order,
    use_process_pool=False
) -> str:

    """Perform face swapping between source and target images, either synchronously or asynchronously."""
    
    target_img, source_faces, target_faces, face_count_to_swap = process_face_swap(
        source_file_name, target_file_name, source_gallery_order, target_gallery_order
    )
    result = target_img

    # If use_process_pool is set to True, use ProcessPoolExecutor, otherwise use ThreadPoolExecutor
    executor_class, executor_args = choose_executor(use_process_pool)

    # Process each face swap using the chosen executor (Thread or Process Pool)
    with executor_class(**executor_args) as executor:
        futures = [
            executor.submit(
                swap_single_face, i, source_faces, target_faces,
                source_gallery_order, target_gallery_order, result
            )
            for i in range(face_count_to_swap)
        ]
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            logger.debug(f'sourceGalleryOrder[{i}] is {source_gallery_order[i]}')
            logger.debug(f'targetGalleryOrder[{i}] is {target_gallery_order[i]}')

            swapped_result = future.result()
            if swapped_result is not None:
                result = swapped_result  # Update the result image with the latest swap
            else:
                logger.error(f'Skipping update for face [{i}] due to error')

    return MediaUtils.convert_to_base64(result)




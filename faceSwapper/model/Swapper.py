import logging

import threading
import insightface

from typing import Any, Tuple

# import cv2

from faceSwapper.commons.config import CommonConfig
from faceSwapper.commons.utils import CommonUtils
from faceSwapper.commons.utils import FileUtils

# logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


class Swapper:
    __THREAD_LOCK = threading.Lock()
    __IS_PRE_CHECKED = False

    FACE_SWAPPER = None

    # def __init__(self, source_path: str, target_path: str, sceneery_path: str):
    def __init__(self):
        logger.info(f'Initiating {__name__} ')

        # if not __IS_PRE_CHECKED and Swapper.__pre_check():
        #     Swapper.__load_model()

        logger.info(f'Done Initiating {__name__} ')


    def pre_check(self) -> Tuple[bool, str]:
        message = 'Swapper pre-check is successful.'
        if not Swapper.__IS_PRE_CHECKED:
            try:
                download_directory_path  = FileUtils.resolve_relative_path(CommonConfig.TARGETS_MODELS_DIR)
                CommonUtils.conditional_download(download_directory_path, [CommonConfig.SWAPPER_MODEL_URL])
                Swapper.__IS_PRE_CHECKED = True
            except Exception as e:
                # Handle or log the exception
                logger.error(f"Error during Swapper pre-check: {str(e)}")
                Swapper.__IS_PRE_CHECKED = False
                message = f'Swapper pre-check failed due to an error: {str(e)}'
        return Swapper.__IS_PRE_CHECKED, message


    @classmethod
    def get_face_swapper(cls) -> Any:
        """
        Class method to ensure FACE_SWAPPER is initialized without needing to instantiate Swapper.
        """
        if cls.FACE_SWAPPER is None:
            logger.info('FACE_SWAPPER is not initialized. Loading model...')
            cls.__load_model()
        return cls.FACE_SWAPPER


    @staticmethod
    def __load_model() -> Any:
        with Swapper.__THREAD_LOCK:
            if Swapper.FACE_SWAPPER is None:
                logger.info(f'Swapper model path: {FileUtils.resolve_relative_path(CommonConfig.SWAPPER_MODEL_PATH)}')
                Swapper.FACE_SWAPPER = insightface.model_zoo.get_model(
                    str(CommonConfig.SWAPPER_MODEL_PATH)
                    , providers=['CoreMLExecutionProvider', 'AzureExecutionProvider', 'CPUExecutionProvider']
                    # , providers=['CPUExecutionProvider'] # 8.35473895072937 secs - Blurred
                    # , providers=['CoreMLExecutionProvider'] # 8.8892662525177 secs
                )
        return Swapper.FACE_SWAPPER
    

    #
    # def swap_face(source_face: Face, target_face: Face, temp_frame: Frame) -> Frame:
    #     return get_face_swapper().get(temp_frame, target_face, source_face, paste_back=True)



import logging
import os
import threading
import insightface

from typing import Any, Tuple

from gfpgan import GFPGANer

from faceSwapper.commons.config import CommonConfig
from faceSwapper.commons.utils import CommonUtils
from faceSwapper.commons.utils import FileUtils

# logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# Set the cache directory for GFPGAN model downloads
os.environ['GFPGAN_CACHE_DIR'] = str(CommonConfig.TARGETS_MODELS_DIR)

class Enhancer:
    __THREAD_LOCK = threading.Lock()
    __IS_PRE_CHECKED = False

    IMAGE_ENHANCER = None

    def __init__(self):
        logger.info(f'Initiating {__name__} ')

        # if not __IS_PRE_CHECKED and Swapper.__pre_check():
        #     Swapper.__load_model()

        logger.info(f'Done Initiating {__name__} ')

    @classmethod
    def get_image_enhancer(cls) -> Any:
        """
        Class method to ensure FACE_SWAPPER is initialized without needing to instantiate Swapper.
        """
        if cls.IMAGE_ENHANCER is None:
            logger.info('IMAGE_ENHANCER is not initialized. Loading model...')
            cls.__load_model()
        return cls.IMAGE_ENHANCER

    @staticmethod
    def __load_model() -> Any:
        with Enhancer.__THREAD_LOCK:
            if Enhancer.IMAGE_ENHANCER is None:
                logger.info(f'Enhancer model path: {FileUtils.resolve_relative_path(CommonConfig.ENHANCER_MODEL_PATH)}')
                Enhancer.IMAGE_ENHANCER = GFPGANer(
                    model_path=str(CommonConfig.ENHANCER_MODEL_PATH),
                    upscale=2, arch='clean', channel_multiplier=2
                )
        return Enhancer.IMAGE_ENHANCER


    def pre_check(self) -> Tuple[bool, str]:
        message = 'Enhancer pre-check is successful.'
        if not Enhancer.__IS_PRE_CHECKED:
            try:
                download_directory_path  = FileUtils.resolve_relative_path(CommonConfig.TARGETS_MODELS_DIR)
                CommonUtils.conditional_download(download_directory_path, [CommonConfig.ENHANCER_MODEL_URL])
                Enhancer.__IS_PRE_CHECKED = True
            except Exception as e:
                # Handle or log the exception
                logger.error(f"Error during Enhancer pre-check: {str(e)}")
                Enhancer.__IS_PRE_CHECKED = False
                message = f'Enhancer pre-check failed due to an error: {str(e)}'
        return Enhancer.__IS_PRE_CHECKED, message

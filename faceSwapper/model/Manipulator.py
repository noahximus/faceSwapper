import sys
import logging
import shutil
import json
import threading

# from typing import Any, List
# import cv2
# import insightface


from visuals.facial.swapper.Swapper import Swapper

import visuals.commons.CommonConfig as CommonConfig
import visuals.commons.utils.FileUtils as FileUtils

FACE_SWAPPER = None
THREAD_LOCK = threading.Lock()

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


class Manipulator:

    # swapper = 

    def __init__(self):
        
        logger.debug(f'START')

        # swapper = Swapper()
        # swapper.pre_check()

        # if self.pre_check():
        #     logger.info(f'  ALL OK')
            
        logger.debug(f'END')


    def pre_check(self):
        message = 'Pre-check is successful.'
        status = 'success'
        # if sys.version_info < (3, 9):
        if sys.version_info < (3, 13):
            message = f'Python version {sys.version_info} is not supported - please upgrade to 3.9 or higher. {message}'
            status = 'error'

        if not shutil.which('ffmpeg'):
            message = f'ffmpeg is not installed. {message}'
            status = 'error'
            logger.error(f'{message}')

        return status, message


import sys
import logging
import shutil
import threading

FACE_SWAPPER = None
THREAD_LOCK = threading.Lock()

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


class Manipulator:

    def __init__(self):
        
        logger.debug(f'START')

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


import sys
import logging
import shutil
import threading

from typing import Any, Dict, Tuple

from flask import abort

from faceSwapper.model.Swapper import Swapper
from faceSwapper.model.Enhancer import Enhancer

FACE_SWAPPER = None
THREAD_LOCK = threading.Lock()

# logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


class FaceSwapper:
    __IS_PRE_CHECKED = False

    def __init__(self):
        logger.debug(f'START')

        logger.debug(f'END')

    def python_checked(self) -> Tuple[bool, str]:
        python_message = ''
        python_checked = True
        if sys.version_info < (3, 9):
            python_message = f'Python version {sys.version_info} is not supported - please upgrade to 3.9 or higher.'
            python_checked = False
        return python_checked, python_message


    def ffmpeg_checked(self) -> Tuple[bool, str]:
        ffmpeg_message = ''
        ffmpeg_checked = True
        if sys.version_info < (3, 9):
            ffmpeg_message = f'Python version {sys.version_info} is not supported - please upgrade to 3.9 or higher.'
            ffmpeg_checked = False
        return ffmpeg_checked, ffmpeg_message


    def dependencies_checked(self) -> Tuple[bool, str]:
        python_checked, python_message = self.python_checked()
        ffmpeg_checked, ffmpeg_message = self.ffmpeg_checked()

        dependencies_message = ' '.join([s for s, include in [(python_message, python_checked),
                                                              (ffmpeg_message, ffmpeg_checked)] if not include])

        dependencies_checked = python_checked and ffmpeg_checked

        return dependencies_checked, dependencies_message


    def is_checked(self) -> Tuple[bool, str]:
        dependencies_checked, dependencies_message = self.dependencies_checked()

        swapper = Swapper()
        swapper_checked, swapper_message = swapper.pre_check()
        enhancer = Enhancer()
        enhancer_checked, enhancer_message = enhancer.pre_check()

        message = ' '.join([s for s, include in [(dependencies_message, dependencies_checked), 
                                                (swapper_message, swapper_checked), 
                                                (enhancer_message, enhancer_checked)] if not include])
        FaceSwapper.__IS_PRE_CHECKED = dependencies_checked and swapper_checked and enhancer_checked

        return FaceSwapper.__IS_PRE_CHECKED, message


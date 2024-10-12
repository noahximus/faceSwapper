import logging

import insightface
from insightface.app import FaceAnalysis

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

assert insightface.__version__>='0.7'

class Analyzer():

    FACE_ANALYZER = FaceAnalysis(name='buffalo_l')
    FACE_ANALYZER.prepare(ctx_id=0, det_size=(640, 640))

    def __init__(self):
        logger.debug('START')



# -*- coding: utf-8 -*-
from __future__ import annotations

import logging

from flask import Blueprint, render_template
from flask_cors import CORS  # Import CORS

# from commons.utils.CommonUtils import 
from faceSwapper.commons.config import CommonConfig

from faceSwapper.model.Manipulator import Manipulator

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a Blueprint for the SwapperAPI
faceSwapper_routes = Blueprint('faceSwapper_routes', __name__)

CORS(faceSwapper_routes)  # Enable CORS for all routes

@faceSwapper_routes.route('/')
def index():
    logger.debug(f'Templates: {CommonConfig.USER_INTERFACE_WEB_TEMPLATES_DIR}')
    logger.debug(f'Statics: {CommonConfig.USER_INTERFACE_WEB_STATIC_DIR}')
    
    logger.debug(f'APPLICATION_URL: {CommonConfig.APPLICATION_URL}')
    logger.debug(f'UPLOAD_URL: {CommonConfig.UPLOAD_URL}')
    logger.debug(f'FACESWAP_URL: {CommonConfig.FACESWAP_URL}')

    manipulator = Manipulator()
    pre_check = manipulator.pre_check()

    if pre_check[0] == 'error':
        logger.error(f'Fatal Error: {pre_check[1]}')

    return render_template(
        'index.html',
        apiUrlForUploads=CommonConfig.UPLOAD_URL, # Pass API URL to template
        apiUrlForFaceSwap=CommonConfig.FACESWAP_URL, # Pass API URL to template
    )


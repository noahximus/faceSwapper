# -*- coding: utf-8 -*-
from __future__ import annotations

import logging

from flask import Blueprint, render_template, abort
from flask_cors import CORS  # Import CORS

# from commons.utils.CommonUtils import 
from faceSwapper.commons.config import CommonConfig

from faceSwapper.model.FaceSwapper import FaceSwapper
from faceSwapper.model.Swapper import Swapper

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

    faceSwapper = FaceSwapper()
    is_checked, message = faceSwapper.is_checked()

    if not is_checked:
        logger.error(f'Fatal Error: {message}')
        abort(500, description=f'FaceSwapper error: {message}')  # Abort if error occurs
    
    return render_template(
        'index.html',
        apiUrlForUploads=CommonConfig.UPLOAD_URL, # Pass API URL to template
        apiUrlForSwap=CommonConfig.SWAP_URL, # Pass API URL to template
        apiUrlForEnhance=CommonConfig.ENHANCE_URL, # Pass API URL to template
        apiUrlForFaceExtract=CommonConfig.EXTRACT_URL, # Pass API URL to template
    )

@faceSwapper_routes.errorhandler(500)
def internal_server_error(error):
    logger.error(f"Server error: {error}")
    return render_template('500.html', error=error), 500

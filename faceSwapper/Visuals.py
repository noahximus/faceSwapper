# -*- coding: utf-8 -*-
from __future__ import annotations

from os import wait
import sys
import subprocess
import logging
import json

from logging import Formatter, FileHandler

from flask import Flask, render_template, redirect, url_for, request
from flask_cors import CORS  # Import CORS

# from datetime import datetime

# from numpy import swapaxes

# from commons.utils.CommonUtils import 
from faceSwapper.commons.config import CommonConfig

from faceSwapper.apis.SwapperAPI import swapperAPI_routes
from faceSwapper.apis.UploadsAPI import uploadsAPI_routes

from faceSwapper.model.Manipulator import Manipulator

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(
    __name__, 
    template_folder=CommonConfig.USER_INTERFACE_WEB_TEMPLATES_DIR,
    static_folder=CommonConfig.USER_INTERFACE_WEB_STATIC_DIR
)
app.register_blueprint(swapperAPI_routes)
app.register_blueprint(uploadsAPI_routes)

CORS(app)  # Enable CORS for all routes


@app.route('/')
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

if __name__ == '__main__':
    #Setup the logger
    file_handler = FileHandler('output.log')
    handler = logging.StreamHandler()
    
    FORMAT = "['%(asctime)s - %(levelname)7s - %(filename)21s:%(lineno)3s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    
    file_handler.setLevel(logging.DEBUG)
    handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    handler.setFormatter(Formatter(
       '%(asctime)s %(levelname)s: %(message)s '
       '[in %(pathname)s:%(lineno)d]'
    ))
    # app.logger.addHandler(handler)
    # app.logger.addHandler(file_handler)
    # app.logger.error('first test message...')

    app.run(debug=True)
    # app.run(debug=False)


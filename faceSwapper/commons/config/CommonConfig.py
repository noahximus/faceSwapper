# -*- coding: utf-8 -*-
import yaml
from pathlib import Path

__CODE_LEVEL = 2
__CODE_LEVEL_PARENT = __CODE_LEVEL + 1
FILE_DIR = Path(__file__)  # This is the Project Root directory
PROJECT_ROOT_DIR = FILE_DIR.resolve().parents[__CODE_LEVEL]
PROJECT_ROOT_PARENT_DIR = FILE_DIR.resolve().parents[__CODE_LEVEL_PARENT]

__CONFIGURATION_FILE_NAME = 'config.yaml'
CONFIGURATION_FILE_PATH = PROJECT_ROOT_PARENT_DIR.joinpath(__CONFIGURATION_FILE_NAME)

# Load the configuration from the YAML file
with open(CONFIGURATION_FILE_PATH, 'r') as CONFIGURATION_FILE:
    CONFIGURATION = yaml.safe_load(CONFIGURATION_FILE)

APPLICATION_NAME = CONFIGURATION['application']['name']
APPLICATION_URL = CONFIGURATION['application']['url']

# UPLOADS URL
UPLOAD_URL =  CONFIGURATION['application']['uploader']['face_uploader']['url']
UPLOADS_URL =  CONFIGURATION['application']['uploader']['face_uploads']['url']
SWAP_URL = CONFIGURATION['application']['swapper']['face_swap']['url']
ENHANCE_URL = CONFIGURATION['application']['enhancer']['face_enhance']['url']
EXTRACT_URL = CONFIGURATION['application']['extractor']['face_extract']['url']

ALLOWED_UPLOAD_FILE_EXTENSIONS = CONFIGURATION['application']['uploader']['allowed_extensions']

# TARGETS related folders
TARGETS_DIR = PROJECT_ROOT_PARENT_DIR.joinpath(f'{APPLICATION_NAME}-targets')
TARGETS_MODELS_DIR = TARGETS_DIR.joinpath('models')
TARGETS_UPLOADS_DIR = TARGETS_DIR.joinpath('uploads')
TARGETS_OUTPUT_DIR= TARGETS_DIR.joinpath('output')
TARGETS_UPLOADS_SOURCE_DIR = TARGETS_UPLOADS_DIR.joinpath('source')
TARGETS_UPLOADS_TARGET_DIR = TARGETS_UPLOADS_DIR.joinpath('target')

# USER INTERFACE related folders
USER_INTERFACE_DIR = PROJECT_ROOT_PARENT_DIR.joinpath(f'{APPLICATION_NAME}-ui')
USER_INTERFACE_FACIAL_DIR = USER_INTERFACE_DIR.joinpath('facial')

# For WEB UI
USER_INTERFACE_WEB_DIR = USER_INTERFACE_DIR.joinpath('web')
USER_INTERFACE_WEB_TEMPLATES_DIR = USER_INTERFACE_WEB_DIR.joinpath('templates')
USER_INTERFACE_WEB_STATIC_DIR = USER_INTERFACE_WEB_DIR.joinpath('static')

# URL for inswapper and GFPGAN models
SWAPPER_MODEL_URL =  CONFIGURATION['application']['swapper']['model']['url']
SWAPPER_MODEL_NAME =  CONFIGURATION['application']['swapper']['model']['name']
SWAPPER_MODEL_PATH =  TARGETS_MODELS_DIR.joinpath(SWAPPER_MODEL_NAME)

ENHANCER_MODEL_URL = CONFIGURATION['application']['enhancer']['model']['url']
ENHANCER_MODEL_NAME =  CONFIGURATION['application']['enhancer']['model']['name']
ENHANCER_MODEL_PATH =  TARGETS_MODELS_DIR.joinpath(ENHANCER_MODEL_NAME)


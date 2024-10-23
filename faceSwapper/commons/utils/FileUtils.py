# -*- coding: utf-8 -*-
import os
import logging
import shutil
import mimetypes

from pathlib import Path

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


logger = logging.getLogger(__name__)


def create_directory(dir_path: str) -> bool:
    
    try:
        os.mkdir(dir_path)
    except OSError:
        logger.debug("Creation of the training_directory %s failed" % dir_path)
        return False
    else:
        logger.debug("Successfully created the training_directory %s " % dir_path)
    return True


def delete_directory(dir_path: str) -> bool:
    try:
        shutil.rmtree(dir_path)
    except OSError:
        logger.debug("Deletion of the directory %s failed" % dir_path)
        return False
    else:
        logger.debug("Successfully deleted the directory %s" % dir_path)
    return True


def resolve_relative_path(path: Path) -> Path:
    return Path(os.path.abspath(os.path.join(os.path.dirname(__file__), path)))


# Function to handle file upload
def save_file(file: FileStorage, upload_folder) -> Path:
    # Ensure the uploads directory exists
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filename = secure_filename(str(file.filename))
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return Path(file_path)


def uploaded_path(file_name: str, upload_folder) -> Path:
    filename = secure_filename(file_name)
    file_path = os.path.join(upload_folder, filename)
    return Path(file_path)


def file_type(file_path: str):
    mimetype, _ = mimetypes.guess_type(file_path)
    logger.debug(f'File mimetype: {mimetype}')
    return mimetype

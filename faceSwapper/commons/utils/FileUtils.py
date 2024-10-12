# -*- coding: utf-8 -*-
import os
import logging
import shutil
import mimetypes
import urllib.request

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from pathlib import Path
from typing import List
from tqdm import tqdm


logging.root.setLevel(logging.DEBUG)
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

def conditional_download(download_directory_path: Path, urls: List[str]) -> bool:
    if not os.path.exists(download_directory_path):
        logger.debug(f'Directory [ {download_directory_path} ] created.')
        os.makedirs(download_directory_path)
    
    for url in urls:
        download_file_path = os.path.join(download_directory_path, os.path.basename(url))
        
        if not os.path.exists(download_file_path):
            logger.debug(f'Downloading [ {url} ] into [ {download_directory_path} ] .')
            
            request = urllib.request.urlopen(url) # type: ignore[attr-defined]
            total = int(request.headers.get('Content-Length', 0))
            with tqdm(total=total, desc='Downloading', unit='B', unit_scale=True, unit_divisor=1024) as progress:
                urllib.request.urlretrieve(url, download_file_path, reporthook=lambda count, block_size, total_size: progress.update(block_size)) # type: ignore[attr-defined]

    return True

def resolve_relative_path(path: Path) -> Path:
    return Path(os.path.abspath(os.path.join(os.path.dirname(__file__), path)))

def is_file_type(file_path: str, file_type_prefix: str) -> bool:
    if file_path and os.path.isfile(file_path):
        mimetype, _ = mimetypes.guess_type(file_path)
        return bool(mimetype and mimetype.startswith(file_type_prefix))
    return False

def file_type(file_path: str):
    mimetype, _ = mimetypes.guess_type(file_path)
    logger.debug(f'File mimetype: {mimetype}')
    return mimetype

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

import os
import logging
import urllib.request

from typing import List
from tqdm import tqdm
from pathlib import Path

logger = logging.getLogger(__name__)


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


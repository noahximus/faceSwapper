import os
import mimetypes


def is_file_type(file_path: str, file_type_prefix: str) -> bool:
    if file_path and os.path.isfile(file_path):
        mimetype, _ = mimetypes.guess_type(file_path)
        return bool(mimetype and mimetype.startswith(file_type_prefix))
    return False

def is_image(image_path: str) -> bool:
    return is_file_type(image_path,'image/')

def is_video(video_path: str) -> bool:
    return is_file_type(video_path,'video/')


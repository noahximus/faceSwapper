
from faceSwapper.commons.config import CommonConfig

from werkzeug.utils import secure_filename

# Function to check if the file extension is allowed
def is_file_allowed(file) -> bool:
    return '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in CommonConfig.ALLOWED_UPLOAD_FILE_EXTENSIONS

def is_uploaded(file) -> bool:
   return file.filename != ''

def is_upload_valid(file) -> bool:
    return is_uploaded(file) and is_file_allowed(file)


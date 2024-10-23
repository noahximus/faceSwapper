from gfpgan import GFPGANer


from faceSwapper.commons.utils import MediaUtils
from faceSwapper.model.Enhancer import Enhancer

ENHANCER = Enhancer.get_image_enhancer()

def enhance_image(image):
    image = MediaUtils.convert_base64_to_cv2_image(image)

    # Perform enhancement
    _, _, enhanced_image = ENHANCER.enhance(image, has_aligned=False, only_center_face=False, paste_back=True)

    return MediaUtils.convert_cv2_image_to_base64_URI_string(enhanced_image)

from gfpgan import GFPGANer


from faceSwapper.commons.utils import MediaUtils
from faceSwapper.model.Enhancer import Enhancer

ENHANCER = Enhancer.get_image_enhancer()

def enhance_image(image):
    image = MediaUtils.base64_to_numpy(image)

    # Perform enhancement
    _, _, enhanced_image = ENHANCER.enhance(image, has_aligned=False, only_center_face=False, paste_back=True)

    return MediaUtils.convert_to_base64(enhanced_image)

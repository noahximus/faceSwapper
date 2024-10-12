import unittest

from faceSwapper.commons.utils import MediaUtils


class TestUtilities(unittest.TestCase):
   
    image_path = '/Users/noah/Pictures/DesktopBackground/hdDesktopBG/pexels-esra-salturk-1165434438-27524208.jpg'

    def test_image_filetype(self):
        assert MediaUtils.is_image(self.image_path) == True

    def test_video_filetype(self):
        assert MediaUtils.is_video(self. image_path) == False

if __name__ == "__main__":
    unittest.main()



import os
import pytest

from unittest.mock import patch, MagicMock
from faceSwapper.services import SwapperService


# Mock MediaUtils and ANALYZER dependencies
# @patch('faceSwapper.services.SwapperService.MediaUtils')
# @patch('faceSwapper.services.SwapperService.ANALYZER')
# def test_swap_faces_sync(mock_analyzer, mock_media_utils):
def test_swap_faces_sync(common_config):
    # Mock the behavior of the MediaUtils and ANALYZER for testing
    # mock_media_utils.load_image.return_value = MagicMock()  # Mocked image
    # mock_analyzer.get.return_value = [MagicMock(bbox=[0, 0, 100, 100])]  # Mocked face detection

    # Sample data for the test
    sample_data_dir = common_config["sample_data_dir"]
    source_file_name = os.path.join(sample_data_dir, 'source.jpg')
    source_gallery_order = [0, 1]
    target_file_name = os.path.join(sample_data_dir, 'target.jpg')
    target_gallery_order = [0, 1, 2, 3, 4, 5]

    # Call the function to test
    result = SwapperService.swap_faces_sync(
        source_file_name, source_gallery_order,
        target_file_name, target_gallery_order
    )

    # Assertions to verify correct behavior
    # mock_media_utils.load_image.assert_called_with(source_file_name)
    # mock_analyzer.get.assert_called()  # Ensure face detection was called
    assert result.startswith("data:image/jpeg;base64,")


# @patch('faceSwapper.services.SwapperService.MediaUtils')
# @patch('faceSwapper.services.SwapperService.ANALYZER')
# def test_swap_faces_async(mock_analyzer, mock_media_utils):
#     # Mock similar to synchronous test
#     mock_media_utils.load_image.return_value = MagicMock()
#     mock_analyzer.get.return_value = [MagicMock(bbox=[0, 0, 100, 100])]
#
#     # Reference the new location for your test data
#     source_file_name = os.path.join(SAMPLE_DATA_DIR, 'source.jpg')
#     target_file_name = os.path.join(SAMPLE_DATA_DIR, 'target.jpg')
#
#     # Sample data for the test
#     # source_file_name = 'data/source.jpg'
#     source_gallery_order = [0, 1]
#     # target_file_name = 'data/target.jpg'
#     target_gallery_order = [0, 1, 2, 3, 4, 5]
#
#     # Call the async version
#     result = SwapperService.swap_faces_async(
#         source_file_name, source_gallery_order,
#         target_file_name, target_gallery_order,
#         use_process_pool=False  # Testing with threads
#     )
#
#     assert result.startswith("data:image/jpeg;base64,")

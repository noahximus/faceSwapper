import pytest
import os

@pytest.fixture(scope="session")
def common_config():
    """Common configuration for all tests."""
    config = {
        "sample_data_dir": os.path.join(os.path.dirname(__file__), "data"),
        "max_face_count": 10,
        "some_other_config": "value"
    }
    return config

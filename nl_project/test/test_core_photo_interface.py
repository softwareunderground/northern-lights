from nl_project.data_layer.core_photo_interface import CorePhotoInterface
import numpy as np


class TestCorePhotoInterface:
    def test_get_photos_for_depth_range(self):
        interface = CorePhotoInterface('test_well')
        photos = interface.get_photos_for_depth_range(2592.5, 2649.0)
        if len(photos) < 5:
            raise Exception('Test Failed')

    def test_get_sample_at_depth(self):
        interface = CorePhotoInterface('test_well')
        photo_sample = interface.get_sample_at_depth(2593.1)
        if not isinstance(photo_sample, np.ndarray):
            raise Exception('Test Failed')


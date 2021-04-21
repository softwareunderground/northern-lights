from nl_project.data_layer.core_photo_interface import CorePhotoInterface


class TestCorePhotoInterface:
    def test_get_photos_for_depth_range(self):
        interface = CorePhotoInterface('test_well')
        print('here')

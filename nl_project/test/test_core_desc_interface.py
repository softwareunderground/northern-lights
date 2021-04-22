from ..data_layer.core_desc_interface import CoreDescriptionInterface


class TestCoreDescriptionInterface:
    def test_get_nearest_desc_for_depth(self):
        interface = CoreDescriptionInterface(name='Test')
        info = interface.get_nearest_desc_for_depth(2643.7)




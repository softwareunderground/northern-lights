from unittest import TestCase
from input_layer.get_data import GetProjectData


class TestAzureInput(TestCase):
    def test_get_core_report(self):
        data = GetProjectData().get_data_of_type('Core Report')
        print('here')

    def test_get_core_photo_metadata(self):
        data = GetProjectData().get_data_of_type('Core Photo Metadata')
        print('here')
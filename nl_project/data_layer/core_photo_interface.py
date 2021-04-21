from .well_data import WellInterface
from nl_project.input_layer.get_data import GetProjectData


class CorePhotoInterface(WellInterface):
    """Interface to work with core photo data"""
    def __init__(self, name):
        super().__init__(name)
        self.data = self.get_data(key='Core Photo Data')

    def get_photos_for_depth_range(self, start_md, end_md):
        pass

    def _load_from_sources(self, key):
        # Load the core metadata table
        core_metadata = GetProjectData().get_data_of_type('Core Photo Metadata')
        # Make Image Loader/Referencer
        print('here')

        pass

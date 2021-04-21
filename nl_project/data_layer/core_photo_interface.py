from .well_data import WellInterface
from nl_project.input_layer.get_data import GetProjectData
from PIL import Image


class CorePhotoInterface(WellInterface):
    """Interface to work with core photo data"""
    def __init__(self, name):
        super().__init__(name)
        self.core_photo_metadata = None
        self.loaded_photos = {}
        print('WARNING: Loading core photos, may take a long time the first time!')
        self.data = self.get_data(key='Core Photo Data')

    def get_photos_for_depth_range(self, start_md, end_md):
        start_md_filter = float(int(start_md) - 1)
        top_filter = self.core_photo_metadata['top_depth'] > start_md_filter
        bottom_filter = self.core_photo_metadata['end_depth'] < end_md
        filtered_photos = self.core_photo_metadata.loc[top_filter & bottom_filter, :]
        self._clean_up_photos(filtered_photos)

    def _load_from_sources(self, key):
        # Load the core metadata table
        self.core_photo_metadata = GetProjectData().get_data_of_type('Core Photo Metadata')[0]
        self._load_photos(self.core_photo_metadata)
        return self.loaded_photos

    def _load_photos(self, photo_info_df):
        for idx, row in photo_info_df.iterrows():
            if not self.data_exists(key=f'core_photo{idx}'):
                print(f'Loading Photo at idx: {idx}')
                current_photo = GetProjectData().get_data_with_name(name=row['file_key'], download=False)
                self.set_data(key=f'core_photo{idx}', data=current_photo)
            self.loaded_photos[idx] = f'core_photo{idx}'

    def _clean_up_photos(self, photos_df):
        for idx, row in photos_df.iterrows():
            print('here')

import pandas as pd

from .well_data import WellInterface
from nl_project.input_layer.get_data import GetProjectData
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import sobel


class CorePhotoInterface(WellInterface):
    """Interface to work with core photo data"""
    def __init__(self, name):
        super().__init__(name)
        self.core_photo_metadata = None
        self.loaded_photos = {}
        print('WARNING: Loading core photos, may take a long time the first time!')
        self.data = self.get_data(key='Core Photo Data')

    def report_available_core_photos(self) -> pd.DataFrame:
        return self.core_photo_metadata

    def get_sample_at_depth(self, md, sample_thickness=0.08) -> object:
        photos = self.get_photos_for_depth_range(md - sample_thickness, md + sample_thickness)
        sample_photos = photos['filtered_photos']
        top_idx = sample_photos.columns.get_loc('top_depth')
        btm_idx = sample_photos.columns.get_loc('bottom_depth')
        photo_top = sample_photos.iat[0, top_idx]
        photo_btm = sample_photos.iat[sample_photos.shape[0] - 1, btm_idx]
        if sample_photos.empty:
            print('no core photos for this depth')
            return None
        else:
            photo = photos['interval 1']
            photo_thickness = photo_btm - photo_top
            px_per_m = photo.shape[0] / photo_thickness
            start_pix = int((md - sample_thickness - photo_top) * px_per_m)
            end_pix = int((md + sample_thickness - photo_top) * px_per_m)
            photo_sample = photo[start_pix:end_pix, 50:350, :]
            return photo_sample

    def get_photos_for_depth_range(self, start_md, end_md):
        start_md_filter = float(int(start_md))
        top_filter = self.core_photo_metadata['top_depth'] >= start_md_filter
        bottom_filter = self.core_photo_metadata['bottom_depth'] < end_md + 1.0
        filtered_photos = self.core_photo_metadata.loc[top_filter & bottom_filter, :]
        filtered_photos = filtered_photos.loc[~filtered_photos['top_depth'].duplicated()]
        change_points = filtered_photos['top_depth'].diff() > 4.0
        list_of_core_changes = list(change_points.loc[change_points == True].index)
        list_of_core_changes = [0] + list_of_core_changes
        photos_out = {}
        interval = 1
        for ind, x in enumerate(list_of_core_changes):

            if x != list_of_core_changes[-1]:
                photos = filtered_photos.loc[x:list_of_core_changes[ind + 1]]
                meta = self.core_photo_metadata.loc[x:list_of_core_changes[ind + 1]]
            else:
                photos = filtered_photos.loc[x:]
                meta = self.core_photo_metadata.loc[x:]
            photos_out[f'interval {interval}'] = self._clean_up_photos(photos)
            photos_out[f'interval {interval} top'] = meta.loc[x, 'top_depth']
            photos_out[f'interval {interval} bottom'] = meta.loc[x, 'top_depth']
            interval += 1
        photos_out['filtered_photos'] = filtered_photos
        return photos_out


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
        output_photos = []
        for idx, row in photos_df.iterrows():
            current_photo = self.get_data(key=f'core_photo{idx}', load=False)[0]['image_array']
            current_photo = current_photo[:, 75:, :]

            max_val = 255 * current_photo.shape[0]
            max_val_rows = 255 * current_photo.shape[1]
            brightness = current_photo[:, :, 0] * 0.21 + current_photo[:, :, 1] * 0.72 + current_photo[:, :, 2] * 0.07
            # plt.hist(np.sum(brightness, axis=0)/max_val)
            brightness_filter = ((np.sum(brightness, axis=0)/max_val) > 0.3) & ((np.sum(brightness, axis=0)/max_val) < 0.98)

            row_brightness_filter = np.sum(brightness, axis=1) / max_val_rows > 0.1
            cleaned_photo = current_photo[:, brightness_filter, :]
            # Check for header at the top
            if np.sum(~row_brightness_filter[:230]) > 60:
                cleaned_photo = cleaned_photo[230:, :, :]
            cleaned_photo = cleaned_photo[:, :900, :]
            output_photos.append(cleaned_photo)
            if cleaned_photo.shape[1] < 400:
                im = Image.fromarray(cleaned_photo)
                im.show()
        combined_photo = np.concatenate(output_photos, axis=0)
        return combined_photo

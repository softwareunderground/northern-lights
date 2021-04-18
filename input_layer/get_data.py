import pandas as pd
from .azure_input import AzureInput


class GetProjectData(object):
    """Class for easy access to the northern lights dataset"""
    config_path = './Source_Config.csv'
    source_types = {
        'azure_blob': AzureInput
    }

    def __init__(self):
        self.sources = None
        self.download = True

    def list_available_sources(self):
        self._check_sources()
        return self.sources

    def get_data_of_type(self, data_type, download=True):
        self._check_sources()
        self.download = download
        temp_list = self.sources[self.sources.SourceCategory == data_type]
        return self._retrieve_sources(temp_list)

    def download_project_data(self):
        self.download = True
        self._check_sources()
        self._retrieve_sources(self.sources, capture_outputs=False)

    def _retrieve_sources(self, source_df, capture_outputs=True):
        output_data = []
        for idx, row in source_df.iterrows():
            source = self.source_types[row['SourceType']]
            row_dict = dict(row)
            row_dict['download'] = self.download
            source_to_load = source(**row_dict)
            if capture_outputs:
                data = source_to_load.get_data()
                output_data.append(data)
            else:
                _ = source_to_load.get_data()
        return output_data

    def _check_sources(self):
        if self.sources is None:
            self.sources = pd.read_csv(self.config_path)



import pandas as pd
from .azure_input import AzureInput, ContainerClient
from collections import defaultdict
from nl_project.validation_and_parsing.core_photo_metadata_parser import CorePhotoMetadataParser

class GetProjectData(object):
    """Class for easy access to the northern lights dataset"""
    config_path = './Source_Config.csv'
    source_types = {
        'azure_blob': AzureInput
    }
    parsers = {
        'photo_metadata': CorePhotoMetadataParser(),
    }

    def __init__(self):
        self.sources = None
        self.download = True
        self.repo_names = self._get_repo_names()

    def list_available_sources(self):
        self._check_sources()
        return self.sources

    def get_data_with_name(self, name, download=False):
        self._check_sources()
        self.download = download
        psuedo_source = self.sources.iloc[[0]].copy()
        psuedo_source['SourceName'] = name
        return self._retrieve_sources(psuedo_source)

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
            parser = row['Parser']
            row_dict = dict(row)
            row_dict['download'] = self.download
            source_to_load = source(**row_dict)
            if capture_outputs:
                data = source_to_load.get_data()
                if parser is not None:
                    file_parser = self.parsers[parser]
                    if row['ParseType'] == 'df':
                        data = file_parser.parse_to_df(data)
                    else:
                        data = file_parser.parse_to_array(data)
                output_data.append(data)
            else:
                _ = source_to_load.get_data()
        return output_data

    def _check_sources(self):
        if self.sources is None:
            self.sources = pd.read_csv(self.config_path)

    def _get_repo_names(self):
        url_postfix = 'sv=2018-03-28&sr=c&sig=ySdG6%2BRmccOC1Eg4H0UlVDyVQgAQ1QzQdxCh1dxcTXs%3D&se=2021-05-16T16%3A56%3A39Z&sp=rl'
        url = 'https://datavillagesa.blob.core.windows.net/northernlights?'
        nl_container = ContainerClient.from_container_url(container_url=url + url_postfix)
        blob_list = nl_container.list_blobs()
        output = defaultdict(list)
        for blob in blob_list:
            output['SourceName'].append(blob.name)
        return pd.DataFrame(output)


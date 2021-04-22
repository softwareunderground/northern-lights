import pandas as pd

from .well_data import WellInterface
from nl_project.input_layer.get_data import GetProjectData


class CoreDescriptionInterface(WellInterface):
    """Load and interact with SPWLA Style Core Desc data"""
    def __init__(self, name):
        super().__init__(name)
        load = not self.data_exists(key='Core Description')
        self.description = self.get_data(key='Core Description', load=load)[0]

    def _load_from_sources(self, key):
        data = GetProjectData().get_data_of_type(key)
        self.set_data(key, data)
        return data

    def get_nearest_desc_for_depth(self, md):
        samples = self._find_associated_core_samples(md)
        if (samples is None) or (len(samples) < 1):
            print('no core description associated w input depth')
            return None
        best_idx = None
        closest_sample = 10000000000
        for idx, sample in enumerate(samples):
            diff = abs(sample['depth'] - md)
            if diff < closest_sample:
                closest_sample = diff
                best_idx = idx
        if best_idx is None:
            return None
        best_sample = samples[best_idx]
        output = {}
        output['depth'] = [best_sample['depth']]
        output['descr'] = [best_sample['descr']]
        for idx, x in enumerate(best_sample['data']):
            output[self.description['fields'][idx]] = [x]
        return pd.DataFrame(output)

    def _find_associated_core_samples(self, md):
        for core in self.description['cores']:
            if (md >= core['meta']['start']) and (md <= core['meta']['stop']):
                return core['samples']
        return None


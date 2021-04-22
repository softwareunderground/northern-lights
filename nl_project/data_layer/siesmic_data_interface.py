import pandas as pd
from .well_data import WellInterface
from nl_project.input_layer.get_data import GetProjectData


class BoreholeSiesmicInterface(WellInterface):
    def __init__(self, name):
        super().__init__(name)
        load = not self.data_exists(key='Borehole Siesmic Raw')
        print('getting raw data')
        self.raw_data = self.get_data(key='Borehole Siesmic Raw', load=load)
        print('getting computed time data')
        self.computed_time_data = self.get_data(key='Borehole Siesmic Computed Time', load=load)
        print('getting gathered time data')
        self.gathered_time_data = self.get_data(key='Borehole Siesmic Time Gather', load=load)

    def _load_from_sources(self, key):
        data = GetProjectData().get_data_of_type(key)
        self.set_data(key, data)
        return data

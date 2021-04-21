import pickle
import pkg_resources
import os


class StructuredData(object):
    """Base class for data interfaces, used to manage data caching/retrieval
    during a data pipeline"""
    def __init__(self, name):
        self.name = name
        self.cache = './cache/'
        self.data_path = f'{self.cache}{self.name}/'
        pkg_resources.ensure_directory(self.data_path)

    def list_data_keys(self):
        data_listing = os.listdir(self.data_path)
        return [x.split('.')[0] for x in data_listing]

    def get_data(self, key, load=True):
        if load:
            return self._load_from_sources(key)
        else:
            try:
                return self._load_from_cache(key)
            except Exception as ex:
                print(ex)
                raise ex

    def set_data(self, key, data):
        with open(f'{self.data_path}{key}.pkl', mode='wb') as f:
            pickle.dump(data, f)

    def data_exists(self, key):
        data_list = self.list_data_keys()
        if key in data_list:
            return True
        else:
            return False

    def _load_from_sources(self, key):
        raise NotImplementedError('do not use abstract method')

    def _load_from_cache(self, key):
        outputs = []
        with open(f'{self.data_path}{key}.pkl', mode='rb') as f:
            while True:
                try:
                    outputs.append(pickle.load(f))
                except EOFError:
                    break
        return outputs[0]

    def delete_data(self, key):
        raise NotImplementedError("Will implement this if needed")
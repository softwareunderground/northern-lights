class InputData(object):
    filter = ''
    data_type = ''

    def __init__(self, **kwargs):
        super().__init__()
        self.data_type = kwargs.get('SourceCategory', '')
        self.filter = kwargs.get('SourceFilter', '')

    def get_data(self) -> dict:
        raise NotImplementedError('Do not use abstract method')

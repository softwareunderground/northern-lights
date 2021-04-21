class FileHandler(object):
    def read_from_bytes(self, bytes):
        raise NotImplementedError('Do not use abstract method')

    def read_from_path(self, path):
        raise NotImplementedError('Do not use abstract method')

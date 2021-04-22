from .pdf_file_handler import PdfFileHandler
from .asc_text_file_handler import AscFileHandler
from .tif_handler import TifHandler
# from .las_handler import LasHandler
from .segy_handler import SegyHandler
from .spwla_handler import SpwlaHandler


class ChooseFileHandler(object):
    handlers = {'pdf': PdfFileHandler(),
                'asc': AscFileHandler(),
                'tif': TifHandler(),
                'tiff': TifHandler(),
                # 'las': LasHandler(),
                'segy': SegyHandler(),
                'spwla': SpwlaHandler(),
                }

    def read_from_bytes(self, bytes, file_extension):
        handler = self.handlers[file_extension.lower()]
        return handler.read_from_bytes(bytes)

    def read_from_path(self, path, file_extension):
        handler = self.handlers[file_extension.lower()]
        return handler.read_from_path(path)

from .pdf_file_handler import PdfFileHandler
from .asc_text_file_handler import AscFileHandler


class ChooseFileHandler(object):
    handlers = {'pdf': PdfFileHandler(),
                'asc': AscFileHandler(),
                }

    def read_from_bytes(self, bytes, file_extension):
        handler = self.handlers[file_extension.lower()]
        return handler.read_from_bytes(bytes)

    def read_from_path(self, path, file_extension):
        handler = self.handlers[file_extension.lower()]
        return handler.read_from_path(path)

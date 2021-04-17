from .pdf_file_handler import PdfFileHandler


class ChooseFileHandler(object):
    handlers = {'pdf': PdfFileHandler()}

    def read_from_bytes(self, bytes, file_extension):
        handler = self.handlers[file_extension.lower()]
        return handler.read_from_bytes(bytes)

    def read_from_path(self, path, file_extension):
        handler = self.handlers[file_extension.lower()]
        return handler.read_from_path(path)

from .file_handler import FileHandler
from ..validation_and_parsing.spwla import parse
import os


class SpwlaHandler(FileHandler):
    def read_from_bytes(self, bytes):
        bytes.seek(0)
        with open('./temp_file.spwla', 'wb') as out:  ## Open temporary file as bytes
            out.write(bytes.read())
        output = parse('./temp_file.spwla')
        os.remove('./temp_file.spwla')
        return output

    def read_from_path(self, path):
        output = parse(path)
        return output

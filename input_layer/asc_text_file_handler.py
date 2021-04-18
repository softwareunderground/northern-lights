from .file_handler import FileHandler
import pandas as pd
from io import TextIOWrapper


class AscFileHandler(FileHandler):
    """Class to read in the text from the .asc files, these files are wild and come in many forms, we are going
    to need a way to parse some of these to pandas dataframes, but those can target specific data that we need, as needed"""
    def read_from_bytes(self, bytes):
        bytes.seek(0)
        text_doc_bytes = bytes.read()
        output = str(text_doc_bytes, 'utf-8', 'ignore').split('\n')
        return {'lines': output}

    def read_from_path(self, path):
        with open(path, 'r', errors='replace') as f:
            lines = f.readlines()
        return {'lines': lines}

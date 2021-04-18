from .file_handler import FileHandler
import pandas as pd


class AscFileHandler(FileHandler):
    """Class to read in the text from the .asc files, these files are wild and come in many forms, we are going
    to need a way to parse some of these to pandas dataframes, but those can target specific data that we need, as needed"""
    def read_from_bytes(self, bytes):
        pass

    def read_from_path(self, path):
        pass

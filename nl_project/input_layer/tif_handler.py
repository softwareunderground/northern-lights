from .file_handler import FileHandler
from PIL import Image
import numpy as np


class TifHandler(FileHandler):
    def read_from_path(self, path):
        return self._load_image(path)

    def read_from_bytes(self, bytes):
        return self._load_image(bytes)

    def _load_image(self, path):
        im = Image.open(path)
        # im.show() # for debugging purposes
        imarray = np.array(im)
        return {'image_array': imarray}

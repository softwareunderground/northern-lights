from .file_handler import FileHandler
import segyio
import numpy as np
import os


class SegyHandler(FileHandler):
    def read_from_path(self, path):
        return self._read_sgy(path)

    def read_from_bytes(self, bytes):
        bytes.seek(0)
        with open('./temp_file.segy', 'wb') as out:  ## Open temporary file as bytes
            out.write(bytes.read())
        output = self._read_sgy('./temp_file.segy')
        os.remove('./temp_file.segy')
        return output

    def _read_sgy(self, reader):
        with segyio.open(reader, strict=False) as s:
            rawdata = np.stack(t.astype(np.float64) for t in s.trace)
        return rawdata

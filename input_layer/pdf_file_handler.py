from .file_handler import FileHandler
import PyPDF4


class PdfFileHandler(FileHandler):
    def read_from_path(self, path):
        pdf_file = PyPDF4.PdfFileReader(path)
        return self._extract_text(pdf_file)

    def read_from_bytes(self, bytes):
        pdf_file = PyPDF4.PdfFileReader(bytes)
        return self._extract_text(pdf_file)

    def _extract_text(self, pdf_file):
        output = {}
        for x in range(pdf_file.numPages):
            try:
                page = pdf_file.getPage(x + 1)
                output[x] = page.extractText()
            except Exception as ex:
                print(f'page {x+1} failed!')
        return output

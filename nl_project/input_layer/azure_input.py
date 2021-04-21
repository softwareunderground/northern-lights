from .input_base import InputData
from azure.storage.blob import ContainerClient, BlobClient
from io import BytesIO, StringIO
from .choose_file_handler import ChooseFileHandler


class AzureInput(InputData):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = kwargs.get('Endpoint', '')
        self.postfix = kwargs.get('AdditionalConnectionInfo', '')
        self.blob_name = kwargs.get('SourceName', '')
        self.download_data = kwargs.get('download', True)
        self.file_handler = None

    def get_data(self) -> dict:
        return self._find_blob_and_load_file()

    def _find_blob_and_load_file(self):
        nl_container = ContainerClient.from_container_url(container_url=f"{self.url}?{self.postfix}")
        blob_list = nl_container.list_blobs()
        return self._search_container_and_return_data(blob_list)

    def _search_container_and_return_data(self, blob_list):
        for blob in blob_list:
            if blob.name == self.blob_name:
                file_handler = ChooseFileHandler()
                file_extension = blob.name.split('.')[-1]
                blob_client = BlobClient.from_blob_url(
                    blob_url=f"{self.url}/{blob.name}?{self.postfix}")
                if self.download_data:
                    path = self._download_blob(blob_client, blob)
                    return file_handler.read_from_path(path, file_extension)
                else:
                    with BytesIO() as my_blob:
                        bytes = self._read_blob(blob_client, my_blob)
                        return file_handler.read_from_bytes(bytes, file_extension)

    def _download_blob(self, blob_client, blob):
        name_parts = blob.name.split('/')
        path = f"./{name_parts[-1]}"
        with open(path, "wb") as my_blob:
            blob_data = blob_client.download_blob()
            blob_data.readinto(my_blob)
        return path

    def _read_blob(self, blob_client, my_blob):
        blob_data = blob_client.download_blob()
        blob_data.readinto(my_blob)
        return my_blob
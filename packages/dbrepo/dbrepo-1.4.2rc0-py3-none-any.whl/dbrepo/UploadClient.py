from tusclient import client

from dbrepo.api.exceptions import UploadError


class UploadClient:
    endpoint: str

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def upload(self, file_path: str) -> str:
        """
        Uploads a file located at file_path to the Upload Service.

        :param file_path: The location of the file on the local filesystem.

        :return: Filename on the S3 backend of the Upload Service, if successful.
        """
        my_client = client.TusClient(url=f'{self.endpoint}/api/upload/files/')
        uploader = my_client.uploader(file_path=file_path)
        uploader.upload()
        filename = uploader.url[uploader.url.rfind('/') + 1:uploader.url.rfind('+')]
        if filename is None or len(filename) == 0:
            raise UploadError(f'Failed to upload the file to {self.endpoint}')
        return filename

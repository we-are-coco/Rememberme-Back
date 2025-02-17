from azure.storage.blob import BlobServiceClient
from config import get_settings
from typing import BinaryIO

settings = get_settings()

class AzureBlobStorage:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(settings.azure_storage_connection_string)
        self.container_client = self.blob_service_client.get_container_client(settings.azure_blob_container_name)

    def upload_image(self, file_path: str, blob_name: str):
        blob_client = self.container_client.get_blob_client(blob_name)

        with open(file_path, "rb") as file:
            blob_client.upload_blob(file, overwrite=True)

        return blob_client.url
    
    def download_image(self, blob_name: str, file_path: str):
        blob_client = self.container_client.get_blob_client(blob_name)

        with open(file_path, "wb") as file:
            data = blob_client.download_blob()
            data.readinto(file)
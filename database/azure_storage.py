# database/azure_storage.py
# Handles communication with Azure Blob Storage.
# Responsible for uploading listing images, generating unique blob names,
# returning image URLs, and deleting images when necessary.

import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

class AzureBlobStorage:
    def __init__(self):
        """
        Initialize the AzureBlobStorage instance with the given connection string and container name.
        """
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "").strip()
        if not connection_string:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is required")

        container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        if not container_name:
            raise ValueError("AZURE_STORAGE_CONTAINER_NAME environment variable is required")
        
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def upload_image(self, blob_name: str, image_data: bytes) -> str:
        """
        Upload an image to Azure Blob Storage.
        Returns the URL of the uploaded image.
        """
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.upload_blob(image_data, overwrite=True)
        return blob_client.url

    def delete_image(self, blob_name: str):
        """
        Delete an image from Azure Blob Storage.
        """
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.delete_blob()


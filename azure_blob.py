from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import os
from typing import List, Union
from ..config import settings

class AzureBlobService:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.blob_service_client = BlobServiceClient(
            account_url=f"https://{settings.AZURE_STORAGE_ACCOUNT}.blob.core.windows.net",
            credential=self.credential
        )
        self.container_client = self.blob_service_client.get_container_client(settings.AZURE_STORAGE_CONTAINER)

    async def upload_file(self, file_path: str, blob_name: str = None) -> str:
        """Upload a single file to Azure Blob Storage"""
        if blob_name is None:
            blob_name = os.path.basename(file_path)
        
        with open(file_path, "rb") as data:
            self.container_client.upload_blob(name=blob_name, data=data, overwrite=True)
        return blob_name

    async def upload_folder(self, folder_path: str) -> List[str]:
        """Upload all files from a folder to Azure Blob Storage"""
        uploaded_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path)
                blob_name = await self.upload_file(file_path, relative_path)
                uploaded_files.append(blob_name)
        return uploaded_files

    def get_blob_url(self, blob_name: str) -> str:
        """Get the URL for a blob"""
        return f"https://{settings.AZURE_STORAGE_ACCOUNT}.blob.core.windows.net/{settings.AZURE_STORAGE_CONTAINER}/{blob_name}" 
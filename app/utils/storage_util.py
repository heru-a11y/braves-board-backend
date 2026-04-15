# type: ignore
import uuid
from datetime import timedelta
from fastapi import UploadFile
from google.cloud import storage
from app.core.config import settings

class StorageUtil:
    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_name = settings.GCS_BUCKET_NAME 
        self.bucket = self.storage_client.bucket(self.bucket_name)

    def upload_file(self, file: UploadFile, destination_path: str) -> str:
        blob = self.bucket.blob(destination_path)
        blob.upload_from_file(file.file, content_type=file.content_type)
        return f"https://storage.googleapis.com/{self.bucket_name}/{destination_path}"

    def generate_signed_url(self, file_url: str, expiration_minutes: int = 15) -> str:
        prefix = f"https://storage.googleapis.com/{self.bucket_name}/"
        if not file_url.startswith(prefix):
            return file_url

        blob_name = file_url.replace(prefix, "")
        blob = self.bucket.blob(blob_name)

        return blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=expiration_minutes),
            method="GET",
        )
    
    def delete_file(self, file_url: str) -> bool:
        prefix = f"https://storage.googleapis.com/{self.bucket_name}/"

        if not file_url.startswith(prefix):
            return False
        
        blob_name = file_url.replace(prefix, "")
        blob = self.bucket.blob(blob_name)
        
        try:
            blob.delete()
            return True
        except Exception:
            return False
# File: app/models/media.py
from pydantic import BaseModel
import uuid

class UploadResponse(BaseModel):
    status: str = "success"
    file_id: uuid.UUID
    filename: str
# File: app/api/v1/endpoints/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.models.media import UploadResponse
from app.services.transcription import process_and_transcribe_audio
import uuid
import shutil
from pathlib import Path

router = APIRouter()
DATA_PATH = Path("data")

@router.post("/audio", response_model=UploadResponse)
async def upload_audio(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an audio file.")

    file_id = uuid.uuid4()
    # You can use the extension from the original file or standardize it
    file_location = DATA_PATH / "audio" / f"{file_id}.wav" # example: standardize to wav
    file_location.parent.mkdir(parents=True, exist_ok=True)

    try:
        with file_location.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # TODO: Store metadata in DB here
        
        # This is a placeholder for Task 4. We can do it in the background.
        # background_tasks.add_task(process_and_transcribe_audio, file_id=file_id, file_path=file_location)

    finally:
        file.file.close()

    return UploadResponse(file_id=file_id, filename=file.filename)

# You can create a similar endpoint for /video
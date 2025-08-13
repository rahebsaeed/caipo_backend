# File: app/services/transcription.py
import whisper
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
DATA_PATH = Path("data")
TRANSCRIPTS_PATH = DATA_PATH / "transcripts"
TRANSCRIPTS_PATH.mkdir(parents=True, exist_ok=True)

# Load the model once when the application starts
# For a prototype, 'tiny' or 'base' is fine.
try:
    model = whisper.load_model("base")
    logger.info("Whisper model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading whisper model: {e}")
    model = None

def process_and_transcribe_audio(file_id: str, file_path: Path):
    """
    The core transcription logic. This function is designed to be run
    in the background to avoid blocking the API response.
    """
    if not model:
        logger.error("Whisper model not available. Cannot transcribe.")
        # TODO: Update DB to reflect transcription failure
        return

    logger.info(f"Starting transcription for file_id: {file_id}")
    try:
        # Note: Whisper needs the file path as a string
        result = model.transcribe(str(file_path), fp16=False) # fp16=False if no GPU

        # Save the full transcript JSON
        transcript_file_path = TRANSCRIPTS_PATH / f"{file_id}.json"
        with transcript_file_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Transcription for {file_id} completed and saved.")
        # TODO: Update the DB row with transcript path and status
        # For example: db.update_media(file_id, transcript_path=str(transcript_file_path), status="completed")

    except Exception as e:
        logger.error(f"Transcription failed for {file_id}: {e}")
        # TODO: Update DB to reflect failure status
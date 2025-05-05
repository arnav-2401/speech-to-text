# api_server.py
import os, shutil, tempfile, mimetypes
from fastapi import FastAPI, File, UploadFile, HTTPException
from transcribe import transcribe_audio

app = FastAPI(title="Whisper‑cpp Audio Transcription API")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # 1) basic validation ─ allow any audio; reject everything else
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Upload must be an audio file")

    # 2) pick a sensible suffix (".wav", ".mp3", etc.) for the temp file
    guessed_ext = mimetypes.guess_extension(file.content_type) or ".bin"
    with tempfile.NamedTemporaryFile(delete=False, suffix=guessed_ext) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # 3) transcribe  – use convert=True so WAV/MP3/AAC all get down‑sampled
        text = transcribe_audio(
            tmp_path,
            output_text="ignored.txt",   # side‑file not needed for API use‑case
            model="small",
            threads=4,
            convert=False,               # <-- KEEP TRUE so every format is normalised
        )
    finally:
        os.remove(tmp_path)

    return {"transcription": text}

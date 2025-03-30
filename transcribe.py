import subprocess
import os

def transcribe_audio(input_audio, output_text="transcription.txt", model="small", threads=4):
   
 # Ensure whisper.cpp is built
    if not os.path.exists("whisper.cpp/main"):
        raise FileNotFoundError("whisper.cpp not found. Please clone and build it first.")

    # Convert audio to mono, 16kHz WAV (if not already)
    temp_audio = "converted.wav"
    subprocess.run(["ffmpeg", "-y", "-i", input_audio, "-ac", "1", "-ar", "16000", temp_audio], check=True)

    # Run whisper.cpp transcription
    model_path = f"whisper.cpp/models/ggml-{model}.bin"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file {model_path} not found. Please download it.")

    result = subprocess.run(
        ["whisper.cpp/main", "-m", model_path, "-f", temp_audio, "-t", str(threads)],
        capture_output=True, text=True
    )

    # Extract and save the transcription
    transcription = result.stdout.strip()
    with open(output_text, "w") as f:
        f.write(transcription)

    return transcription

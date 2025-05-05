import subprocess
import os

def transcribe_audio(input_audio, output_text="transcription.txt", model="small", threads=4, convert=True):
   
 # Ensure whisper.cpp is built
    if not os.path.exists("whisper.cpp/build/bin/whisper-cli"):
        raise FileNotFoundError("whisper.cpp not found. Please clone and build it first.")

    # Convert audio to mono, 16kHz WAV (if not already)
    if (convert):
        temp_audio = "converted.wav"
        subprocess.run([
        "ffmpeg", "-y",
        "-f", "s16le",         # Format: signed 16-bit little-endian
        "-ar", "44100",        # Original sample rate
        "-ac", "1",            # Mono audio
        "-i", input_audio,     # Input file
        "-ar", "16000",        # Resample to 16kHz
        "-ac", "1",            # Output as mono
        temp_audio
    ], check=True)
    else:
        temp_audio = input_audio


    # Run whisper.cpp transcription
    model_path = f"whisper.cpp/models/ggml-{model}.bin"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file {model_path} not found. Please download it.")

    result = subprocess.run(
        ["whisper.cpp/build/bin/whisper-cli", "-m", model_path, "-f", temp_audio, "-t", str(threads)],
        capture_output=True, text=True
    )
    # Extract and save the transcription
    transcription = result.stdout.strip()
    with open(output_text, "w") as f:
        f.write(transcription)

    return transcription

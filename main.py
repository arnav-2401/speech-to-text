import subprocess
import os

from startup import startup
startup()
from summary import summarize


def record_audio():
    try:
        subprocess.run(["./record_alsa"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Recording failed: {e}")

def main():
    filename = input("Enter a name for the transcribed text file: ").strip()
    if not filename:
        print("No filename provided. Using default 'output.txt'.")
        filename = "output"

    record_audio()
    print("Now transcribing...")

    from transcribe import transcribe_audio
    output_path = os.path.join("transcriptions", f"{filename}.txt")
    final_path = os.path.join("summary", f"{filename}.txt")
    transcription = transcribe_audio("test.raw", output_path, model="small", threads=4)
    
    print("Transcription complete:\n")

    summarize(output_path, final_path)
    

if __name__ == "__main__":
    main()

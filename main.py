import subprocess

def record_audio():
    try:
        subprocess.run(["./record_alsa"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Recording failed: {e}")

def main():
    record_audio()
    print("Now transcribing...")

    from transcribe import transcribe_audio
    transcription = transcribe_audio("test.raw", "output.txt", model="small", threads=4)

    print("Transcription complete:\n")
    print(transcription)

if __name__ == "__main__":
    main()

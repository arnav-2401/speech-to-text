from transcribe import transcribe_audio

def main():
    input_audio = "test.raw"  # Or any other input file
    output_text = "output.txt"
    model = "small"  # Options: tiny, base, small, medium, large
    threads = 4

    try:
        text = transcribe_audio(input_audio, output_text, model, threads)
        print("Transcription completed:\n")
        print(text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

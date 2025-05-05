from transcribe import transcribe_audio
import argparse
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transcription.log'),
        logging.StreamHandler()
    ]
)

def main():
    parser = argparse.ArgumentParser(description="Process an audio file.")
    parser.add_argument("filepath", help="Path to the audio file")
    args = parser.parse_args()

    # Derive output filename
    input_path = args.filepath
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    
    # Create transcriptions directory if it doesn't exist
    os.makedirs("transcriptions", exist_ok=True)
    output_path = os.path.join("transcriptions", base_name + ".txt")

    # Skip if already processed
    if os.path.exists(output_path):
        logging.info(f"Skipping {input_path} - already processed")
        return

    # Transcribe
    logging.info(f"Starting transcription of {input_path}")
    transcription = transcribe_audio(input_path, output_path, model="small", threads=4, convert=False)
    logging.info(f"Completed transcription of {input_path}")

    print("\nTranscription complete:")
    print(transcription)

if __name__ == "__main__":
    main()

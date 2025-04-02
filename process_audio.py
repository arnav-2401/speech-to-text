from transcribe import transcribe_audio
import argparse
import os

parser = argparse.ArgumentParser(description="Process an audio file.")
parser.add_argument("filepath", help="Path to the audio file")
args = parser.parse_args()

# Derive output filename
input_path = args.filepath
base_name = os.path.splitext(os.path.basename(input_path))[0]  # 'song.mp3' → 'song'
output_path = os.path.join(base_name + ".txt")

# Transcribe
transcription = transcribe_audio(input_path, output_path, model="small", threads=4, convert=False)

print("Transcription complete:\n")
print(transcription)

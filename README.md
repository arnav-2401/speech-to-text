# Audio Transcription System

A comprehensive system for recording and transcribing audio files using ALSA, Whisper.cpp.

## Overview

This project provides three core capabilities:
1. **CLI Audio Recording** - Capture audio from microphone (C program)
2. **Transcription** - Transcribe new audio files through whisper.cpp

Key components:
- `record_alsa`: Low-level audio recorder (C)
- `main.py`: CLI interface for recording/transcription
- `api_server.py`: FastAPI web service

## Installation

### Requirements
- Linux/Raspberry Pi OS
- Python 3.8+
- ALSA development libraries
- FFmpeg

### Setup

1. **Install Dependencies**
```bash
sudo apt-get update
sudo apt-get install libasound2-dev ffmpeg python3-pip

2. **Building whisper.cpp**
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp && make
cd ..

3. **Downloading the small whisper model**
wget -P whisper.cpp/models/ https://huggingface.co/datasets/ggerganov/whisper.cpp/resolve/main/ggml-small.bin

4. **Compiling the record_mp3.c**
We have provided a makefile. Just run make in the terminal to compile the script to record the audio

## Usage
Run main.py, record audio using the raspberry pi mic. Hit ctrl+C when you're done recording. You'll be prompted for the name of the output file you want to save. Find the trnascribed text in the transcriptions folder.
You can also run the program with flask api server.

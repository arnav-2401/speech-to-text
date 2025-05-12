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
```

2. **Install Python Packages**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Building whisper.cpp**

```bash
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp && make
cd ..
```

3. **Downloading the small whisper model**

```bash
wget -P whisper.cpp/models/ https://huggingface.co/datasets/ggerganov/whisper.cpp/resolve/main/ggml-small.bin
```

4. **Compiling the record_mp3.c**

```bash
We have provided a makefile. Just run make in the terminal to compile the script to record the audio
```

## Usage

Run main.py, record audio using the raspberry pi mic. Hit ctrl+c when you're done recording. You'll be prompted for the name of the output file you want to save. Find the transcribed text in the transcriptions folder.

```bash
python main.py
```

You can also run the program with uvicorn api server.

```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

## Contributions

### Advait

- Implemented recording functionality using ALSA
- Developed CLI interface for recording and transcription
- Worked on the FastAPI server for summary and transcription

### Arnav

- Implemented transcription functionality using whisper.cpp
- Worked on integrating everything together in main.py

### Mhark

- Worked on summary functionality, experimented with different models
- Worked on startup.py, helping seamlessly manage venvs

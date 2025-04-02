from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import subprocess
import os

WATCH_DIR = os.path.expanduser("~/cs341H/MP3")
print(f"Watching folder: {WATCH_DIR}")

if not os.path.exists(WATCH_DIR):
    raise FileNotFoundError(f"Watch directory does not exist: {WATCH_DIR}")

class AudioHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith((".wav")):
            print(f"New file detected: {event.src_path}")
            subprocess.run(["python3", "process_audio.py", event.src_path])

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(AudioHandler(), WATCH_DIR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

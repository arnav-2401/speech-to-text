from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import subprocess
import os
import queue
import logging
from typing import Set

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('watcher.log'),
        logging.StreamHandler()
    ]
)

WATCH_DIR = os.path.expanduser("~/cs341H/MP3")
SUPPORTED_FORMATS = {".wav", ".mp3"}
COOLDOWN_PERIOD = 30  # seconds to wait between processing files

class AudioProcessor:
    def __init__(self):
        self.file_queue = queue.Queue()
        self.is_processing = False
        self.last_process_time = 0
    
    def process_queue(self):
        """Process files from the queue one at a time with cooling periods"""
        if self.is_processing:
            return
            
        self.is_processing = True
        try:
            while not self.file_queue.empty():
                # Check if we need to wait for cooldown
                time_since_last = time.time() - self.last_process_time
                if time_since_last < COOLDOWN_PERIOD:
                    cooling_time = COOLDOWN_PERIOD - time_since_last
                    logging.info(f"Cooling down for {cooling_time:.1f} seconds before next file...")
                    time.sleep(cooling_time)
                
                file_path = self.file_queue.get()
                try:
                    logging.info(f"Processing file: {file_path} (Queue size: {self.file_queue.qsize()})")
                    subprocess.run(["python3", "process_audio.py", file_path], check=True)
                    self.last_process_time = time.time()
                except subprocess.CalledProcessError as e:
                    logging.error(f"Error processing {file_path}: {e}")
                finally:
                    self.file_queue.task_done()
                    
                # Log queue status after processing
                remaining = self.file_queue.qsize()
                if remaining > 0:
                    logging.info(f"Completed file. {remaining} files remaining in queue.")
        finally:
            self.is_processing = False
            if not self.file_queue.empty():
                logging.warning(f"Processing stopped with {self.file_queue.qsize()} files still in queue")
    
    def add_file(self, file_path: str):
        """Add a file to the processing queue and start processing if not already running"""
        logging.info(f"Adding file to queue: {file_path} (Current queue size: {self.file_queue.qsize()})")
        self.file_queue.put(file_path)
        self.process_queue()  # Start processing if not already running

class AudioHandler(FileSystemEventHandler):
    def __init__(self, processor: AudioProcessor):
        self.processor = processor
        
    def on_created(self, event):
        if event.is_directory:
            return
            
        _, ext = os.path.splitext(event.src_path)
        if ext.lower() in SUPPORTED_FORMATS:
            logging.info(f"New file detected: {event.src_path}")
            self.processor.add_file(event.src_path)

def main():
    if not os.path.exists(WATCH_DIR):
        raise FileNotFoundError(f"Watch directory does not exist: {WATCH_DIR}")
    
    logging.info(f"Starting file watcher in: {WATCH_DIR}")
    logging.info(f"Using {COOLDOWN_PERIOD} second cooldown between files")
    
    # Initialize the audio processor
    processor = AudioProcessor()
    
    # Set up the file system observer
    observer = Observer()
    observer.schedule(AudioHandler(processor), WATCH_DIR, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down...")
        observer.stop()
        
    observer.join()

if __name__ == "__main__":
    main()

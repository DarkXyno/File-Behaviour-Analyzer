from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from monitor.handler import FileEventHandler
import time

class WatchHandler(FileSystemEventHandler):
    def __init__(self, logger):
        self.logger = logger

    def on_created(self, event):
        self.logger.log_event("created", event.src_path, event.is_directory)

    def on_modified(self, event):
        self.logger.log_event("modified", event.src_path, event.is_directory)

    def on_deleted(self, event):
        self.logger.log_event("deleted", event.src_path, event.is_directory)

    def on_moved(self, event):
        self.logger.log_event("moved", event.dest_path, event.is_directory)

def start_observer(path: str, duration: int | None = None):
    logger = FileEventHandler()
    event_handler = WatchHandler(logger)

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    print(f"[+] Monitoring Started on {path}")

    try:
        if duration:
            time.sleep(duration)
        else:
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")

    observer.stop()
    observer.join()
    logger.close()

    print("[+] Monitoring stopped.")
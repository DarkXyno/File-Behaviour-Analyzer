from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from monitor.handler import DBLogger
import time

class FSHandler(FileSystemEventHandler):
    def __init__(self, logger):
        self.logger = logger

    def on_any_event(self, event):
        try:
            event_type = event.event_type
            path = event.src_path
            is_directory = event.is_directory

            # Handle moves properly
            if hasattr(event, "dest_path"):
                path = f"{event.src_path} -> {event.dest_path}"

            print(f"[EVENT] {event_type} -> {path}")
            self.logger.log_event(event_type, path, is_directory)

        except Exception as e:
            print(f"[ERROR] Handler failure: {e}")

def start_observer(path, duration):

    logger = DBLogger()
    handler = FSHandler(logger)

    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    observer.start()

    print(f"[+] Monitoring Started on {path}")

    try:
        time.sleep(duration)
    finally:
        observer.stop()
        observer.join()
        logger.close()
        print("[+] Monitoring stopped.")

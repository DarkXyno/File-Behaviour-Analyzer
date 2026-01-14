from datetime import datetime
from storage.db import get_connection
from process.resolver import resolve_process

class FileEventHandler:
    def __init__(self):
        self.conn = None

    def _ensure_connection(self):
        if self.conn is None:
            self.conn = get_connection()

    def log_event(self, event_type, path, is_directory):
        self._ensure_connection()

        timestamp = datetime.utcnow().isoformat()
        process_name, pid = resolve_process(path)

        cursor = self.conn.cursor()
        cursor.execute("""
                       INSERT INTO events(
                       timestamp, 
                       event_type,
                       path,
                       is_directory,
                       process_name,
                       pid
                       ) VALUES (?, ?, ?, ?, ?, ?)""", (
                           timestamp,
                           event_type,
                           path,
                           int(is_directory),
                           process_name,
                           pid
                       ))
        
        self.conn.commit()

    def close(self):
        pass
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from storage.db import get_db_path

class EventLogger:
    def __init__(self):
        self.conn = None
        self._ensure_connection()

    def _ensure_connection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(get_db_path(), check_same_thread=False)
            self._init_table()

    def _init_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                event_type TEXT,
                path TEXT,
                is_directory INTEGER
            )
        """)
        self.conn.commit()

    def log_event(self, event_type, path, is_directory):
        ts = datetime.now(timezone.utc).isoformat()

        try:
            conn = sqlite3.connect(get_db_path())
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO events (timestamp, event_type, path, is_directory)
            VALUES (?, ?, ?, ?)
            """, (ts, event_type, path, int(is_directory)))

            conn.commit()
            conn.close()
        
        except Exception as e:
            print(f"[DB ERROR] {e}")
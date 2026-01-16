import sqlite3
from pathlib import Path

DB_PATH = Path("data/events.db")

class DBLogger:
    def __init__(self):
        self.conn = None
        self._ensure_connection()

    def _ensure_connection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
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
        self._ensure_connection()  # <-- THIS is the key fix

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO events (timestamp, event_type, path, is_directory)
            VALUES (strftime('%Y-%m-%d %H:%M:%S', 'now'), ?, ?, ?)
        """, (event_type, path, int(is_directory)))
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

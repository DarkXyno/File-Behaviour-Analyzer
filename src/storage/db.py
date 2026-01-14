import sqlite3
from pathlib import Path

DB_PATH = Path("data/events.db")

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    print(f"[DB] Using database at {DB_PATH.resolve()}")
    return sqlite3.connect(DB_PATH)
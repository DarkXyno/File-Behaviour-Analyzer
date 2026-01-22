import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "data" / "events.db"

def get_db_path():
    return DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)
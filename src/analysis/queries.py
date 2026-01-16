import sqlite3 
from pathlib import Path

DB_PATH = Path("data/events.db")

def top_files(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT path, COUNT(*) as cnt
                   FROM events
                   GROUP BY path
                   ORDER BY cnt DESC
                   LIMIT ?
                   """, (limit,))
    
    results = cursor.fetchall()
    conn.close()
    return results

def top_processes(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT process_name, COUNT(*) as cnt
                   FROM events
                   WHERE process_name IS NOT NULL
                   GROUP BY process_name
                   ORDER BY cnt DESC
                   LIMIT ?
                   """, (limit,))
    
    results = cursor.fetchall()
    conn.close()
    return results
import sqlite3
from pathlib import Path
from collections import defaultdict

DB_PATH = Path("data\events.db")

def folder_summary(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT path, event_type
                   FROM events
                   WHERE is_directory = 0
                   """)
    
    rows = cursor.fetchall()
    conn.close()

    stats = defaultdict(lambda: {
        "total": 0,
        "unique_files": set(),
        "created": 0,
        "modified": 0,
        "deleted": 0,
        "moved": 0,
    })

    for path, event_type in rows:
        folder = str(Path(path).parent)

        stats[folder]["total"] += 1
        stats[folder]["unique_files"].add(path)
        stats[folder][event_type] += 1

    #sort by total activity
    sorted_folders = sorted(
        stats.items(),
        key=lambda x:x[1]["total"],
        reverse=True
    )[:limit]

    result = []
    for folder, data in sorted_folders:
        result.append((
            folder,
            data["total"],
            len(data["unique_files"]),
            data["created"],
            data["modified"],
            data["deleted"],
            data["moved"],
        ))

    return result
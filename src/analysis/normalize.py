import sqlite3
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from storage.db import get_db_path

WINDOW_SECONDS = 3  # how long events are grouped

def normalize_events():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    # Fetch raw events ordered by time
    cursor.execute("""
        SELECT timestamp, event_type, path
        FROM events
        ORDER BY timestamp ASC
    """)
    rows = cursor.fetchall()

    if not rows:
        conn.close()
        return

    groups = defaultdict(list)

    for ts, event_type, path in rows:
        ts_dt = datetime.fromisoformat(ts).replace(tzinfo=timezone.utc)
        clean_path = path.split("->")[0].strip()
        groups[clean_path].append((ts_dt, event_type))

    normalized = []

    for path, events in groups.items():
        events.sort()
        types = [e[1] for e in events]
        last_ts = events[-1][0].isoformat()

        # NORMALIZATION RULES
        if "created" in types and "deleted" in types:
            action = "file_created_and_deleted"
        elif "created" in types:
            action = "file_created"
        elif "deleted" in types:
            action = "file_deleted"
        elif "moved" in types:
            action = "file_renamed"
        elif "modified" in types:
            action = "file_modified"
        else:
            action = "file_touched"

        if action == "file_renamed":
            stored_path = path
        else:
            stored_path = clean_path

        normalized.append((last_ts, action, stored_path))

    # Insert normalized events
    cursor.executemany("""
        INSERT INTO normalized_events (timestamp, action, path)
        VALUES (?, ?, ?)
    """, normalized)

    conn.commit()
    conn.close()

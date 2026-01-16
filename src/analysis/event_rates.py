import sqlite3
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta

DB_PATH = Path("data/events.db")

def event_rates(minutes_back=5):
    """
    Returns per-minute event counts for the last N minutes.
    """
    cutoff = datetime.utcnow() - timedelta(minutes=minutes_back)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    cursor.execute("""
                   SELECT timestamp, path, is_directory
                   FROM events
                   """)
    
    rows = cursor.fetchall()
    conn.close()

    #folder count rate
    rates = defaultdict(lambda: defaultdict(int))

    for row in rows:
        ts, path = row[0], row[1]
        # is_directory = row[2]  # Not used in current implementation
        ts_dt = datetime.fromisoformat(ts)
        if ts_dt < cutoff:
            continue

        folder = str(Path(path).parent)

        #Parse timestamp and bucket by minute
        minute = datetime.fromisoformat(ts).replace(second=0, microsecond=0)

        rates[folder][minute] += 1

    return rates
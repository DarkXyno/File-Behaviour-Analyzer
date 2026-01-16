import sqlite3
from pathlib import Path
from collections import defaultdict
from datetime import datetime

DB_PATH = Path("data/events.db")

def event_rates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
SELECT timestamp, path
                   FROM events
                   WHERE is_directory = 0
                   """)
    
    rows = cursor.fetchall()
    conn.close()

    #folder count rate
    rates = defaultdict(lambda: defaultdict(int))

    for ts, path in rows:
        folder = str(Path(path).parent)

        #Parse timestamp and bucket by minute
        minute = datetime.fromisoformat(ts).replace(second=0, microsecond=0)

        rates[folder][minute] += 1

    return rates
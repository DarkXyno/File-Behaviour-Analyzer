from analysis.folder_summary import folder_summary
from analysis.event_rates import event_rates
from analysis.bursts import detect_bursts
from analysis.normalize import normalize_events
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
#temp
import sqlite3
from pathlib import Path
from storage.db import get_db_path

LOCAL_TZ = ZoneInfo("Asia/Kolkata")

def to_local(ts_str):
    utc_dt = datetime.fromisoformat(ts_str).replace(tzinfo=timezone.utc)
    return utc_dt.astimezone(LOCAL_TZ)

def run():
    normalize_events()
    print("\nFolder activity summary:\n")

    for folder, total, unique, c, m, d, mv in folder_summary():
        print(folder)
        print(f"  Total events: {total}")
        print(f"  Unique files: {unique}")
        print(f"  Creates: {c}, Modifies: {m}, Deletes: {d}, Moves: {mv}")
        print()

    rates = event_rates(minutes_back=5)

    print("\nEvent rates (last 5 mins) for top folders:\n")

    if not rates:
        print("No recent activity.")
    else:
        for folder, minutes in rates.items():
            print(folder)
            for minute, count in sorted(minutes.items()):
                print(f" {minute}: {count}")
            print()

    bursts = detect_bursts()

    print("\nBurst detection:\n")

    if not bursts:
        print("No bursts detected.")
    else:
        for b in bursts:
            print("[BURST]")
            print(f"Folder: {b['folder']}")
            print(f"Action: {b['type']}")
            print(f"Count: {b['count']} in {b['window_seconds']}")
            print(f"Baseline rate: {b['baseline_rate']}")
            print(f"Window rate: {b['window_rate']}")
            print(f"Reason: {b['reason']}")
            print()

    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    print("\nNormalized events: \n")
    cursor.execute("""
                SELECT action, path, timestamp
                FROM normalized_events
                ORDER BY id DESC
                LIMIT 10
                """)

    for action, path, ts in cursor.fetchall():
        local_ts = to_local(ts)
        print(f"{local_ts} | {action} | {path}")

    conn.close()
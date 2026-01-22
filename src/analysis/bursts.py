import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean
from storage.db import get_db_path

WINDOW_SECONDS = 10
MIN_EVENTS = 5
BASELINE_MULTIPLIER = 3

def detect_bursts():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, action, path
        FROM normalized_events
        ORDER BY timestamp ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return []

    events = []
    for ts, action, path in rows:
        clean_path = path.split("->")[-1].strip()
        folder = str(Path(clean_path).parent) if clean_path else "UNKNOWN"

        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        events.append({
            "time": dt,
            "action": action,
            "folder": folder
        })

    grouped = defaultdict(list)

    for e in events:
        grouped[(e["folder"], e["action"])].append(e["time"])

    bursts = []

    for (folder, action), times in grouped.items():
        times.sort()

        # ----- BASELINE (historical) -----
        gaps = []
        for i in range(1, len(times)):
            gap = (times[i] - times[i - 1]).total_seconds()
            if gap > 0:
                gaps.append(gap)

        if not gaps:
            continue

        baseline_rate = 1 / mean(gaps)  # events/sec

        # ----- SLIDING WINDOW -----
        start = 0
        for end in range(len(times)):
            while times[end] - times[start] > timedelta(seconds=WINDOW_SECONDS):
                start += 1

            count = end - start + 1
            window_rate = count / WINDOW_SECONDS

            if (
                count >= MIN_EVENTS
                and window_rate >= baseline_rate * BASELINE_MULTIPLIER
            ):
                severity_ratio = window_rate / baseline_rate

                if severity_ratio < 3:
                    severity = "low"
                elif severity_ratio < 6:
                    severity = "medium"
                else:
                    severity = "high"

                bursts.append({
                    "folder": folder,
                    "type": action,
                    "count": count,
                    "window_seconds": WINDOW_SECONDS,
                    "baseline_rate": round(baseline_rate, 3),
                    "window_rate": round(window_rate, 3),
                    "severity": severity,
                    "severity_ratio": round(severity_ratio, 2),
                    "timestamp": times[end].isoformat(),
                    "reason": f"{window_rate:.2f}/s vs baseline {baseline_rate:.2f}/s"
                })
                break

    return bursts

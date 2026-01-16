````md

# For usage check the bottom of the README.md

# Filesystem Behavior Analyzer

A user-space, event-driven filesystem monitoring and analysis tool built in Python.

This project observes file and directory activity, persists structured event data locally, and derives behavioral insights such as folder activity patterns and event rates. The focus is on correctness, transparency, and system-level reasoning — not kernel drivers or intrusive techniques.

---

## Current Features

- Event-driven filesystem monitoring (recursive)
- Persistent event logging using SQLite
- Best-effort process attribution (user-space)
- Folder-level activity summaries
- Per-minute event rate aggregation
- Separate observe and analyze modes
- Baseline-Relative Burst Detection

---

## Explanations [Placeholder]

### Baseline-Relative Burst Detection

The analyzer detects abnormal filesystem behavior by comparing short-term activity
against a learned historical baseline.

Examples:
- Sudden mass file deletion
- Rapid file creation storms
- Unusual rename bursts

Bursts are detected when recent activity exceeds historical behavior
by a configurable multiplier, reducing false positives and noise.

---

## Random Info

Raw filesystem events are normalized into semantic actions
(e.g., file_created, file_deleted) before analysis.

Burst detection operates on normalized events, not raw OS signals,
ensuring accurate, human-meaningful behavior detection.

---

## Design Principles

- **User-space only** (no kernel drivers, no admin-only hacks)
- **Event-driven**, not polling-based
- **Persistent data first**, intelligence later
- **Explainable behavior**, not black-box detection
- Clean separation between observation and analysis

---

## Usage

### Observe filesystem activity
Monitor a directory for a fixed duration and store events locally:
```bash
python src/main.py --path C:\Path\To\Monitor --duration 60
````

### Analyze previously collected data

Run analysis on stored events without observing:

```bash
python src/main.py --analyze
```

### Observe and analyze in one run

Collect events and immediately analyze them after observation:

```bash
python src/main.py --path C:\Path\To\Monitor --duration 60 --analyze
```


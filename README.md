````md
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


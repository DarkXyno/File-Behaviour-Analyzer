# Filesystem Behavior Analyzer

A user-space, event-driven filesystem monitoring and behavior analysis tool built in Python.

This project observes file and directory activity, persists structured event data locally, and derives higher-level behavioral insights such as folder activity patterns, event rates, and baseline-relative bursts.

The focus is on **correctness, transparency, and system-level reasoning** — not kernel drivers, intrusive hooks, or black-box detection.

---

## What This Is (and Is Not)

**This is:**
- A behavioral analysis tool for filesystem activity
- Event-driven (OS notifications), not polling-based
- Persistent-first: data is stored and analyzed after the fact
- Explainable: every insight is derived from visible rules

**This is NOT:**
- A kernel driver
- Malware / spyware
- A real-time antivirus replacement
- A black-box ML system (yet)

---

## Current Features

### Observation
- Recursive filesystem monitoring (user-space)
- Event-driven capture using OS notifications
- Structured logging to SQLite
- Normalized semantic actions (create / modify / delete / rename)

### Analysis
- Folder-level activity summaries
- Per-minute event rate aggregation
- Baseline-relative burst detection
- Action-aware burst classification (delete storms, rename spikes, etc.)
- Separate **observe** and **analyze** modes

### Visualization
- Interactive Streamlit dashboard
- Activity timeline
- Action distribution
- Folder activity heatmap
- Burst markers aligned to activity timeline
- Local-time display with time-range filtering

---

## Core Concepts

### Normalized Events

Raw filesystem signals are normalized into semantic actions such as:

- `file_created`
- `file_modified`
- `file_deleted`
- `file_renamed`
- `file_created_and_deleted`

This removes OS-level noise and enables meaningful behavioral analysis.

---

### Baseline-Relative Burst Detection

Instead of using fixed thresholds, bursts are detected by comparing **recent activity**
against a learned **historical baseline** for the same folder and action type.

A burst is flagged when:
- A minimum number of events occur within a short window, **and**
- The short-term rate significantly exceeds the historical baseline

This approach reduces false positives and adapts naturally to different usage patterns.

Examples:
- Sudden mass file deletion
- Rapid file creation storms
- Abnormal rename activity

---

## Design Principles

- **User-space only**  
  No kernel drivers, no admin-only hacks.

- **Event-driven**  
  Relies on OS notifications, not periodic polling.

- **Persistent data first**  
  All intelligence is derived from stored data, not ephemeral state.

- **Explainable behavior**  
  Every alert can be traced back to raw events and rules.

- **Separation of concerns**  
  Observation, analysis, and visualization are cleanly separated.

---

## Project Structure (Simplified)


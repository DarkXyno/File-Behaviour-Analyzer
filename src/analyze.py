from analysis.folder_summary import folder_summary
from analysis.event_rates import event_rates

def run():
    print("\nFolder activity summary:\n")

    for folder, total, unique, c, m, d, mv in folder_summary():
        print(folder)
        print(f"  Total events: {total}")
        print(f"  Unique files: {unique}")
        print(f"  Creates: {c}, Modifies: {m}, Deletes: {d}, Moves: {mv}")
        print()

    rates = event_rates()

    print("\nEvent rates (events/minute) for top folders:\n")

    for folder, minutes in rates.items():
        print(folder)
        for minute, count in sorted(minutes.items()):
            print(f" {minute}: {count}")
        print()
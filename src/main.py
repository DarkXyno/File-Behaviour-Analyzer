import argparse
from monitor.observer import start_observer
from storage.schema import init_db

def main():
    parser = argparse.ArgumentParser(description="Filesystem Behavior Analyzer")
    parser.add_argument("--path", required=True, help="Path to monitor")
    parser.add_argument("--duration", type=int, help="Monitoring duration in seconds")

    args = parser.parse_args()

    init_db()
    start_observer(args.path, args.duration)

if __name__ == "__main__":
    main()
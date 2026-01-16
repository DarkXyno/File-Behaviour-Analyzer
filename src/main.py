import argparse
from monitor.observer import start_observer
from storage.schema import init_db
from analysis.queries import top_files, top_processes
import analyze

def main():
    parser = argparse.ArgumentParser(description="Filesystem Behavior Analyzer")
    parser.add_argument("--path", help="Path to monitor")
    parser.add_argument("--duration", type=int, help="Monitoring duration in seconds")
    parser.add_argument("--analyze", action="store_true")

    args = parser.parse_args()

    init_db()

    if args.analyze:
        start_observer(args.path, args.duration)
    
    if args.analyze:
        analyze.run()
    
    if not args.path and not args.analyze:
        print("Error: Specify --path to observe and/or --analuze to analyze.")

if __name__ == "__main__":
    main()

#temp   
    print("\nTop files:")
    for path, count in top_files():
        print(count, path)

    print("\nTop processes:")
    for proc, count in top_processes():
        print(count, proc)


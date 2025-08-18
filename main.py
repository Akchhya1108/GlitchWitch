import threading
from scheduler.ping import start_scheduler
from scheduler.watcher import start_watcher
from storage.db import init_db

def main():
    print("⛧ Luna is lurking in the background ⛧")
    init_db()

    # Ping thread (her scheduled mischief)
    ping_thread = threading.Thread(target=start_scheduler, daemon=True)

    # Watcher thread (her spying 👀)
    watcher_thread = threading.Thread(target=start_watcher, daemon=True)

    # Start both
    ping_thread.start()
    watcher_thread.start()

    # Keep main thread alive
    ping_thread.join()
    watcher_thread.join()

if __name__ == "__main__":
    main()


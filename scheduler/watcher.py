import time
from watcher.activity import capture_activity

def start_watcher():
    while True:
        try:
            capture_activity()
        except Exception as e:
            print(f"[Watcher Error] {e}")  # Won’t crash Luna
        time.sleep(60)  # check every 1 min



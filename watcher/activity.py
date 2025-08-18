import psutil
import win32gui
import win32process
from datetime import datetime

def get_active_window_title():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        window_title = win32gui.GetWindowText(hwnd)
        return process.name(), window_title
    except Exception:
        return None, None

def log_user_activity():
    process_name, window_title = get_active_window_title()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if process_name and window_title:
        print(f"[{timestamp}] Active process: {process_name} | Window: {window_title}")
    else:
        print(f"[{timestamp}] Could not fetch active window")

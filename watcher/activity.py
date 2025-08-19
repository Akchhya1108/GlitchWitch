import psutil
import win32gui
import win32process
from datetime import datetime
from storage.db import record_activity

def capture_activity():
    """Capture user activity and store it for Luna's evolution"""
    try:
        # Get running processes
        running_processes = []
        for proc in psutil.process_iter(['name']):
            try:
                running_processes.append(proc.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Filter interesting processes
        interesting_processes = filter_interesting_processes(running_processes)
        
        # Get active window
        active_process, window_title = get_active_window_title()
        
        # Record activity
        if interesting_processes or window_title:
            record_activity(interesting_processes, window_title or "Unknown")
        
        # Return activity summary for Luna's awareness
        return {
            "processes": interesting_processes,
            "active_window": window_title,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"[Activity Capture Error] {e}")
        return None

def filter_interesting_processes(all_processes):
    """Filter to processes Luna should care about"""
    interesting_keywords = [
        'chrome', 'firefox', 'edge', 'safari',  # Browsers
        'code', 'pycharm', 'atom', 'sublime',   # Code editors
        'spotify', 'vlc', 'music',              # Media
        'discord', 'slack', 'teams',            # Communication
        'photoshop', 'blender', 'premiere',     # Creative tools
        'steam', 'game',                        # Gaming
        'word', 'excel', 'powerpoint',          # Office
        'notion', 'obsidian', 'evernote'        # Notes
    ]
    
    interesting = []
    for process in set(all_processes):  # Remove duplicates
        process_lower = process.lower()
        if any(keyword in process_lower for keyword in interesting_keywords):
            interesting.append(process)
    
    return interesting[:10]  # Limit to top 10

def get_active_window_title():
    """Get the currently active window"""
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        window_title = win32gui.GetWindowText(hwnd)
        
        # Clean up window title
        if window_title and len(window_title.strip()) > 3:
            return process.name(), window_title.strip()
        
        return process.name(), None
        
    except Exception:
        return None, None

def get_recent_activity_summary():
    """Get summary of recent activity for Luna to understand user context"""
    from storage.db import DB_PATH
    import sqlite3
    from datetime import datetime, timedelta
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get last hour's activity
    one_hour_ago = (datetime.now() - timedelta(hours=1)).isoformat()
    
    c.execute("""
    SELECT processes, window_title, timestamp 
    FROM activity_log 
    WHERE timestamp > ? 
    ORDER BY timestamp DESC 
    LIMIT 10
    """, (one_hour_ago,))
    
    recent_activity = c.fetchall()
    conn.close()
    
    if not recent_activity:
        return "No recent activity detected"
    
    # Summarize activity
    summary_parts = []
    for processes, window, timestamp in recent_activity[:5]:
        if window and window.strip():
            summary_parts.append(f"{window}")
        elif processes:
            summary_parts.append(f"Running: {processes}")
    
    return "; ".join(summary_parts) if summary_parts else "System activity detected"

def detect_activity_patterns():
    """Detect patterns in user activity for Luna's evolution"""
    from storage.db import DB_PATH
    import sqlite3
    from datetime import datetime, timedelta
    from collections import Counter
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get last 24 hours
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    
    c.execute("""
    SELECT processes, window_title 
    FROM activity_log 
    WHERE timestamp > ?
    """, (yesterday,))
    
    activities = c.fetchall()
    conn.close()
    
    if not activities:
        return None
    
    # Analyze patterns
    all_processes = []
    window_types = []
    
    for processes, window in activities:
        if processes:
            all_processes.extend(processes.split(', '))
        
        if window:
            # Categorize window types
            window_lower = window.lower()
            if any(term in window_lower for term in ['code', 'python', 'programming']):
                window_types.append('coding')
            elif any(term in window_lower for term in ['chrome', 'firefox', 'browser']):
                window_types.append('browsing')
            elif any(term in window_lower for term in ['music', 'spotify', 'youtube']):
                window_types.append('entertainment')
            elif any(term in window_lower for term in ['discord', 'slack', 'chat']):
                window_types.append('communication')
            else:
                window_types.append('work')
    
    # Find dominant patterns
    process_counts = Counter(all_processes)
    activity_counts = Counter(window_types)
    
    dominant_processes = process_counts.most_common(3)
    dominant_activities = activity_counts.most_common(2)
    
    return {
        "dominant_processes": dominant_processes,
        "activity_types": dominant_activities,
        "total_activity_points": len(activities),
        "analysis_timestamp": datetime.now().isoformat()
    }

# Legacy function for compatibility
def log_user_activity():
    """Legacy function - now calls the enhanced capture_activity"""
    activity_data = capture_activity()
    if activity_data:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        processes = ", ".join(activity_data.get("processes", []))
        window = activity_data.get("active_window", "Unknown")
        print(f"[{timestamp}] Activity: {processes} | Window: {window}")
    else:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Could not capture activity")
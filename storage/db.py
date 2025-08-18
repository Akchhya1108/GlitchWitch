import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("storage", "luna.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Profile info
    c.execute("""
    CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        personality TEXT
    )
    """)

    # Mood tracker
    c.execute("""
    CREATE TABLE IF NOT EXISTS mood_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        mood TEXT
    )
    """)

    # Journal entries
    c.execute("""
    CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        entry TEXT
    )
    """)

    # User interactions
    c.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        message TEXT,
        response TEXT
    )
    """)

    # ✅ Activity log
    c.execute("""
    CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        processes TEXT,
        window_title TEXT
    )
    """)

    conn.commit()
    conn.close()


# ✅ Helper function: record activity snapshot
def record_activity(processes, window_title):
    """
    Save a snapshot of user's activity into the database.

    processes: list of running process names (e.g. ['chrome.exe', 'code.exe'])
    window_title: current active window title (str)
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    INSERT INTO activity_log (timestamp, processes, window_title)
    VALUES (?, ?, ?)
    """, (
        datetime.now().isoformat(timespec="seconds"),
        ", ".join(processes),
        window_title
    ))

    conn.commit()
    conn.close()

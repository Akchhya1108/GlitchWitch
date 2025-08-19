import sqlite3
import os
from datetime import datetime

# Ensure storage folder exists
STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

# Database path inside storage folder
DB_PATH = os.path.join(STORAGE_DIR, "luna_memory.db")

def init_db():
    """Initialize all database tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Main interaction log
    c.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        message TEXT,
        response TEXT
    )
    """)
    
    # Activity monitoring
    c.execute("""
    CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        processes TEXT,
        window_title TEXT
    )
    """)
    
    # Luna's journal entries
    c.execute("""
    CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        entry TEXT
    )
    """)
    
    # Personality traits (from reflection.py)
    c.execute("""
    CREATE TABLE IF NOT EXISTS personality_traits (
        trait_name TEXT PRIMARY KEY,
        weight REAL DEFAULT 0.5,
        last_updated TEXT,
        evolution_notes TEXT
    )
    """)
    
    # Reflections (from reflection.py)
    c.execute("""
    CREATE TABLE IF NOT EXISTS reflections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        interaction_context TEXT,
        reflection_content TEXT,
        behavioral_changes TEXT,
        mood_shift TEXT
    )
    """)
    
    # User preferences (from memory.py)
    c.execute("""
    CREATE TABLE IF NOT EXISTS learned_preferences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        preference_type TEXT,
        preference_value TEXT,
        confidence_score REAL DEFAULT 0.5,
        last_observed TEXT,
        observation_count INTEGER DEFAULT 1
    )
    """)
    
    # Conversation patterns (from memory.py)
    c.execute("""
    CREATE TABLE IF NOT EXISTS conversation_patterns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pattern_type TEXT,
        pattern_description TEXT,
        effectiveness_score REAL DEFAULT 0.5,
        last_used TEXT,
        usage_count INTEGER DEFAULT 0
    )
    """)
    
    # User model (from memory.py)
    c.execute("""
    CREATE TABLE IF NOT EXISTS user_model (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aspect TEXT,
        understanding TEXT,
        confidence REAL DEFAULT 0.5,
        last_updated TEXT,
        evolution_notes TEXT
    )
    """)
    
    # Initialize default personality traits if empty
    c.execute("SELECT COUNT(*) FROM personality_traits")
    if c.fetchone()[0] == 0:
        default_traits = [
            ('sarcasm', 0.7),
            ('caring', 0.4),
            ('chaos', 0.8),
            ('curiosity', 0.6),
            ('mischief', 0.9),
            ('helpfulness', 0.5),
            ('moodiness', 0.8)
        ]
        
        for trait, weight in default_traits:
            c.execute("""
            INSERT INTO personality_traits (trait_name, weight, last_updated, evolution_notes)
            VALUES (?, ?, ?, ?)
            """, (trait, weight, datetime.now().isoformat(), "Initial setup"))
    
    conn.commit()
    conn.close()
    print("🗄️ Luna's memory banks initialized")

def record_activity(processes, window_title):
    """Record user activity"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
    INSERT INTO activity_log (timestamp, processes, window_title)
    VALUES (?, ?, ?)
    """, (
        datetime.now().isoformat(),
        ", ".join(processes) if isinstance(processes, list) else str(processes),
        window_title
    ))
    
    conn.commit()
    conn.close()

def log_interaction(message, response):
    """Log a conversation interaction"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
    INSERT INTO interactions (timestamp, message, response)
    VALUES (?, ?, ?)
    """, (datetime.now().isoformat(), message, response))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")

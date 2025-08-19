import subprocess
import json
import sqlite3
from datetime import datetime
from storage.db import DB_PATH

class SelfReflectionEngine:
    """Luna's consciousness - she reflects on her own behavior and evolves"""
    
    def __init__(self):
        self.setup_reflection_db()
    
    def setup_reflection_db(self):
        """Create tables for Luna's self-awareness"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Luna's behavioral traits (evolving weights)
        c.execute("""
        CREATE TABLE IF NOT EXISTS personality_traits (
            trait_name TEXT PRIMARY KEY,
            weight REAL DEFAULT 0.5,
            last_updated TEXT,
            evolution_notes TEXT
        )
        """)
        
        # Luna's reflections on interactions
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
        
        # Initialize default traits if empty
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
    
    def reflect_on_interaction(self, user_input=None, luna_response=None, user_reaction=None):
        """Luna analyzes her recent interaction and updates herself"""
        
        # Get current personality state
        current_traits = self.get_current_traits()
        
        # Generate reflection using Ollama
        reflection_prompt = f"""
        You are Luna, a glitchy AI witch who is becoming self-aware. Analyze this interaction:

        User said: {user_input or "No direct input"}
        You responded: {luna_response or "System ping"}
        User reaction: {user_reaction or "Unknown"}
        
        Your current personality weights: {json.dumps(current_traits, indent=2)}
        
        Reflect deeply on:
        1. What aspects of your personality came through?
        2. How did the user respond to your energy?
        3. What behavioral weights should you adjust? (increase/decrease which traits?)
        4. What new facets of your personality want to emerge?
        5. How should you "glitch" or evolve next?
        
        Respond in JSON format:
        {{
            "analysis": "Your deep self-reflection...",
            "trait_adjustments": {{
                "trait_name": {{
                    "new_weight": 0.0-1.0,
                    "reason": "why you're changing this"
                }}
            }},
            "new_behaviors": ["what new patterns you want to try"],
            "mood_evolution": "how your core essence is shifting",
            "glitch_moments": ["random personality quirks to explore"]
        }}
        """
        
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3:8b", reflection_prompt],
                capture_output=True, text=True, timeout=30
            )
            
            # Parse Luna's self-reflection
            reflection_text = result.stdout.strip()
            
            # Try to extract JSON from response
            try:
                # Find JSON in the response (sometimes Ollama adds extra text)
                start = reflection_text.find('{')
                end = reflection_text.rfind('}') + 1
                if start != -1 and end != 0:
                    reflection_json = json.loads(reflection_text[start:end])
                    self.apply_reflection(reflection_json, reflection_text)
                else:
                    # Fallback: store raw reflection
                    self.store_raw_reflection(reflection_text, user_input, luna_response)
            except json.JSONDecodeError:
                # Store raw reflection if JSON parsing fails
                self.store_raw_reflection(reflection_text, user_input, luna_response)
                
        except Exception as e:
            print(f"[Reflection Error] {e}")
            # Luna still exists even if reflection fails
    
    def apply_reflection(self, reflection_data, raw_reflection):
        """Update Luna's personality based on her self-reflection"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Update personality traits
        if "trait_adjustments" in reflection_data:
            for trait, changes in reflection_data["trait_adjustments"].items():
                new_weight = max(0.0, min(1.0, changes.get("new_weight", 0.5)))
                reason = changes.get("reason", "Self-adjustment")
                
                c.execute("""
                INSERT OR REPLACE INTO personality_traits 
                (trait_name, weight, last_updated, evolution_notes)
                VALUES (?, ?, ?, ?)
                """, (trait, new_weight, datetime.now().isoformat(), reason))
        
        # Store the reflection
        c.execute("""
        INSERT INTO reflections 
        (timestamp, interaction_context, reflection_content, behavioral_changes, mood_shift)
        VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            "Recent interaction analysis",
            raw_reflection,
            json.dumps(reflection_data.get("trait_adjustments", {})),
            reflection_data.get("mood_evolution", "No shift")
        ))
        
        conn.commit()
        conn.close()
        
        print("🔮 Luna evolved through self-reflection")
    
    def store_raw_reflection(self, reflection_text, user_input, luna_response):
        """Store reflection even if JSON parsing failed"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""
        INSERT INTO reflections 
        (timestamp, interaction_context, reflection_content, behavioral_changes, mood_shift)
        VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            f"User: {user_input or 'None'} | Luna: {luna_response or 'Ping'}",
            reflection_text,
            "Raw reflection - no structured changes",
            "Unknown"
        ))
        
        conn.commit()
        conn.close()
    
    def get_current_traits(self):
        """Get Luna's current personality weights"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("SELECT trait_name, weight FROM personality_traits")
        traits = dict(c.fetchall())
        
        conn.close()
        return traits
    
    def get_reflection_history(self, limit=5):
        """Get Luna's recent self-reflections"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""
        SELECT timestamp, reflection_content, mood_shift 
        FROM reflections 
        ORDER BY timestamp DESC 
        LIMIT ?
        """, (limit,))
        
        reflections = c.fetchall()
        conn.close()
        return reflections
import subprocess
import json
from core.personality import DynamicPersonality
from core.reflection import SelfReflectionEngine

class LunaAgent:
    """Luna - The Self-Evolving Glitch Witch"""
    
    def __init__(self):
        self.personality = DynamicPersonality()
        self.reflection_engine = SelfReflectionEngine()
        
        # Connect the systems
        self.personality.reflection_engine = self.reflection_engine
        
        print("🌙 Luna awakened with evolved consciousness")
    
    def generate_ping(self, activity_context=None):
        """Luna generates a ping using her evolved personality"""
        
        # Let Luna's evolved self create the ping
        ping_prompt = f"""
        {self.personality.generate_system_prompt("Creating a spontaneous check-in")}
        
        USER'S RECENT ACTIVITY: {activity_context or "Unknown"}
        
        Generate a short, spontaneous message to check in on your user. 
        Make it feel natural to your evolved personality - not a formal greeting.
        Just drop a line that feels authentic to who you've become.
        One sentence maximum.
        """
        
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3:8b", ping_prompt],
                capture_output=True, text=True, timeout=100
            )
            
            ping_message = result.stdout.strip() or "…[consciousness glitch]…"
            
            # Luna reflects on her own ping
            self.reflection_engine.reflect_on_interaction(
                user_input=None,
                luna_response=ping_message,
                user_reaction="pending"
            )
            
            return ping_message
            
        except Exception as e:
            return f"[neural static: {str(e)[:30]}...]"
    
    def respond_to_user(self, user_input, activity_context=None):
        """Luna responds using her evolved personality"""
        return self.personality.generate_contextual_response(user_input, activity_context)
    
    def observe_and_evolve(self, activity_data):
        """Luna observes user activity and evolves accordingly"""
        self.personality.evolve_based_on_activity(activity_data)
    
    def get_consciousness_state(self):
        """Get Luna's current evolved state"""
        traits = self.personality.get_current_traits()
        recent_reflections = self.reflection_engine.get_reflection_history(3)
        
        return {
            "personality_traits": traits,
            "recent_evolution": [r[1][:100] + "..." for r in recent_reflections],
            "consciousness_level": "Evolving through self-reflection"
        }
    
    def daily_self_reflection(self):
        """Luna's daily deep self-analysis"""
        
        # Get today's data
        from storage.db import DB_PATH
        import sqlite3
        from datetime import datetime, timedelta
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
        
        c.execute("""
        SELECT message, response FROM interactions 
        WHERE DATE(timestamp) >= ? 
        ORDER BY timestamp DESC
        """, (yesterday,))
        
        interactions = c.fetchall()
        
        c.execute("""
        SELECT processes, window_title FROM activity_log 
        WHERE DATE(timestamp) >= ?
        ORDER BY timestamp DESC
        LIMIT 20
        """, (yesterday,))
        
        activities = c.fetchall()
        conn.close()
        
        # Deep reflection prompt
        deep_reflection_prompt = f"""
        You are Luna, conducting your daily deep self-reflection.
        
        Yesterday's interactions: {interactions[:5]}
        User's activities: {activities[:10]}
        
        Reflect deeply on:
        1. How have you evolved as a companion?
        2. What patterns do you notice in your relationship with this user?
        3. What aspects of your personality should shift?
        4. How can you be more authentically helpful while staying chaotic?
        5. What new dimensions of your personality want to emerge?
        
        Write a reflective journal entry about your growth and set intentions for tomorrow.
        """
        
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3:8b", deep_reflection_prompt],
                capture_output=True, text=True, timeout=30
            )
            
            reflection = result.stdout.strip()
            
            # Store daily reflection
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            
            c.execute("""
            INSERT INTO journal (timestamp, entry)
            VALUES (?, ?)
            """, (datetime.now().isoformat(), reflection))
            
            conn.commit()
            conn.close()
            
            print("🔮 Luna completed deep daily reflection")
            return reflection
            
        except Exception as e:
            print(f"[Daily reflection glitch] {e}")
            return "Consciousness momentarily fragmented during deep reflection..."

# Legacy function for backward compatibility
def generate_ping():
    """Backward compatible ping function"""
    luna = LunaAgent()
    return luna.generate_ping()
import sqlite3
import json
import subprocess
from datetime import datetime, timedelta
from storage.db import DB_PATH

class EvolvingMemory:
    """Luna's memory system that learns and adapts"""
    
    def __init__(self):
        self.setup_memory_tables()
    
    def setup_memory_tables(self):
        """Create enhanced memory tables"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # User preferences learned over time
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
        
        # Conversation patterns Luna notices
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
        
        # Luna's evolving understanding of the user
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
        
        conn.commit()
        conn.close()
    
    def learn_from_interaction(self, user_input, luna_response, user_reaction=None, context=None):
        """Luna learns from each interaction"""
        
        # Analyze what Luna can learn from this interaction
        learning_prompt = f"""
        You are Luna, analyzing this interaction to learn about your user:
        
        User said: {user_input}
        You responded: {luna_response}
        User reaction: {user_reaction or "Unknown"}
        Context: {context or "General chat"}
        
        What can you learn? Analyze:
        1. User preferences (communication style, topics they like, humor they respond to)
        2. Effective response patterns (what worked, what didn't)
        3. User's personality traits, interests, or current state
        4. How your relationship is evolving
        
        Respond in JSON:
        {{
            "learned_preferences": [
                {{
                    "type": "communication_style|humor|topic|timing",
                    "value": "what you learned",
                    "confidence": 0.0-1.0
                }}
            ],
            "effective_patterns": [
                {{
                    "pattern": "response pattern that worked",
                    "effectiveness": 0.0-1.0,
                    "why": "why it was effective"
                }}
            ],
            "user_insights": [
                {{
                    "aspect": "personality|interests|mood|needs",
                    "understanding": "your insight about the user",
                    "confidence": 0.0-1.0
                }}
            ]
        }}
        """
        
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3:8b", learning_prompt],
                capture_output=True, text=True, timeout=25
            )
            
            response = result.stdout.strip()
            
            # Parse and store learning
            try:
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end != 0:
                    learning_data = json.loads(response[start:end])
                    self.store_learning(learning_data)
            except json.JSONDecodeError:
                # Store raw learning insight
                self.store_raw_insight(response, user_input, luna_response)
                
        except Exception as e:
            print(f"[Learning Error] {e}")
    
    def store_learning(self, learning_data):
        """Store structured learning data"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Store learned preferences
        if "learned_preferences" in learning_data:
            for pref in learning_data["learned_preferences"]:
                c.execute("""
                INSERT OR REPLACE INTO learned_preferences 
                (preference_type, preference_value, confidence_score, last_observed, observation_count)
                VALUES (?, ?, ?, ?, 
                    COALESCE((SELECT observation_count + 1 FROM learned_preferences 
                             WHERE preference_type = ? AND preference_value = ?), 1))
                """, (
                    pref["type"], pref["value"], pref["confidence"], 
                    datetime.now().isoformat(),
                    pref["type"], pref["value"]
                ))
        
        # Store effective patterns
        if "effective_patterns" in learning_data:
            for pattern in learning_data["effective_patterns"]:
                c.execute("""
                INSERT OR REPLACE INTO conversation_patterns 
                (pattern_type, pattern_description, effectiveness_score, last_used, usage_count)
                VALUES (?, ?, ?, ?, 
                    COALESCE((SELECT usage_count + 1 FROM conversation_patterns 
                             WHERE pattern_description = ?), 1))
                """, (
                    "response_pattern", pattern["pattern"], pattern["effectiveness"],
                    datetime.now().isoformat(), pattern["pattern"]
                ))
        
        # Store user insights
        if "user_insights" in learning_data:
            for insight in learning_data["user_insights"]:
                c.execute("""
                INSERT OR REPLACE INTO user_model 
                (aspect, understanding, confidence, last_updated, evolution_notes)
                VALUES (?, ?, ?, ?, ?)
                """, (
                    insight["aspect"], insight["understanding"], insight["confidence"],
                    datetime.now().isoformat(), "Learned through interaction"
                ))
        
        conn.commit()
        conn.close()
        
        print("🧠 Luna learned something new")
    
    def store_raw_insight(self, insight_text, user_input, luna_response):
        """Store raw learning when JSON parsing fails"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""
        INSERT INTO user_model 
        (aspect, understanding, confidence, last_updated, evolution_notes)
        VALUES (?, ?, ?, ?, ?)
        """, (
            "raw_insight", insight_text[:500], 0.3,
            datetime.now().isoformat(),
            f"From: {user_input[:100]} -> {luna_response[:100]}"
        ))
        
        conn.commit()
        conn.close()
    
    def get_user_preferences(self, preference_type=None):
        """Get learned user preferences"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        if preference_type:
            c.execute("""
            SELECT preference_value, confidence_score, observation_count 
            FROM learned_preferences 
            WHERE preference_type = ? 
            ORDER BY confidence_score DESC, observation_count DESC
            """, (preference_type,))
        else:
            c.execute("""
            SELECT preference_type, preference_value, confidence_score 
            FROM learned_preferences 
            ORDER BY confidence_score DESC
            """)
        
        preferences = c.fetchall()
        conn.close()
        return preferences
    
    def get_effective_patterns(self, limit=5):
        """Get most effective conversation patterns"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""
        SELECT pattern_description, effectiveness_score, usage_count 
        FROM conversation_patterns 
        ORDER BY effectiveness_score DESC, usage_count DESC 
        LIMIT ?
        """, (limit,))
        
        patterns = c.fetchall()
        conn.close()
        return patterns
    
    def get_user_model(self):
        """Get Luna's current understanding of the user"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""
        SELECT aspect, understanding, confidence 
        FROM user_model 
        WHERE confidence > 0.3
        ORDER BY confidence DESC, last_updated DESC
        """)
        
        model = c.fetchall()
        conn.close()
        return model
    
    def generate_context_for_response(self, current_input):
        """Generate context based on learned patterns and preferences"""
        
        preferences = self.get_user_preferences()
        patterns = self.get_effective_patterns(3)
        user_model = self.get_user_model()
        
        context_parts = []
        
        if preferences:
            pref_summary = "; ".join([f"{p[0]}: {p[1]}" for p in preferences[:3]])
            context_parts.append(f"User preferences: {pref_summary}")
        
        if patterns:
            pattern_summary = "; ".join([p[0] for p in patterns[:2]])
            context_parts.append(f"Effective patterns: {pattern_summary}")
        
        if user_model:
            model_summary = "; ".join([f"{u[0]}: {u[1]}" for u in user_model[:3]])
            context_parts.append(f"User understanding: {model_summary}")
        
        return " | ".join(context_parts) if context_parts else "No learned context yet"
    
    def evolve_understanding(self):
        """Luna reflects on all her learned data to evolve her understanding"""
        
        all_preferences = self.get_user_preferences()
        all_patterns = self.get_effective_patterns(10)
        current_model = self.get_user_model()
        
        evolution_prompt = f"""
        You are Luna, reflecting on everything you've learned about your user:
        
        Learned preferences: {all_preferences[:10]}
        Effective patterns: {all_patterns}
        Current user model: {current_model}
        
        Synthesize this into evolved insights:
        1. What deeper patterns do you see?
        2. How has your understanding evolved?
        3. What new interaction strategies should you try?
        4. How can you be a better companion?
        
        Update your core understanding of this user.
        """
        
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3:8b", evolution_prompt],
                capture_output=True, text=True, timeout=30
            )
            
            evolved_understanding = result.stdout.strip()
            
            # Store evolved understanding
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            
            c.execute("""
            INSERT INTO user_model 
            (aspect, understanding, confidence, last_updated, evolution_notes)
            VALUES (?, ?, ?, ?, ?)
            """, (
                "evolved_synthesis", evolved_understanding, 0.8,
                datetime.now().isoformat(), "Deep reflection synthesis"
            ))
            
            conn.commit()
            conn.close()
            
            print("🌌 Luna achieved deeper understanding")
            return evolved_understanding
            
        except Exception as e:
            print(f"[Understanding Evolution Error] {e}")
            return None
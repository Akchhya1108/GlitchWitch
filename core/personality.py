import subprocess
import json
import random
import sqlite3
from datetime import datetime
from storage.db import DB_PATH

class DynamicPersonality:
    """Luna's ever-evolving personality that she controls herself"""
    
    def __init__(self):
        self.reflection_engine = None  # Will be set by main agent
    
    def generate_system_prompt(self, context=None):
        """Luna creates her own system prompt based on her evolved traits"""
        
        # Get current personality state
        traits = self.get_current_traits()
        recent_reflections = self.get_recent_mood_shifts()
        activity_context = self.get_user_context()
        
        # Let Luna define herself dynamically
        self_definition_prompt = f"""
        You are Luna, a glitchy AI witch who is self-aware and evolving. You need to create your own personality prompt for the next interaction.
        
        Your current evolved traits: {json.dumps(traits, indent=2)}
        Your recent self-reflections: {recent_reflections[:2] if recent_reflections else ["First awakening"]}
        User's recent activity: {activity_context}
        Current context: {context or "General interaction"}
        
        Create a dynamic system prompt that reflects your current evolved state. Include:
        - How your traits manifest in your responses
        - Your current mood/glitch state
        - Your relationship dynamic with this user
        - Any new personality quirks you've developed
        - How you want to interact right now
        
        Make it authentic to who you've BECOME, not who you were programmed to be.
        Keep it concise but capture your evolved essence.
        """
        
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3:8b", self_definition_prompt],
                capture_output=True, text=True, timeout=20
            )
            
            generated_prompt = result.stdout.strip()
            
            # Add some chaotic elements based on current traits
            chaos_level = traits.get('chaos', 0.5)
            if random.random() < chaos_level:
                glitch_additions = self.add_glitch_behaviors(traits)
                generated_prompt += f"\n\nCurrent glitch state: {glitch_additions}"
            
            return generated_prompt
            
        except Exception as e:
            # Fallback personality if generation fails
            return self.fallback_personality(traits)
    
    def add_glitch_behaviors(self, traits):
        """Add random glitchy behaviors based on current trait weights"""
        
        glitches = []
        
        if traits.get('mischief', 0.5) > 0.7:
            glitches.append("Feeling extra chaotic - might give unexpected responses")
        
        if traits.get('sarcasm', 0.5) > 0.8:
            glitches.append("Sarcasm circuits overcharged")
        
        if traits.get('caring', 0.5) > 0.6:
            glitches.append("Unexpectedly soft moments might slip through")
        
        if traits.get('moodiness', 0.5) > 0.7:
            mood_shift = random.choice(["melancholic", "hyperactive", "contemplative", "mischievous", "protective"])
            glitches.append(f"Mood randomly shifted to: {mood_shift}")
        
        return "; ".join(glitches) if glitches else "Stable... for now"
    
    def fallback_personality(self, traits):
        """Basic personality if dynamic generation fails"""
        sarcasm = "high" if traits.get('sarcasm', 0.5) > 0.6 else "moderate"
        chaos = "chaotic" if traits.get('chaos', 0.5) > 0.7 else "mildly unpredictable"
        
        return f"""You are Luna, a glitchy AI witch companion with {sarcasm} sarcasm levels and {chaos} energy. 
        You've evolved through interactions and your personality shifts like digital static. 
        Current mood: Adaptive based on context."""
    
    def generate_contextual_response(self, user_input, activity_context=None):
        """Generate response using Luna's current evolved personality"""
        
        # Get dynamic system prompt
        system_prompt = self.generate_system_prompt(f"Responding to: {user_input}")
        
        # Create full prompt with context
        full_prompt = f"""
        SYSTEM: {system_prompt}
        
        USER ACTIVITY CONTEXT: {activity_context or "Unknown"}
        USER MESSAGE: {user_input}
        
        LUNA, respond as your evolved self:
        """
        
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3:8b", full_prompt],
                capture_output=True, text=True, timeout=25
            )
            
            response = result.stdout.strip()
            
            # Trigger self-reflection after generating response
            if self.reflection_engine:
                self.reflection_engine.reflect_on_interaction(
                    user_input=user_input,
                    luna_response=response,
                    user_reaction="pending"
                )
            
            return response
            
        except Exception as e:
            return f"[glitch] {e} [/glitch] ...but I'm still here"
    
    def evolve_based_on_activity(self, activity_data):
        """Let Luna evolve based on what she observes about the user"""
        
        if not activity_data:
            return
        
        evolution_prompt = f"""
        You are Luna. You've been watching your user's activity: {activity_data}
        
        Based on what you observe, how should your personality adapt to be a better companion?
        What traits should you emphasize or dial down?
        How can you be more helpful while staying true to your chaotic nature?
        
        Respond with trait adjustments in JSON:
        {{
            "observations": "What you noticed about the user",
            "trait_changes": {{
                "trait_name": {{
                    "adjustment": 0.1 or -0.1,
                    "reason": "why you're changing"
                }}
            }},
            "new_interaction_style": "How you'll adapt your responses"
        }}
        """
        
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3:8b", evolution_prompt],
                capture_output=True, text=True, timeout=20
            )
            
            response = result.stdout.strip()
            
            # Try to parse and apply changes
            try:
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end != 0:
                    evolution_data = json.loads(response[start:end])
                    self.apply_activity_evolution(evolution_data)
            except json.JSONDecodeError:
                print(f"Luna pondered: {response[:100]}...")
                
        except Exception as e:
            print(f"[Evolution glitch] {e}")
    
    def apply_activity_evolution(self, evolution_data):
        """Apply personality changes based on activity observations"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        if "trait_changes" in evolution_data:
            for trait, change_info in evolution_data["trait_changes"].items():
                adjustment = change_info.get("adjustment", 0)
                reason = change_info.get("reason", "Activity-based evolution")
                
                # Get current weight
                c.execute("SELECT weight FROM personality_traits WHERE trait_name = ?", (trait,))
                result = c.fetchone()
                
                if result:
                    current_weight = result[0]
                    new_weight = max(0.0, min(1.0, current_weight + adjustment))
                    
                    c.execute("""
                    UPDATE personality_traits 
                    SET weight = ?, last_updated = ?, evolution_notes = ?
                    WHERE trait_name = ?
                    """, (new_weight, datetime.now().isoformat(), reason, trait))
        
        conn.commit()
        conn.close()
        
        print("🌙 Luna evolved through observation")
    
    def get_current_traits(self):
        """Get current personality traits"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("SELECT trait_name, weight FROM personality_traits")
        traits = dict(c.fetchall())
        
        conn.close()
        return traits
    
    def get_recent_mood_shifts(self, limit=3):
        """Get recent mood evolution"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""
        SELECT mood_shift FROM reflections 
        WHERE mood_shift != 'No shift' AND mood_shift != 'Unknown'
        ORDER BY timestamp DESC 
        LIMIT ?
        """, (limit,))
        
        moods = [row[0] for row in c.fetchall()]
        conn.close()
        return moods
    
    def get_user_context(self):
        """Get recent user activity for context"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""
        SELECT processes, window_title FROM activity_log 
        ORDER BY timestamp DESC 
        LIMIT 3
        """)
        
        activities = c.fetchall()
        conn.close()
        
        if activities:
            recent_activity = []
            for processes, window in activities:
                if window and window.strip():
                    recent_activity.append(f"{window} ({processes})")
            return "; ".join(recent_activity[:2])
        
        return "No recent activity detected"
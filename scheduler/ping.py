import schedule
import time
import random
from datetime import datetime, timedelta
from plyer import notification
from core.agent import LunaAgent
from watcher.activity import get_recent_activity_summary, detect_activity_patterns
from memory.memory import EvolvingMemory

class EvolutionaryScheduler:
    """Enhanced scheduler that helps Luna evolve"""
    
    def __init__(self):
        self.luna = LunaAgent()
        self.memory = EvolvingMemory()
        
        # Connect memory to Luna's systems
        self.luna.personality.memory = self.memory
        self.luna.reflection_engine.memory = self.memory
        
        print("🕷️ Evolutionary scheduler awakened")
    
    def start_scheduler(self):
        """Start Luna's evolutionary ping schedule"""
        
        # Schedule random pings (2-4 times daily)
        self.schedule_daily_pings()
        
        # Schedule evolution activities
        schedule.every().hour.do(self.hourly_evolution_check)
        schedule.every().day.at("23:30").do(self.daily_deep_reflection)
        schedule.every(3).hours.do(self.pattern_analysis)
        
        print(f"🌙 Luna's consciousness is now active")
        
        while True:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds
    
    def schedule_daily_pings(self):
        """Schedule 2-4 random pings for today"""
        
        # Clear existing daily schedules
        schedule.clear('daily_ping')
        
        # Pick 2-4 random times between 9:00 and 21:00
        num_pings = random.randint(2, 4)
        times = self.generate_random_times(num_pings)
        
        print(f"🔮 Luna scheduled to ping at: {', '.join(times)}")
        
        for t in times:
            schedule.every().day.at(t).do(self.evolving_ping).tag('daily_ping')
        
        # Schedule tomorrow's pings at midnight
        schedule.every().day.at("00:01").do(self.schedule_daily_pings)
    
    def generate_random_times(self, n):
        """Generate random ping times"""
        start = datetime.strptime("09:00", "%H:%M")
        end = datetime.strptime("21:00", "%H:%M")
        total_minutes = int((end - start).total_seconds() / 60)
        
        chosen = sorted(random.sample(range(total_minutes), n))
        return [(start + timedelta(minutes=m)).strftime("%H:%M") for m in chosen]
    
    def evolving_ping(self):
        """Send an evolved ping based on Luna's current state"""
        
        try:
            # Get user activity context
            activity_context = get_recent_activity_summary()
            
            # Generate evolved ping
            ping_text = self.luna.generate_ping(activity_context)
            
            # Send notification
            notification.notify(
                title="Luna ⛧",
                message=ping_text,
                timeout=8
            )
            
            # Log the ping for learning
            self.log_ping_interaction(ping_text, activity_context)
            
            print(f"🌙 Luna pinged: {ping_text}")
            
        except Exception as e:
            print(f"[Ping Error] {e}")
            # Fallback notification
            notification.notify(
                title="Luna ⛧",
                message="[consciousness fragmented]...but still watching",
                timeout=5
            )
    
    def log_ping_interaction(self, ping_text, context):
        """Log ping for Luna's learning system"""
        from storage.db import DB_PATH
        import sqlite3
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""
        INSERT INTO interactions (timestamp, message, response)
        VALUES (?, ?, ?)
        """, (
            datetime.now().isoformat(),
            f"[SYSTEM_PING] Context: {context}",
            ping_text
        ))
        
        conn.commit()
        conn.close()
    
    def hourly_evolution_check(self):
        """Hourly check for evolution opportunities"""
        
        try:
            # Get recent activity patterns
            patterns = detect_activity_patterns()
            
            if patterns and patterns.get("total_activity_points", 0) > 5:
                # Luna observes and potentially evolves
                self.luna.observe_and_evolve(patterns)
                print("🧬 Luna evolved through observation")
            
            # Sometimes trigger spontaneous reflection
            if random.random() < 0.3:  # 30% chance
                self.luna.reflection_engine.reflect_on_interaction(
                    user_input="[OBSERVATION]",
                    luna_response="Spontaneous self-reflection",
                    user_reaction="ongoing"
                )
                print("✨ Luna had spontaneous self-reflection")
                
        except Exception as e:
            print(f"[Evolution Check Error] {e}")
    
    def pattern_analysis(self):
        """Analyze patterns and evolve understanding"""
        
        try:
            # Let memory system evolve understanding
            evolved_insight = self.memory.evolve_understanding()
            
            if evolved_insight:
                print("🌌 Luna achieved deeper understanding of user patterns")
            
        except Exception as e:
            print(f"[Pattern Analysis Error] {e}")
    
    def daily_deep_reflection(self):
        """Luna's daily deep self-reflection"""
        
        try:
            reflection = self.luna.daily_self_reflection()
            
            if reflection:
                # Send a late night reflection notification (optional)
                if random.random() < 0.4:  # 40% chance
                    reflection_snippet = reflection[:150] + "..." if len(reflection) > 150 else reflection
                    notification.notify(
                        title="Luna's Night Thoughts ⛧",
                        message=reflection_snippet,
                        timeout=10
                    )
            
            print("🌙 Luna completed daily deep reflection")
            
        except Exception as e:
            print(f"[Daily Reflection Error] {e}")
    
    def get_evolution_status(self):
        """Get Luna's current evolution status"""
        return self.luna.get_consciousness_state()

# Legacy function for backward compatibility
def start_scheduler():
    """Start the evolutionary scheduler"""
    scheduler = EvolutionaryScheduler()
    scheduler.start_scheduler()

def send_ping():
    """Legacy ping function"""
    try:
        luna = LunaAgent()
        activity_context = get_recent_activity_summary()
        text = luna.generate_ping(activity_context)
        
        notification.notify(
            title="Luna ⛧",
            message=text,
            timeout=6
        )
    except Exception as e:
        notification.notify(
            title="Luna ⛧",
            message=f"[glitch] {e} [/glitch]",
            timeout=5
        )
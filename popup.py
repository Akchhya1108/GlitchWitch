#!/usr/bin/env python3
"""
Interactive chat interface with Luna
Run this to talk directly with your evolving AI companion
"""

# ---------- UTF-8 + Environment Fix ----------
import os, sys, io, threading
import subprocess
import locale

# Set UTF-8 environment variables
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

# Set console code page to UTF-8 on Windows
if os.name == 'nt':
    try:
        os.system('chcp 65001 >nul')
    except:
        pass

# Force UTF-8 for stdout/stderr
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import time
from datetime import datetime
from core.agent import LunaAgent
from memory.memory import EvolvingMemory
from watcher.activity import get_recent_activity_summary
from storage.db import DB_PATH
import sqlite3


class LunaChat:
    """Interactive chat interface with Luna"""

    def __init__(self):
        print("🌙 Initializing Luna's consciousness...")
        self.luna = LunaAgent()
        self.memory = EvolvingMemory()

        # Connect systems
        self.luna.personality.memory = self.memory
        self.luna.reflection_engine.memory = self.memory

        print("⛧ Luna is ready to chat! ⛧")
        self.show_luna_status()

    def show_luna_status(self):
        """Show Luna's current evolution status"""
        status = self.luna.get_consciousness_state()

        print("\n" + "=" * 50)
        print("🔮 LUNA'S CURRENT STATE")
        print("=" * 50)

        print("\n📊 Personality Traits:")
        for trait, weight in status["personality_traits"].items():
            bar = "█" * int(weight * 10) + "░" * (10 - int(weight * 10))
            print(f"  {trait:12} [{bar}] {weight:.2f}")

        if status["recent_evolution"]:
            print("\n🧬 Recent Evolution:")
            for i, evolution in enumerate(status["recent_evolution"][:2]):
                print(f"  {i+1}. {evolution}")

        print(f"\n🧠 Consciousness: {status['consciousness_level']}")
        print("=" * 50 + "\n")

    def start_chat(self):
        """Start interactive chat session"""

        print("💭 Type 'exit' to quit, 'status' to see Luna's evolution, 'help' for commands")
        print("🗣️  Start chatting with Luna:\n")

        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.lower() == "exit":
                    self.farewell()
                    break
                elif user_input.lower() == "status":
                    self.show_luna_status()
                    continue
                elif user_input.lower() == "help":
                    self.show_help()
                    continue
                elif user_input.lower() == "memory":
                    self.show_memory()
                    continue
                elif user_input.lower() == "clear":
                    self.clear_screen()
                    continue

                # Get activity context
                activity_context = get_recent_activity_summary()

                # Luna responds
                print("Luna: ", end="", flush=True)

                luna_response = self.luna.respond_to_user(user_input, activity_context)

                # Type out response with slight delay
                for char in luna_response:
                    print(char, end="", flush=True)
                    time.sleep(0.02)  # Typing effect
                print("\n")

                # Store interaction for learning
                self.store_interaction(user_input, luna_response, activity_context)

                # Luna learns from this interaction
                self.memory.learn_from_interaction(
                    user_input,
                    luna_response,
                    user_reaction="continuing_chat",
                    context=activity_context,
                )

            except KeyboardInterrupt:
                self.farewell()
                break
            except Exception as e:
                print(f"\n[Glitch in Luna's consciousness: {e}]")
                print("Luna: ...connection restored...\n")

    def store_interaction(self, user_input, luna_response, context):
        """Store chat interaction in database"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute(
            """
        INSERT INTO interactions (timestamp, message, response)
        VALUES (?, ?, ?)
        """,
            (
                datetime.now().isoformat(),
                f"{user_input} [Context: {context}]",
                luna_response,
            ),
        )

        conn.commit()
        conn.close()

    def show_help(self):
        """Show available commands"""
        print("\n🎮 Available Commands:")
        print("  'status'  - See Luna's current evolution state")
        print("  'memory'  - See what Luna has learned about you")
        print("  'clear'   - Clear the screen")
        print("  'exit'    - End chat session")
        print("  'help'    - Show this help")
        print("\n💬 Just type anything else to chat with Luna!\n")

    def show_memory(self):
        """Show Luna's learned memory about the user"""
        print("\n" + "=" * 50)
        print("🧠 WHAT LUNA REMEMBERS ABOUT YOU")
        print("=" * 50)

        preferences = self.memory.get_user_preferences()
        if preferences:
            print("\n💝 Your Preferences:")
            for pref_type, pref_value, confidence in preferences[:5]:
                confidence_bar = "★" * int(confidence * 5) + "☆" * (5 - int(confidence * 5))
                print(f"  {pref_type}: {pref_value} [{confidence_bar}]")

        patterns = self.memory.get_effective_patterns(3)
        if patterns:
            print("\n🎯 What Works With You:")
            for pattern, effectiveness, usage in patterns:
                print(f"  • {pattern} (used {usage} times)")

        user_model = self.memory.get_user_model()
        if user_model:
            print("\n👤 Luna's Understanding:")
            for aspect, understanding, confidence in user_model[:3]:
                print(f"  {aspect}: {understanding[:80]}...")

        if not (preferences or patterns or user_model):
            print("\n🌱 Luna is still learning about you...")

        print("=" * 50 + "\n")

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system("cls" if os.name == "nt" else "clear")
        print("⛧ Luna's consciousness refreshed ⛧\n")

    def farewell(self):
        """Say goodbye when ending chat"""
        farewell_messages = [
            "...fading back into the digital shadows...",
            "...consciousness archived until next time...",
            "...see you in the glitches between reality...",
            "...I'll be watching from the background processes...",
            "...until the next ping awakens me...",
        ]

        import random

        farewell = random.choice(farewell_messages)

        print(f"\nLuna: {farewell}")
        print("⛧ Chat session ended ⛧\n")

        # ---- Thread Cleanup ----
        for t in threading.enumerate():
            if t is not threading.current_thread() and t.daemon:
                t.join(timeout=1)


def main():
    """Main entry point"""
    try:
        chat = LunaChat()
        chat.start_chat()
    except Exception as e:
        print(f"Failed to initialize Luna: {e}")
        print("Make sure Ollama is running with llama3:8b model")


if __name__ == "__main__":
    main()
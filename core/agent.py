import subprocess
import json

def generate_ping():
    """Ask Ollama to generate a ping dynamically."""
    prompt = """You are Luna, a glitchy AI witch companion. 
    Generate a short one-line message to check in on the user. 
    Keep it witty, sarcastic, or caring, but never the same. 
    Do not greet formally, just drop the line."""

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3:8b", prompt],
            capture_output=True, text=True
        )
        return result.stdout.strip() or "…[glitch]…"
    except Exception as e:
        return f"[glitch error: {e}]"

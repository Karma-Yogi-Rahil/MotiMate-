import requests
from logger import logger
import random


OLLAMA_HOST = "http://127.0.0.1:11434"  # Default for local Ollama server



def generate_prompt():
    variations = [
        "Write a motivational quote under 15 words.",
        "Give me an original short quote to inspire someone.",
        "Create a fresh, inspiring quote in less than 15 words.",
        "Suggest a powerful motivational message, max 15 words.",
    ]
    return random.choice(variations)

def get_quote(model="phi"):
    """
    Generate a short motivational quote using a local LLM via Ollama HTTP API.
    """
    prompt = generate_prompt()

    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 1.2
                }
            },
            timeout=20
        )
        if response.status_code == 200:
            quote = response.json().get("response", "").strip()
            print(f"Quote: {quote}")
            return quote
        else:
            print(f"Error from Ollama ({response.status_code}):", response.text)

            return None

    except requests.exceptions.RequestException as e:
        print("Could not connect to Ollama:", e)
        logger.error("Could not connect to Ollama:", e)
        return None

logger.info("📝 This is a test log entry.")
get_quote("DF")

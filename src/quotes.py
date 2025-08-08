import requests
from logger import logger
import random
from dotenv import load_dotenv
import os



load_dotenv()
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi")

def generate_prompt():
    variations = [
        "Write a motivational quote under 15 words.",
        "Give me an original short quote to inspire someone.",
        "Create a fresh, inspiring quote in less than 15 words.",
        "Suggest a powerful motivational message, max 15 words.",
    ]

    prompt = random.choice(variations)
    logger.debug(f"Generated prompt -> {prompt}")
    return prompt

def get_quote(model="phi"):
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
            logger.info(f"Generated quote: {quote}")
            return quote
        else:
            logger.error(f"Error from Ollama ({response.status_code}):", response.text)
            return None

    except requests.exceptions.RequestException as e:
        logger.error("Could not connect to Ollama:", e)
        return None
    except Exception as e:
        logger.critical(f"Ollama ({response.status_code}):", e)

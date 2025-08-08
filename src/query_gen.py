import os
import requests
import random
from dotenv import load_dotenv
from logger import logger

load_dotenv()
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi")

def get_visual_query(quote):
    prompt = f"""
Suggest 5 short visual scene prompts that match this motivational quote:

"{quote}"

Return them as a comma-separated list of simple visual keywords like 'sunrise', 'mountains', 'runner', etc.
Do not include explanations — just the 5 keywords.
"""

    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt.strip(),
                "stream": False,
                "options": {
                    "temperature": 1.0
                }
            },
            timeout=20
        )

        if response.status_code == 200:
            raw_output = response.json().get("response", "").strip()
            logger.info(f"Raw visual options: {raw_output}")

            # Convert comma-separated string into list
            keywords = [word.strip().lower() for word in raw_output.split(",") if word.strip()]
            if not keywords:
                raise ValueError("No valid visual prompts found.")

            selected = random.choice(keywords)
            logger.info(f"Selected visual query: {selected}")
            return selected

        else:
            logger.error(f"LLM query generation failed: {response.status_code}")
            return "nature"

    except Exception as e:
        logger.error("Error generating visual query:", exc_info=True)
        return "nature"



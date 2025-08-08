import os
import random
import requests
from pathlib import Path
from dotenv import load_dotenv
from logger import logger

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_VIDEO_DIR = Path("assets/backgrounds")
PEXELS_VIDEO_DIR.mkdir(parents=True, exist_ok=True)


def get_background_video(query="nature", duration_limit=15):
    logger.info(f"Searching Pexels for: {query}")

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": query,
        "per_page": 10
    }

    response = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params)

    if response.status_code != 200:
        logger.error(f"Failed to fetch Pexels videos: {response.status_code}")
        raise Exception("Pexels API error")

    videos = response.json().get("videos", [])
    if not videos:
        logger.warning("No videos found for query")
        return None

    # Filter short videos
    suitable = [v for v in videos if v["duration"] <= duration_limit]
    if not suitable:
        suitable = videos

    video_url = random.choice(suitable)["video_files"][0]["link"]

    output_path = PEXELS_VIDEO_DIR / "pexels_background.mp4"
    logger.info(f"Downloading video to: {output_path}")

    with open(output_path, "wb") as f:
        f.write(requests.get(video_url).content)

    return str(output_path)
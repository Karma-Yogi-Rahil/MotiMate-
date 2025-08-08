from quotes import get_quote
from query_gen import get_visual_query
from video_fetcher import get_background_video
from logger import logger
from text_overlay import add_text_overlay
from uploader import upload_reel

import os
from dotenv import load_dotenv
load_dotenv()

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

def main():
    logger.info("Starting MotiMate automation...")

    # step 1 - generate motivational quote
    quote = get_quote()
    if not quote:
        logger.error("Quote generation failed. Exiting.")
        return

    logger.info(f"Quote: {quote}")

    # step 2 -use LLM to generate matching visual search term
    visual_query = get_visual_query(quote)
    logger.info(f"Visual search term: {visual_query}")

    # step 3 - fetch background video from Pexels
    video_path = get_background_video(visual_query)
    if not video_path:
        logger.error("Failed to fetch video. Exiting.")
        return
    logger.info(f"Video saved at: {video_path}")

    # Step 4: add quote overlay
    final_video_path = add_text_overlay(video_path, quote)
    if not final_video_path:
        logger.error("Failed to generate final video. Exiting.")
        return
    logger.info(f"Final video ready: {final_video_path}")

    # Step 5: Upload to Instagram via instagrapi
    logger.info("Uploading to Instagram...")
    caption = f"{quote.strip()}\n\n– MotiMate"
    try:
        upload_reel(USERNAME, PASSWORD, final_video_path, caption)
        logger.info("Successfully uploaded to Instagram.")
    except Exception as e:
        logger.error(f"Upload failed: {e}")

if __name__ == "__main__":
    main()
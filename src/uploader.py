# uploader.py
import os
from pathlib import Path
from instagrapi import Client

SETTINGS_PATH = Path(os.getenv("INSTA_SETTINGS_PATH", "data/insta_settings.json"))

def upload_reel(username, password, video_path, caption):
    cl = Client()

    # Reuse session if present
    if SETTINGS_PATH.exists():
        cl.load_settings(SETTINGS_PATH)
    cl.login(
        username,
        password,
        #verification_code=lambda: input("📩 Enter Instagram verification code: ")
    )
    # Save session for next runs
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    cl.dump_settings(SETTINGS_PATH)

    cl.clip_upload(Path(video_path), caption=caption)
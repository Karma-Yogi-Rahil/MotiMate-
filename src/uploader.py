
from instagrapi import Client
from pathlib import Path

def upload_reel(username, password, video_path, caption):
    cl = Client()
    if Path("insta_settings.json").exists():
        cl.load_settings("insta_settings.json")
        cl.login(username, password)
    else:
        cl.login(
            username,
            password,
            #verification_code=lambda: input("Enter Instagram verification code: ")
        )
        cl.dump_settings("insta_settings.json")

    # Upload the reel
    video_path = Path(video_path)
    cl.clip_upload(
        video_path,
        caption=caption,
    )
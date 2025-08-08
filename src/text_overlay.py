from moviepy import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.Crop import Crop
import  random
import numpy as np
import logger as logger
FONTS = [
    "Arial", "Helvetica", "Courier", "Georgia", "Times", "Verdana",
    "Palatino", "Trebuchet MS",
]

def split_quote_author(full_quote):
    if " - " in full_quote:
        parts = full_quote.split(" - ", 1)
        quote = parts[0].strip()
        author = f"- {parts[1].strip()}"
    else:
        quote = full_quote.strip()
        author = ""
    return quote, author

def get_random_font():
    return random.choice(FONTS)

def get_contrasting_color(clip, y_start_ratio=0.3, y_end_ratio=0.8):
    frame = clip.get_frame(1.0)
    h, w, _ = frame.shape

    y1 = int(h * y_start_ratio)
    y2 = int(h * y_end_ratio)
    cropped_area = frame[y1:y2, :, :3]

    avg_brightness = np.mean(cropped_area)
    return "white" if avg_brightness < 128 else "black"

def add_text_overlay(video_path, quote, output_path="output/with_text.mp4"):
    clip = VideoFileClip(video_path)

    # Resize and crop to vertical 608x1080
    resized = clip.resized(height=1080)
    cropped = resized.with_effects([Crop(x_center=resized.w// 2,width=608, height=1080)])

    color = get_contrasting_color(cropped)
    font = get_random_font()
    logger.info(f"Font: {font} | Color: {color}")


    font_size_main = int(cropped.w * 0.06)  # Main quote
    font_size_author = int(cropped.w * 0.05)  # Smaller signature

    quote_line,author_line =split_quote_author(quote)
    logger.info(f"Quote: {quote_line} ")
    logger.info(f"Author: {author_line}")

    # Main quote (center)
    quote_clip = TextClip(
        text=quote_line,
        font=font,
        font_size=font_size_main,
        color=color,
        method="caption",
        size=(cropped.w-30, cropped.h),
    ).with_duration(cropped.duration).with_position("center")

    # Author or name (bottom)
    author_clip = TextClip(
        text=author_line,
        font=font,
        font_size=font_size_author,
        color=color,
        method="caption",
    size = (cropped.w - 30, font_size_author * 2),
    ).with_duration(cropped.duration).with_position(("center", cropped.h - font_size_author - 300))

    # Combine
    final = CompositeVideoClip([cropped, quote_clip, author_clip])
    final.write_videofile(output_path, fps=24)
    logger.info(f"Text overlay written to {output_path}")
    return output_path


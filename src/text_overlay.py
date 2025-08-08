from moviepy import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.Crop import Crop
import  random
import numpy as np
from logger import logger
import subprocess
import shlex
import os
# Requested font names
FONTS = [
    "Arial", "Helvetica", "Courier", "Georgia", "Times", "Verdana",
    "Palatino", "Trebuchet MS",
]

# Map requested names to real family names in Debian
NAME_MAP = {
    "Arial": "Arial",
    "Helvetica": "TeX Gyre Heros",       # Helvetica-like
    "Courier": "Courier New",            # Monospace
    "Georgia": "Georgia",
    "Times": "Times New Roman",          # Times-like
    "Verdana": "Verdana",
    "Palatino": "TeX Gyre Pagella",      # Palatino-like
    "Trebuchet MS": "Trebuchet MS",
}

def split_quote_author(full_quote):
    if " - " in full_quote:
        parts = full_quote.split(" - ", 1)
        quote = parts[0].strip()
        author = f"- {parts[1].strip()}"
    else:
        quote = full_quote.strip()
        author = ""
    return quote, author

def get_font_path(family):
    """Return the actual font file path for a given family, or None if not found."""
    try:
        fam = NAME_MAP.get(family, family)
        cmd = f'fc-match -f "%{{file}}\\n" {shlex.quote(fam)}'
        path = subprocess.check_output(cmd, shell=True, text=True).strip()
        return path if os.path.isfile(path) else None
    except Exception:
        return None

def get_random_font():
    """Pick a random font from FONTS and return its file path or a fallback."""
    random.shuffle(FONTS)  # randomize order
    for fam in FONTS:
        path = get_font_path(fam)
        if path:
            return path
    # Fallback if none found
    return "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

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
    logger.info(f"Font size quote: {font_size_main}")
    font_size_author = max(1, int(cropped.w * 0.05)) # Smaller signature
    logger.info(f"Font size author: {font_size_main}")

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


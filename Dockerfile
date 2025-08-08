# syntax=docker/dockerfile:1
FROM python:3.11-slim

# OS deps: ffmpeg for video, fonts for text rendering
ENV DEBIAN_FRONTEND=noninteractive



# Enable contrib + non-free to get mscorefonts
RUN printf "deb http://deb.debian.org/debian bookworm main contrib non-free non-free-firmware\n\
deb http://deb.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware\n\
deb http://deb.debian.org/debian bookworm-updates main contrib non-free non-free-firmware\n" > /etc/apt/sources.list && \
    apt-get update && \
    echo 'ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true' | debconf-set-selections && \
    apt-get install -y --no-install-recommends \
      fontconfig fontconfig-config debconf-utils ca-certificates wget cabextract \
      ttf-mscorefonts-installer \
      fonts-dejavu fonts-liberation fonts-texgyre && \
    fc-cache -f -v && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app


# Install Python deps first (cache friendly)
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade moviepy --no-deps


# Copy project
COPY src/ ./src


# Persist session (instagrapi) + outputs
VOLUME ["/app/data", "/app/output"]

# Let code know where to cache login/session
ENV INSTA_SETTINGS_PATH=/app/data/insta_settings.json
ENV PYTHONUNBUFFERED=1

ENV TZ=Asia/Kolkata PYTHONUNBUFFERED=1

# at the end:
CMD ["python", "src/run_scheduler.py"]

# syntax=docker/dockerfile:1
FROM python:3.11-slim

# OS deps: ffmpeg for video, fonts for text rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg fonts-dejavu fonts-liberation ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (cache friendly)
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir instagrapi==2.2.1 --no-deps

# Copy project
COPY src/ ./src


# Persist session (instagrapi) + outputs
VOLUME ["/app/data", "/app/output"]

# Let code know where to cache login/session
ENV INSTA_SETTINGS_PATH=/app/data/insta_settings.json
ENV PYTHONUNBUFFERED=1

# Default command runs the pipeline once
CMD ["python", "src/main.py"]
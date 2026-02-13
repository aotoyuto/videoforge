FROM python:3.12-slim

# Install FFmpeg and Japanese fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    fonts-noto-cjk \
    fonts-noto-cjk-extra \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY src/ src/
COPY examples/ examples/

# Install the package
RUN pip install --no-cache-dir -e .

# Create output directory
RUN mkdir -p /app/output

# Set default font for Docker (Noto Sans CJK)
ENV DEFAULT_FONT="Noto Sans CJK JP"
ENV OUTPUT_DIR=/app/output

ENTRYPOINT ["videoforge"]
CMD ["--help"]

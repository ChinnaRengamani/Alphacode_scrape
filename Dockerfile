# Use Python slim-buster as the base image
FROM python:3.9-slim-buster

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    firefox-esr

# Set up GeckoDriver for Firefox
RUN GECKO_DRIVER_VERSION=$(curl -sL "https://api.github.com/repos/mozilla/geckodriver/releases/latest" | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/') && \
    wget -q --continue -P /geckodriver "https://github.com/mozilla/geckodriver/releases/download/v$GECKO_DRIVER_VERSION/geckodriver-v$GECKO_DRIVER_VERSION-linux64.tar.gz" && \
    tar -xzf /geckodriver/geckodriver-v$GECKO_DRIVER_VERSION-linux64.tar.gz -C /usr/bin/ && \
    chmod +x /usr/bin/geckodriver && \
    rm -rf /var/lib/apt/lists/*

# Set up a working directory
WORKDIR /app

# Copy Python requirements and install them
COPY app /app
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point to run the Python script
CMD ["python", "scrape.py"]

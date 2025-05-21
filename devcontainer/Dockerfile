FROM python:3.9

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    chromium-driver \
    libnotify-bin \
    python3-dbus \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

RUN CHROME_VERSION=$(chromium --version | grep -oP 'Chromium \K\d+') \
    && wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION -O chromedriver-version.txt \
    && wget https://chromedriver.storage.googleapis.com/$(cat chromedriver-version.txt)/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip

WORKDIR /workspace
COPY . .
RUN pip install -r requirements.txt

ENV DISPLAY=:99
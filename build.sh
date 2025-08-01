#!/bin/bash

# Install Chrome without sudo
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -x google-chrome-stable_current_amd64.deb /tmp/chrome
export PATH="/tmp/chrome/opt/google/chrome:$PATH"

# Get Chrome version
CHROME_VERSION=$(/tmp/chrome/opt/google/chrome/google-chrome --version | awk '{print $3}')
CHROME_MAJOR=${CHROME_VERSION%%.*}

# Download matching ChromeDriver
CHROMEDRIVER_URL="https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR"
CHROMEDRIVER_VERSION=$(wget -qO- $CHROMEDRIVER_URL)
wget "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
chmod +x chromedriver

# Install Python dependencies
pip install -r requirements.txt

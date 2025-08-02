#!/bin/bash
set -e  # Exit immediately if any command fails

echo "=== Creating Render-Specific Directories ==="
mkdir -p /opt/render/project/.render/chrome
mkdir -p /opt/render/project/.render/drivers

echo "=== Installing Chrome ==="
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg-deb -x google-chrome-stable_current_amd64.deb /opt/render/project/.render/chrome
rm google-chrome-stable_current_amd64.deb

echo "=== Installing ChromeDriver ==="
CHROME_VERSION=$(/opt/render/project/.render/chrome/opt/google/chrome/chrome --version | awk '{print $3}')
CHROME_MAJOR=${CHROME_VERSION%%.*}
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR")
wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip -d /opt/render/project/.render/drivers
rm chromedriver_linux64.zip
chmod +x /opt/render/project/.render/drivers/chromedriver

echo "=== Setting Up Python Environment ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Verification ==="
/opt/render/project/.render/chrome/opt/google/chrome/chrome --version
/opt/render/project/.render/drivers/chromedriver --version
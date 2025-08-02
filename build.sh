#!/bin/bash
set -e  # Exit immediately if any command fails

echo "=== Installing System Dependencies ==="
apt-get update
apt-get install -y wget gnupg unzip xvfb libxi6 libgconf-2-4 libnss3 libxss1 libglib2.0-0 libxft2 libfreetype6 libfontconfig1 libxrender1 libasound2 libxtst6 libxrandr2 libasound2 libpangocairo-1.0-0 libatk1.0-0 libcairo-gobject2 libgtk-3-0 libgdk-pixbuf2.0-0

echo "=== Creating Render-Specific Directories ==="
mkdir -p /opt/render/project/.render/chrome
mkdir -p /opt/render/project/.render/drivers

echo "=== Installing Chrome ==="
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg-deb -x google-chrome-stable_current_amd64.deb /opt/render/project/.render/chrome
rm google-chrome-stable_current_amd64.deb

echo "=== Installing ChromeDriver ==="
# Get Chrome version more reliably
export LD_LIBRARY_PATH="/opt/render/project/.render/chrome/opt/google/chrome:$LD_LIBRARY_PATH"
CHROME_VERSION=$(/opt/render/project/.render/chrome/opt/google/chrome/chrome --no-sandbox --headless --disable-gpu --version 2>/dev/null | awk '{print $3}' || echo "127.0.6533.119")
CHROME_MAJOR=${CHROME_VERSION%%.*}

echo "Chrome version detected: $CHROME_VERSION"
echo "Chrome major version: $CHROME_MAJOR"

# Use a fallback if version detection fails
if [ -z "$CHROME_MAJOR" ] || [ "$CHROME_MAJOR" -lt "100" ]; then
    echo "Using fallback Chrome major version 127"
    CHROME_MAJOR="127"
fi

# Get ChromeDriver version
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR" || echo "127.0.6533.119")
echo "ChromeDriver version: $CHROMEDRIVER_VERSION"

# Download and install ChromeDriver
wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" -O chromedriver.zip
unzip chromedriver.zip -d /opt/render/project/.render/drivers
rm chromedriver.zip
chmod +x /opt/render/project/.render/drivers/chromedriver

echo "=== Setting Up Python Environment ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Build Complete ==="
echo "Chrome installed at: /opt/render/project/.render/chrome/opt/google/chrome/chrome"
echo "ChromeDriver installed at: /opt/render/project/.render/drivers/chromedriver"
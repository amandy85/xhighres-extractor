#!/bin/bash
set -o errexit

# Install Chrome
mkdir -p /opt/render/project/src/.render/chrome
cd /opt/render/project/src/.render/chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
ar x google-chrome-stable_current_amd64.deb data.tar.xz
tar -xf data.tar.xz
rm google-chrome-stable_current_amd64.deb data.tar.xz
chmod +x /opt/render/project/src/.render/chrome/opt/google/chrome/google-chrome

# Install specific ChromeDriver version (compatible with Chrome 138)
CHROMEDRIVER_VERSION="138.0.0"
wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
mv chromedriver /usr/local/bin/

# Install Python dependencies
cd /opt/render/project/src
pip install -r requirements.txt
#!/bin/bash
set -o errexit

# Create directory for Chrome
mkdir -p /opt/render/project/src/.render/chrome
cd /opt/render/project/src/.render/chrome

# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
ar x google-chrome-stable_current_amd64.deb data.tar.xz
tar -xf data.tar.xz
rm google-chrome-stable_current_amd64.deb data.tar.xz
chmod +x /opt/render/project/src/.render/chrome/opt/google/chrome/google-chrome

# Navigate back to project root and install Python dependencies
cd /opt/render/project/src
pip install -r requirements.txt
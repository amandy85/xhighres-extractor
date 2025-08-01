#!/bin/bash
set -o errexit

# Create directory for Chrome
mkdir -p /opt/render/project/src/.render/chrome

# Download and install Chrome
cd /opt/render/project/src/.render/chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
ar x google-chrome-stable_current_amd64.deb data.tar.xz
tar -xf data.tar.xz
rm google-chrome-stable_current_amd64.deb data.tar.xz

# Set correct permissions
chmod +x /opt/render/project/src/.render/chrome/opt/google/chrome/google-chrome

# Install Python dependencies
pip install -r requirements.txt
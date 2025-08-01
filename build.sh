#!/bin/bash
set -o errexit

# Install system dependencies
apt-get update
apt-get install -y python3 python3-pip python3-dev
apt-get install -y wget gnupg

# Install Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

# Install Python packages
pip install -r requirements.txt
#!/bin/bash
set -e  # Exit immediately if any command fails

echo "=== Installing System Dependencies ==="

# Install Chrome without apt (Render-compatible)
echo "Downloading Chrome..."
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
mkdir -p chrome
dpkg -x google-chrome-stable_current_amd64.deb chrome
rm google-chrome-stable_current_amd64.deb

echo "=== Setting Up Python Environment ==="
pip install --upgrade pip
pip install -r requirements.txt  # Install all dependencies from requirements

echo "=== Verifying Installations ==="
python -c "from selenium import webdriver; from webdriver_manager.chrome import ChromeDriverManager; from bs4 import BeautifulSoup; print('All dependencies verified')"
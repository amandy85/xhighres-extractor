#!/bin/bash
set -e  # Exit on error

echo "=== Installing System Dependencies ==="
apt-get update
apt-get install -y wget unzip gnupg

echo "=== Installing Chrome ==="
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

echo "=== Installing Python Dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Verifying Installations ==="
google-chrome --version
python -c "from webdriver_manager.chrome import ChromeDriverManager; print('webdriver-manager available')"
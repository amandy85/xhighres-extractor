#!/bin/bash
set -e  # Exit on error

echo "=== Installing Python Dependencies ==="
pip install --upgrade pip
pip install webdriver-manager selenium  # Add other dependencies as needed

echo "=== Verifying Installations ==="
python -c "from webdriver_manager.chrome import ChromeDriverManager; print('webdriver-manager available')"
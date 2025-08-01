#!/bin/bash
set -e  # Exit on error

# Set Chrome path
export PATH="$PWD/chrome/opt/google/chrome:$PATH"

# Initialize WebDriver (warm-up)
python -c "
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')
webdriver.Chrome(service=service, options=options).quit()
"

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120 app:app
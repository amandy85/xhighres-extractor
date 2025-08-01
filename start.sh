#!/bin/bash
set -e  # Exit on error

# Set Chrome path
export PATH="$PWD/chrome/opt/google/chrome:$PATH"

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120 app:app
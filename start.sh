#!/bin/bash
set -e  # Exit on error

# Add Chrome to PATH
export PATH="/usr/bin/google-chrome-stable:$PATH"

# Activate virtual environment if exists
if [ -d "venv" ]; then
  source venv/bin/activate
fi

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT app:app
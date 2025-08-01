#!/bin/bash
set -o errexit

# Add Chrome to PATH
export PATH="/opt/render/project/src/.render/chrome/opt/google/chrome:$PATH"

# Start the app
gunicorn app:app --workers 1 --bind 0.0.0.0:$PORT --timeout 300
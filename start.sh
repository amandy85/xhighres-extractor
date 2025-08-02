#!/bin/bash
set -e  # Exit on error

# Set Render-specific paths
export PATH="/opt/render/project/.render/chrome/opt/google/chrome:$PATH"
export PATH="/opt/render/project/.render/drivers:$PATH"

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120 app:app
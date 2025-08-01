#!/bin/bash
set -o errexit

export PATH="/opt/render/project/src/.render/chrome/opt/google/chrome:$PATH"
gunicorn app:app --workers 1 --bind 0.0.0.0:$PORT --timeout 300
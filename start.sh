#!/bin/bash
set -o errexit

gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT --timeout 180
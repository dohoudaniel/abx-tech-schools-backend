#!/usr/bin/env bash
# Exit on error
set -o errexit

echo ">>> Starting Gunicorn..."
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT

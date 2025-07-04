#!/bin/bash

# Production start script for Render
echo "Starting Global Rabbit Population Dashboard..."

# Set production environment
export ENVIRONMENT=production

# Start with Gunicorn for production
# Use the exposed Flask server instance (named 'server')
exec gunicorn app:server \
    --bind 0.0.0.0:${PORT:-8050} \
    --workers 4 \
    --log-level info

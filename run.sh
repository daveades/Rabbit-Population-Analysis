#!/bin/bash

# Production start script for Render
echo "Starting Global Rabbit Population Dashboard..."

# Set production environment
export ENVIRONMENT=production

# Run the application
python app.py

#!/bin/bash

# Build script for Render deployment
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setting up data directories..."
mkdir -p data/raw data/processed

echo "Build completed successfully!"

#!/bin/bash

# Simple build script for deployment
echo "Starting build process..."

# Upgrade pip and setuptools
python -m pip install --upgrade pip setuptools wheel

echo "Installing Python dependencies..."
pip install --no-cache-dir --timeout 300 -r requirements.txt

echo "Setting up data directories..."
mkdir -p data/raw data/processed

echo "Verifying critical packages..."
python -c "import dash, pandas, plotly; print('Core packages installed successfully')"

echo "Build completed successfully!"

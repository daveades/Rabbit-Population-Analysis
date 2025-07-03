#!/bin/bash

# Build script for Render deployment
echo "Starting build process..."

# Upgrade pip and setuptools first
python -m pip install --upgrade pip setuptools wheel

echo "Installing core Python dependencies..."
# Use simplified requirements for Render
if [ -f "requirements-render.txt" ]; then
    echo "Using Render-specific requirements..."
    pip install --no-cache-dir --timeout 300 -r requirements-render.txt
else
    echo "Using standard requirements..."
    pip install --no-cache-dir --timeout 300 -r requirements.txt
fi

echo "Setting up data directories..."
mkdir -p data/raw data/processed

echo "Verifying critical packages..."
python -c "import dash; print('Dash installed successfully')"
python -c "import pandas; print('Pandas installed successfully')"
python -c "import plotly; print('Plotly installed successfully')"

echo "Build completed successfully!"

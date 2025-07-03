#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Run the application
python app.py

# Deactivate virtual environment when the app is stopped
deactivate

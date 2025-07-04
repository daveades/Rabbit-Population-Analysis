# 🐰 Global Rabbit Population Dashboard

This is a simple dashboard for exploring global rabbit population data. It uses Dash and Plotly to track trends, compare species, and show habitat impacts in real time.

## Features

- Track rabbit population trends over time
- Compare species distribution by region
- View how different habitats affect populations
- Check conservation status at a glance

Filters update instantly as you make selections.

## Getting Started

### Local Setup

1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the dashboard:
   ```bash
   python app.py
   ```
4. Open your browser at `http://127.0.0.1:8050/`.

### Production Deployment

On hosting platforms like Render, the app auto-switches to production mode. Just:

1. Make sure `gunicorn` is listed in `requirements.txt`.
2. Set the start command to `./run.sh` (already executable).
3. Point your service URL to the live dashboard.

## How It Works

- **Data Generation**: Sample data is created by `src/analysis/data_processor.py`.
- **Visuals Engine**: Charts and maps live in `src/visualization/charts.py`.
- **Web App**: `app.py` ties everything together with Dash and Flask.
- **API (Optional)**: `src/api/routes.py` provides JSON endpoints if you need raw data.

Enjoy exploring rabbit populations—no scientific background required!

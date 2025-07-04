# 🐰 Global Rabbit Population Dashboard

Welcome to the Global Rabbit Population Dashboard! This tool helps you explore rabbit population data from around the world. With clear visuals and useful insights, it shows how rabbit populations are distributed, their habitats, and the challenges they face.

## What Is This Dashboard About?

This project is designed to make rabbit population data accessible and engaging. Through an intuitive web interface, you can:

- View population trends over time
- Explore species distribution across regions
- Understand conservation challenges
- Analyze how habitats affect populations

The dashboard updates in real-time, responding instantly to your inputs.

## How It Works

The dashboard combines data processing, visualization, and web technologies. Here’s a breakdown of its main components:

### Core Components

1. **Data Processing Pipeline** (`src/analysis/data_processor.py`)
   - Prepares raw data for visualization
   - Handles CSV data or generates sample data for testing

2. **Visualization Engine** (`src/visualization/charts.py`)
   - Creates interactive charts with Plotly
   - Visualizes species distribution, habitat impacts, and conservation statuses

3. **Web Application** (`app.py`)
   - Provides a responsive interface using Dash and Flask
   - Connects data, visualizations, and user interactions

4. **API Layer** (`src/api/routes.py`)
   - Offers endpoints for accessing rabbit population data

### User Experience

The dashboard is user-friendly and interactive. You can:

- Track population changes with dynamic charts
- Explore species distribution across regions
- Monitor endangered populations
- Analyze habitat influences on populations

Charts update instantly as you adjust filters for time, region, species, or conservation status.

### Data Flow

1. Raw data is processed through the pipeline.
2. The visualization engine creates charts.
3. The web app displays these charts with interactive controls.
4. Your inputs reshape the data views in real-time.

## Getting Started

### Local Development

To run the dashboard locally, use:
```bash
python app.py
```
Or run the included script:
```bash
chmod +x run.sh
./run.sh
```

Open your browser at `http://127.0.0.1:8050/` to access the dashboard.

### Production Deployment
In production environments like Render, the app automatically switches to production mode. It detects environment variables to configure itself and suppresses development warnings for a smoother experience.

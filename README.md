# 🐰 Global Rabbit Population Dashboard

An interactive web dashboard for visualizing and analyzing worldwide rabbit population trends, powered by Python data analysis and interactive Plotly visualizations.

## Project Overview

This project is a data visualization dashboard that explores global rabbit population dynamics. It provides interactive insights into population trends, species distribution, conservation status, and habitat analysis through an intuitive web interface.

## How It Works

The dashboard combines several key components that work together to provide data-driven insights:

### Core Components

1. **Data Processing Pipeline** (`src/analysis/data_processor.py`)
   - Handles loading and preprocessing of rabbit population data
   - Performs data transformations for visualization readiness
   - Supports both CSV data files and sample data generation

2. **Visualization Engine** (`src/visualization/charts.py`)
   - Creates interactive Plotly charts for population trends
   - Generates species distribution visualizations
   - Provides habitat analysis and conservation status charts

3. **Web Application** (`app.py`)
   - Builds the interactive Dash/Flask web interface
   - Manages user interactions and filter selections
   - Coordinates data flow between processing and visualization components

4. **API Layer** (`src/api/routes.py`)
   - Provides REST endpoints for accessing rabbit population data
   - Enables external applications to consume dashboard data

### User Experience

The dashboard offers an intuitive interface with multiple interactive visualizations:

- **Population Trends**: Track how rabbit populations change over time
- **Species Distribution**: Explore geographic spread of different rabbit species
- **Conservation Status**: Monitor endangered and vulnerable populations
- **Habitat Analysis**: Understand environmental impact on populations

All visualizations update dynamically as users interact with filters for time periods, regions, species, and conservation status.

### Data Flow

1. Raw rabbit population data is processed through the data pipeline
2. The visualization engine transforms this data into interactive charts
3. The web application presents these visualizations with user controls
4. User interactions trigger real-time updates to all visualizations

## Running the Project

Simply execute `python app.py` or use the provided `run.sh` script to launch the dashboard. The application will be available at `http://127.0.0.1:8050/` in your web browser.

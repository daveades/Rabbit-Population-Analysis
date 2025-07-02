"""
API endpoints for the rabbit population dashboard
"""

from flask import Blueprint, jsonify, request
import pandas as pd
import os

# Import local modules
from src.analysis.data_processor import load_data, preprocess_data

# Create a Blueprint for the API routes
api_bp = Blueprint('api', __name__)


@api_bp.route('/data', methods=['GET'])
def get_data():
    """
    API endpoint to get rabbit population data with optional filtering.
    
    Query parameters:
    - region: Filter by region
    - species: Filter by species
    - year_min: Minimum year to include
    - year_max: Maximum year to include
    - conservation_status: Filter by conservation status
    
    Returns:
        JSON: Filtered data in JSON format
    """
    try:
        # Load data
        df = load_data()
        
        # Apply filters from query parameters
        region = request.args.get('region')
        species = request.args.get('species')
        year_min = request.args.get('year_min')
        year_max = request.args.get('year_max')
        conservation_status = request.args.get('conservation_status')
        
        # Filter by region
        if region:
            df = df[df['Region'] == region]
        
        # Filter by species
        if species:
            df = df[df['Species'] == species]
        
        # Filter by year range
        if year_min:
            df = df[df['Year'] >= int(year_min)]
        if year_max:
            df = df[df['Year'] <= int(year_max)]
        
        # Filter by conservation status
        if conservation_status:
            df = df[df['Conservation_Status'] == conservation_status]
        
        # Convert to dictionary for JSON response
        data = df.to_dict(orient='records')
        
        return jsonify({
            'status': 'success',
            'data': data,
            'count': len(data)
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@api_bp.route('/summary', methods=['GET'])
def get_summary():
    """
    API endpoint to get summary statistics of rabbit population data.
    
    Returns:
        JSON: Summary statistics in JSON format
    """
    try:
        # Load data
        df = load_data()
        
        # Get the most recent year
        max_year = df['Year'].max()
        recent_data = df[df['Year'] == max_year]
        
        # Calculate summary statistics
        total_population = recent_data['Population'].sum()
        species_count = df['Species'].nunique()
        regions_count = df['Region'].nunique()
        endangered_count = recent_data[recent_data['Conservation_Status'] == 'Endangered']['Population'].sum()
        endangered_percent = (endangered_count / total_population * 100) if total_population > 0 else 0
        
        # Species distribution
        species_distribution = recent_data.groupby('Species')['Population'].sum().to_dict()
        
        # Region distribution
        region_distribution = recent_data.groupby('Region')['Population'].sum().to_dict()
        
        # Habitat distribution
        habitat_distribution = recent_data.groupby('Habitat')['Population'].sum().to_dict()
        
        # Conservation status distribution
        conservation_distribution = recent_data.groupby('Conservation_Status')['Population'].sum().to_dict()
        
        return jsonify({
            'status': 'success',
            'summary': {
                'year': max_year,
                'total_population': total_population,
                'species_count': species_count,
                'regions_count': regions_count,
                'endangered_percent': endangered_percent,
                'species_distribution': species_distribution,
                'region_distribution': region_distribution,
                'habitat_distribution': habitat_distribution,
                'conservation_distribution': conservation_distribution
            }
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@api_bp.route('/trends', methods=['GET'])
def get_trends():
    """
    API endpoint to get population trends over time.
    
    Returns:
        JSON: Trend data in JSON format
    """
    try:
        # Load data
        df = load_data()
        
        # Apply filters from query parameters
        region = request.args.get('region')
        species = request.args.get('species')
        
        # Filter by region
        if region:
            df = df[df['Region'] == region]
        
        # Filter by species
        if species:
            df = df[df['Species'] == species]
        
        # Aggregate by year
        yearly_data = df.groupby('Year')['Population'].sum().reset_index()
        
        # Calculate year-over-year growth rates
        yearly_data['Growth_Rate'] = yearly_data['Population'].pct_change() * 100
        
        # Convert to dictionary for JSON response
        data = yearly_data.to_dict(orient='records')
        
        return jsonify({
            'status': 'success',
            'data': data
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


def register_api_routes(app):
    """
    Register the API Blueprint with the Flask app.
    
    Args:
        app: Flask application instance
    """
    app.register_blueprint(api_bp, url_prefix='/api')

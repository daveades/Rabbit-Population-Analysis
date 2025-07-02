"""
Data processor module to load and preprocess rabbit population data
"""

import os
import pandas as pd
import numpy as np


def load_data(data_path=None):
    """
    Load data from CSV files in the data directory.
    
    Args:
        data_path (str, optional): Path to the data directory.
            Defaults to 'data/processed/rabbit_population.csv'.
    
    Returns:
        pd.DataFrame: Processed dataframe with rabbit population data
    
    Raises:
        FileNotFoundError: If the data file doesn't exist
    """
    if data_path is None:
        data_path = os.path.join('data', 'processed', 'rabbit_population.csv')
    
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    else:
        # If we're in development and don't have real data yet, 
        # we'll raise this error and let app.py create sample data
        raise FileNotFoundError(f"Data file not found at {data_path}")


def preprocess_data(df):
    """
    Preprocess the rabbit population data.
    
    Args:
        df (pd.DataFrame): Raw dataframe with rabbit population data
    
    Returns:
        pd.DataFrame: Processed dataframe ready for visualization
    """
    # Create a copy to avoid modifying the original dataframe
    processed_df = df.copy()
    
    # Convert Year to integer if it's not already
    processed_df['Year'] = processed_df['Year'].astype(int)
    
    # Ensure Population is numeric
    processed_df['Population'] = pd.to_numeric(processed_df['Population'], errors='coerce')
    
    # Drop rows with missing population values
    processed_df = processed_df.dropna(subset=['Population'])
    
    # Add some derived features that might be useful for analysis
    
    # Calculate year-over-year growth rate
    processed_df = calculate_growth_rates(processed_df)
    
    # Calculate population density (if area data is available)
    # This is just a placeholder for now
    
    return processed_df


def calculate_growth_rates(df):
    """
    Calculate year-over-year growth rates for each region and species.
    
    Args:
        df (pd.DataFrame): Dataframe with rabbit population data
    
    Returns:
        pd.DataFrame: Dataframe with additional growth rate columns
    """
    # Create a copy to avoid modifying the original dataframe
    result_df = df.copy()
    
    # Sort by Region, Species, and Year
    result_df = result_df.sort_values(['Region', 'Species', 'Year'])
    
    # Calculate year-over-year growth rate for each region and species
    result_df['Growth_Rate'] = result_df.groupby(['Region', 'Species'])['Population'].pct_change() * 100
    
    return result_df


def generate_sample_data(output_path='data/processed/rabbit_population.csv'):
    """
    Generate sample rabbit population data for development.
    
    Args:
        output_path (str): Path to save the generated data
    
    Returns:
        pd.DataFrame: The generated sample data
    """
    # Create sample data parameters
    years = list(range(2000, 2026))
    regions = ['North America', 'Europe', 'Asia', 'Africa', 'Australia', 'South America']
    species = ['European Rabbit', 'Cottontail', 'Hare', 'Jackrabbit', 'Pygmy Rabbit']
    
    # Generate sample population data
    data = []
    for year in years:
        for region in regions:
            for specie in species:
                # Create some variation in the data with upward trend and seasonal pattern
                base_population = np.random.randint(10000, 50000)
                trend = (year - 2000) * 500  # Increasing trend over time
                seasonal = np.sin(year) * 2000  # Some seasonal variation
                random_factor = np.random.normal(0, 5000)  # Random noise
                
                population = max(100, base_population + trend + seasonal + random_factor)
                
                data.append({
                    'Year': year,
                    'Region': region,
                    'Species': specie,
                    'Population': int(population),
                    'Habitat': np.random.choice(['Forest', 'Grassland', 'Desert', 'Urban']),
                    'Conservation_Status': np.random.choice(['Least Concern', 'Near Threatened', 'Vulnerable', 'Endangered'], p=[0.6, 0.2, 0.15, 0.05])
                })
    
    df = pd.DataFrame(data)
    
    # Make sure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    return df


if __name__ == "__main__":
    # Generate sample data when run directly
    sample_data = generate_sample_data()
    print(f"Generated sample data with {len(sample_data)} records")

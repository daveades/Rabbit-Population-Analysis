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
    
    # Handle outliers in population data using IQR method
    for region in processed_df['Region'].unique():
        for species in processed_df['Species'].unique():
            mask = (processed_df['Region'] == region) & (processed_df['Species'] == species)
            if mask.sum() > 10:  # Only apply if we have enough data points
                q1 = processed_df.loc[mask, 'Population'].quantile(0.25)
                q3 = processed_df.loc[mask, 'Population'].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                # Cap outliers instead of removing them
                processed_df.loc[mask & (processed_df['Population'] < lower_bound), 'Population'] = lower_bound
                processed_df.loc[mask & (processed_df['Population'] > upper_bound), 'Population'] = upper_bound
    
    # Add derived features for analysis
    
    # Calculate year-over-year growth rate
    processed_df = calculate_growth_rates(processed_df)
    
    # Add normalized population (relative to the max for that species)
    processed_df['Normalized_Population'] = processed_df.groupby(['Species'])['Population'].transform(
        lambda x: (x - x.min()) / (x.max() - x.min()) if (x.max() - x.min()) > 0 else 0
    )
    
    # Add binary feature for endangered/non-endangered
    processed_df['Is_Endangered'] = processed_df['Conservation_Status'].apply(
        lambda x: 1 if x == 'Endangered' else 0
    )
    
    # Add species dominance (% of total population in a region)
    processed_df['Species_Dominance'] = processed_df.apply(
        lambda row: row['Population'] / processed_df[(processed_df['Year'] == row['Year']) & 
                                                   (processed_df['Region'] == row['Region'])]['Population'].sum(),
        axis=1
    )
    
    # Add seasonal flag (assuming breeding seasons)
    processed_df['Season'] = processed_df['Year'].apply(
        lambda x: 'Spring' if x % 1 == 0.25 else 
                  'Summer' if x % 1 == 0.5 else
                  'Fall' if x % 1 == 0.75 else 'Winter'
    )
    
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
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # ensure output directory exists
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    return df


def identify_population_trends(df):
    """
    Identify long-term population trends for each species and region.
    
    Args:
        df (pd.DataFrame): Dataframe with rabbit population data
    
    Returns:
        pd.DataFrame: Dataframe with trend information
    """
    # Group by region and species to get the time series for each
    trend_data = []
    
    for region in df['Region'].unique():
        for species in df['Species'].unique():
            subset = df[(df['Region'] == region) & (df['Species'] == species)].sort_values('Year')
            
            if len(subset) < 5:  # Need enough data points for a trend
                continue
                
            # Calculate trend using linear regression
            years = subset['Year'].values.reshape(-1, 1)
            populations = subset['Population'].values
            
            if len(years) > 1:  # Check if we have at least 2 data points
                from sklearn.linear_model import LinearRegression
                model = LinearRegression()
                model.fit(years, populations)
                
                # Get the slope coefficient
                slope = model.coef_[0]
                
                # Calculate average annual growth rate
                start_pop = subset.iloc[0]['Population']
                end_pop = subset.iloc[-1]['Population']
                years_diff = subset.iloc[-1]['Year'] - subset.iloc[0]['Year']
                
                if years_diff > 0 and start_pop > 0:
                    avg_annual_growth = ((end_pop / start_pop) ** (1 / years_diff) - 1) * 100
                else:
                    avg_annual_growth = 0
                
                # Determine trend direction
                if slope > 100:
                    trend = 'Increasing'
                elif slope < -100:
                    trend = 'Decreasing'
                else:
                    trend = 'Stable'
                
                trend_data.append({
                    'Region': region,
                    'Species': species,
                    'Slope': slope,
                    'Avg_Annual_Growth': avg_annual_growth,
                    'Trend': trend,
                    'Start_Year': subset.iloc[0]['Year'],
                    'End_Year': subset.iloc[-1]['Year'],
                    'Start_Population': start_pop,
                    'End_Population': end_pop
                })
    
    return pd.DataFrame(trend_data)


if __name__ == "__main__":
    # Generate sample data when run directly
    sample_data = generate_sample_data()
    print(f"Generated sample data with {len(sample_data)} records")

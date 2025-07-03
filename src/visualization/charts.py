"""
Charts module for creating visualizations for the rabbit population dashboard
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_population_chart(df, regions=None, species=None, year_range=None):
    """
    Create a line chart showing population trends over time.
    
    Args:
        df (pd.DataFrame): DataFrame with rabbit population data
        regions (list, optional): List of regions to include. Defaults to all.
        species (list, optional): List of species to include. Defaults to all.
        year_range (list, optional): [min_year, max_year] range. Defaults to all.
        
    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    # Filter data based on parameters
    filtered_df = filter_dataframe(df, regions, species, year_range)
    
    # Aggregate by year
    yearly_data = filtered_df.groupby('Year')['Population'].sum().reset_index()
    
    fig = px.line(
        yearly_data,
        x='Year',
        y='Population',
        title='Global Rabbit Population Trend',
    )
    
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Population',
        template='plotly_white',
    )
    
    return fig


def create_species_distribution_chart(df, year=None, regions=None):
    """
    Create a stacked bar chart showing species distribution by region.
    
    Args:
        df (pd.DataFrame): DataFrame with rabbit population data
        year (int, optional): Year to display. Defaults to the most recent year.
        regions (list, optional): List of regions to include. Defaults to all.
        
    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    # Make a copy to avoid modifying the original
    filtered_df = df.copy()
    
    # Filter by regions if specified
    if regions:
        filtered_df = filtered_df[filtered_df['Region'].isin(regions)]
    
    # Filter by year (use the most recent year if not specified)
    if year is None:
        year = filtered_df['Year'].max()
    
    filtered_df = filtered_df[filtered_df['Year'] == year]
    
    # Aggregate by region and species
    distribution_data = filtered_df.groupby(['Region', 'Species'])['Population'].sum().reset_index()
    
    fig = px.bar(
        distribution_data,
        x='Region',
        y='Population',
        color='Species',
        title=f'Species Distribution by Region (Year: {year})',
        barmode='stack',
    )
    
    fig.update_layout(
        xaxis_title='Region',
        yaxis_title='Population',
        template='plotly_white',
        legend_title='Species',
    )
    
    return fig


def create_habitat_chart(df, year=None, regions=None, species=None):
    """
    Create a pie chart showing population distribution by habitat.
    
    Args:
        df (pd.DataFrame): DataFrame with rabbit population data
        year (int, optional): Year to display. Defaults to the most recent year.
        regions (list, optional): List of regions to include. Defaults to all.
        species (list, optional): List of species to include. Defaults to all.
        
    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    # Filter data based on parameters
    filtered_df = filter_dataframe(df, regions, species, year_range=None)
    
    # Filter by year (use the most recent year if not specified)
    if year is None:
        year = filtered_df['Year'].max()
    
    filtered_df = filtered_df[filtered_df['Year'] == year]
    
    # Aggregate by habitat
    habitat_data = filtered_df.groupby('Habitat')['Population'].sum().reset_index()
    
    fig = px.pie(
        habitat_data,
        values='Population',
        names='Habitat',
        title=f'Rabbit Population by Habitat Type (Year: {year})',
        hole=0.3,
    )
    
    fig.update_layout(
        template='plotly_white',
        legend_title='Habitat Type',
    )
    
    return fig


def create_conservation_status_chart(df, regions=None, species=None, year_range=None):
    """
    Create an area chart showing population by conservation status over time.
    
    Args:
        df (pd.DataFrame): DataFrame with rabbit population data
        regions (list, optional): List of regions to include. Defaults to all.
        species (list, optional): List of species to include. Defaults to all.
        year_range (list, optional): [min_year, max_year] range. Defaults to all.
        
    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    # Filter data based on parameters
    filtered_df = filter_dataframe(df, regions, species, year_range)
    
    # Aggregate by conservation status and year
    conservation_data = filtered_df.groupby(['Year', 'Conservation_Status'])['Population'].sum().reset_index()
    
    fig = px.area(
        conservation_data,
        x='Year',
        y='Population',
        color='Conservation_Status',
        title='Population by Conservation Status Over Time',
        color_discrete_map={
            'Least Concern': 'green',
            'Near Threatened': 'yellow',
            'Vulnerable': 'orange',
            'Endangered': 'red',
        },
    )
    
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Population',
        template='plotly_white',
        legend_title='Conservation Status',
    )
    
    return fig


def create_geographic_map(df, year=None):
    """
    Create a choropleth map showing rabbit population by region.
    
    Args:
        df (pd.DataFrame): DataFrame with rabbit population data
        year (int, optional): Year to display. Defaults to the most recent year.
        
    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    import plotly.graph_objects as go
    
    # If no year specified, use the most recent year
    if year is None:
        year = df['Year'].max()
    
    # Filter data for the specified year
    df_year = df[df['Year'] == year]
    
    # Aggregate data by region
    region_data = df_year.groupby('Region')['Population'].sum().reset_index()
    
    # Simple mapping of regions to representative latitude and longitude
    # In a real application, we would use more precise geographic data
    region_coords = {
        'North America': {'lat': 40.7128, 'lon': -74.0060},
        'Europe': {'lat': 51.5074, 'lon': 0.1278},
        'Asia': {'lat': 34.0522, 'lon': 118.2437},
        'Africa': {'lat': -33.9249, 'lon': 18.4241},
        'Australia': {'lat': -33.8688, 'lon': 151.2093},
        'South America': {'lat': -23.5505, 'lon': -46.6333}
    }
    
    # Prepare data for the map
    lats = []
    lons = []
    texts = []
    sizes = []
    
    for _, row in region_data.iterrows():
        region = row['Region']
        population = row['Population']
        
        if region in region_coords:
            lats.append(region_coords[region]['lat'])
            lons.append(region_coords[region]['lon'])
            texts.append(f"{region}: {population:,}")
            # Scale the marker size logarithmically based on population
            sizes.append(np.log10(population) * 5)
    
    # Create a scatter map
    fig = go.Figure()
    
    fig.add_trace(go.Scattergeo(
        lat=lats,
        lon=lons,
        text=texts,
        marker=dict(
            size=sizes,
            color='#4e937a',
            line_color='rgb(40, 40, 40)',
            line_width=0.5,
            sizemode='area'
        ),
        mode='markers',
        name='Rabbit Population'
    ))
    
    fig.update_layout(
        title=f'Global Rabbit Population Distribution (Year: {year})',
        geo=dict(
            showland=True,
            landcolor='rgb(217, 217, 217)',
            countrycolor='rgb(255, 255, 255)',
            coastlinecolor='rgb(255, 255, 255)',
            projection_type='natural earth'
        ),
        height=600
    )
    
    return fig


def create_breeding_patterns_chart(df, species=None, regions=None):
    """
    Create a heatmap showing rabbit breeding patterns throughout the year.
    
    Args:
        df (pd.DataFrame): DataFrame with rabbit population data
        species (list, optional): List of species to include. Defaults to all.
        regions (list, optional): List of regions to include. Defaults to all.
        
    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    import plotly.graph_objects as go
    import numpy as np
    import pandas as pd
    
    # Filter data based on parameters
    filtered_df = filter_dataframe(df, regions, species, None)
    
    # Extract month from the year (we'll use decimal part to represent month)
    # Since our data is yearly, we'll generate synthetic monthly data for this example
    monthly_data = []
    
    for year in filtered_df['Year'].unique():
        base_year_data = filtered_df[filtered_df['Year'] == year]
        
        for month in range(1, 13):
            # Create monthly factor - higher in spring/summer (breeding season for many rabbits)
            if 3 <= month <= 8:  # Spring and summer months
                seasonal_factor = 1.2 + 0.2 * np.sin(np.pi * month / 6)
            else:  # Fall and winter months
                seasonal_factor = 0.8 + 0.1 * np.sin(np.pi * month / 6)
            
            # Add some randomness
            random_factor = np.random.normal(1, 0.1)
            
            # For each species and region
            for _, row in base_year_data.iterrows():
                monthly_data.append({
                    'Year': year,
                    'Month': month,
                    'Region': row['Region'],
                    'Species': row['Species'],
                    'MonthlyGrowth': row.get('YoY_Growth', 5) * seasonal_factor * random_factor / 12,
                    'MonthName': pd.Timestamp(year=2000, month=month, day=1).strftime('%b')
                })
    
    # Create a monthly growth heatmap
    monthly_df = pd.DataFrame(monthly_data)
    
    # Aggregate by month and species
    heatmap_data = monthly_df.groupby(['Month', 'Species'])['MonthlyGrowth'].mean().reset_index()
    
    # Pivot for heatmap format
    pivot_data = heatmap_data.pivot(index='Species', columns='Month', values='MonthlyGrowth')
    
    # Replace numeric months with month names
    month_names = [pd.Timestamp(year=2000, month=i, day=1).strftime('%b') for i in range(1, 13)]
    pivot_data.columns = month_names
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=month_names,
        y=pivot_data.index,
        colorscale='Viridis',
        colorbar=dict(title='Growth Rate (%)'),
    ))
    
    fig.update_layout(
        title='Monthly Breeding Patterns by Species',
        xaxis_title='Month',
        yaxis_title='Species',
        template='plotly_white',
        height=500
    )
    
    return fig


def filter_dataframe(df, regions=None, species=None, year_range=None, conservation_statuses=None):
    """
    Filter the dataframe based on user selections.
    
    Args:
        df (pd.DataFrame): DataFrame with rabbit population data
        regions (list, optional): List of regions to include. Defaults to all.
        species (list, optional): List of species to include. Defaults to all.
        year_range (list, optional): [min_year, max_year] range. Defaults to all.
        conservation_statuses (list, optional): List of conservation statuses to include. Defaults to all.
        
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    # Create a copy to avoid modifying the original
    filtered_df = df.copy()
    
    # Filter by regions if selected
    if regions and len(regions) > 0:
        filtered_df = filtered_df[filtered_df['Region'].isin(regions)]
    
    # Filter by species if selected
    if species and len(species) > 0:
        filtered_df = filtered_df[filtered_df['Species'].isin(species)]
    
    # Filter by year range
    if year_range and len(year_range) == 2:
        filtered_df = filtered_df[(filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])]
    
    # Filter by conservation status
    if conservation_statuses and len(conservation_statuses) > 0:
        filtered_df = filtered_df[filtered_df['Conservation_Status'].isin(conservation_statuses)]
    
    return filtered_df

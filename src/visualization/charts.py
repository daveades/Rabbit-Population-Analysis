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
    # This is a placeholder for a future geographic mapping feature
    # Would require additional geographic data (e.g., GeoJSON files for regions)
    pass


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

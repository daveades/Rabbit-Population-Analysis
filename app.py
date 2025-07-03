"""
Global Rabbit Population Dashboard
Main application file that initializes and runs the Dash app
"""

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import io
import base64

# Import local modules
from src.analysis.data_processor import load_data
from src.visualization.charts import create_population_chart, create_species_distribution_chart

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.title = "Global Rabbit Population Dashboard"
server = app.server

# Load sample data (will be replaced with actual data loading function)
try:
    df = load_data()
except FileNotFoundError:
    # Create sample data if real data is not available yet
    import numpy as np
    
    # Sample data for initial development
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

# App layout
app.layout = dbc.Container(
    [
        # Header
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H1("🐰 Global Rabbit Population Dashboard", className="display-4"),
                        html.P(
                            "Interactive visualizations of worldwide rabbit populations, species distribution, and habitat analysis",
                            className="lead",
                        ),
                        html.Hr(),
                    ],
                    className="text-center my-4",
                )
            )
        ),
        
        # Main dashboard content
        dbc.Row(
            [
                # Sidebar with filters
                dbc.Col(
                    [
                        html.H4("Filters", className="text-center"),
                        html.Label("Select Region:"),
                        dcc.Dropdown(
                            id="region-dropdown",
                            options=[{"label": region, "value": region} for region in sorted(df["Region"].unique())],
                            value=None,
                            placeholder="All Regions",
                            multi=True,
                            className="mb-3",
                        ),
                        
                        html.Label("Select Species:"),
                        dcc.Dropdown(
                            id="species-dropdown",
                            options=[{"label": species, "value": species} for species in sorted(df["Species"].unique())],
                            value=None,
                            placeholder="All Species",
                            multi=True,
                            className="mb-3",
                        ),
                        
                        html.Label("Year Range:"),
                        dcc.RangeSlider(
                            id="year-slider",
                            min=df["Year"].min(),
                            max=df["Year"].max(),
                            step=1,
                            marks={i: str(i) for i in range(df["Year"].min(), df["Year"].max() + 1, 5)},
                            value=[df["Year"].min(), df["Year"].max()],
                            className="mb-4",
                        ),
                        
                        html.Label("Conservation Status:"),
                        dcc.Checklist(
                            id="conservation-checklist",
                            options=[{"label": status, "value": status} for status in sorted(df["Conservation_Status"].unique())],
                            value=df["Conservation_Status"].unique().tolist(),
                            className="mb-3",
                        ),
                        
                        html.Hr(),
                        
                        # Summary statistics
                        html.Div(id="summary-stats", className="my-4"),
                        
                        # Data export section
                        html.Hr(),
                        html.H5("Data Export", className="text-center"),
                        html.P("Export filtered data:", className="mb-2"),
                        dbc.ButtonGroup(
                            [
                                dbc.Button("CSV", id="export-csv", color="primary", size="sm"),
                                dbc.Button("JSON", id="export-json", color="secondary", size="sm"),
                            ],
                            className="mb-3 d-grid",
                        ),
                        dcc.Download(id="download-data"),
                    ],
                    width=3,
                    className="bg-light p-3 border rounded",
                ),
                
                # Main content area with charts
                dbc.Col(
                    [
                        dbc.Tabs(
                            [
                                dbc.Tab(
                                    [
                                        html.Div(
                                            [
                                                html.H4("Global Rabbit Population Trends", className="text-center my-3"),
                                                dcc.Graph(id="population-trend-chart"),
                                            ]
                                        )
                                    ],
                                    label="Population Trends",
                                ),
                                dbc.Tab(
                                    [
                                        html.H4("Species Distribution by Region", className="text-center my-3"),
                                        dcc.Graph(id="species-distribution-chart"),
                                    ],
                                    label="Species Distribution",
                                ),
                                dbc.Tab(
                                    [
                                        html.H4("Habitat Analysis", className="text-center my-3"),
                                        dcc.Graph(id="habitat-chart"),
                                    ],
                                    label="Habitat Analysis",
                                ),
                                dbc.Tab(
                                    [
                                        html.H4("Conservation Status", className="text-center my-3"),
                                        dcc.Graph(id="conservation-chart"),
                                    ],
                                    label="Conservation Status",
                                ),
                            ]
                        )
                    ],
                    width=9,
                ),
            ]
        ),
        
        # Footer
        dbc.Row(
            dbc.Col(
                html.Footer(
                    html.P(
                        "Global Rabbit Population Dashboard - Analyzing worldwide rabbit data since 2025",
                        className="text-center text-muted",
                    ),
                    className="mt-5 pt-3 border-top",
                )
            )
        ),
    ],
    fluid=True,
)


# Callback to update summary statistics
@app.callback(
    Output("summary-stats", "children"),
    [
        Input("region-dropdown", "value"),
        Input("species-dropdown", "value"),
        Input("year-slider", "value"),
        Input("conservation-checklist", "value"),
    ],
)
def update_summary_stats(regions, species, year_range, conservation_statuses):
    filtered_df = filter_dataframe(df, regions, species, year_range, conservation_statuses)
    
    # Calculate summary statistics
    total_population = filtered_df[filtered_df["Year"] == max(filtered_df["Year"])]["Population"].sum()
    num_species = filtered_df["Species"].nunique()
    num_regions = filtered_df["Region"].nunique()
    endangered_percent = filtered_df[filtered_df["Conservation_Status"] == "Endangered"]["Population"].sum() / total_population * 100 if total_population > 0 else 0
    
    return [
        html.H5("Summary Statistics", className="text-center"),
        html.P(f"Total Population: {total_population:,}", className="mb-0"),
        html.P(f"Species Count: {num_species}", className="mb-0"),
        html.P(f"Regions: {num_regions}", className="mb-0"),
        html.P(f"Endangered: {endangered_percent:.1f}%", className="mb-0"),
    ]


# Callback to update population trend chart
@app.callback(
    Output("population-trend-chart", "figure"),
    [
        Input("region-dropdown", "value"),
        Input("species-dropdown", "value"),
        Input("year-slider", "value"),
        Input("conservation-checklist", "value"),
    ],
)
def update_population_trend(regions, species, year_range, conservation_statuses):
    filtered_df = filter_dataframe(df, regions, species, year_range, conservation_statuses)
    
    # Aggregate by year
    yearly_data = filtered_df.groupby("Year")["Population"].sum().reset_index()
    
    fig = px.line(
        yearly_data,
        x="Year",
        y="Population",
        title="Global Rabbit Population Trend",
    )
    
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Population",
        template="plotly_white",
        legend_title="Region",
    )
    
    return fig


# Callback to update species distribution chart
@app.callback(
    Output("species-distribution-chart", "figure"),
    [
        Input("region-dropdown", "value"),
        Input("species-dropdown", "value"),
        Input("year-slider", "value"),
        Input("conservation-checklist", "value"),
    ],
)
def update_species_distribution(regions, species, year_range, conservation_statuses):
    filtered_df = filter_dataframe(df, regions, species, year_range, conservation_statuses)
    
    # Get the most recent year data
    max_year = filtered_df["Year"].max()
    recent_data = filtered_df[filtered_df["Year"] == max_year]
    
    # Aggregate by region and species
    distribution_data = recent_data.groupby(["Region", "Species"])["Population"].sum().reset_index()
    
    fig = px.bar(
        distribution_data,
        x="Region",
        y="Population",
        color="Species",
        title=f"Species Distribution by Region (Year: {max_year})",
        barmode="stack",
    )
    
    fig.update_layout(
        xaxis_title="Region",
        yaxis_title="Population",
        template="plotly_white",
        legend_title="Species",
    )
    
    return fig


# Callback to update habitat chart
@app.callback(
    Output("habitat-chart", "figure"),
    [
        Input("region-dropdown", "value"),
        Input("species-dropdown", "value"),
        Input("year-slider", "value"),
        Input("conservation-checklist", "value"),
    ],
)
def update_habitat_chart(regions, species, year_range, conservation_statuses):
    filtered_df = filter_dataframe(df, regions, species, year_range, conservation_statuses)
    
    # Get the most recent year data
    max_year = filtered_df["Year"].max()
    recent_data = filtered_df[filtered_df["Year"] == max_year]
    
    # Aggregate by habitat and species
    habitat_data = recent_data.groupby(["Habitat", "Species"])["Population"].sum().reset_index()
    
    fig = px.pie(
        habitat_data,
        values="Population",
        names="Habitat",
        title=f"Rabbit Population by Habitat Type (Year: {max_year})",
        hole=0.3,
    )
    
    fig.update_layout(
        template="plotly_white",
        legend_title="Habitat Type",
    )
    
    return fig


# Callback to update conservation chart
@app.callback(
    Output("conservation-chart", "figure"),
    [
        Input("region-dropdown", "value"),
        Input("species-dropdown", "value"),
        Input("year-slider", "value"),
        Input("conservation-checklist", "value"),
    ],
)
def update_conservation_chart(regions, species, year_range, conservation_statuses):
    filtered_df = filter_dataframe(df, regions, species, year_range, conservation_statuses)
    
    # Aggregate by conservation status and year
    conservation_data = filtered_df.groupby(["Year", "Conservation_Status"])["Population"].sum().reset_index()
    
    fig = px.area(
        conservation_data,
        x="Year",
        y="Population",
        color="Conservation_Status",
        title="Population by Conservation Status Over Time",
        color_discrete_map={
            "Least Concern": "green",
            "Near Threatened": "yellow",
            "Vulnerable": "orange",
            "Endangered": "red",
        },
    )
    
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Population",
        template="plotly_white",
        legend_title="Conservation Status",
    )
    
    return fig


# Helper function to filter dataframe based on user selections
def filter_dataframe(df, regions, species, year_range, conservation_statuses):
    """Filter the dataframe based on user selections."""
    filtered_df = df.copy()
    
    # Filter by regions if selected
    if regions and len(regions) > 0:
        filtered_df = filtered_df[filtered_df["Region"].isin(regions)]
    
    # Filter by species if selected
    if species and len(species) > 0:
        filtered_df = filtered_df[filtered_df["Species"].isin(species)]
    
    # Filter by year range
    filtered_df = filtered_df[(filtered_df["Year"] >= year_range[0]) & (filtered_df["Year"] <= year_range[1])]
    
    # Filter by conservation status
    if conservation_statuses and len(conservation_statuses) > 0:
        filtered_df = filtered_df[filtered_df["Conservation_Status"].isin(conservation_statuses)]
    
    return filtered_df


# Callback for data export
@app.callback(
    Output("download-data", "data"),
    [
        Input("export-csv", "n_clicks"),
        Input("export-json", "n_clicks"),
    ],
    [
        Input("region-dropdown", "value"),
        Input("species-dropdown", "value"),
        Input("year-slider", "value"),
        Input("conservation-checklist", "value"),
    ],
    prevent_initial_call=True,
)
def export_data(csv_clicks, json_clicks, regions, species, year_range, conservation_statuses):
    """Handle data export in CSV or JSON format."""
    ctx = dash.callback_context
    if not ctx.triggered:
        return None
    
    # Get the filtered data
    filtered_df = filter_dataframe(df, regions, species, year_range, conservation_statuses)
    
    # Determine which button was clicked
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if button_id == "export-csv":
        return dcc.send_data_frame(filtered_df.to_csv, "rabbit_population_data.csv", index=False)
    elif button_id == "export-json":
        return dcc.send_data_frame(filtered_df.to_json, "rabbit_population_data.json", orient="records")
    
    return None


if __name__ == "__main__":
    app.run_server(debug=True)

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
from src.analysis.data_processor import generate_sample_data
from src.visualization.charts import create_population_chart, create_species_distribution_chart

# Initialize the Dash app and load sample data
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.title = "Global Rabbit Population Dashboard"
server = app.server

df = generate_sample_data()

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
                        
                        html.Div(
                            [
                                html.Label("Theme:", className="mr-2"),
                                dbc.RadioItems(
                                    id="theme-switch",
                                    options=[
                                        {"label": "Light", "value": "light"},
                                        {"label": "Dark", "value": "dark"},
                                    ],
                                    value="light",
                                    inline=True,
                                ),
                            ],
                            className="mb-3",
                        ),
                        
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
                                dbc.Tab(
                                    [
                                        html.H4("Geographic Distribution", className="text-center my-3"),
                                        dcc.Graph(id="geographic-map"),
                                    ],
                                    label="Geographic Map",
                                ),
                                dbc.Tab(
                                    [
                                        html.H4("Breeding Patterns", className="text-center my-3"),
                                        dcc.Graph(id="breeding-patterns-chart"),
                                    ],
                                    label="Breeding Patterns",
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


# Callback to update geographic map
@app.callback(
    Output("geographic-map", "figure"),
    [
        Input("region-dropdown", "value"),
        Input("species-dropdown", "value"),
        Input("year-slider", "value"),
        Input("conservation-checklist", "value"),
    ],
)
def update_geographic_map(regions, species, year_range, conservation_statuses):
    filtered_df = filter_dataframe(df, regions, species, year_range, conservation_statuses)
    
    # Get the most recent year
    max_year = filtered_df["Year"].max()
    
    # Import visualization function from charts module
    from src.visualization.charts import create_geographic_map
    
    # Generate the map
    fig = create_geographic_map(filtered_df, max_year)
    
    return fig


# Callback to update breeding patterns chart
@app.callback(
    Output("breeding-patterns-chart", "figure"),
    [
        Input("region-dropdown", "value"),
        Input("species-dropdown", "value"),
        Input("year-slider", "value"),
        Input("conservation-checklist", "value"),
    ],
)
def update_breeding_patterns(regions, species, year_range, conservation_statuses):
    filtered_df = filter_dataframe(df, regions, species, year_range, conservation_statuses)
    
    # Import visualization function from charts module
    from src.visualization.charts import create_breeding_patterns_chart
    
    # Generate the chart
    fig = create_breeding_patterns_chart(filtered_df, species, regions)
    
    return fig


# Callback to update theme
@app.callback(
    Output("population-trend-chart", "figure", allow_duplicate=True),
    Output("species-distribution-chart", "figure", allow_duplicate=True),
    Output("habitat-chart", "figure", allow_duplicate=True),
    Output("conservation-chart", "figure", allow_duplicate=True),
    Output("geographic-map", "figure", allow_duplicate=True),
    Output("breeding-patterns-chart", "figure", allow_duplicate=True),
    Input("theme-switch", "value"),
    prevent_initial_call=True,
)
def update_theme(theme):
    """
    Update chart themes based on the theme switch value.
    """
    # Get all current figures
    ctx = dash.callback_context
    
    # Update template for all figures
    template = "plotly_dark" if theme == "dark" else "plotly_white"
    
    # Get the current charts
    trend_fig = update_population_trend(None, None, None, None)
    species_fig = update_species_distribution(None, None, None, None)
    habitat_fig = update_habitat_chart(None, None, None, None)
    conservation_fig = update_conservation_chart(None, None, None, None)
    geo_fig = update_geographic_map(None, None, None, None)
    breeding_fig = update_breeding_patterns(None, None, None, None)
    
    # Update each figure's template
    for fig in [trend_fig, species_fig, habitat_fig, conservation_fig, geo_fig, breeding_fig]:
        fig.update_layout(template=template)
    
    return trend_fig, species_fig, habitat_fig, conservation_fig, geo_fig, breeding_fig


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
    if year_range and len(year_range) == 2:
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
    import os
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get("PORT", 8050))
    
    # Check if we're running on Render (Render sets this environment variable)
    is_render = "RENDER" in os.environ
    
    # Set environment based on Render detection or explicit environment variable
    environment = os.environ.get("ENVIRONMENT", "production" if is_render else "development")
    debug_mode = environment == "development"
    
    print(f"Starting server in {environment} mode on port {port}")
    
    # For production deployment, use production-ready settings
    if environment == "production":
        # Use Gunicorn if available (in production), otherwise fall back to Flask's production server
        app.run_server(
            host="0.0.0.0",
            port=port,
            debug=False
        )
    else:
        # Development mode - use Dash's built-in server with debug enabled
        app.run_server(
            host="0.0.0.0",
            port=port,
            debug=debug_mode
        )

# 🐰 Global Rabbit Population Dashboard

A comprehensive dashboard for tracking and analyzing worldwide rabbit population data, featuring interactive visualizations and data-driven insights, powered by **Python data analysis**.

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Project Structure](#-project-structure)
- [Data Architecture](#-data-architecture)
- [Code Explanation](#-code-explanation)
- [Dashboard Features](#-dashboard-features)
- [Setup & Installation](#-setup--installation)
- [Development Workflow](#️-development-workflow)
- [Testing](#-testing)

## 🎯 Project Overview

This project is a full-stack data visualization dashboard that analyzes global rabbit population trends. It combines Python-based data processing with interactive web visualizations to provide insights into:

- **Population Dynamics**: How rabbit populations change over time
- **Species Distribution**: Geographic spread of different rabbit species
- **Conservation Status**: Tracking endangered and vulnerable populations
- **Habitat Analysis**: Understanding environmental impact on populations
- **Predictive Modeling**: Forecasting future population trends

## 📁 Project Structure

```
layovated/
├── 📱 app.py                    # Main Dash application (entry point)
├── 📋 requirements.txt          # Python dependencies
├── 🚀 run.sh                   # Application launcher script
├── 🧪 run_tests.py             # Test runner script
├── 📖 README.md                # Project documentation
├── 🚫 .gitignore               # Git ignore rules
│
├── 📊 src/                     # Source code modules
│   ├── 🔬 analysis/           # Data processing and analysis
│   │   ├── __init__.py
│   │   └── data_processor.py   # Core data loading and processing
│   ├── 📈 visualization/       # Chart and graph generation
│   │   ├── __init__.py
│   │   └── charts.py          # Plotly chart creation functions
│   └── 🌐 api/                # REST API endpoints
│       ├── __init__.py
│       └── routes.py          # API route definitions
│
├── 🌐 public/                  # Frontend static assets
│   ├── 📄 index.html          # Static HTML dashboard
│   ├── 🎨 css/
│   │   └── styles.css         # Dashboard styling
│   └── ⚡ js/
│       └── dashboard.js       # Client-side interactions
│
├── 📊 data/                    # Data storage
│   ├── raw/                   # Original, unprocessed data
│   └── processed/             # Cleaned and structured data
│
├── 📓 notebooks/               # Jupyter notebooks
│   └── rabbit_population_analysis.ipynb  # Data exploration
│
└── 🧪 tests/                  # Unit tests
    ├── test_data_processor.py  # Tests for data processing
    └── test_visualization_charts.py  # Tests for visualizations
```

## 🚀 Dashboard Features

### 📊 **Interactive Visualizations**

**1. Population Trends Tab**
- **Chart Type**: Line chart with time series
- **Data**: Aggregated population by year
- **Features**: 
  - Hover tooltips with exact values
  - Zooming and panning capabilities
  - Trend lines and moving averages
  - Downloadable as PNG/PDF

**2. Species Distribution Tab**
- **Chart Type**: Stacked bar chart
- **Data**: Population by region and species
- **Features**:
  - Color-coded species identification
  - Interactive legend (click to hide/show species)
  - Percentage view toggle
  - Regional comparison capabilities

**3. Habitat Analysis Tab**
- **Chart Type**: Donut pie chart
- **Data**: Population distribution by habitat type
- **Features**:
  - Percentage and absolute value display
  - Interactive segments (click to highlight)
  - Habitat-specific insights panel
  - Environmental correlation data

**4. Conservation Status Tab**
- **Chart Type**: Stacked area chart
- **Data**: Population by conservation status over time
- **Features**:
  - Color-coded risk levels (green to red)
  - Cumulative and percentage views
  - Endangered species alerts
  - Conservation trend analysis

### 🎛️ **Interactive Filters**

**Filter Synchronization**: All charts update simultaneously when any filter changes.

**1. Region Selector**
```python
# Multi-select dropdown
regions = ['North America', 'Europe', 'Asia', 'Africa', 'Australia', 'South America']
# Effect: Filters all data to selected regions only
```

**2. Species Selector**
```python
# Multi-select dropdown  
species = ['European Rabbit', 'Cottontail', 'Hare', 'Jackrabbit', 'Pygmy Rabbit']
# Effect: Shows only selected species in all visualizations
```

**3. Year Range Slider**
```python
# Range slider: 2000 ←→ 2025
# Effect: Temporal filtering across all charts
# Updates trend analysis and growth calculations
```

**4. Conservation Status Checklist**
```python
# Multiple checkboxes
statuses = ['Least Concern', 'Near Threatened', 'Vulnerable', 'Endangered']
# Effect: Filters by conservation risk level
```

### 📈 **Summary Statistics Panel**

Real-time calculated metrics that update with filter changes:

```python
# Live calculations
total_population = filtered_data[filtered_data['Year'] == max_year]['Population'].sum()
species_count = filtered_data['Species'].nunique()
region_count = filtered_data['Region'].nunique()
endangered_percent = (endangered_pop / total_population) * 100
```

**Displayed Metrics:**
- 🔢 **Total Population**: Current population in filtered dataset
- 🐰 **Species Count**: Number of distinct species in selection
- 🌍 **Regions**: Number of geographic regions included
- ⚠️ **Endangered %**: Percentage of population at risk

### 💾 **Data Export Features**

**CSV Export**:
```python
# Downloads: rabbit_population_data.csv
# Contains: All filtered data with current selections
# Format: Comma-separated values, ready for Excel/analysis
```

**JSON Export**:
```python
# Downloads: rabbit_population_data.json
# Format: [{"Year": 2023, "Region": "Europe", ...}, ...]
# Use case: API integration, web applications
```

## 🔧 Setup & Installation

### Prerequisites
- **Python 3.8+** (tested on 3.8.10)
- **pip** package manager
- **Git** for version control

### Quick Start

**1. Clone the Repository**
```bash
git clone https://github.com/yourusername/layovated.git
cd layovated
```

**2. Set Up Virtual Environment**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

**3. Install Dependencies**
```bash
# Install all required packages
pip install -r requirements.txt
```

**4. Run the Application**
```bash
# Option 1: Direct Python execution
python app.py

# Option 2: Using the launcher script
chmod +x run.sh
./run.sh

# Option 3: Background process
nohup python app.py > app.log 2>&1 &
```

**5. Access the Dashboard**
- Open browser to: `http://127.0.0.1:8050/`
- The dashboard will load with sample data
- All interactive features are immediately available

### 📦 **Dependencies Explained**

```python
# Core Web Framework
dash==2.14.1                    # Interactive web applications
dash-bootstrap-components==1.4.2 # Bootstrap UI components
flask==2.3.2                    # Web server backend
werkzeug==2.3.6                 # WSGI utility library

# Data Processing
pandas==1.5.3                   # Data manipulation and analysis
numpy==1.24.3                   # Numerical computations

# Visualization
plotly==5.14.1                  # Interactive charts and graphs
matplotlib==3.7.1               # Static plotting (fallback)
seaborn==0.12.2                 # Statistical visualizations

# Scientific Computing
scipy==1.10.1                   # Scientific algorithms
scikit-learn==1.2.2             # Machine learning tools

# Geospatial Analysis
geopandas==0.12.2               # Geographic data processing
folium==0.14.0                  # Interactive maps

# Development Environment
notebook==6.5.4                 # Jupyter notebook server
jupyter-console==6.6.3          # Jupyter console interface
nbconvert==7.2.9                # Notebook format conversion
ipykernel==6.19.4               # IPython kernel for Jupyter

# Testing & Quality
pytest==7.3.1                   # Testing framework
pylint==2.17.0                  # Code quality analysis
black==23.3.0                   # Code formatting
```

### 🗂️ **Data Setup** (Optional)

If you have real rabbit population data:

**1. Prepare CSV Files**
```bash
# Place CSV files in data/raw/
# Required columns: Year, Region, Species, Population, Habitat, Conservation_Status
```

**2. Update Data Paths**
```python
# In src/analysis/data_processor.py
def load_data(data_path='data/processed/rabbit_population.csv'):
    # Update path to your data file
```

## 🏗️ Data Architecture

### Data Structure

Our rabbit population dataset follows a structured schema designed for comprehensive analysis:

```python
# Core Data Schema
{
    'Year': int,                    # Year of observation (2000-2025)
    'Region': str,                  # Geographic region
    'Species': str,                 # Rabbit species name
    'Population': int,              # Estimated population count
    'Habitat': str,                 # Primary habitat type
    'Conservation_Status': str      # IUCN conservation status
}
```

### Sample Data Structure
```python
{
    'Year': 2023,
    'Region': 'North America',
    'Species': 'Cottontail',
    'Population': 45000,
    'Habitat': 'Grassland',
    'Conservation_Status': 'Least Concern'
}
```

### Data Categories

#### 🌍 **Regions** (6 global regions)
- North America
- Europe
- Asia
- Africa
- Australia
- South America

#### 🐰 **Species** (5 main rabbit types)
- European Rabbit (*Oryctolagus cuniculus*)
- Cottontail (*Sylvilagus* species)
- Hare (*Lepus* species)
- Jackrabbit (*Lepus californicus*)
- Pygmy Rabbit (*Brachylagus idahoensis*)

#### 🏞️ **Habitats** (4 primary types)
- **Forest**: Wooded areas with tree cover
- **Grassland**: Open meadows and prairies
- **Desert**: Arid and semi-arid regions
- **Urban**: Human-developed areas

#### 🚨 **Conservation Status** (IUCN Categories)
- **Least Concern** (60%): Stable populations
- **Near Threatened** (20%): Declining but not endangered
- **Vulnerable** (15%): High risk of endangerment
- **Endangered** (5%): Very high risk of extinction

### Data Flow Pipeline

```
Raw Data → Data Processor → Filtered Data → Visualizations
    ↓           ↓              ↓              ↓
CSV Files → Load & Clean → Apply Filters → Generate Charts
    ↓           ↓              ↓              ↓
Multiple → Pandas DataFrame → User Selection → Plotly Graphs
Sources
```

## 💻 Code Explanation

### 🚀 **app.py** - Main Application

This is the heart of the dashboard - a Dash application that creates an interactive web interface.

**Key Components:**
```python
# 1. Data Loading & Generation
try:
    df = load_data()  # Try to load real data
except FileNotFoundError:
    # Generate synthetic data for development
    # Creates 26 years × 6 regions × 5 species = 780 data points per year
```

**2. Dashboard Layout:**
- **Header**: Title and description
- **Sidebar (25% width)**: Interactive filters
  - Region dropdown (multi-select)
  - Species dropdown (multi-select)
  - Year range slider (2000-2025)
  - Conservation status checklist
  - Summary statistics display
  - Data export buttons (CSV/JSON)
- **Main Area (75% width)**: Tabbed visualizations
  - Population Trends (line chart)
  - Species Distribution (stacked bar chart)
  - Habitat Analysis (pie chart)
  - Conservation Status (area chart)

**3. Interactive Callbacks:**
```python
@app.callback(
    Output("chart-id", "figure"),
    [Input("filter-id", "value"), ...]
)
def update_chart(filter_values):
    # Filter data based on user selections
    # Generate updated visualization
    # Return new chart
```

### 🔬 **src/analysis/data_processor.py** - Data Processing Engine

**Core Functions:**

**1. Data Loading:**
```python
def load_data(data_path=None):
    """
    Loads rabbit population data from CSV files.
    Falls back to sample data generation if files don't exist.
    
    Returns: pandas.DataFrame with standardized columns
    """
```

**2. Data Cleaning:**
```python
def clean_data(df):
    """
    - Removes invalid entries (negative populations, missing values)
    - Standardizes species names and region codes
    - Validates conservation status categories
    - Ensures data type consistency
    """
```

**3. Data Aggregation:**
```python
def aggregate_by_region(df, year_range):
    """
    Groups population data by region and calculates:
    - Total population per region
    - Species diversity per region
    - Average growth rates
    - Conservation risk percentages
    """
```

### 📈 **src/visualization/charts.py** - Chart Generation

**Chart Types:**

**1. Population Trend Chart:**
```python
def create_population_chart(filtered_data):
    """
    Creates time-series line chart showing:
    - Total population over time
    - Trend lines for each region
    - Moving averages for smoothing
    - Confidence intervals for predictions
    """
```

**2. Species Distribution Chart:**
```python
def create_species_distribution_chart(filtered_data):
    """
    Creates stacked bar chart showing:
    - Species composition by region
    - Relative abundance of each species
    - Geographic distribution patterns
    """
```

**3. Filtering System:**
```python
def filter_dataframe(df, regions, species, year_range, conservation_statuses):
    """
    Advanced filtering logic:
    1. Region filtering: df[df['Region'].isin(regions)]
    2. Species filtering: df[df['Species'].isin(species)]
    3. Year range: df[(df['Year'] >= start) & (df['Year'] <= end)]
    4. Conservation status: df[df['Conservation_Status'].isin(statuses)]
    
    Returns: Filtered pandas DataFrame
    """
```

### 🌐 **src/api/routes.py** - REST API

**API Endpoints:**
```python
# GET /api/populations - Get all population data
# GET /api/populations?region=Europe&species=Hare - Filtered data
# GET /api/species - List all species
# GET /api/regions - List all regions
# GET /api/stats - Summary statistics
# POST /api/predictions - Generate population predictions
```

### 🎨 **Frontend Components**

**1. public/index.html:**
- Static HTML dashboard (alternative to Dash)
- Semantic HTML structure
- Responsive grid layout
- Accessibility features (ARIA labels, alt text)

**2. public/css/styles.css:**
- Mobile-first responsive design
- CSS Grid and Flexbox layouts
- Custom color scheme for data visualization
- Print-friendly styles

**3. public/js/dashboard.js:**
- Client-side data fetching
- Interactive chart updates
- Form validation
- Local storage for user preferences

### 🧪 **Testing Framework**

**1. tests/test_data_processor.py:**
```python
class TestDataProcessor(unittest.TestCase):
    def test_load_data_success():
        # Test successful data loading
    
    def test_data_cleaning():
        # Test data validation and cleaning
    
    def test_aggregation_functions():
        # Test grouping and calculation functions
```

**2. tests/test_visualization_charts.py:**
```python
class TestVisualizationCharts(unittest.TestCase):
    def test_filter_dataframe():
        # Test filtering logic with sample data
    
    def test_chart_generation():
        # Test chart creation functions
```

## 🔄 Data Processing Workflow

### 1. Data Ingestion
```
Raw CSV Files → pandas.read_csv() → Initial DataFrame
```

### 2. Data Validation
```python
# Check for required columns
required_cols = ['Year', 'Region', 'Species', 'Population', 'Habitat', 'Conservation_Status']

# Validate data types
df['Year'] = pd.to_numeric(df['Year'])
df['Population'] = pd.to_numeric(df['Population'])

# Remove invalid entries
df = df.dropna()
df = df[df['Population'] >= 0]
```

### 3. Data Transformation
```python
# Standardize region names
region_mapping = {
    'N. America': 'North America',
    'N America': 'North America',
    # ... other mappings
}
df['Region'] = df['Region'].map(region_mapping)

# Calculate derived metrics
df['Population_Density'] = df['Population'] / df['Area']
df['Growth_Rate'] = df.groupby(['Region', 'Species'])['Population'].pct_change()
```

### 4. Real-time Filtering
```python
# User selects: Region=['Europe'], Species=['Hare'], Year=[2020,2023]
filtered_df = df[
    (df['Region'].isin(['Europe'])) &
    (df['Species'].isin(['Hare'])) &
    (df['Year'] >= 2020) &
    (df['Year'] <= 2023)
]
# Result: 4 rows (1 species × 1 region × 4 years)
```

### 5. Aggregation for Visualization
```python
# For population trend chart
yearly_totals = filtered_df.groupby('Year')['Population'].sum()

# For species distribution
species_by_region = filtered_df.groupby(['Region', 'Species'])['Population'].sum()

# For habitat analysis
habitat_distribution = filtered_df.groupby('Habitat')['Population'].sum()
```

## 🎛️ Interactive Features

### Real-time Data Updates
- **Filters trigger callbacks** → **Data re-filtering** → **Chart regeneration**
- All visualizations update simultaneously when filters change
- Summary statistics recalculate automatically

### Export Functionality
```python
# CSV Export
filtered_df.to_csv('rabbit_population_filtered.csv', index=False)

# JSON Export
filtered_df.to_json('rabbit_population_filtered.json', orient='records')
```

### Responsive Design
- **Desktop**: Full sidebar + main content
- **Tablet**: Collapsible sidebar
- **Mobile**: Stacked layout with bottom filters

## 🛠️ Development Workflow

### Git Branching Strategy

This project follows a **feature-based branching workflow** with atomic commits for each change:

```bash
master/main              # Production-ready code
├── feature/data-processing      # Enhanced data processing
├── feature/enhanced-visualizations    # New chart types  
├── feature/dashboard-ui         # UI/UX improvements
├── feature/api-endpoints        # REST API development
├── feature/unit-tests           # Testing infrastructure
├── feature/environment-setup    # Dependency management
└── feature/data-export          # Export functionality
```

### Development Workflow Steps

**1. Create Feature Branch**
```bash
# Start from latest master
git checkout master
git pull origin master

# Create new feature branch
git checkout -b feature/your-feature-name
```

**2. Make Atomic Commits**
```bash
# Make focused changes
git add specific_file.py
git commit -m "feat: add data validation function

- Implement input sanitization for CSV uploads
- Add error handling for malformed data
- Include unit tests for validation logic"

# Each commit should be:
# - Focused on one specific change
# - Include descriptive commit message
# - Be independently testable
```

**3. Push and Create Pull Request**
```bash
# Push feature branch
git push origin feature/your-feature-name

# Create pull request on GitHub/GitLab
# Include description of changes and testing done
```

**4. Code Review and Merge**
```bash
# After review approval, merge to master
git checkout master
git merge feature/your-feature-name
git push origin master

# Clean up feature branch
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

### Commit Message Convention

```bash
# Format: type(scope): description
#
# Types:
feat:     # New feature
fix:      # Bug fix  
docs:     # Documentation
style:    # Code style changes
refactor: # Code refactoring
test:     # Adding tests
chore:    # Maintenance tasks

# Examples:
feat(dashboard): add species filter dropdown
fix(data): resolve CSV parsing error for European data
docs(readme): update installation instructions
test(analysis): add unit tests for data aggregation
```

### Branch Examples from This Project

**1. feature/environment-setup**
```bash
# Commits made:
529d305 feat: add comprehensive test suite
2e8cbcd fix: resolve Flask/Werkzeug compatibility issues
6d8d21b feat: enhance frontend dashboard interface

# Purpose: Set up development environment and fix dependencies
```

**2. feature/data-export** 
```bash
# Commits made:
d96c722 feat: add data export functionality

# Purpose: Allow users to download filtered data as CSV/JSON
```

## 🧪 Testing

### Test Structure
```
tests/
├── test_data_processor.py       # Data processing logic tests
├── test_visualization_charts.py # Chart generation tests
└── run_tests.py                # Test runner script
```

### Running Tests

**1. All Tests**
```bash
# Using test runner
python run_tests.py

# Using pytest directly
pytest tests/ -v
```

**2. Specific Test Categories**
```bash
# Data processing tests only
pytest tests/test_data_processor.py -v

# Visualization tests only  
pytest tests/test_visualization_charts.py -v
```

**3. Test Examples**
```python
# Data filtering test
def test_filter_dataframe_regions():
    result = filter_dataframe(sample_data, regions=['North America'])
    assert result['Region'].unique().tolist() == ['North America']

# Data validation test  
def test_load_data_validates_columns():
    df = load_data()
    required_cols = ['Year', 'Region', 'Species', 'Population']
    assert all(col in df.columns for col in required_cols)
```

## 📊 Performance & Scalability

### Data Optimization
```python
# Efficient filtering for large datasets
def filter_with_query(df, filters):
    query_parts = []
    if filters.get('regions'):
        query_parts.append(f"Region in {filters['regions']}")
    if filters.get('species'):
        query_parts.append(f"Species in {filters['species']}")
    
    query = ' and '.join(query_parts)
    return df.query(query) if query else df
```

### Memory Management
```python
# Load large files in chunks
def load_large_dataset(file_path, chunk_size=10000):
    chunks = pd.read_csv(file_path, chunksize=chunk_size)
    return pd.concat(chunks, ignore_index=True)
```

## 🚀 Deployment Options

### Local Production
```bash
# Using Gunicorn WSGI server
pip install gunicorn
gunicorn app:server -b 0.0.0.0:8050 --workers 4
```

### Docker Deployment
```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8050
CMD ["python", "app.py"]
```

### Cloud Platforms
- **Heroku**: `git push heroku main` for automatic deployment
- **AWS EC2**: Full virtual machine control
- **Google Cloud Run**: Serverless container hosting
- **DigitalOcean App Platform**: Simple PaaS deployment

## 📚 Research Applications

### Conservation Biology
- **Species Recovery Monitoring**: Track endangered rabbit populations
- **Habitat Restoration**: Measure habitat improvement impact
- **Climate Change Research**: Study temperature effects on populations

### Wildlife Management
- **Sustainable Hunting**: Set evidence-based hunting quotas
- **Ecosystem Balance**: Monitor predator-prey dynamics
- **Disease Surveillance**: Track population health indicators

### Academic Research
- **Population Dynamics**: Mathematical modeling of growth patterns
- **Genetic Studies**: Correlate population size with genetic diversity
- **Behavioral Ecology**: Study territorial and social behaviors

## 🤝 Contributing

### Getting Started
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Ensure all tests pass: `python run_tests.py`
5. Commit your changes: `git commit -m 'feat: add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Standards
- **Python**: Follow PEP 8 style guidelines
- **Testing**: Maintain >80% code coverage
- **Documentation**: Update README for new features
- **Commits**: Use conventional commit messages

## 📞 Support & Contact

### Getting Help
- **Documentation**: Check this README first
- **Issues**: [GitHub Issues](https://github.com/yourusername/layovated/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/layovated/discussions)

### Reporting Bugs
Please include:
- Python version and OS
- Steps to reproduce the issue
- Expected vs actual behavior
- Console/error output

### Feature Requests
Use the GitHub Issues template for feature requests with:
- Clear description of the requested feature
- Use case and benefits
- Implementation suggestions (optional)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### License Summary
- ✅ Commercial use allowed
- ✅ Modification allowed  
- ✅ Distribution allowed
- ✅ Private use allowed
- ❌ No warranty provided
- ❌ Authors not liable

---

**🐰 Happy Analyzing!** | Built with ❤️ for wildlife conservation | Last updated: July 2025

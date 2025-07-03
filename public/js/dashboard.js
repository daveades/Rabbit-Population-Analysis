/**
 * Global Rabbit Population Dashboard JavaScript
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Fetch data from our API
    fetchDashboardData();

    // Set up event listeners for filters
    setupEventListeners();

    // Smooth scroll for navigation links
    setupSmoothScrolling();
});

/**
 * Fetch data for the dashboard
 */
async function fetchDashboardData() {
    try {
        // For demonstration, we'll use sample data instead of actual API calls
        // In a real application, these would be actual fetch requests to the API

        // Generate sample data
        const data = generateSampleData();

        // Update dashboard with the data
        updateDashboard(data);

    } catch (error) {
        console.error('Error fetching dashboard data:', error);
        showErrorMessage('Failed to load dashboard data. Please try again later.');
    }
}

/**
 * Generate sample data for development
 */
function generateSampleData() {
    // Sample regions
    const regions = ['North America', 'Europe', 'Asia', 'Africa', 'Australia', 'South America'];

    // Sample species
    const species = ['European Rabbit', 'Cottontail', 'Hare', 'Jackrabbit', 'Pygmy Rabbit'];

    // Sample years
    const years = Array.from({ length: 26 }, (_, i) => 2000 + i);

    // Sample habitats
    const habitats = ['Forest', 'Grassland', 'Desert', 'Urban'];

    // Sample conservation statuses
    const conservationStatuses = ['Least Concern', 'Near Threatened', 'Vulnerable', 'Endangered'];

    // Generate population data
    const populationData = [];

    for (const year of years) {
        for (const region of regions) {
            for (const specie of species) {
                // Create some variation in the data with upward trend and seasonal pattern
                const basePopulation = Math.floor(Math.random() * 40000) + 10000;
                const trend = (year - 2000) * 500;  // Increasing trend over time
                const seasonal = Math.sin(year) * 2000;  // Some seasonal variation
                const randomFactor = (Math.random() - 0.5) * 10000;  // Random noise

                const population = Math.max(100, Math.floor(basePopulation + trend + seasonal + randomFactor));

                // Randomly assign habitat and conservation status
                const habitat = habitats[Math.floor(Math.random() * habitats.length)];

                // Weight the conservation statuses to make Least Concern most common
                let conservationStatus;
                const rand = Math.random();
                if (rand < 0.6) {
                    conservationStatus = conservationStatuses[0]; // Least Concern
                } else if (rand < 0.8) {
                    conservationStatus = conservationStatuses[1]; // Near Threatened
                } else if (rand < 0.95) {
                    conservationStatus = conservationStatuses[2]; // Vulnerable
                } else {
                    conservationStatus = conservationStatuses[3]; // Endangered
                }

                populationData.push({
                    year,
                    region,
                    species: specie,
                    population,
                    habitat,
                    conservationStatus
                });
            }
        }
    }

    // Create summary data
    const currentYear = 2025;
    const currentYearData = populationData.filter(d => d.year === currentYear);

    const totalPopulation = currentYearData.reduce((sum, d) => sum + d.population, 0);
    const growthRate = 2.7; // Sample growth rate
    const regionsCount = regions.length;
    const speciesCount = species.length;

    // Prepare data for population trend chart
    const populationByYear = years.map(year => {
        const yearData = populationData.filter(d => d.year === year);
        return {
            year,
            population: yearData.reduce((sum, d) => sum + d.population, 0)
        };
    });

    // Prepare data for species distribution chart
    const speciesDistribution = species.map(specie => {
        const specieData = currentYearData.filter(d => d.species === specie);
        return {
            species: specie,
            population: specieData.reduce((sum, d) => sum + d.population, 0)
        };
    });

    // Prepare data for habitat chart
    const habitatDistribution = habitats.map(habitat => {
        const habitatData = currentYearData.filter(d => d.habitat === habitat);
        return {
            habitat,
            population: habitatData.reduce((sum, d) => sum + d.population, 0)
        };
    });

    // Prepare data for conservation status chart
    const conservationData = years.map(year => {
        const yearData = populationData.filter(d => d.year === year);

        return {
            year,
            leastConcern: yearData.filter(d => d.conservationStatus === 'Least Concern')
                .reduce((sum, d) => sum + d.population, 0),
            nearThreatened: yearData.filter(d => d.conservationStatus === 'Near Threatened')
                .reduce((sum, d) => sum + d.population, 0),
            vulnerable: yearData.filter(d => d.conservationStatus === 'Vulnerable')
                .reduce((sum, d) => sum + d.population, 0),
            endangered: yearData.filter(d => d.conservationStatus === 'Endangered')
                .reduce((sum, d) => sum + d.population, 0)
        };
    });

    return {
        summary: {
            totalPopulation,
            growthRate,
            regionsCount,
            speciesCount
        },
        populationByYear,
        speciesDistribution,
        habitatDistribution,
        conservationData,
        regions,
        species,
        years
    };
}

/**
 * Update the dashboard with the provided data
 */
function updateDashboard(data) {
    // Update summary metrics
    document.getElementById('total-population').textContent = formatNumber(data.summary.totalPopulation);
    document.getElementById('growth-rate').textContent = `${data.summary.growthRate}%`;
    document.getElementById('regions-count').textContent = data.summary.regionsCount;
    document.getElementById('species-count').textContent = data.summary.speciesCount;

    // Populate filter dropdowns
    populateFilterDropdowns(data);

    // Create charts
    createPopulationTrendChart(data.populationByYear);
    createPopulationByRegionChart(data);
    createSpeciesDistributionChart(data.speciesDistribution);
    createHabitatChart(data.habitatDistribution);
    createConservationChart(data.conservationData);
}

/**
 * Populate filter dropdowns with data
 */
function populateFilterDropdowns(data) {
    // Populate region filter
    const regionFilter = document.getElementById('region-filter');
    if (regionFilter) {
        // Clear existing options except the "All Regions" option
        regionFilter.innerHTML = '<option value="all">All Regions</option>';

        // Add regions as options
        data.regions.forEach(region => {
            const option = document.createElement('option');
            option.value = region;
            option.textContent = region;
            regionFilter.appendChild(option);
        });
    }

    // Populate species filter
    const speciesFilter = document.getElementById('species-filter');
    if (speciesFilter) {
        // Clear existing options except the "All Species" option
        speciesFilter.innerHTML = '<option value="all">All Species</option>';

        // Add species as options
        data.species.forEach(species => {
            const option = document.createElement('option');
            option.value = species;
            option.textContent = species;
            speciesFilter.appendChild(option);
        });
    }
}

/**
 * Create the population trend chart
 */
function createPopulationTrendChart(data) {
    const chartElement = document.getElementById('population-trend-chart');
    if (!chartElement) return;

    const years = data.map(d => d.year);
    const populations = data.map(d => d.population);

    const trace = {
        x: years,
        y: populations,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Global Population',
        line: {
            color: '#4e937a',
            width: 3
        },
        marker: {
            color: '#4e937a',
            size: 8
        }
    };

    const layout = {
        title: 'Global Rabbit Population Trend (2000-2025)',
        xaxis: {
            title: 'Year',
            tickmode: 'linear',
            tick0: 2000,
            dtick: 5
        },
        yaxis: {
            title: 'Population',
            rangemode: 'tozero'
        },
        margin: { t: 50, b: 50, l: 70, r: 40 },
        hovermode: 'closest',
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)'
    };

    Plotly.newPlot(chartElement, [trace], layout, { responsive: true });
}

/**
 * Create the population by region chart
 */
function createPopulationByRegionChart(data) {
    const chartElement = document.getElementById('population-by-region-chart');
    if (!chartElement) return;

    // Process data to get population by region over time
    const regions = data.regions;
    const years = data.years;

    const traces = regions.map(region => {
        // For this demo, we'll just create some random data
        // In a real app, this would come from the actual data
        const populations = years.map(year => {
            const baseValue = Math.floor(Math.random() * 400000) + 100000;
            const trend = (year - 2000) * 10000;
            return baseValue + trend;
        });

        return {
            x: years,
            y: populations,
            type: 'scatter',
            mode: 'lines',
            name: region
        };
    });

    const layout = {
        title: 'Population by Region Over Time',
        xaxis: {
            title: 'Year',
            tickmode: 'linear',
            tick0: 2000,
            dtick: 5
        },
        yaxis: {
            title: 'Population'
        },
        margin: { t: 50, b: 50, l: 70, r: 40 },
        hovermode: 'closest',
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)'
    };

    Plotly.newPlot(chartElement, traces, layout, { responsive: true });
}

/**
 * Create the species distribution chart
 */
function createSpeciesDistributionChart(data) {
    const chartElement = document.getElementById('species-distribution-chart');
    if (!chartElement) return;

    const species = data.map(d => d.species);
    const populations = data.map(d => d.population);

    const trace = {
        x: species,
        y: populations,
        type: 'bar',
        marker: {
            color: [
                '#4e937a',
                '#78c2ad',
                '#f8a978',
                '#e74c3c',
                '#3498db'
            ]
        }
    };

    const layout = {
        title: 'Global Population by Species (2025)',
        xaxis: {
            title: 'Species'
        },
        yaxis: {
            title: 'Population'
        },
        margin: { t: 50, b: 100, l: 70, r: 40 },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)'
    };

    Plotly.newPlot(chartElement, [trace], layout, { responsive: true });
}

/**
 * Create the habitat chart
 */
function createHabitatChart(data) {
    const chartElement = document.getElementById('habitat-chart');
    if (!chartElement) return;

    const habitats = data.map(d => d.habitat);
    const populations = data.map(d => d.population);

    const trace = {
        labels: habitats,
        values: populations,
        type: 'pie',
        hole: 0.4,
        marker: {
            colors: [
                '#4e937a',
                '#78c2ad',
                '#f8a978',
                '#3498db'
            ]
        },
        textinfo: 'label+percent',
        insidetextorientation: 'radial'
    };

    const layout = {
        title: 'Population Distribution by Habitat (2025)',
        margin: { t: 50, b: 50, l: 50, r: 50 },
        showlegend: true,
        legend: {
            orientation: 'h',
            y: -0.2
        },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)'
    };

    Plotly.newPlot(chartElement, [trace], layout, { responsive: true });
}

/**
 * Create the conservation status chart
 */
function createConservationChart(data) {
    const chartElement = document.getElementById('conservation-chart');
    if (!chartElement) return;

    const years = data.map(d => d.year);

    const traces = [
        {
            x: years,
            y: data.map(d => d.leastConcern),
            name: 'Least Concern',
            type: 'scatter',
            mode: 'lines',
            stackgroup: 'one',
            fillcolor: '#2ecc71'
        },
        {
            x: years,
            y: data.map(d => d.nearThreatened),
            name: 'Near Threatened',
            type: 'scatter',
            mode: 'lines',
            stackgroup: 'one',
            fillcolor: '#f39c12'
        },
        {
            x: years,
            y: data.map(d => d.vulnerable),
            name: 'Vulnerable',
            type: 'scatter',
            mode: 'lines',
            stackgroup: 'one',
            fillcolor: '#f8a978'
        },
        {
            x: years,
            y: data.map(d => d.endangered),
            name: 'Endangered',
            type: 'scatter',
            mode: 'lines',
            stackgroup: 'one',
            fillcolor: '#e74c3c'
        }
    ];

    const layout = {
        title: 'Population by Conservation Status Over Time',
        xaxis: {
            title: 'Year',
            tickmode: 'linear',
            tick0: 2000,
            dtick: 5
        },
        yaxis: {
            title: 'Population'
        },
        margin: { t: 50, b: 50, l: 70, r: 40 },
        hovermode: 'closest',
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)'
    };

    Plotly.newPlot(chartElement, traces, layout, { responsive: true });
}

/**
 * Set up event listeners for filters
 */
function setupEventListeners() {
    // Region filter
    const regionFilter = document.getElementById('region-filter');
    if (regionFilter) {
        regionFilter.addEventListener('change', handleFilterChange);
    }

    // Species filter
    const speciesFilter = document.getElementById('species-filter');
    if (speciesFilter) {
        speciesFilter.addEventListener('change', handleFilterChange);
    }

    // For a real application, we would also handle the year range slider
}

/**
 * Handle filter changes
 */
function handleFilterChange() {
    // For demonstration purposes, we'll just show an alert
    // In a real application, this would re-fetch or filter the data
    console.log('Filter changed - would update charts in a real application');

    // Alternatively, we could just regenerate sample data
    const data = generateSampleData();
    updateDashboard(data);
}

/**
 * Set up smooth scrolling for navigation links
 */
function setupSmoothScrolling() {
    const navLinks = document.querySelectorAll('nav a');

    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                // Remove active class from all links
                navLinks.forEach(link => link.classList.remove('active'));

                // Add active class to the clicked link
                this.classList.add('active');

                // Smooth scroll to the target
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Highlight active section on scroll
    window.addEventListener('scroll', function () {
        const sections = document.querySelectorAll('section');
        const scrollPosition = window.scrollY + 100; // Add some offset

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;

            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                const targetLink = document.querySelector(`nav a[href="#${section.id}"]`);

                if (targetLink) {
                    // Remove active class from all links
                    navLinks.forEach(link => link.classList.remove('active'));

                    // Add active class to the corresponding link
                    targetLink.classList.add('active');
                }
            }
        });
    });
}

/**
 * Format a number with commas
 */
function formatNumber(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Show an error message on the dashboard
 */
function showErrorMessage(message) {
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.textContent = message;

    // Insert at the top of the main content
    const mainElement = document.querySelector('main');
    if (mainElement) {
        mainElement.insertBefore(errorElement, mainElement.firstChild);

        // Automatically remove after 5 seconds
        setTimeout(() => {
            errorElement.remove();
        }, 5000);
    }
}

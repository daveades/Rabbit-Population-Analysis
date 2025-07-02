"""
Unit tests for the visualization charts module
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.visualization.charts import filter_dataframe


class TestVisualizationCharts(unittest.TestCase):
    """Test cases for the visualization charts module"""
    
    def setUp(self):
        """Set up test data"""
        # Create sample data for testing
        self.sample_data = pd.DataFrame({
            'Year': [2020, 2021, 2022, 2020, 2021, 2022],
            'Region': ['North America', 'North America', 'North America', 'Europe', 'Europe', 'Europe'],
            'Species': ['European Rabbit', 'European Rabbit', 'European Rabbit', 'Hare', 'Hare', 'Hare'],
            'Population': [10000, 12000, 15000, 8000, 7500, 9000],
            'Habitat': ['Forest', 'Forest', 'Forest', 'Grassland', 'Grassland', 'Grassland'],
            'Conservation_Status': ['Least Concern', 'Least Concern', 'Least Concern', 'Near Threatened', 'Near Threatened', 'Near Threatened']
        })
    
    def test_filter_dataframe_regions(self):
        """Test filtering dataframe by regions"""
        # Filter by region
        result = filter_dataframe(self.sample_data, regions=['North America'])
        
        # Check that only North America data remains
        self.assertEqual(result['Region'].unique().tolist(), ['North America'])
        self.assertEqual(len(result), 3)
    
    def test_filter_dataframe_species(self):
        """Test filtering dataframe by species"""
        # Filter by species
        result = filter_dataframe(self.sample_data, species=['Hare'])
        
        # Check that only Hare data remains
        self.assertEqual(result['Species'].unique().tolist(), ['Hare'])
        self.assertEqual(len(result), 3)
    
    def test_filter_dataframe_year_range(self):
        """Test filtering dataframe by year range"""
        # Filter by year range
        result = filter_dataframe(self.sample_data, year_range=[2021, 2022])
        
        # Check that only data from 2021-2022 remains
        self.assertTrue(all(year >= 2021 and year <= 2022 for year in result['Year']))
        self.assertEqual(len(result), 4)
    
    def test_filter_dataframe_conservation_status(self):
        """Test filtering dataframe by conservation status"""
        # Filter by conservation status
        result = filter_dataframe(self.sample_data, conservation_statuses=['Near Threatened'])
        
        # Check that only Near Threatened data remains
        self.assertEqual(result['Conservation_Status'].unique().tolist(), ['Near Threatened'])
        self.assertEqual(len(result), 3)
    
    def test_filter_dataframe_multiple_filters(self):
        """Test filtering dataframe with multiple filters"""
        # Apply multiple filters
        result = filter_dataframe(
            self.sample_data,
            regions=['Europe'],
            species=['Hare'],
            year_range=[2021, 2022],
            conservation_statuses=['Near Threatened']
        )
        
        # Check that the filters were applied correctly
        self.assertEqual(len(result), 2)
        self.assertEqual(result['Region'].unique().tolist(), ['Europe'])
        self.assertEqual(result['Species'].unique().tolist(), ['Hare'])
        self.assertTrue(all(year >= 2021 and year <= 2022 for year in result['Year']))
        self.assertEqual(result['Conservation_Status'].unique().tolist(), ['Near Threatened'])


if __name__ == '__main__':
    unittest.main()

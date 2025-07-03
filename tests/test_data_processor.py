"""
Unit tests for the data processor module
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analysis.data_processor import load_data, preprocess_data, calculate_growth_rates


class TestDataProcessor(unittest.TestCase):
    """Test cases for the data processor module"""
    
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
    
    def test_calculate_growth_rates(self):
        """Test the calculate_growth_rates function"""
        # Apply the function
        result = calculate_growth_rates(self.sample_data)
        
        # Check that the result has the expected column
        self.assertIn('Growth_Rate', result.columns)
        
        # Check that the growth rates are calculated correctly
        # For European Rabbit: (12000 - 10000) / 10000 * 100 = 20%
        # For Hare: (7500 - 8000) / 8000 * 100 = -6.25%
        expected_growth_rates = [None, 20.0, 25.0, None, -6.25, 20.0]
        
        # Allow for small floating point differences
        for i, expected in enumerate(expected_growth_rates):
            if expected is None:
                self.assertTrue(pd.isna(result.iloc[i]['Growth_Rate']))
            else:
                self.assertAlmostEqual(result.iloc[i]['Growth_Rate'], expected, places=2)
    
    def test_preprocess_data(self):
        """Test the preprocess_data function"""
        # Apply the function
        result = preprocess_data(self.sample_data)
        
        # Check that the result has the expected shape
        self.assertEqual(result.shape[0], self.sample_data.shape[0])
        
        # Check that population values are numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(result['Population']))
        
        # Check that year values are integers
        self.assertTrue(pd.api.types.is_integer_dtype(result['Year']))


if __name__ == '__main__':
    unittest.main()

"""
Run all unit tests for the Global Rabbit Population Dashboard
"""

import unittest
import sys
import os

if __name__ == '__main__':
    # Discover and run all tests
    test_suite = unittest.defaultTestLoader.discover('tests', pattern='test_*.py')
    test_runner = unittest.TextTestRunner()
    result = test_runner.run(test_suite)
    
    # Exit with non-zero status if tests failed
    sys.exit(not result.wasSuccessful())

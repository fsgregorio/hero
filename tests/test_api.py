"""
Unit tests for the FastAPI endpoints.

This module contains tests for the API, using FastAPI's TestClient to simulate HTTP requests.
Assumes the API is running in a test environment with dummy data.
"""

import unittest
from fastapi.testclient import TestClient
from src.main import app

# Create the TestClient to simulate HTTP requests
client = TestClient(app)

class TestAPI(unittest.TestCase):
    """
    Test cases for the API endpoints.
    """
    
    def test_get_accounts_by_category_not_found(self):
        """
        Test fetching accounts by a non-existent category.
        The endpoint should return a 404 status code.
        """
        response = client.get("/accounts/category/nonexistent")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()

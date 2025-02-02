"""
Unit tests for the FastAPI endpoints.
Assumes that the API is running in a test environment with dummy data.
"""

import unittest
from src.api import app as api_app
from src.database import SessionLocal
from fastapi.testclient import TestClient
from src.main import app
from src.models import Base

# Cria o TestClient para simular requisições HTTP
client = TestClient(app)

class TestAPI(unittest.TestCase):

    def test_get_accounts_by_category_not_found(self):
        """Test fetching accounts by a non-existent category."""
        response = client.get("/accounts/category/nonexistent")
        #Nosso endpoint retorna 404 se a categoria não for encontrada
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()

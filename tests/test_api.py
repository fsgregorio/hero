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
    def test_get_accounts_by_category_success():
        """Test fetching accounts by an existing category."""
        response = client.get("/accounts/category/Investment")
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, dict)
        assert "category" in data
        assert data["category"] == "Investment"
        assert "accounts" in data
        assert isinstance(data["accounts"], list)

        # ✅ Garantir que a conta dummy foi retornada
        assert "dummy-account" in data["accounts"]
        
    # def test_get_accounts_by_category(self):
    #     """Test fetching accounts by category."""
    #     response = client.get("/accounts/category/Investment")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.json(), list)

    # def test_get_accounts_by_category_not_found(self):
    #     """Test fetching accounts by a non-existent category."""
    #     response = client.get("/accounts/category/nonexistent")
    #     Nosso endpoint retorna 404 se a categoria não for encontrada
    #     self.assertEqual(response.status_code, 404)

    # def test_get_large_accounts(setup_test_db):
    #     """Testa se apenas contas com mais de 1 milhão de inscritos são retornadas"""
    #     response = client.get("/accounts/million-plus")
    #     assert response.status_code == 200
        
    #     data = response.json()
    #     assert "accounts" in data
    #     assert len(data["accounts"]) == 1  # Apenas uma conta tem mais de 1 milhão
    #     assert data["accounts"][0] == "123456"  # Conta correta é retornada

    # def test_get_accounts_by_growth(self):
    #     """Test fetching accounts with growth above a threshold.
    #        Com os dados dummy, espera-se que a conta 'dummy-account' apresente crescimento acima de 10%.
    #     """
    #     response = client.get("/accounts/growth", params={"min_growth": 10.0})
    #     self.assertEqual(response.status_code, 200)
    #     data = response.json()
    #     self.assertIsInstance(data, dict)
    #     self.assertIn("high_growth_accounts", data)
    #     self.assertIsInstance(data["high_growth_accounts"], list)
    #     # Verifica se 'dummy-account' está entre as contas com alto crescimento
    #     account_ids = [acct["account_id"] for acct in data["high_growth_accounts"]]
    #     self.assertIn("dummy-account", account_ids)
    #     # Opcional: verifique que o percentual de crescimento é maior que 10%
    #     for acct in data["high_growth_accounts"]:
    #         self.assertGreater(acct["growth_percentage"], 10)

    # def test_upload_new_accounts(self):
    #     """Test the upload endpoint for ingesting new accounts.
    #        Esse teste assume que o endpoint POST /accounts/upload utiliza um caminho fixo ou não requer payload.
    #     """
    #     response = client.post("/accounts/upload")
    #     self.assertEqual(response.status_code, 200)
    #     data = response.json()
    #     # Verifica se a mensagem indica sucesso na ingestão
    #     self.assertIn("ingested successfully", data["message"].lower())

if __name__ == "__main__":
    unittest.main()

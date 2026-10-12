import os

from dotenv import load_dotenv
from fastapi.testclient import TestClient

load_dotenv()

from src.api.v1.app import app

client = TestClient(app)


def test_generate_transaction_endpoint_requires_header():
    response = client.post("/generate_transaction")
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_generate_transaction_endpoint_with_valid_header():
    response = client.post(
        "/generate_transaction",
        headers={"X-Client-Token": os.getenv("X_CLIENT_TOKEN", "mi-token-secreto-local")},
    )
    assert response.status_code == 200
    data = response.json()
    assert "transaction" in data
    transaction = data["transaction"]
    assert isinstance(transaction["transaction_id"], str)
    assert isinstance(transaction["user_id"], str)
    assert isinstance(transaction["merchant_id"], str)
    assert isinstance(transaction["amount"], float)
    assert transaction["status"] in ["pending", "completed", "failed", "refunded"]
    assert isinstance(transaction["timestamp"], str)


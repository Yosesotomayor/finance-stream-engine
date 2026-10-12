from fastapi.testclient import TestClient
from src.api.v1.app import app

client = TestClient(app)


def test_generate_transaction_endpoint():
    response = client.get("/generate_transaction")
    assert response.status_code == 200
    data = response.json()
    assert "transaction" in data
    transaction = data["transaction"]
    assert isinstance(transaction["transaction_id"], str)
    assert isinstance(transaction["user_id"], str)
    assert isinstance(transaction["merchant_id"], str)
    assert isinstance(transaction["amount"], float)
    assert transaction["status"] in ["pending", "completed", "failed", "refunded"]
    assert isinstance(transaction["timestamp"], str)  # timestamp is returned as a string in JSON


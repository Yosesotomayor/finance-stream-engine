from dotenv import load_dotenv, find_dotenv

from fastapi.testclient import TestClient

from unittest.mock import patch

from src.api.v1.app import app
from src.database.connection import get_db

import os
load_dotenv(find_dotenv())

X_CLIENT_TOKEN = os.environ["X_CLIENT_TOKEN"]

client = TestClient(app)

def test_generate_transaction_endpoint_requires_header():
    test_payload = {
        "transaction_id": "test_transaction_id",
        "user_id": "1001",
        "merchant_id": "1002",
        "amount": 100.0,
        "status": "pending",
        "timestamp": "2024-06-01T12:00:00Z"
    }
    response = client.post("/generate_transaction", json=test_payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


@patch("src.api.v1.routes.transactions.producer")
def test_create_transaction_success(mock_producer):
    test_payload = {
        "transaction_id": "test_transaction_id",
        "user_id": "1001",
        "merchant_id": "1002",
        "amount": 100.0,
        "status": "pending",
        "timestamp": "2024-06-01T12:00:00Z"
    }

    response = client.post(
        "/generate_transaction",
        json=test_payload,
        headers={"X-Client-Token": X_CLIENT_TOKEN}
    )

    assert response.status_code == 202
    assert response.json().get("message") == "Transaction event published to stream successfully"
    assert response.json().get("status") == "accepted"

    mock_producer.produce.assert_called_once()

def test_create_transaction_invalid_payload():
    bad_payload = {
        "transaction_id": "abc-123",
        "amount": "no_soy_un_numero" 
    }

    response = client.post("/generate_transaction", json=bad_payload, headers={"X-Client-Token": X_CLIENT_TOKEN})
    assert response.status_code == 422
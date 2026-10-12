import os

from dotenv import load_dotenv, find_dotenv
from fastapi.testclient import TestClient

load_dotenv(find_dotenv())

from src.api.v1.app import app
from src.database.connection import get_db

client = TestClient(app)

def test_generate_transaction_endpoint_requires_header():
    response = client.post("/generate_transaction")
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_generate_transaction_endpoint_with_valid_header(db_session):
    app.dependency_overrides[get_db] = lambda: db_session

    response = client.post(
        "/generate_transaction",
        headers={"X-Client-Token": os.environ["X_CLIENT_TOKEN"]},
    )

    try:   
        response = client.post(
            "/generate_transaction",
            headers={"X-Client-Token": os.environ["X_CLIENT_TOKEN"]},
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

        from src.models.db_models import TransactionDBModel
        saved_item = db_session.query(TransactionDBModel).filter_by(transaction_id=transaction["transaction_id"]).first()
        assert saved_item is not None
        assert saved_item.amount == transaction["amount"]

    finally:
        app.dependency_overrides.clear()
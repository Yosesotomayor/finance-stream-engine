from datetime import datetime
from src.models.db_models import TransactionDBModel

def test_save_and_retrieve_transaction(db_session):
    # We use the 'db_session' fixture directly as an argument
    test_transaction_id = "test-uuid-1234"
    test_user_id = "1001"
    test_merchant_id = "1002"
    test_amount = 50.75
    test_status = "completed"
    test_timestamp = datetime.now()

    db_item = TransactionDBModel(
        transaction_id=test_transaction_id,
        user_id=test_user_id,
        merchant_id=test_merchant_id,
        amount=test_amount,
        status=test_status,
        timestamp=test_timestamp
    )

    db_session.add(db_item)
    db_session.commit()

    # Retrieve the item from the database
    retrieved_item = db_session.query(TransactionDBModel).filter_by(transaction_id=test_transaction_id).first()

    assert retrieved_item is not None
    assert retrieved_item.transaction_id == test_transaction_id
    assert retrieved_item.user_id == test_user_id
    assert retrieved_item.merchant_id == test_merchant_id
    assert retrieved_item.amount == test_amount
    assert retrieved_item.status == test_status
    assert retrieved_item.timestamp == test_timestamp
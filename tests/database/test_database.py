from datetime import datetime
from src.database.connection import get_session
from src.models.db_models import TransactionDBModel
from src.models.transaction_event import TransactionEvent

def test_save_and_retrieve_transaction():
      test_transaction_id = "test-uuid-1234"
      test_user_id = 1001
      test_merchant_id = 1002
      test_amount = 50.75
      test_status = "completed"
      test_timestamp = datetime.now()

      session = get_session()
      try:
            db_item = TransactionDBModel(
            transaction_id=test_transaction_id,
            user_id=str(test_user_id),
            merchant_id=str(test_merchant_id),
            amount=test_amount,
            status=test_status,
            timestamp=test_timestamp
            )

            session.add(db_item)
            session.commit()

            retrieved_item = session.query(TransactionDBModel).filter_by(transaction_id=test_transaction_id).first()

            assert retrieved_item is not None
            assert retrieved_item.transaction_id == test_transaction_id
            assert retrieved_item.user_id == str(test_user_id)
            assert retrieved_item.merchant_id == str(test_merchant_id)
            assert retrieved_item.amount == test_amount
            assert retrieved_item.status == test_status
            assert retrieved_item.timestamp == test_timestamp

            session.delete(retrieved_item)
            session.commit()

      except Exception as e:
          raise RuntimeError(f"Error during test_save_and_retrieve_transaction: {e}")

      finally:
          session.close()
from datetime import datetime
from src.generator.generator import TransactionGenerator
import logging
logger = logging.getLogger(__name__)

generator = TransactionGenerator()

def test_generate_transaction():
      transaction = generator.generate_transaction()
      logger.info(f"Generated transaction: {transaction!r}")

      assert isinstance(transaction.transaction_id, str)
      assert isinstance(transaction.user_id, str)
      assert isinstance(transaction.merchant_id, str)
      assert isinstance(transaction.amount, float)
      assert transaction.status in ["pending", "completed", "failed", "refunded"]
      assert isinstance(transaction.timestamp, datetime)
      assert (transaction.timestamp >= datetime(2026, 1, 1) and transaction.timestamp <= datetime.now())

      assert transaction.transaction_id != ""
      assert transaction.user_id != ""
      assert transaction.merchant_id != ""
      assert transaction.amount > 0.0

      # make sure is uuid4
      assert transaction.transaction_id.count("-") == 4
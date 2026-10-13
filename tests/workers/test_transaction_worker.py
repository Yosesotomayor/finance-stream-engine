import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError, OperationalError

from src.workers.transaction_worker import process_transaction, PoisonPillError

@patch("src.workers.transaction_worker.get_session")
def test_process_transaction_success(mock_get_session):
      mock_msg = MagicMock()
      mock_msg.value.return_value = b'{"transaction_id": "asd123-12s3-12b3-123a", "user_id": "1001", "merchant_id": "1002", "amount": 100.0, "status": "pending", "timestamp": "2026-10-13T12:00:00"}'

      process_transaction(mock_msg)
      mock_get_session.assert_called_once()

@patch("src.workers.transaction_worker.get_session")
def test_process_transaction_duplicate(mock_get_session):
      mock_session = mock_get_session.return_value.__enter__.return_value
      mock_session.commit.side_effect = IntegrityError("Unique violaton UUID dupe", None, None)

      mock_msg = MagicMock()
      mock_msg.value.return_value = b'{"transaction_id": "asd123-12s3-12b3-123a", "user_id": "1001", "merchant_id": "1002", "amount": 100.0, "status": "pending", "timestamp": "2026-10-13T12:00:00"}'

      process_transaction(mock_msg)

def test_process_transaction_poison_pill():
    mock_msg = MagicMock()
    mock_msg.value.return_value = b'{ "esto_es_un_json_roto": '

    with pytest.raises(PoisonPillError):
        process_transaction(mock_msg)

@patch("src.workers.transaction_worker.get_session")
def test_process_transaction_transient_error(mock_get_session):
      mock_session = mock_get_session.return_value.__enter__.return_value
      mock_session.commit.side_effect = OperationalError("Transient error DB DOWN", None, None)

      mock_msg = MagicMock()
      mock_msg.value.return_value = b'{"transaction_id": "asd123-12s3-12b3-123a", "user_id": "1001", "merchant_id": "1002", "amount": 100.0, "status": "pending", "timestamp": "2026-10-13T12:00:00"}'

      with pytest.raises(OperationalError):
          process_transaction(mock_msg)

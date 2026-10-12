from pydantic import BaseModel
from datetime import datetime

class TransactionEvent(BaseModel):
      transaction_id: str
      user_id: str
      merchant_id: str
      amount: float
      status: str
      timestamp: datetime
from sqlalchemy import Column, DateTime, Float, String

from src.database.base import Base


class TransactionDBModel(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    merchant_id = Column(String, index=True)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
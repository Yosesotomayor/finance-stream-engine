import os

from dotenv import find_dotenv, load_dotenv
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from src.generator.generator import TransactionGenerator

from src.database.connection import get_db          
from src.models.db_models import TransactionDBModel 

import logging

logger = logging.getLogger(__name__)
load_dotenv(find_dotenv())

router = APIRouter()
CLIENT_TOKEN = os.environ["X_CLIENT_TOKEN"]


@router.post("/generate_transaction", tags=["Transactions"])
async def generate_transaction(
    x_client_token: str | None = Header(default=None, alias="X-Client-Token"),
    db: Session = Depends(get_db)
):
      if not x_client_token or x_client_token != CLIENT_TOKEN:
            raise HTTPException(
                  status_code=status.HTTP_401_UNAUTHORIZED,
                  detail="Unauthorized",
            )

      transaction = TransactionGenerator().generate_transaction()

      db_item = TransactionDBModel(
            transaction_id=transaction.transaction_id,
            user_id=transaction.user_id,
            merchant_id=transaction.merchant_id,
            amount=transaction.amount,
            status=transaction.status,
            timestamp=transaction.timestamp,
      )
      
      try:
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
      except Exception as e:
            db.rollback()
            raise HTTPException(
                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                  detail=f"Error saving transaction to the database: {e}",
            )

      logger.info(f"Transaction {transaction.transaction_id} generated and saved to the database.")

      return {"transaction": transaction.model_dump()}

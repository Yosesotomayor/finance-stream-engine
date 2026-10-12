from dotenv import load_dotenv
load_dotenv()

import os

from dotenv import find_dotenv, load_dotenv
from fastapi import APIRouter, Header, HTTPException, status

from src.generator.generator import TransactionGenerator

load_dotenv(find_dotenv())

router = APIRouter()
CLIENT_TOKEN = os.environ["X_CLIENT_TOKEN"]


@router.post("/generate_transaction", tags=["Transactions"])
async def generate_transaction(
    x_client_token: str | None = Header(default=None, alias="X-Client-Token"),
):
    if not x_client_token or x_client_token != CLIENT_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    transaction = TransactionGenerator().generate_transaction()
    return {"transaction": transaction.model_dump()}

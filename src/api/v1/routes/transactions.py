from fastapi import APIRouter

from src.generator.generator import TransactionGenerator

router = APIRouter()
transaction_generator = TransactionGenerator()

@router.get("/generate_transaction")
async def generate_transaction():
    transaction = transaction_generator.generate_transaction()
    return {"transaction": transaction.model_dump()}
from fastapi import FastAPI

from .routes.health import router as health_router
from .routes.transactions import router as transactions_router

app = FastAPI(
    title="Transaction Generator API",
    description="An API for generating random financial transactions.",
    version="1.0.0",
)

@app.get("/")
def run_root():
    return {"message": "Welcome to the Transaction Generator API!"}

app.include_router(health_router)
app.include_router(transactions_router)
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def run_health():
    return {"status": "ok"}
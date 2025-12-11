# backend/app/api/v1/ai.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def ai_test():
    return {"message": "AI 接口就绪"}
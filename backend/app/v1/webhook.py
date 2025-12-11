# backend/app/api/v1/webhook.py
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/log")
async def receive_log(request: Request):
    data = await request.json()
    return {"status": "received", "data": data}
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/log")
async def webhook_log(request: Request):
    data = await request.json()
    return {"status": "ok", "received": data}
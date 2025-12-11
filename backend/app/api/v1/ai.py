from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def ai_test():
    return {"message": "AI 分析模块已就绪"}
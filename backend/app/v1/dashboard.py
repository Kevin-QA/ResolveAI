# backend/app/api/v1/dashboard.py
from fastapi import APIRouter
from app.database import prisma

router = APIRouter()

@router.get("/")
async def get_dashboard():
    total = await prisma.ticket.count()
    critical = await prisma.ticket.count(where={"severity": "CRITICAL"})
    return {
        "total_tickets": total,
        "critical_count": critical,
        "message": "仪表盘数据（后续可加图表）"
    }
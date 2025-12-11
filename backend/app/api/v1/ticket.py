from fastapi import APIRouter
from app.database import prisma

router = APIRouter()

@router.get("/")
async def get_tickets():
    tickets = await prisma.ticket.find_many(order_by={"createdAt": "desc"})
    return {"tickets": tickets}
# backend/app/services/ticket_service.py
from app.database import prisma

async def create_ticket_from_ai(log: str, ai_result: dict):
    parsed = ai_result["parsed"]
    return await prisma.ticket.create({
        "title": f"【{parsed['severity']}】{parsed['summary']}",
        "content": log,
        "aiAnalysis": parsed["solution_suggestion"],
        "aiRawOutput": ai_result,
        "severity": parsed["severity"],
        "category": parsed["category"],
        "assignee": parsed["suggested_assignee"],
        "status": "ASSIGNED"
    })
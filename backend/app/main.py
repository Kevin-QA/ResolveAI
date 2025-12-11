# backend/app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 加载 .env（虽然你已经用 $env 设了，但保险起见再加载一次）
load_dotenv(override=True)

# 导入 prisma 客户端
from app.database import prisma

# 导入你的服务
from app.services.ai_service import analyze_log_with_openrouter
from app.services.ticket_service import create_ticket_from_ai

async def lifespan(app: FastAPI):
    # 启动时连接数据库
    await prisma.connect()
    print("数据库连接成功！")

    # 启动时自动创建一条演示工单（只创建一次）
    try:
        count = await prisma.ticket.count()
        if count == 0:
            print("正在用 AI 分析演示日志并创建工单...")
            demo_log = """
2025-12-11 08:23:11 kernel: Out of memory: Kill process 12345 (java) score 965 or sacrifice child
2025-12-11 08:23:11 kernel: Killed process 12345 (java) total-vm:1585392kB, anon-rss:1285392kB
2025-12-11 08:23:12 prometheus-alertmanager: [CRITICAL] Memory usage > 95% for 10m
"""
            ai_result = await analyze_log_with_openrouter(demo_log)
            await create_ticket_from_ai(demo_log, ai_result)
            print("演示工单创建成功！")
    except Exception as e:
        print(f"创建演示工单失败：{e}")

    yield  # 程序运行期间保持连接

    # 关闭时断开
    await prisma.disconnect()
    print("数据库已断开")

# 关键！这一行必须叫 app！
app = FastAPI(
    title="ResolveAI - AI智能服务器故障派单系统",
    description="接入服务器日志 → AI分析 → 自动派单",
    version="1.0.0",
    lifespan=lifespan
)

# 允许前端跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由（你已经建好这四个文件了）
from app.api.v1 import dashboard, ticket, ai, webhook

app.include_router(dashboard.router, prefix="/api/v1/dashboard")
app.include_router(ticket.router,    prefix="/api/v1/tickets")
app.include_router(ai.router,        prefix="/api/v1/ai")
app.include_router(webhook.router,   prefix="/api/v1/webhook")

@app.get("/")
async def root():
    return {"message": "ResolveAI 后端已启动！访问 /docs 查看接口文档"}
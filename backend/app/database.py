# backend/app/database.py
# 最终定版，100% 兼容你现在的环境

from prisma import Prisma

prisma = Prisma()

async def init_db():
    """启动时连接数据库"""
    await prisma.connect()

async def close_db():
    """关闭时断开数据库"""
    await prisma.disconnect()
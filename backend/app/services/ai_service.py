# backend/app/services/ai_service.py
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()


async def analyze_log_with_openrouter(log: str) -> dict:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "ResolveAI",
    }

    prompt = f"""
你是一个专业的 Linux 运维专家，请分析以下服务器日志，严格按照 JSON 格式输出：

{log}

请输出以下字段（只输出纯 JSON，不要多余文字）：
{{
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "category": "CPU|Memory|Disk|Network|Service|Other",
  "summary": "一句话总结问题",
  "suggested_assignee": "张工|李工|王工|硬件组",
  "solution_suggestion": "推荐处理步骤"
}}
"""

    payload = {
        "model": "nvidia/nemotron-nano-12b-v2-vl:free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 500
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            raw = response.json()["choices"][0]["message"]["content"]

            # 提取 JSON
            start = raw.find("{")
            end = raw.rfind("}") + 1
            json_str = raw[start:end]
            parsed = json.loads(json_str)
            return {"raw": raw, "parsed": parsed}
        except Exception as e:
            return {"raw": str(e), "parsed": {
                "severity": "HIGH",
                "category": "Other",
                "summary": "AI 分析失败，请人工查看",
                "suggested_assignee": "李工",
                "solution_suggestion": "请检查网络或 API Key"
            }}
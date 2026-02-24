# -*- coding: utf-8 -*-
"""
服务层：FastAPI 应用与 SSE 流式接口。

职责：创建应用、注册路由、将流程层的流式结果格式化为 SSE 响应。
"""

from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from app.flow import run_stream


# -----------------------------------------------------------------------------
# SSE 格式化
# -----------------------------------------------------------------------------


def format_sse(data: str) -> str:
    """将一条内容格式化为 SSE 消息。"""
    return f"data: {data}\n\n"


# -----------------------------------------------------------------------------
# 流式响应生成（流程 + SSE 格式）
# -----------------------------------------------------------------------------


async def stream_response(user_input: str) -> AsyncGenerator[str, None]:
    """
    调用流程层 run_stream，将图输出的 stream_log 与最终结果转为 SSE 逐条 yield。
    """
    node_output: dict = {}
    async for chunk in run_stream(user_input):
        node_output = chunk.get("llm_node", {})
        stream_log = node_output.get("stream_log") or []
        if stream_log:
            yield format_sse(stream_log[-1])

    final_result = node_output.get("llm_response", "无结果")
    yield format_sse(f"最终结果：{final_result}")


# -----------------------------------------------------------------------------
# FastAPI 应用
# -----------------------------------------------------------------------------


def create_app() -> FastAPI:
    """创建 FastAPI 应用。"""
    return FastAPI(title="LangGraph + LLM + 流式输出 Demo")


def register_routes(app: FastAPI) -> None:
    """注册流式聊天路由。"""

    @app.get("/chat")
    async def chat(user_input: str):
        """
        流式聊天接口：GET /chat?user_input=你的问题
        返回 text/event-stream（SSE）。
        """
        if not user_input or not user_input.strip():
            raise HTTPException(status_code=400, detail="user_input 不能为空")

        return StreamingResponse(
            stream_response(user_input.strip()),
            media_type="text/event-stream",
        )

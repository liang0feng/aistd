# -*- coding: utf-8 -*-
"""
LangGraph + FastAPI + LLM 流式输出最小 Demo

功能：大模型节点 + LangGraph 流式编排 + FastAPI 对外提供 SSE 流式聊天接口。
企业级「AI 流式接口」的最小闭环，可基于此扩展为完整智能问答服务。
"""

import os
from typing import TypedDict, AsyncGenerator
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

# 加载 .env 中的环境变量（OPENAI_API_KEY、OPENAI_BASE_URL 等）
load_dotenv()

# ======================
# 1. 定义 State（极简版）
# ======================
# 所有节点只读当前 State，通过返回值「补丁」更新，不直接修改原 State，无线程安全问题。


class State(TypedDict):
    """图的状态：节点间通过 State 传递数据。"""

    user_input: str  # 用户输入的问题
    llm_response: str  # 大模型完整回复（拼接流式结果）
    stream_log: list[str]  # 流式输出日志，用于 SSE 逐段返回


# ======================
# 2. 大模型 Node（核心）
# ======================
# 使用 OpenAI 兼容接口，可替换为 DeepSeek/智谱等（改 base_url 或换 ChatZhipuAI 等）


llm = ChatOpenAI(
    model="deepseek-r1",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    streaming=True,  # 开启大模型原生流式输出
)


def llm_node(state: State) -> dict:
    """
    大模型节点：调用 LLM，将流式结果拼接到 State，并记录 stream_log。

    仅返回需要更新的字段（State 补丁），不修改原 state。
    """
    # 1. 调用大模型（流式），每收到一段 content 就迭代一次
    response = llm.stream(f"请简洁回答：{state['user_input']}")

    # 2. 拼接流式结果并记录到 stream_log（便于 SSE 逐段推给前端）
    full_response = ""
    stream_log = state["stream_log"].copy()
    for chunk in response:
        content = chunk.content
        if content:
            full_response += content
            stream_log.append(f"LLM 流式输出：{content}")

    # 3. 返回 State 补丁（只更新这两项，其它键保持不变）
    return {
        "llm_response": full_response,
        "stream_log": stream_log,
    }


# ======================
# 3. 构建 LangGraph 图
# ======================
# 单节点图：入口 -> llm_node -> END。可在此扩展多节点、条件边、工具调用等。


builder = StateGraph(State)
builder.add_node("llm_node", llm_node)
builder.set_entry_point("llm_node")
builder.add_edge("llm_node", END)

# 编译图（支持流式调用 graph.astream）
graph = builder.compile()


# ======================
# 4. FastAPI 服务（对外提供流式接口）
# ======================

app = FastAPI(title="LangGraph + LLM + 流式输出 Demo")


async def stream_response(user_input: str) -> AsyncGenerator[str, None]:
    """
    生成流式响应的核心函数：用 graph.astream 跑图，按 SSE 格式逐条 yield。
    """
    initial_state: State = {
        "user_input": user_input,
        "llm_response": "",
        "stream_log": [],
    }
    node_output: dict = {}  # 避免循环后未定义

    # 流式执行 LangGraph（异步迭代每步状态更新）
    async for chunk in graph.astream(initial_state):
        node_output = chunk.get("llm_node", {})
        if node_output.get("stream_log"):
            # 只推送最新一条流式日志（逐段返回给前端）
            latest_log = node_output["stream_log"][-1]
            yield f"data: {latest_log}\n\n"

    # 最后返回最终完整结果
    final_result = node_output.get("llm_response", "无结果")
    yield f"data: 最终结果：{final_result}\n\n"


@app.get("/chat")
async def chat(user_input: str):
    """
    对外的流式聊天接口：GET /chat?user_input=你的问题

    返回 text/event-stream（SSE），浏览器或 curl 可逐行接收。
    """
    if not user_input:
        raise HTTPException(status_code=400, detail="user_input 不能为空")

    return StreamingResponse(
        stream_response(user_input),
        media_type="text/event-stream",
    )


# ======================
# 5. 运行服务
# ======================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

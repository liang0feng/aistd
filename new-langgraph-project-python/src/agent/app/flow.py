# -*- coding: utf-8 -*-
"""
流程层：LangGraph 图与节点定义。

职责：State、LLM 节点、图的构建与流式执行，不涉及 HTTP/SSE。
"""

import os
from typing import TypedDict, AsyncGenerator
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI


# -----------------------------------------------------------------------------
# State
# -----------------------------------------------------------------------------


class State(TypedDict):
    """图的状态：节点间通过 State 传递数据，仅通过返回值补丁更新。"""

    user_input: str
    llm_response: str
    stream_log: list[str]


def make_initial_state(user_input: str) -> State:
    """根据用户输入构造初始状态。"""
    return {
        "user_input": user_input,
        "llm_response": "",
        "stream_log": [],
    }


# -----------------------------------------------------------------------------
# LLM 与节点
# -----------------------------------------------------------------------------


def _create_llm() -> ChatOpenAI:
    """创建流式 LLM（OpenAI 兼容）。"""
    return ChatOpenAI(
        model="deepseek-r1",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        streaming=True,
    )


_llm = _create_llm()


def llm_node(state: State) -> dict:
    """
    大模型节点：流式调用 LLM，拼接结果并记录 stream_log。
    仅返回需要更新的字段（State 补丁）。
    """
    response = _llm.stream(f"{state.get('user_input', '')}")

    full_response = ""
    stream_log = list(state.get("stream_log", []))
    for chunk in response:
        content = chunk.content
        if content:
            full_response += content
            stream_log.append(f"LLM 流式输出：{content}")

    return {
        "llm_response": full_response,
        "stream_log": stream_log,
    }


# -----------------------------------------------------------------------------
# 图构建与流式执行
# -----------------------------------------------------------------------------


def build_graph():
    """构建并编译图：入口 -> llm_node -> END。"""
    builder = StateGraph(State)
    builder.add_node("llm_node", llm_node)
    builder.set_entry_point("llm_node")
    builder.add_edge("llm_node", END)
    return builder.compile()


# 单例图
graph = build_graph()


async def run_stream(user_input: str) -> AsyncGenerator[dict, None]:
    """
    流式执行图，按节点产出 chunk。
    每步 yield 当前步的 chunk（如 {"llm_node": {...}}），由调用方转成 SSE 等。
    """
    initial = make_initial_state(user_input)
    async for chunk in graph.astream(initial):
        yield chunk

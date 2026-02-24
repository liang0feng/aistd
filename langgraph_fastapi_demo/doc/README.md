# LangGraph + FastAPI 流式 Demo

## 目录结构

```
langgraph_fastapi_demo/
├── doc/                        # 文档目录
│   ├── README.md               # 本说明
│   └── Python开发环境与插件说明.md
├── src/                        # 源码目录
│   ├── app/                    # 重构后的应用包
│   │   ├── __init__.py
│   │   ├── flow.py             # 流程层：State、图、LLM 节点、run_stream
│   │   └── service.py          # 服务层：FastAPI、SSE、/chat 路由
│   ├── run_demo.py             # 入口：装配并启动服务
│   └── langgraph_fastapi_demo.py  # 原单文件（未修改）
├── run_demo.py                 # 根目录启动器（推荐）
├── .env                        # 环境变量（OPENAI_API_KEY、OPENAI_BASE_URL）
└── README.md                   # 项目简介与入口
```

## 运行方式

- **推荐**：在项目根目录执行 `python run_demo.py`
- **原单文件**：`python src/langgraph_fastapi_demo.py` 或先 `cd src` 再 `python langgraph_fastapi_demo.py`
- **从 src 直接运行重构版**：`cd src` 后 `python run_demo.py`

均提供 `GET /chat?user_input=你的问题` 的 SSE 流式接口。

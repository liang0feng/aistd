# LangGraph + FastAPI 流式 Demo

LangGraph + LLM 流式编排，FastAPI 提供 SSE 流式聊天接口。

## 目录结构

| 目录/文件 | 说明 |
|-----------|------|
| **doc/** | 文档目录：项目说明、开发环境与插件说明等 |
| **src/** | 源码目录：`app` 包、单文件 demo、入口脚本 |
| **run_demo.py** | 根目录启动器（推荐直接运行） |
| **.env** | 环境变量（OPENAI_API_KEY、OPENAI_BASE_URL） |

## 运行方式

在项目根目录执行：

```bash
python run_demo.py
```

或进入源码目录运行：`cd src && python run_demo.py`；原单文件：`python src/langgraph_fastapi_demo.py`。

接口：`GET /chat?user_input=你的问题`，返回 SSE 流式响应。

## 文档

- [doc/README.md](doc/README.md) — 目录说明与运行方式
- [doc/Python开发环境与插件说明.md](doc/Python开发环境与插件说明.md) — 开发环境与插件

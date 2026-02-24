# -*- coding: utf-8 -*-
"""
Demo 入口：组装流程层与服务层，启动流式聊天服务。

目录结构：见项目根目录 doc/README.md，源码在 src/ 下。
"""

from pathlib import Path

from dotenv import load_dotenv

# 先加载 .env，再导入 app（app.flow 在导入时会创建 LLM，需要 OPENAI_API_KEY 等）
_root = Path(__file__).resolve().parent.parent
load_dotenv(_root / ".env")

from app import create_app, register_routes

# 装配：创建应用并注册路由
app = create_app()
register_routes(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

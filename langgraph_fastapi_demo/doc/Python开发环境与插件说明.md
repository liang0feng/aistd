# Python 开发环境与插件说明

本文档说明本项目推荐的 Cursor / VS Code Python 插件、安装方式及用途示例。

---

## 一、插件安装

### 方式一：工作区推荐安装（推荐）

1. 用 Cursor 打开本目录 `langgraph_fastapi_demo`。
2. 若右下角弹出「此工作区有扩展建议」，点击 **安装全部** 即可一键安装下列推荐插件。

### 方式二：扩展面板手动安装

1. 按 `Ctrl+Shift+X` 打开「扩展」面板。
2. 在搜索框中输入下表「扩展 ID」，找到对应扩展后点击 **安装**。

### 方式三：命令行安装

在终端中执行（需已安装 `code` 或 `cursor` 命令行）：

```bash
# 进入项目目录后执行
cursor --install-extension ms-python.python
cursor --install-extension ms-python.vscode-pylance
cursor --install-extension ms-python.debugpy
cursor --install-extension ms-python.black-formatter
cursor --install-extension ms-python.flake8
cursor --install-extension littlefoxteam.vscode-python-test-adapter
cursor --install-extension njpwerner.autodocstring
cursor --install-extension kevinrose.vsc-python-indent
```

### 选对 Python 解释器（代码提示必备）

安装插件后若仍无代码提示，请指定本项目的虚拟环境：

1. `Ctrl+Shift+P` → 输入 **Python: Select Interpreter**。
2. 选择带 `langgraph_fastapi_demo\.venv` 的项（如 `.\langgraph_fastapi_demo\.venv\Scripts\python.exe`）。

---

## 二、推荐插件列表与用途

| 序号 | 扩展名称 | 扩展 ID | 用途简述 |
|------|----------|---------|----------|
| 1 | Python | ms-python.python | 运行、调试、测试、虚拟环境管理 |
| 2 | Pylance | ms-python.vscode-pylance | 智能补全、类型检查、跳转定义、查找引用 |
| 3 | Debugpy | ms-python.debugpy | 断点调试、变量查看、调用栈 |
| 4 | Black Formatter | ms-python.black-formatter | 按 Black 规范自动格式化代码 |
| 5 | Flake8 | ms-python.flake8 | 代码风格与简单错误检查 |
| 6 | Python Test Adapter | littlefoxteam.vscode-python-test-adapter | 侧边栏运行 pytest/unittest |
| 7 | autoDocstring | njpwerner.autodocstring | 自动生成函数/类文档字符串 |
| 8 | Python Indent | kevinrose.vsc-python-indent | 按 PEP8 自动缩进 |

---

## 三、各插件用途与使用示例

### 1. Python（ms-python.python）

- **用途**：提供运行、调试、测试、虚拟环境选择等核心能力。
- **示例**：
  - 在 `src/langgraph_fastapi_demo.py` 或 `src/run_demo.py` 中右键 → **在终端中运行 Python 文件**，直接运行当前脚本。
  - 按 **F5** 启动调试，配合断点查看程序执行流程。
  - 底部状态栏点击「Python x.x.x」切换解释器（选 `.venv` 以使用项目依赖）。

---

### 2. Pylance（ms-python.vscode-pylance）

- **用途**：智能补全、类型信息、跳转定义、查找引用、类型检查。
- **示例**：
  - 输入 `StateGraph` 时自动补全并显示来自 `langgraph.graph` 的说明。
  - **Ctrl+点击** `StateGraph`、`FastAPI` 等跳转到库源码或类型定义。
  - 鼠标悬停到变量/函数上查看类型与文档；对未定义变量、类型错误等会有波浪线提示。

---

### 3. Debugpy（ms-python.debugpy）

- **用途**：断点、单步、变量监视、调用栈，用于排查逻辑与数据问题。
- **示例**：
  - 在 `llm_response += chunk` 或 `yield f"data: {line}\n\n"` 行左侧点击设断点，**F5** 调试，请求流式接口触发断点。
  - 在「变量」面板查看 `state`、`chunk` 等；在「监视」里输入表达式如 `len(llm_response)` 实时查看。

---

### 4. Black Formatter（ms-python.black-formatter）

- **用途**：按 Black 规范统一代码格式（缩进、引号、换行等）。
- **示例**：
  - 保存时若已开启「保存时格式化」，会自动用 Black 格式化当前文件。
  - 或右键编辑器 → **使用 Black 格式化文档** 手动格式化。

---

### 5. Flake8（ms-python.flake8）

- **用途**：静态检查未使用变量、行过长、命名规范等。
- **示例**：
  - 未使用的 `import` 或变量会显示波浪线；在「问题」面板（Ctrl+Shift+M）中点击可跳转到对应行修改。

---

### 6. Python Test Adapter（littlefoxteam.vscode-python-test-adapter）

- **用途**：在侧边栏发现并运行 pytest/unittest 测试。
- **示例**：
  - 项目中有 `test_*.py` 或 `*_test.py` 时，侧边栏出现测试树，可运行单个用例或整个文件，查看通过/失败结果。

---

### 7. autoDocstring（njpwerner.autodocstring）

- **用途**：根据函数/类签名自动生成文档字符串模板。
- **示例**：
  - 在 `def stream_chat(...):` 下一行输入 `"""` 并回车，自动生成 Google/NumPy 等风格的参数、返回值说明模板，再按需填写描述。

---

### 8. Python Indent（kevinrose.vsc-python-indent）

- **用途**：按 PEP8 在 `if`/`for`/`def` 等后自动缩进，减少手工对齐。
- **示例**：
  - 在 `if user_input:` 后回车，下一行自动缩进到正确层级；多行括号内换行时也会保持合理缩进。

---

## 四、与代码提示相关的配置说明

- **代码提示** 依赖：**Python** + **Pylance**，且解释器需选为本项目的 `.venv`。
- 工作区已通过 `.vscode/settings.json`（若存在）或上层目录的 `.vscode/settings.json` 指定 `python.defaultInterpreterPath` 为 `langgraph_fastapi_demo/.venv`，首次打开时按上文「选对 Python 解释器」确认一次即可。

---

## 五、参考

- 推荐列表来源：本目录下 `.vscode/extensions.json` 中的 `recommendations`。
- 若需调整格式化或检查规则，可在工作区或用户 `settings.json` 中配置 `python.formatting.*`、`flake8.*` 等。

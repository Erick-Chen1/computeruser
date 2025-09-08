# computeruser

一个让 AI 以类似人类方式控制电脑的最小化模块化框架。

## 架构

该项目采用六步循环：

1. **交互** — 校验用户输入的自然语言指令。
2. **感知** — 截取真实屏幕，并通过 OmniParser 生成轻量级 UI 树。
3. **决策** — 调用 OpenAI LLM 将指令转换为结构化动作 JSON。
4. **执行** — 使用 `pyautogui` 将动作 JSON 转成鼠标/键盘操作。
5. **验证** — 使用 OpenAI VLM 比较执行前后截图与 UI 树，确认是否完成。
6. **记忆** — 记录每次循环中的指令、截图、UI 树与执行结果，便于后续分析。

所有步骤都位于 `ai_controller` 包中，各模块解耦，可单独替换或拓展。

## 使用方法

安装依赖：

```bash
pip install -r requirements.txt
```

在运行前，先复制示例配置并填写 API key 等信息：

```bash
cp .env.example .env   # Linux / macOS
# 或
copy .env.example .env # Windows
```

然后编辑 `.env`，设置 `OPENAI_API_KEY`，并可按需修改 `LLM_MODEL`、`VLM_MODEL` 等配置。


若要启用截图解析，请从 [OmniParser 仓库](https://github.com/microsoft/OmniParser) 安装其依赖，并在 `.env` 中设置 `OMNIPARSER_CMD` 为可执行命令，例如 `python /path/to/OmniParser/run.py`。未设置时感知模块将返回空 UI 树。

运行主程序：

```bash
python main.py
```

在提示符中输入如 “点击 OK” 或 “输入 hello” 等自然语言，即可让 AI 执行相应操作。输入 `exit` 可退出程序。
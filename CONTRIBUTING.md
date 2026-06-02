# 贡献指南 (Contributing Guide)

感谢你关注 **小宝工具箱 (xiaobao-tools)**！我们非常欢迎并期待社区的开发者能够共同参与维护，无论是修复 Bug、优化现有工具，还是分享你日常编写的 Python 实用小脚本。

为了保持项目的整洁与高质量，请在提交贡献前阅读以下指南：

---

## 目录

1. [我们的行为准则](#我们的行为准则)
2. [如何参与贡献](#如何参与贡献)
   - [报告 Bug](#报告-bug)
   - [建议新工具/新功能](#建议新工具新功能)
   - [提交代码 (Pull Request)](#提交代码-pull-request)
3. [开发与代码规范](#开发与代码规范)
4. [AI (OpenAI Codex) 辅助指南](#ai-openai-codex-辅助指南)

---

## 我们的行为准则

参与本项目的开发与互动即表示你同意遵守我们的 [行为准则 (Code of Conduct)](./CODE_OF_CONDUCT.md)。请保持友好、尊重与开放的交流态度。

## 如何参与贡献

### 报告 Bug

如果你在运行现有小工具时遇到了问题：
1. 请先在 [Issues](https://github.com/HenryYannis/xiaobao-toos/issues) 中搜索是否已有相似的报告。
2. 如果没有，请使用我们的 **Bug Report 模板** 创建一个新的 Issue。
3. 请尽可能提供：
   - 运行环境（OS版本、Python版本）。
   - 触发错误的完整日志。
   - 复现步骤及截图（如有）。

### 建议新工具/新功能

我们非常欢迎各种能够提高效率、极具创意的小工具：
1. 在 [Issues](https://github.com/HenryYannis/xiaobao-toos/issues) 提交一个 Feature Request。
2. 说明该工具的解决场景、输入和预期输出。

### 提交代码 (Pull Request)

1. **Fork** 本仓库到你自己的 GitHub 账号下。
2. **Clone** 到本地并创建一个新的开发分支：
   ```bash
   git checkout -b feature/your-tool-name
   ```
3. 在本地编写并测试你的脚本（如果是独立小工具，请直接在根目录下创建 `你的工具名.py`，如果是复杂工具，可创建专属的子目录）。
4. 确保代码符合下文的 [开发与代码规范](#开发与代码规范)。
5. 提交你的修改并推送到你的 Fork 仓库：
   ```bash
   git add .
   git commit -m "feat: 新增 XXX 实用工具"
   git push origin feature/your-tool-name
   ```
6. 在本仓库提交一个 **Pull Request**，并关联对应的 Issue。

---

## 开发与代码规范

为了让每一位用户都能无痛上手你开发的小工具，请遵循以下规范：

1. **语言与注释**：
   - 本项目优先面向中文用户。所有小工具的文件名请使用**清晰的中文描述**（例如：`时钟.py`、`工具-图片转图标`）。
   - 脚本内部的关键函数和复杂逻辑必须包含**详尽的简体中文注释**。
2. **依赖管理**：
   - 尽量减少外部库依赖，多使用 Python 标准库。
   - 如果你的小工具必须依赖第三方库（如 `opencv-python`, `pygame`, `mediapipe` 等），请在你的工具子目录下放置 `requirements.txt`，或者在脚本头部通过注释注明需要安装的依赖。
3. **代码风格**：
   - 遵循 PEP 8 风格指南。
   - 缩进使用 4 个空格，避免使用 Tab。
   - 为函数和模块添加清晰的 Docstring。

---

## AI (OpenAI Codex) 辅助指南

本仓库积极推行 **AI 辅助研发与维护工作流**。你可以使用 OpenAI Codex/ChatGPT 协助你：
- 自动为脚本生成符合 PEP 257 的 Docstring。
- 自动编写单元测试并放置在 `tests/` 目录。
- 重构冗长代码，提升运行效率和可读性。

在提交 Pull Request 时，如果使用了 AI 辅助编写，欢迎在 PR 描述中注明：`🤖 本次提交由 AI (Codex) 辅助进行代码重构/测试生成`，让我们一起推动智能化开源！

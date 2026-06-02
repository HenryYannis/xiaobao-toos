# 🛠 Xiaobao Tools (xiaobao-tools)

🌐 **[简体中文](./README.md) | English**

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/HenryYannis/xiaobao-toos)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![Codex Enabled](https://img.shields.io/badge/OpenAI%20Codex-Enabled-green.svg)](https://openai.com/form/codex-for-oss/)
[![Build Status](https://github.com/HenryYannis/xiaobao-toos/actions/workflows/lint.yml/badge.svg)](https://github.com/HenryYannis/xiaobao-toos/actions)

**Xiaobao Tools (xiaobao-tools)** is a highly curated, modular open-source toolkit comprising 20+ Python scripts and Windows configuration tools designed for independent developers, system administrators, and office professionals. The project aims to provide out-of-the-box, lightweight, and highly efficient automation solutions, covering registry optimizations, local network interactive utilities, computer vision gesture tracking, multimedia processing, and interactive edutainment.

---

## 🌟 Key Features

1. **Zero Threshold, Run Instantly**: The majority of the tools are lightweight, single `.py` files. No complex dependencies or database setups needed. Execute with a simple double-click or CLI command.
2. **Diverse Scenarios, Solving Real Needs**: Covers daily office productivity, local multiplayer games, computer vision algorithms, and Windows system-level policy tweaks.
3. **Engineering Standard & CI Automation**: Integrated with GitHub Actions CI workflows. Follows PEP 8 coding standards and features a forward-looking **OpenAI Codex AI-driven Maintenance Plan**.

---

## 🎯 Target Audiences & Scenarios Matrix

This project is not only dedicated to software developers but is highly focused on serving diverse groups of users with distinct automation needs through lightweight scripts. Below are the six typical user cohorts and pain points our tools successfully resolve:

| 🎯 Target User Cohort | 💡 Core Problems Resolved (Pain Points) | 🛠️ Recommended Tools |
| :--- | :--- | :--- |
| 🧑‍🏫 **Educators & Lab Administrators** | Restricting download actions, locking desktop wallpapers, or removing Windows lock screen Spotlight popup ads in classrooms/kiosks. | [Edge-Disable-Downloads](./system/Edge-禁止下载), [Disable-Wallpaper-Change](./system/禁止-修改壁纸), [Remove-Spotlight-Info](./system/移除-了解此图片) |
| 🎬 **Content Creators & UI Designers** | Merging multiple voice recordings (MP3s) locally, or converting PNG/JPG images into high-fidelity Windows software icons (.ico). | [Image-to-ICO](./productivity/工具-图片转图标), [Audio-Merger](./productivity/工具-音频合并) |
| 🧑‍🎓 **Language Learners & Students** | Joining interactive local network multiplayer word matching games to memory English vocabulary effortlessly while having fun. | [LAN-Word-Battle](./network/局域网-单词对战) |
| 🧑‍💻 **Developers & AI Enthusiasts** | Accessing shared AI chat nodes over local network seamlessly; scanning files via AST to build code outlines for precise LLM Code Reviews. | [LAN-AI-Chat](./network/局域网-Ai对话), [Code-Structure-Outline-Generator](./productivity/工具-代码结构大纲生成器.py) |
| 💼 **Office Workers & Time Managers** | Generating highly secure temporary passwords randomly, or displaying desktop dashboard clocks/precise count down timers for Pomodoro study. | [temporary_password.py](./productivity/临时密码.py), [dashboard_clock.py](./games_and_fun/全时钟.py), [countdown.py](./productivity/数字倒计时.py) |
| 🤖 **Geeks & CV Algorithm Explorers** | Harnessing 21 landmarks hand skeletal tracing pipelines, or customizing green hacker code-rain screensavers and Turtle 3D roses. | [gesture_recognizer.py](./vision/手势识别.py), [hand_tracking.py](./vision/手部跟踪.py), [hacker_matrix.py](./games_and_fun/黑客特效.py) |

---

## 📂 Modular Tool Matrix Directory

To help you quickly locate what you need, our tools are structured into five major category folders:

### 1. 🛜 Network & LAN Utilities
| Tool Name / Folder | English Tag | Description |
| :--- | :--- | :--- |
| [局域网-Ai对话](./network/局域网-Ai对话) | `LAN-AI-Chat` | A local LAN server-client utility facilitating multi-device AI chats without complex configurations. |
| [局域网-单词对战](./network/局域网-单词对战) | `LAN-Word-Battle` | An engaging LAN multiplayer English vocabulary battle game combining learning and fun. |

### 2. 💻 System & Browser Optimization
| Tool Name / Folder | English Tag | Description |
| :--- | :--- | :--- |
| [Edge-禁止下载](./system/Edge-禁止下载) | `Edge-Disable-Downloads` | Securely disables the download capability of Microsoft Edge via Registry and Group Policy edits. |
| [Edge-联网控制](./system/Edge-联网控制) | `Edge-Internet-Control` | A powerful lower-level script to block or permit MS Edge internet permissions dynamically. |
| [禁止-修改壁纸](./system/禁止-修改壁纸) | `Disable-Wallpaper-Change` | Restricts wallpaper modifications to lock desktop wallpaper, ideal for kiosks or public displays. |
| [移除-了解此图片](./system/移除-了解此图片) | `Remove-Spotlight-Info` | Instantly removes the distracting "Learn about this picture" spotlight pop-up from Windows lock screens. |

### 3. 🛠 Office Automation & Productivity
| Tool Name / Script | English Tag | Description |
| :--- | :--- | :--- |
| [工具-图片转图标](./productivity/工具-图片转图标) | `Image-to-ICO` | Converts ordinary image formats (PNG/JPG) locally into high-resolution, multi-size Windows `.ico` icons. |
| [工具-音频合并](./productivity/工具-音频合并) | `Audio-Merger` | Scans directories and concatenates multiple audio clips (e.g. MP3 files) effortlessly. |
| [工具-代码结构大纲生成器.py](./productivity/工具-代码结构大纲生成器.py) | `code_outline_generator` | Scans files using Python's AST parser to extract classes, functions, and docstrings into a beautiful markdown outline. |
| [临时密码.py](./productivity/临时密码.py) | `temp_password.py` | Generates highly secure, random passwords with customizable lengths and character sets. |
| [数字倒计时.py](./productivity/数字倒计时.py) | `countdown.py` | A lightweight countdown timer with sound notifications precise to the second. |
| [进度条.py](./productivity/进度条.py) | `progress_bar.py` | An elegant, animated CLI progress bar module designed for command-line developers. |

### 4. 👁 Interaction & Vision Algorithms
| Tool Name / Script | English Tag | Description |
| :--- | :--- | :--- |
| [手势识别.py](./vision/手势识别.py) | `gesture_recognizer.py` | Employs OpenCV & MediaPipe to recognize complex gestures and map them into Windows keyboard shortcuts. |
| [手部跟踪.py](./vision/手部跟踪.py) | `hand_tracking.py` | Fast framework to capture camera video streams, locate 21 hand skeletal landmarks, and stream 3D coordinates. |

### 5. 🎮 Games & Interactive Edutainment
| Tool Name / Script | English Tag | Description |
| :--- | :--- | :--- |
| [井字棋.py](./games_and_fun/井字棋.py) | `tic_tac_toe.py` | A classic double-player Tic-Tac-Toe GUI game based on Tkinter. |
| [时钟.py](./games_and_fun/时钟.py) | `clock.py` | A minimalistic desktop electronic clock window for easy timekeeping. |
| [全时钟.py](./games_and_fun/全时钟.py) | `dashboard_clock.py` | A feature-rich dashboard clock displaying multi-timezones, alarms, stopwatches, and stopwatch cards. |
| [黑客特效.py](./games_and_fun/黑客特效.py) | `hacker_matrix.py` | The classic green "Hacker Matrix Digital Rain" screen saver and wallpaper simulator written in Pygame. |
| [玫瑰花程序.py](./games_and_fun/玫瑰花程序.py) | `turtle_rose.py` | Draws a highly detailed, 3D-shaded aesthetic rose vector animation using Python's Turtle canvas. |
| [破译程序.py](./games_and_fun/破译程序.py) | `cipher_decrypter.py` | An educational cipher decryptor illustrating substitution encryption and brute force cryptography theories. |

---

## 🤖 OpenAI Codex Maintenance & Integration Plan

As a project maintained by a single core developer, utilizing AI to maximize daily maintenance and QA efficiency is a core focus. We are actively experimenting with integrating **OpenAI Codex & API** into the "xiaobao-tools" software lifecycle across four distinct scenarios:

1. **Automated PR Reviews & Intelligent Refactoring (AI Code Review)**:
   Leverages Codex to automatically audit incoming community PR submissions, identifying memory issues, code smells, or style violations, and posting refactored, PEP-8 compliant suggestions directly inside PR comments.
2. **AI-driven Unit Test Generation (AI Test Coverage)**:
   Uses Codex to analyze input/output boundaries of the 20+ standalone scripts and automatically generate `pytest` regression tests inside the `tests/` directory to assure cross-version Windows compatibility.
3. **Smart Issue Triage & Bug Diagnosis (Traceback Analysis)**:
   Feeds user-submitted terminal traceback logs to Codex, automatically extracting environmental details (e.g. OpenCV version, OS version) and auto-assigning tags like `bug` or `os:windows`.
4. **Automated Multilingual Docs Sync (AI Localization)**:
   Extracts code functions to write docstrings using Codex, and keeps the Chinese and English READMEs completely synchronized with zero translation overhead.

---

## 🚀 Quick Start

### 1. Clone the Repository
Ensure you have Python 3.8+ installed. Clone the repository:
```bash
git clone https://github.com/HenryYannis/xiaobao-toos.git
cd xiaobao-toos
```

### 2. Install Dependencies
While simple scripts run on Python's standard library, complex multi-media/vision tools require third-party libraries. Install them via:
```bash
pip install -r requirements.txt
```

### 3. Run a Tool
Execute any Python script directly inside your terminal:
```bash
python productivity/临时密码.py
```

---

## 🤝 Contributing

We heartily welcome community members to share their small Python scripts!
For detailed coding formats and PR checklists, please see [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## 📄 License

This project is licensed under the **MIT License**. You are free to copy, modify, distribute, and commercially utilize these tools, provided copyright notices are retained. See [LICENSE](./LICENSE) for details.

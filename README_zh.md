<div align="right">
<a href="README.md">English</a> | 中文
</div>

# Simple Whisper Hotkey Dictation (极简 Whisper 热键听写工具)

这是一个简单、轻量级的 Python 脚本，它能让您在 Windows上的**任何应用程序**中，通过一个全局快捷键，实时地将您的语音转换为文字。它由 OpenAI 强大的 Whisper 模型驱动，并为中文用户做了特别优化。

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ 功能特性

*   **🎙️ 全局热键**：在任何文本框、编辑器或聊天窗口，按下您自定义的快捷键即可开始/停止语音输入。
*   **🤫 智能检测**：在您开始说话时自动开始录制，在您停止说话一段时间后自动结束并开始转录。
*   **⌨️ 自动输入**：转录完成后，文字会自动“打”在您当前光标所在的位置，就像您亲手输入一样。
*   **🇨🇳 中文优化**：自动将 Whisper 可能输出的繁体中文转换为简体中文。
*   **⚙️ 首次运行向导**：第一次使用时，程序会引导您完成麦克风、AI 模型和快捷键的配置。
*   **📝 轻量配置**：您的所有设置都会保存在一个简单的 `config.json` 文件中，方便后续修改。
*   **純 CPU 运行**：无需昂贵的显卡，在普通电脑的 CPU 上即可流畅运行。

## 🚀 安装与设置

### 1. 先决条件

*   **Python 3.9 或更高版本**。请确保在安装时勾选了 "Add Python to PATH" 选项。
*   **(重要) FFmpeg**：Whisper 依赖 FFmpeg 来处理音频。
    *   **Windows**: 从 [官网](https://ffmpeg.org/download.html) 下载后，将其 `bin` 目录添加到系统的 PATH 环境变量中。

### 2. 获取代码

将本项目克隆到您的本地：
```bash
git clone https://github.com/xyc0123456789/whisper_dictate.git
cd whisper_dictate
```
或者，直接下载本仓库的 ZIP 文件并解压。

### 3. 安装依赖库

本项目的所有依赖库都已在代码注释中列出。请打开命令行工具 (CMD, PowerShell 或 Terminal)，运行以下命令来一键安装：

```bash
pip install openai-whisper sounddevice numpy keyboard scipy zhconv
```

## ▶️ 如何使用

### 1. 首次运行

在命令行中，进入项目目录，运行脚本：

```bash
python whisper_dictate.py 
```

程序会启动一个交互式设置向导：
1.  **选择麦克风**：它会列出所有可用的输入设备，您只需输入对应的数字编号并按回车。
2.  **选择 AI 模型**：
    *   `tiny` 或 `base`：速度最快，资源占用小，适合日常使用。
    *   `small` 或 `medium`：准确率更高，但处理速度会稍慢。
3.  **设置快捷键**：输入您想用的快捷键组合，例如 `ctrl+alt+space` 或 `f4`，然后按回车。

配置完成后，您的设置将保存到 `config.json` 文件中，程序进入就绪状态。

### 2. 日常使用

*   **开始录音**：切换到任何您想输入文字的应用（如记事本、Word、浏览器），按下您设置的快捷键。
*   **停止录音**：
    *   **手动停止**：再次按下快捷键，会立即停止录音并开始转录。
    *   **自动停止**：说完话后，保持安静约 1.5 秒，程序会自动停止录音并开始转录。
*   **退出程序**：切回到运行脚本的那个**命令行窗口**，按下 `Ctrl + C` 组合键即可安全退出。

## 🔧 进阶配置 (可选)

您可以直接编辑脚本文件顶部的全局配置参数，以适应您的使用环境：

*   `SILENCE_THRESHOLD`: 静音阈值。如果您的环境嘈杂，可以适当调高此值；如果您的麦克风灵敏度低，可以适当调低此值。
*   `SILENCE_DURATION`: 判断为录音结束所需的静音时长（秒）。如果您说话时停顿较长，可以适当增加此值。

## 📦 核心依赖

*   [openai-whisper](https://github.com/openai/whisper): 核心语音识别模型。
*   [sounddevice](https://python-sounddevice.readthedocs.io/): 用于录制音频。
*   [keyboard](https://github.com/boppreh/keyboard): 用于全局热键监听和模拟键盘输入。
*   [numpy](https://numpy.org/) & [scipy](https://scipy.org/): 用于处理音频数据。
*   [zhconv](https://github.com/gumblex/zhconv): 用于繁简体中文转换。

## 📜 许可证

本项目基于 [MIT 许可证](LICENSE)。
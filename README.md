<div align="right">
[English](README.md) | <a href="README_zh.md">中文</a>
</div>

# Simple Whisper Hotkey Dictation

A simple, lightweight Python script that lets you transcribe your voice into text in real-time within **any application** on Windows, using a global hotkey.

Powered by OpenAI's powerful Whisper model, this tool is optimized for both performance and ease of use.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

*   **🎙️ Global Hotkey**: Start and stop dictation in any text box, editor, or chat window with a single, customizable shortcut.
*   **🤫 Intelligent Silence Detection**: Automatically starts recording when you speak and finalizes transcription after a brief period of silence.
*   **⌨️ Automatic Typing**: Transcribed text is automatically typed at your cursor's position, as if by magic.
*   **🚀 GPU Acceleration (Optional)**: Automatically detects and utilizes a CUDA-enabled GPU for significantly faster transcriptions, while maintaining full support for CPU-only operation.
*   **🇨🇳 Chinese Language Optimization**: Includes an option to automatically convert Traditional Chinese characters (common in Whisper's output) to Simplified Chinese.
*   **⚙️ First-Run Setup Wizard**: Guides you through microphone, AI model, and hotkey configuration on the first launch.
*   **📝 Lightweight Configuration**: All your settings are saved in a simple `config.json` file for easy editing.

## 🚀 Installation & Setup

### 1. Prerequisites

*   **Python 3.9 or higher**. Ensure "Add Python to PATH" is checked during installation on Windows.
*   **(Required) FFmpeg**: Whisper depends on FFmpeg to process audio.
    *   **Windows**: Download from the [official website](https://ffmpeg.org/download.html), then add its `bin` directory to your system's PATH environment variable.

### 2. Get the Code

Clone the repository to your local machine:
```bash
git clone https://github.com/xyc0123456789/whisper_dictate.git
cd whisper_dictate
```
Alternatively, download and extract the ZIP file.

### 3. Install Dependencies

**Choose the command that matches your operating system!**

*   **For Windows & Linux:** (Uses the `keyboard` library)
    ```bash
    pip install openai-whisper sounddevice numpy keyboard scipy zhconv
    ```

## ▶️ How to Use

### 1. First Run

Navigate to the project directory in your terminal and run the script:

```bash
python whisper_dictate.py
```

The script will launch an interactive setup wizard:
1.  **Select Microphone**: A list of available input devices will be shown. Enter the corresponding number.
2.  **Select AI Model**: Choose a model size. `base` or `small` are recommended for a good balance of speed and accuracy on most systems.
3.  **Set Hotkey**: Enter your desired key combination.
    *   **Windows/Linux (`keyboard` syntax)**: `ctrl+alt+space` or `f4`

Your settings will be saved to `config.json`, and the script will be ready.

### 2. Daily Use

*   **Start/Stop Recording**: Switch to any application and press your hotkey to start recording. Press it again to manually stop and begin transcription.
*   **Automatic Stop**: If you don't stop manually, the script will automatically stop after 1.5 seconds of silence.
*   **Exit the Program**: Switch back to the terminal window where the script is running and press `Ctrl + C` to exit safely.

## 🔧 Advanced Configuration (Optional)

You can manually edit the global parameters at the top of the script file to fine-tune its behavior:

*   `SILENCE_THRESHOLD`: The volume level required to trigger recording. Increase in noisy environments, decrease for less sensitive microphones.
*   `SILENCE_DURATION`: The length of silence (in seconds) required to automatically stop recording.

## 📦 Core Dependencies

*   [openai-whisper](https://github.com/openai/whisper): The core speech recognition model.
*   [sounddevice](https://python-sounddevice.readthedocs.io/): For audio recording.
*   [keyboard](https://github.com/boppreh/keyboard) (Win/Linux)
*   [numpy](https://numpy.org/) & [scipy](https://scipy.org/): For audio data manipulation.
*   [zhconv](https://github.com/gumblex/zhconv): For Traditional-to-Simplified Chinese conversion.
*   [PyTorch](https://pytorch.org/): The deep learning framework that powers Whisper and enables GPU acceleration.

## 📜 License

This project is licensed under the [MIT License](LICENSE).
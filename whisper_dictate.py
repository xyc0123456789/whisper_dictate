# pip install openai-whisper sounddevice numpy keyboard scipy zhconv

import sounddevice as sd
import numpy as np
import whisper
import keyboard
import json
import os
import time
import threading
from scipy.io.wavfile import write
from zhconv import convert

# --- 全局配置 ---
CONFIG_FILE = 'config.json'
SAMPLE_RATE = 16000
SILENCE_THRESHOLD = 0.02
SILENCE_DURATION = 1.5
TEMP_AUDIO_FILE = "temp_audio.wav"

# --- 全局状态管理 ---
class AppState:
    IDLE = 0
    RECORDING = 1
    PROCESSING = 2

current_state = AppState.IDLE
manual_stop_signal = threading.Event()

# --- 核心功能 ---

def first_time_setup():
    """首次运行时引导用户进行配置。"""
    print("--- 首次运行配置 ---")
    
    print("\n[1] 请选择您的输入设备:")
    devices = sd.query_devices()
    input_devices = [device for device in devices if device['max_input_channels'] > 0]
    for i, device in enumerate(input_devices):
        print(f"  {i}: {device['name']}")
    while True:
        try:
            device_index = int(input(f"请输入设备编号 (0-{len(input_devices)-1}): "))
            if 0 <= device_index < len(input_devices): break
            else: print("无效的编号，请重试。")
        except ValueError: print("请输入一个数字。")

    print("\n[2] 请选择要使用的 Whisper 模型:")
    models = ['tiny', 'base', 'small', 'medium']
    for i, model in enumerate(models): print(f"  {i}: {model} (越往下越准，但速度越慢)")
    while True:
        try:
            model_index = int(input(f"请输入模型编号 (0-{len(models)-1}): "))
            if 0 <= model_index < len(models):
                model_name = models[model_index]
                break
            else: print("无效的编号，请重试。")
        except ValueError: print("请输入一个数字。")

    print("\n[3] 请设置一个全局快捷键 (例如: 'ctrl+alt+s' 或 'f4')")
    hotkey = input("请输入您想设置的快捷键: ")

    config = {'device': device_index, 'model': model_name, 'hotkey': hotkey}
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
        
    print("\n--- 配置完成！---")
    return config

def load_config():
    """加载配置文件。"""
    if not os.path.exists(CONFIG_FILE): return first_time_setup()
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def record_audio(device_id):
    """录制音频，直到静音或手动停止信号。"""
    audio_chunks, is_recording, silent_frames = [], False, 0
    frames_to_stop = int((SILENCE_DURATION * SAMPLE_RATE) / 1024)

    def callback(indata, frames, time, status):
        nonlocal is_recording, silent_frames
        if manual_stop_signal.is_set(): raise sd.CallbackStop
        volume_norm = np.linalg.norm(indata) * 10
        if volume_norm > SILENCE_THRESHOLD:
            if not is_recording: print("检测到声音，开始录制..."); is_recording = True
            audio_chunks.append(indata.copy()); silent_frames = 0
        elif is_recording:
            silent_frames += 1; audio_chunks.append(indata.copy())
            if silent_frames > frames_to_stop: raise sd.CallbackStop

    print("\n请开始说话... (再次按下快捷键可手动停止)")
    try:
        with sd.InputStream(samplerate=SAMPLE_RATE, device=device_id, channels=1, callback=callback, blocksize=1024):
            while not manual_stop_signal.is_set(): sd.sleep(100)
    except sd.CallbackStop: pass
    except Exception as e: print(f"录音时发生错误: {e}"); return None
    
    if audio_chunks: print("录制结束。"); return np.concatenate(audio_chunks, axis=0)
    else: print("未录制到任何内容。"); return None

def process_audio_thread(model, device_id):
    """在一个独立的线程中执行完整的处理流程"""
    global current_state
    
    manual_stop_signal.clear()
    current_state = AppState.RECORDING
    audio_data = record_audio(device_id)
    current_state = AppState.PROCESSING
    
    if audio_data is not None and len(audio_data) > 0:
        write(TEMP_AUDIO_FILE, SAMPLE_RATE, audio_data)

        print("正在转录音频...")
        try:
            result = model.transcribe(TEMP_AUDIO_FILE, fp16=False)
            original_text = result['text'].strip()
            text = convert(original_text, 'zh-cn')
            
            if text:
                print(f"原始识别结果: {original_text}")
                print(f"转换为简体: {text}")
                keyboard.write(text)
            else:
                print("未能识别出任何文字。")
        except Exception as e:
            print(f"转录时发生错误: {e}")
        finally:
            if os.path.exists(TEMP_AUDIO_FILE): os.remove(TEMP_AUDIO_FILE)
    else:
        print("未录制到有效音频。")

    print(f"\n程序已就绪。按下 '{config['hotkey']}' 开始/停止 (在命令行按 Ctrl+C 退出)。")
    current_state = AppState.IDLE

def hotkey_handler(model, device_id):
    """快捷键处理函数"""
    global current_state
    if current_state == AppState.IDLE:
        threading.Thread(target=process_audio_thread, args=(model, device_id)).start()
    elif current_state == AppState.RECORDING:
        print("收到手动停止信号..."); manual_stop_signal.set()
    elif current_state == AppState.PROCESSING:
        print("正在处理中，请稍候...")

def main():
    """主函数"""
    global config
    config = load_config()
    device_id, model_name, hotkey = config['device'], config['model'], config['hotkey']

    print("\n正在加载 Whisper 模型...")
    model = whisper.load_model(model_name)
    print(f"模型 '{model_name}' 加载完毕。")
    print("-" * 30)
    print(f"设备: '{sd.query_devices(device_id)['name']}'")
    print(f"开始/停止快捷键: '{hotkey}'")
    print(f"退出程序请在此命令行窗口按: Ctrl+C")
    print("-" * 30)

    keyboard.add_hotkey(hotkey, lambda: hotkey_handler(model, device_id))

    print(f"\n程序已就绪。按下 '{hotkey}' 开始/停止 (在命令行按 Ctrl+C 退出)。")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n检测到 Ctrl+C，正在退出程序...")

if __name__ == "__main__":
    main()
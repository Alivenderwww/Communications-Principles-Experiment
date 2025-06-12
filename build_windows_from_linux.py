#!/usr/bin/env python3
"""
在Linux环境下构建Windows可执行文件
需要安装wine和PyInstaller的Windows版本
"""

import os
import subprocess
import sys

def build_windows_exe():
    """构建Windows版本的可执行文件"""
    print("正在为Windows平台构建可执行文件...")
    
    # 确保PyInstaller已安装
    subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 使用PyInstaller进行构建
    cmd = [
        sys.executable, 
        "-m", 
        "PyInstaller",
        "--onefile",
        "--hidden-import", "PIL._tkinter_finder",
        "--collect-all", "PIL",
        "--hidden-import", "tkinter",
        "--windowed",
        "--name=SignalSamplingExperiment_Windows",
        "signal_sampling_experiment.py"
    ]
    
    subprocess.call(cmd)
    
    print("构建完成！Windows可执行文件已生成: dist/SignalSamplingExperiment_Windows.exe")

if __name__ == "__main__":
    build_windows_exe()

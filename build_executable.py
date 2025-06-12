#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
打包脚本 - 使用PyInstaller将信号采样实验程序打包成可执行文件
"""

import os
import sys
import platform
import subprocess

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print("PyInstaller已安装。")
        return True
    except ImportError:
        print("PyInstaller未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller已成功安装。")
            return True
        except subprocess.CalledProcessError:
            print("安装PyInstaller失败。请手动安装：pip install pyinstaller")
            return False

def build_executable():
    """构建可执行文件"""
    script_path = "signal_sampling_experiment.py"
    
    # 检查脚本文件是否存在
    if not os.path.exists(script_path):
        print(f"错误：找不到{script_path}文件。")
        return False
    
    # 构建PyInstaller命令
    cmd = [
        "pyinstaller",
        "--onefile",  # 创建单一可执行文件
        "--windowed",  # 对于GUI应用，不显示控制台窗口(Windows)，在Linux下无效但无害
        "--name", "SignalSamplingExperiment",  # 可执行文件名称
        "--icon", "NONE",  # 无图标
        script_path
    ]
    
    print("开始构建可执行文件，这可能需要几分钟时间...")
    try:
        subprocess.check_call(cmd)
        system = platform.system()
        print(f"构建完成！可执行文件已生成在 dist 目录中。")
        if system == "Windows":
            print("Windows可执行文件: dist\\SignalSamplingExperiment.exe")
        else:
            print("Linux可执行文件: dist/SignalSamplingExperiment")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False

if __name__ == "__main__":
    if check_pyinstaller():
        build_executable()

#!/bin/bash
# Linux平台构建脚本

echo "正在构建Linux版本的可执行文件..."

# 确保PyInstaller和Pillow已正确安装
pip install pyinstaller pillow

# 构建可执行文件 - 添加特定的包含选项来解决PIL和Tkinter问题
# --hidden-import确保导入隐藏模块，--collect-all收集所有相关的PIL模块
pyinstaller --onefile \
            --hidden-import PIL._tkinter_finder \
            --collect-all PIL \
            --hidden-import tkinter \
            --noconsole \
            --name SignalSamplingExperiment_Linux \
            --icon=NONE \
            signal_sampling_experiment.py

# 确保dist目录存在
mkdir -p dist

echo "构建完成！可执行文件已生成: dist/SignalSamplingExperiment_Linux"

@echo off
REM Windows平台构建脚本

echo 正在构建Windows版本的可执行文件...

REM 确保PyInstaller和Pillow已正确安装
pip install pyinstaller pillow

REM 构建可执行文件 - 添加特定的包含选项来解决PIL和Tkinter问题
pyinstaller --onefile^
 --hidden-import PIL._tkinter_finder^
 --collect-all PIL^
 --hidden-import tkinter^
 --windowed^
 --name SignalSamplingExperiment_Windows^
 --icon=NONE^
 signal_sampling_experiment.py

REM 确保dist目录存在
if not exist dist mkdir dist

echo 构建完成！可执行文件已生成: dist\SignalSamplingExperiment_Windows.exe
pause

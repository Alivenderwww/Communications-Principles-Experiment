@echo off
REM Windowsƽ̨�����ű�

echo ���ڹ���Windows�汾�Ŀ�ִ���ļ�...

REM ȷ��PyInstaller��Pillow����ȷ��װ
pip install pyinstaller pillow

REM ������ִ���ļ� - ����ض��İ���ѡ�������PIL��Tkinter����
pyinstaller --onefile^
 --hidden-import PIL._tkinter_finder^
 --collect-all PIL^
 --hidden-import tkinter^
 --windowed^
 --name SignalSamplingExperiment_Windows^
 --icon=NONE^
 signal_sampling_experiment.py

REM ȷ��distĿ¼����
if not exist dist mkdir dist

echo ������ɣ���ִ���ļ�������: dist\SignalSamplingExperiment_Windows.exe
pause

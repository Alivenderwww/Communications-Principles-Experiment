#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模拟信号频域采样实验
原始信号: cos(2π*f1*t+π/4) + cos(2π*f2*t) 
其中f1=1000Hz, f2=1100Hz
探究选取不同的采样频率和采样个数下，得到的频谱与实际频谱的差异。

交互控制说明:
- 上/下方向键: 调整采样频率
- 左/右方向键: 调整采样点数
- 's' 键: 保存当前图像
- 'q' 键: 退出
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.fft import fft, fftfreq
import matplotlib as mpl
# 预先导入用于插值的模块，避免每次调用函数时重新导入
from scipy.interpolate import splrep, splev, interp1d

mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题

# 原始信号参数
f1 = 1000  # Hz
f2 = 1100  # Hz
phase = np.pi / 4

# 生成原始信号
def generate_signal(t):
    """生成原始信号 cos(2π*f1*t+π/4) + cos(2π*f2*t)"""
    return np.cos(2 * np.pi * f1 * t + phase) + np.cos(2 * np.pi * f2 * t)

# 进行频谱分析
def analyze_spectrum(signal, fs, N, title=""):
    """分析信号的频谱"""
    # 计算时间点
    t = np.arange(N) / fs
    
    # 采样信号
    sampled_signal = signal(t)
    
    # 计算频谱
    spectrum = fft(sampled_signal)
    magnitude = np.abs(spectrum) / N  # 归一化幅度谱
    
    # 对于实信号，频谱是对称的，我们只需要前半部分
    magnitude = magnitude[:N//2]
    magnitude[1:-1] = 2 * magnitude[1:-1]  # 因为对称性所以幅值乘以2（直流分量和Nyquist频率除外）
    
    # 频率轴
    freqs = fftfreq(N, 1/fs)[:N//2]
    
    # 创建图表
    fig = plt.figure(figsize=(14, 8))
    gs = GridSpec(2, 1, height_ratios=[1, 1])
    
    # 时域信号绘制
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(t, sampled_signal, 'b-', label='Sampled Signal')
    
    # 如果采样点较少，添加采样点标记
    if N <= 100:
        ax1.plot(t, sampled_signal, 'ro', label='Sample Points')
    
    ax1.set_title(f'Time Domain - {title}')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    ax1.grid(True)
    ax1.legend()
    
    # 频域信号绘制
    ax2 = fig.add_subplot(gs[1])
    ax2.stem(freqs, magnitude)  # 新版matplotlib不再需要use_line_collection参数
    
    # 添加频谱拟合曲线
    if len(freqs) > 3:  # 确保有足够的点进行插值
        # 创建更密集的频率点
        interp_freqs = np.linspace(freqs[0], freqs[-1], len(freqs) * 5)
        
        # 使用三次样条插值，确保曲线平滑
        if len(freqs) > 10:
            tck = splrep(freqs, magnitude, s=0.01)  # s是平滑参数
            interp_magnitude = splev(interp_freqs, tck)
        else:
            f = interp1d(freqs, magnitude, kind='quadratic', bounds_error=False, fill_value=0)
            interp_magnitude = f(interp_freqs)
            
        # 绘制拟合曲线 - 使用蓝色而不是红色，避免与f1参考线混淆
        ax2.plot(interp_freqs, interp_magnitude, 'b-', linewidth=1.5, alpha=0.7, 
                label='Spectrum Fit Curve')
    
    # 标记理论频率点
    ax2.axvline(f1, color='r', linestyle='--', label=f'f1={f1}Hz')
    ax2.axvline(f2, color='g', linestyle='--', label=f'f2={f2}Hz')
    
    ax2.set_title(f'Frequency Domain - {title}')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Magnitude')
    ax2.grid(True)
    ax2.legend()
    
    # 限制x轴显示范围为0到2*f2或者Nyquist频率，取较小值
    x_max = min(2 * f2, fs / 2)
    ax2.set_xlim([0, x_max])
    
    plt.tight_layout()
    return fig

def interactive_experiment():
    """交互式实验，使用键盘控制采样频率和采样点数"""
    
    # 初始设置
    fs_init = 4000  # Hz, 初始采样频率
    N_init = 1000   # 初始采样点数
    fs_step = 500   # 采样频率调整步长
    N_step = 100    # 采样点数调整步长
    
    # 创建图形
    fig = plt.figure(figsize=(14, 8))
    gs = GridSpec(2, 1, height_ratios=[1, 1])
    
    # 时域子图
    ax1 = fig.add_subplot(gs[0])
    time_line, = ax1.plot([], [], 'b-', label='Sampled Signal')
    sample_points, = ax1.plot([], [], 'ro', label='Sample Points')
    ax1.grid(True)
    ax1.legend()
    ax1.set_title('')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    
    # 频域子图
    ax2 = fig.add_subplot(gs[1])
    # 初始化时不创建stem图，只在update_plot函数中创建
    ax2.grid(True)
    ax2.set_title('')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Magnitude')
    
    # 参考线
    f1_line = ax2.axvline(f1, color='r', linestyle='--', label=f'f1={f1}Hz')
    f2_line = ax2.axvline(f2, color='g', linestyle='--', label=f'f2={f2}Hz')
    ax2.legend()
    
    # 全局变量存储当前设置
    fs_current = fs_init
    N_current = N_init
    
    def update_plot():
        """更新绘图"""
        nonlocal fs_current, N_current
        
        # 计算时间点 - 使用预分配更高效
        t = np.arange(N_current) / fs_current
        
        # 采样信号
        sampled_signal = generate_signal(t)
        
        # 计算频谱
        spectrum = fft(sampled_signal)
        
        # 对于实信号，频谱是对称的，我们只需要前半部分
        half_point = N_current//2
        magnitude = np.abs(spectrum[:half_point]) / N_current  # 归一化幅度谱
        magnitude[1:half_point-1] *= 2  # 因为对称性所以幅值乘以2（直流分量和Nyquist频率除外）
        
        # 频率轴
        freqs = fftfreq(N_current, 1/fs_current)[:half_point]
        
        # 更新时域图
        time_line.set_data(t, sampled_signal)
        if N_current <= 100:  # 只有在采样点少时才显示采样点
            sample_points.set_data(t, sampled_signal)
            sample_points.set_visible(True)
        else:
            sample_points.set_visible(False)
        
        ax1.set_xlim(0, t[-1])
        ax1.set_ylim(-2.5, 2.5)
        
        # 更新频域图
        # 移除旧的stems和拟合曲线，但保留参考线
        # 首先保存参考线对象
        ref_lines = []
        for line in ax2.lines:
            if line.get_linestyle() == '--':  # 参考线使用虚线样式
                ref_lines.append(line)
                
        # 清除所有内容
        ax2.clear()
        
        # 重新添加网格和标签
        ax2.grid(True)
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Magnitude')
        
        # 先绘制参考线
        for line in ref_lines:
            if line.get_xdata()[0] == f1:
                f1_line = ax2.axvline(f1, color='r', linestyle='--', label=f'f1={f1}Hz')
            elif line.get_xdata()[0] == f2:
                f2_line = ax2.axvline(f2, color='g', linestyle='--', label=f'f2={f2}Hz')
        
        # 创建频谱柱状图
        ax2.stem(freqs, magnitude)
        
        # 创建拟合曲线
        # 使用更密集的点进行插值，让曲线更平滑
        if len(freqs) > 3:  # 确保有足够的点进行插值
            # 创建更密集的频率点
            interp_freqs = np.linspace(freqs[0], freqs[-1], len(freqs) * 5)
            
            # 使用三次样条插值，确保曲线平滑
            if len(freqs) > 10:  # 足够多的点时使用样条插值
                tck = splrep(freqs, magnitude, s=0.01)  # s是平滑参数
                interp_magnitude = splev(interp_freqs, tck)
            else:  # 点较少时使用更简单的方法
                f = interp1d(freqs, magnitude, kind='quadratic', bounds_error=False, fill_value=0)
                interp_magnitude = f(interp_freqs)
                
            # 绘制拟合曲线 - 使用蓝色而不是红色，避免与f1参考线混淆
            ax2.plot(interp_freqs, interp_magnitude, 'b-', linewidth=1.5, alpha=0.7, 
                    label='Spectrum Fit Curve')
            
            # 更新图例
            ax2.legend()
        
        # 限制x轴显示范围为0到2*f2或者Nyquist频率，取较小值
        x_max = min(2 * f2, fs_current / 2)
        ax2.set_xlim(0, x_max)
        ax2.set_ylim(0, 1.1)
        
        # 更新标题
        if fs_current < 2 * f2:
            title_status = "Undersampling"
        else:
            title_status = "Proper Sampling"
            
        ax1.set_title(f'Time Domain - {title_status}: Fs={fs_current}Hz, N={N_current}')
        ax2.set_title(f'Frequency Domain - {title_status}: Fs={fs_current}Hz, N={N_current}')
        
        fig.canvas.draw_idle()
    
    # 键盘事件处理
    def on_key(event):
        nonlocal fs_current, N_current
        
        if event.key == 'up':  # 增加采样频率
            fs_current += fs_step
            print(f"Sampling frequency increased to: {fs_current}Hz")
        elif event.key == 'down' and fs_current > fs_step:  # 减少采样频率
            fs_current -= fs_step
            print(f"Sampling frequency decreased to: {fs_current}Hz")
        elif event.key == 'right':  # 增加采样点数
            N_current += N_step
            print(f"Sample count increased to: {N_current}")
        elif event.key == 'left' and N_current > N_step:  # 减少采样点数
            N_current -= N_step
            print(f"Sample count decreased to: {N_current}")
        elif event.key == 's':  # 保存图像
            filename = f'experiment_fs_{fs_current}_N_{N_current}.png'
            plt.savefig(filename, dpi=150)
            print(f"Image saved as: {filename}")
        elif event.key == 'q':  # 退出
            plt.close(fig)
            return
        else:
            return
            
        update_plot()
    
    # 初始化绘图
    update_plot()
    
    # 绑定键盘事件
    fig.canvas.mpl_connect('key_press_event', on_key)
    
    # 显示图像
    plt.tight_layout()
    plt.show()

def run_standard_experiment():
    """运行标准实验，探究不同采样频率和采样点数的影响"""
    
    # 预分配图表对象列表，避免频繁创建和销毁图表
    figures = []
    
    # 实验1: 不同采样频率
    sampling_frequencies = [2500, 4000, 8000]  # Hz
    N = 1000  # 采样点数
    
    # 对每个采样频率进行实验
    for fs in sampling_frequencies:
        title = f"采样频率={fs}Hz, 采样点数={N}"
        fig = analyze_spectrum(generate_signal, fs, N, title)
        plt.savefig(f'experiment_fs_{fs}_N_{N}.png', dpi=150)
        figures.append(fig)
    
    # 实验2: 不同采样点数
    fs = 4000  # Hz
    sample_sizes = [100, 500, 2000]
    
    # 对每个采样点数进行实验
    for N in sample_sizes:
        title = f"采样频率={fs}Hz, 采样点数={N}"
        fig = analyze_spectrum(generate_signal, fs, N, title)
        plt.savefig(f'experiment_fs_{fs}_N_{N}.png', dpi=150)
        figures.append(fig)
    
    # 实验3: 欠采样情况
    fs_undersampling = [1500, 1800]  # Hz (低于2*f2)
    N = 1000
    
    # 对欠采样频率进行实验
    for fs in fs_undersampling:
        title = f"欠采样: 采样频率={fs}Hz, 采样点数={N}"
        fig = analyze_spectrum(generate_signal, fs, N, title)
        plt.savefig(f'experiment_undersampling_fs_{fs}_N_{N}.png', dpi=150)
        figures.append(fig)
    
    plt.show()

if __name__ == "__main__":
    # 选择运行模式
    interactive_experiment()  # 交互式实验
    # run_standard_experiment()  # 标准固定参数实验

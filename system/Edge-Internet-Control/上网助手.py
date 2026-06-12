#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小宝工具箱 - 上网助手 (Internet Assistant)

功能：
- 定时控制 Edge 浏览器联网状态
- 支持断网和联网时间设置
- 帮助用户专注工作或学习

使用方法：
- 需要以管理员权限运行
- 设置断网和联网时间
- 点击开始按钮

注意事项：
- 仅支持 Windows 系统
- 需要管理员权限
- 需要安装 pywin32：pip install pywin32

作者：小宝科技帝国
日期：2024
"""

import os
import time
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import threading
import sys
import win32event
import win32api
import winerror
import mmap
import ctypes
import subprocess

# ================= 【配置区域】 =================
断网时长_分钟 = 45
联网时长_分钟 = 15

MUTEX_NAME = "Global\\MyApp_ShangWangZhuShou_A3_Mutex"
SHARED_MEM_NAME = "Global\\MyApp_ShangWangZhuShou_Time_Share"
global_mmap_file = None
# ===============================================

# --- 内部计算变量 ---
实际_专注秒数 = 断网时长_分钟 * 60
实际_休息秒数 = 联网时长_分钟 * 60
显示_专注文本 = 断网时长_分钟
显示_休息文本 = 联网时长_分钟

RULE_NAME_X86 = "Block Edge Outbound (x86)"
RULE_NAME_X64 = "Block Edge Outbound (x64)"
EDGE_PATH_X86 = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
EDGE_PATH_X64 = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"


def 执行隐藏命令(command):
    """
    替代 os.system，执行命令时不显示黑窗口，也不显示输出结果
    """
    try:
        startupinfo = subprocess.STARTUPINFO()
        # 关键设置：隐藏窗口
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        subprocess.run(
            command, 
            startupinfo=startupinfo, 
            shell=True, 
            stdout=subprocess.DEVNULL, # 屏蔽标准输出
            stderr=subprocess.DEVNULL  # 屏蔽错误输出
        )
    except Exception:
        pass


def 是否有管理员权限():
    """检测当前程序是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def 智能等待_直到(目标时间点):
    """等待直到某个具体的时间点"""
    while datetime.now() < 目标时间点:
        time.sleep(0.5) 


def 弹窗提示_非阻塞(标题, 内容):
    """在新线程中弹窗，不卡住主程序计时"""
    def _run():
        try:
            root = tk.Tk()
            root.withdraw() 
            root.attributes('-topmost', True)
            messagebox.showinfo(标题, 内容)
            root.destroy()
        except:
            pass
    threading.Thread(target=_run, daemon=True).start()


def 弹窗_3秒自动关闭(标题, 内容):
    """最后的弹窗，显示3秒后自动关闭程序"""
    try:
        root = tk.Tk()
        root.withdraw()
        
        top = tk.Toplevel(root)
        top.title(标题)
        top.attributes('-topmost', True)
        
        tk.Label(top, text=内容, font=("微软雅黑", 10), padx=20, pady=20).pack()
        
        top.update_idletasks()
        w, h = top.winfo_width(), top.winfo_height()
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        top.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")
        
        root.after(3000, root.destroy)
        root.mainloop()
    except:
        pass


def 禁止_edge_上网():
    # 使用新的隐藏命令执行函数，无需再加 >nul
    执行隐藏命令('sc config MpsSvc start= auto')
    执行隐藏命令('sc start MpsSvc')
    执行隐藏命令('netsh advfirewall set allprofiles state on')
    执行隐藏命令(f'netsh advfirewall firewall delete rule name="{RULE_NAME_X86}"')
    执行隐藏命令(f'netsh advfirewall firewall delete rule name="{RULE_NAME_X64}"')
    
    if os.path.exists(EDGE_PATH_X86):
        执行隐藏命令(f'netsh advfirewall firewall add rule name="{RULE_NAME_X86}" dir=out action=block program="{EDGE_PATH_X86}" enable=yes')
    if os.path.exists(EDGE_PATH_X64):
        执行隐藏命令(f'netsh advfirewall firewall add rule name="{RULE_NAME_X64}" dir=out action=block program="{EDGE_PATH_X64}" enable=yes')
    
    执行隐藏命令('taskkill /f /im msedge.exe')


def 允许_edge_上网():
    执行隐藏命令(f'netsh advfirewall firewall delete rule name="{RULE_NAME_X86}"')
    执行隐藏命令(f'netsh advfirewall firewall delete rule name="{RULE_NAME_X64}"')


def 阻断逻辑():
    try:
        # 计算绝对时间点
        当前时间 = datetime.now()
        专注截止时间 = 当前时间 + timedelta(minutes=断网时长_分钟)
        休息截止时间 = 专注截止时间 + timedelta(minutes=联网时长_分钟)

        # --- 1. 禁止上网 (专注阶段) ---
        print("已进入专注阶段，开始计时并持续禁止上网...")

        # 使用循环代替智能等待，实现每隔5秒重新加入防火墙规则
        while datetime.now() < 专注截止时间:
            禁止_edge_上网()
            
            # 计算距离专注截止时间还剩多少秒
            剩余秒数 = (专注截止时间 - datetime.now()).total_seconds()
            
            # 如果剩余时间大于等于5秒，则等待5秒；否则等待剩余时间
            # 确保最后一次等待不会超过截止时间
            等待时长 = min(5.0, max(0.1, 剩余秒数))
            time.sleep(等待时长)
            
            if 剩余秒数 <= 0:
                break


        # --- 2. 休息阶段判断 ---
        # 此时专注阶段已结束
        
        # 检查是否因为某种原因已经错过了休息截止时间
        if datetime.now() >= 休息截止时间:
            禁止_edge_上网() 
            弹窗_3秒自动关闭("提示", f"{显示_休息文本}分钟到，网络已禁止")
            return

        # 如果还在休息时间内，恢复网络
        允许_edge_上网()
        
        弹窗提示_非阻塞("提示", f"网络已恢复{显示_休息文本}分钟")
        print(f"开始计时{显示_休息文本}分钟...")
        
        # 等待直到休息结束
        智能等待_直到(休息截止时间)

        # --- 3. 再次禁止 ---
        禁止_edge_上网()
        
        弹窗_3秒自动关闭("提示", f"{显示_休息文本}分钟到，网络已禁止")
        
    except Exception as e:
        print(f"运行出错: {e}")


def 居中显示(窗口):
    窗口.update_idletasks()
    宽 = 窗口.winfo_width()
    高 = 窗口.winfo_height()
    屏幕宽 = 窗口.winfo_screenwidth()
    屏幕高 = 窗口.winfo_screenheight()
    x = (屏幕宽 - 宽) // 2
    y = (屏幕高 - 高) // 2
    窗口.geometry(f"{宽}x{高}+{x}+{y}")


def 开始任务并提示(窗口):
    global global_mmap_file
    
    预计恢复时间 = datetime.now() + timedelta(minutes=断网时长_分钟)
    时间文本 = 预计恢复时间.strftime("%H:%M")

    try:
        global_mmap_file = mmap.mmap(-1, 1024, tagname=SHARED_MEM_NAME)
        global_mmap_file.write(bytes(时间文本, 'utf-8'))
    except Exception as e:
        messagebox.showerror("内存错误", f"无法写入共享内存：{e}")
        return
    
    try:
        messagebox.showinfo("预计恢复时间", f"预计 {时间文本} 恢复网络")
        窗口.destroy()
        阻断逻辑()
    finally:
        if global_mmap_file:
            try: global_mmap_file.close()
            except: pass


def 主界面():
    if not 是否有管理员权限():
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("权限不足", "错误：请右键点击程序，选择【以管理员身份运行】")
        root.destroy()
        sys.exit(1)
        
    # 启动时清理一次旧规则，防止上次异常退出导致无法上网（此为新增的安全逻辑）
    允许_edge_上网()

    handle = None
    try:
        handle = win32event.CreateMutex(None, 1, MUTEX_NAME)
        if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
            stored_time = "未知时间"
            try:
                shm = mmap.mmap(-1, 1024, tagname=SHARED_MEM_NAME)
                content = shm.read(1024).decode('utf-8').strip('\x00')
                if content: stored_time = content
                shm.close()
            except: pass
            
            messagebox.showwarning(
                "程序已运行", 
                f"  计时器已启动，请勿重复操作\n\n预计 {stored_time} 恢复网络，请认真上课！"
            )
            sys.exit(0)
    except Exception as e:
        messagebox.showerror("错误", f"进程检测失败：{e}")
        sys.exit(1)

    窗口 = tk.Tk()
    窗口.title("上网助手")
    窗口.geometry("340x180")

    窗口.update()
    居中显示(窗口)

    标签 = tk.Label(窗口, text="请选择一个操作", font=("微软雅黑", 12 ,"bold"))
    标签.pack(pady=10)

    按钮文字 = f"{显示_专注文本}分钟后恢复网络"

    按钮1 = tk.Button(
        窗口,
        text=按钮文字,
        width=20,
        height=2,
        command=lambda: 开始任务并提示(窗口)
    )
    按钮1.pack(pady=5)

    按钮2 = tk.Button(
        窗口,
        text="退出",
        width=20,
        height=2,
        command=窗口.destroy
    )
    按钮2.pack()

    窗口.mainloop()
    
    if handle:
        try: win32api.ReleaseMutex(handle)
        except: pass

if __name__ == "__main__":
    主界面()
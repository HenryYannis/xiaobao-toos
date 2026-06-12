#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
屏幕截图工具 (Screen Capture Tool)

功能：
- 全屏截图
- 区域截图
- 窗口截图
- 延时截图
- 自动保存

作者：小宝科技帝国
日期：2024
"""

import os
import sys
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageGrab, Image, ImageDraw
import threading


class ScreenCaptureTool:
    """屏幕截图工具"""

    def __init__(self, root):
        self.root = root
        self.root.title("屏幕截图工具")
        self.root.geometry("600x500")

        # 截图设置
        self.save_dir = os.path.join(os.path.expanduser("~"), "Desktop", "screenshots")
        self.file_format = "PNG"
        self.quality = 95

        # 创建界面
        self.create_widgets()

        # 创建保存目录
        os.makedirs(self.save_dir, exist_ok=True)

    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 标题
        title_label = ttk.Label(main_frame, text="屏幕截图工具", font=("微软雅黑", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # 截图模式
        mode_frame = ttk.LabelFrame(main_frame, text="截图模式", padding="15")
        mode_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))

        # 全屏截图
        full_frame = ttk.Frame(mode_frame)
        full_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(full_frame, text="全屏截图", command=self.full_screen_capture, width=15).grid(row=0, column=0, padx=(0, 10))
        ttk.Label(full_frame, text="截取整个屏幕").grid(row=0, column=1)

        # 区域截图
        region_frame = ttk.Frame(mode_frame)
        region_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(region_frame, text="区域截图", command=self.region_capture, width=15).grid(row=0, column=0, padx=(0, 10))
        ttk.Label(region_frame, text="拖拽选择区域").grid(row=0, column=1)

        # 窗口截图
        window_frame = ttk.Frame(mode_frame)
        window_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(window_frame, text="窗口截图", command=self.window_capture, width=15).grid(row=0, column=0, padx=(0, 10))
        ttk.Label(window_frame, text="截取指定窗口").grid(row=0, column=1)

        # 延时截图
        delay_frame = ttk.Frame(mode_frame)
        delay_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(delay_frame, text="延时截图", command=self.delay_capture, width=15).grid(row=0, column=0, padx=(0, 10))
        ttk.Label(delay_frame, text="延迟时间(秒):").grid(row=0, column=1, padx=(0, 5))
        self.delay_var = tk.StringVar(value="5")
        ttk.Entry(delay_frame, textvariable=self.delay_var, width=5).grid(row=0, column=2)

        # 保存设置
        settings_frame = ttk.LabelFrame(main_frame, text="保存设置", padding="15")
        settings_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))

        # 保存目录
        dir_frame = ttk.Frame(settings_frame)
        dir_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(dir_frame, text="保存目录:").grid(row=0, column=0, padx=(0, 10))
        self.dir_var = tk.StringVar(value=self.save_dir)
        ttk.Entry(dir_frame, textvariable=self.dir_var, width=40).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(dir_frame, text="浏览", command=self.browse_dir).grid(row=0, column=2)

        # 文件格式
        format_frame = ttk.Frame(settings_frame)
        format_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(format_frame, text="文件格式:").grid(row=0, column=0, padx=(0, 10))
        self.format_var = tk.StringVar(value="PNG")
        format_combo = ttk.Combobox(format_frame, textvariable=self.format_var, width=10)
        format_combo['values'] = ["PNG", "JPEG", "BMP"]
        format_combo.grid(row=0, column=1, padx=(0, 20))

        ttk.Label(format_frame, text="质量:").grid(row=0, column=2, padx=(0, 10))
        self.quality_var = tk.IntVar(value=95)
        quality_scale = ttk.Scale(format_frame, from_=1, to=100, variable=self.quality_var,
                                  orient=tk.HORIZONTAL, length=150)
        quality_scale.grid(row=0, column=3, padx=(0, 10))
        self.quality_label = ttk.Label(format_frame, text="95%")
        self.quality_label.grid(row=0, column=4)
        quality_scale.configure(command=self.update_quality_label)

        # 文件名前缀
        prefix_frame = ttk.Frame(settings_frame)
        prefix_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(prefix_frame, text="文件名前缀:").grid(row=0, column=0, padx=(0, 10))
        self.prefix_var = tk.StringVar(value="screenshot")
        ttk.Entry(prefix_frame, textvariable=self.prefix_var, width=20).grid(row=0, column=1)

        # 最近截图
        recent_frame = ttk.LabelFrame(main_frame, text="最近截图", padding="15")
        recent_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 截图列表
        self.recent_listbox = tk.Listbox(recent_frame, height=6)
        recent_scrollbar = ttk.Scrollbar(recent_frame, orient=tk.VERTICAL, command=self.recent_listbox.yview)
        self.recent_listbox.configure(yscrollcommand=recent_scrollbar.set)

        self.recent_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        recent_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # 按钮
        btn_frame = ttk.Frame(recent_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))

        ttk.Button(btn_frame, text="打开文件", command=self.open_file).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="打开目录", command=self.open_dir).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="清空列表", command=self.clear_recent).grid(row=0, column=2, padx=5)

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))

        # 配置权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        recent_frame.columnconfigure(0, weight=1)
        recent_frame.rowconfigure(0, weight=1)

    def update_quality_label(self, value):
        """更新质量标签"""
        self.quality_label.config(text=f"{int(float(value))}%")

    def browse_dir(self):
        """浏览目录"""
        directory = filedialog.askdirectory(title="选择保存目录")
        if directory:
            self.dir_var.set(directory)
            self.save_dir = directory

    def get_filename(self):
        """生成文件名"""
        prefix = self.prefix_var.get()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = self.format_var.get().lower()
        return f"{prefix}_{timestamp}.{ext}"

    def save_image(self, image):
        """保存图片"""
        # 获取保存路径
        filename = self.get_filename()
        filepath = os.path.join(self.save_dir, filename)

        # 保存图片
        if self.format_var.get() == "JPEG":
            image.save(filepath, quality=self.quality_var.get())
        else:
            image.save(filepath)

        # 添加到最近列表
        self.recent_listbox.insert(0, filepath)

        # 更新状态
        self.status_var.set(f"截图已保存: {filepath}")

        return filepath

    def full_screen_capture(self):
        """全屏截图"""
        # 隐藏窗口
        self.root.withdraw()
        time.sleep(0.5)

        try:
            # 截取全屏
            screenshot = ImageGrab.grab()

            # 保存截图
            filepath = self.save_image(screenshot)

            # 显示成功消息
            messagebox.showinfo("成功", f"全屏截图已保存:\n{filepath}")

        except Exception as e:
            messagebox.showerror("错误", f"截图失败: {e}")

        finally:
            # 显示窗口
            self.root.deiconify()

    def region_capture(self):
        """区域截图"""
        # 隐藏窗口
        self.root.withdraw()
        time.sleep(0.5)

        try:
            # 创建选择窗口
            self.selection_window = tk.Toplevel()
            self.selection_window.attributes('-fullscreen', True)
            self.selection_window.attributes('-alpha', 0.3)
            self.selection_window.configure(bg='gray')

            # 绑定事件
            self.selection_window.bind('<Button-1>', self.on_mouse_down)
            self.selection_window.bind('<B1-Motion>', self.on_mouse_drag)
            self.selection_window.bind('<ButtonRelease-1>', self.on_mouse_up)
            self.selection_window.bind('<Escape>', lambda e: self.selection_window.destroy())

            # 初始化变量
            self.start_x = 0
            self.start_y = 0
            self.rect = None

        except Exception as e:
            messagebox.showerror("错误", f"截图失败: {e}")
            self.root.deiconify()

    def on_mouse_down(self, event):
        """鼠标按下"""
        self.start_x = event.x
        self.start_y = event.y

        # 创建矩形
        if self.rect:
            self.selection_window.delete(self.rect)
        self.rect = self.selection_window.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2
        )

    def on_mouse_drag(self, event):
        """鼠标拖拽"""
        # 更新矩形
        self.selection_window.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_mouse_up(self, event):
        """鼠标释放"""
        # 获取选择区域
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)

        # 关闭选择窗口
        self.selection_window.destroy()

        # 截取区域
        if x2 - x1 > 10 and y2 - y1 > 10:
            try:
                screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                filepath = self.save_image(screenshot)
                messagebox.showinfo("成功", f"区域截图已保存:\n{filepath}")
            except Exception as e:
                messagebox.showerror("错误", f"截图失败: {e}")

        # 显示窗口
        self.root.deiconify()

    def window_capture(self):
        """窗口截图"""
        # 隐藏窗口
        self.root.withdraw()
        time.sleep(0.5)

        try:
            # 获取前台窗口
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()

            # 获取窗口位置
            rect = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))

            # 截取窗口
            screenshot = ImageGrab.grab(bbox=(rect.left, rect.top, rect.right, rect.bottom))

            # 保存截图
            filepath = self.save_image(screenshot)

            # 显示成功消息
            messagebox.showinfo("成功", f"窗口截图已保存:\n{filepath}")

        except Exception as e:
            messagebox.showerror("错误", f"截图失败: {e}")

        finally:
            # 显示窗口
            self.root.deiconify()

    def delay_capture(self):
        """延时截图"""
        try:
            delay = int(self.delay_var.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的延迟时间")
            return

        # 隐藏窗口
        self.root.withdraw()

        # 延时
        for i in range(delay, 0, -1):
            self.status_var.set(f"倒计时: {i} 秒")
            self.root.update()
            time.sleep(1)

        try:
            # 截取全屏
            screenshot = ImageGrab.grab()

            # 保存截图
            filepath = self.save_image(screenshot)

            # 显示成功消息
            messagebox.showinfo("成功", f"延时截图已保存:\n{filepath}")

        except Exception as e:
            messagebox.showerror("错误", f"截图失败: {e}")

        finally:
            # 显示窗口
            self.root.deiconify()
            self.status_var.set("就绪")

    def open_file(self):
        """打开文件"""
        selection = self.recent_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择文件")
            return

        filepath = self.recent_listbox.get(selection[0])
        if os.path.exists(filepath):
            os.startfile(filepath)
        else:
            messagebox.showwarning("警告", "文件不存在")

    def open_dir(self):
        """打开目录"""
        if os.path.exists(self.save_dir):
            os.startfile(self.save_dir)
        else:
            messagebox.showwarning("警告", "目录不存在")

    def clear_recent(self):
        """清空最近列表"""
        self.recent_listbox.delete(0, tk.END)


def main():
    """主函数"""
    root = tk.Tk()
    app = ScreenCaptureTool(root)
    root.mainloop()


if __name__ == "__main__":
    main()

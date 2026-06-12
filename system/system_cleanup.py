#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统垃圾清理工具 (System Cleanup Tool)

功能：
- 清理临时文件
- 清理回收站
- 清理浏览器缓存
- 清理系统日志
- 清理Windows更新缓存

作者：小宝科技帝国
日期：2024
"""

import os
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime


class SystemCleanupTool:
    """系统垃圾清理工具"""

    def __init__(self, root):
        self.root = root
        self.root.title("系统垃圾清理工具")
        self.root.geometry("800x600")

        # 清理选项
        self.cleanup_options = {
            "temp_files": {"name": "临时文件", "desc": "清理系统和用户临时文件夹", "size": 0},
            "recycle_bin": {"name": "回收站", "desc": "清空回收站", "size": 0},
            "browser_cache": {"name": "浏览器缓存", "desc": "清理Chrome、Edge等浏览器缓存", "size": 0},
            "system_logs": {"name": "系统日志", "desc": "清理Windows事件日志", "size": 0},
            "update_cache": {"name": "Windows更新缓存", "desc": "清理Windows更新下载缓存", "size": 0},
            "thumbnails": {"name": "缩略图缓存", "desc": "清理Windows缩略图缓存", "size": 0},
        }

        # 创建界面
        self.create_widgets()

        # 扫描垃圾文件
        self.scan_thread = None

    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 标题
        title_label = ttk.Label(main_frame, text="系统垃圾清理工具", font=("微软雅黑", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # 清理选项
        options_frame = ttk.LabelFrame(main_frame, text="清理选项", padding="10")
        options_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # 创建复选框
        self.option_vars = {}
        for i, (key, option) in enumerate(self.cleanup_options.items()):
            var = tk.BooleanVar(value=True)
            self.option_vars[key] = var

            frame = ttk.Frame(options_frame)
            frame.grid(row=i // 2, column=i % 2, sticky=(tk.W, tk.E), padx=5, pady=2)

            ttk.Checkbutton(frame, text=option["name"], variable=var).grid(row=0, column=0, sticky=tk.W)
            ttk.Label(frame, text=option["desc"], foreground="gray").grid(row=1, column=0, sticky=tk.W, padx=(20, 0))

        # 扫描结果
        result_frame = ttk.LabelFrame(main_frame, text="扫描结果", padding="10")
        result_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # 结果树形视图
        self.result_tree = ttk.Treeview(result_frame, columns=("type", "size", "count"), show="headings", height=10)
        self.result_tree.heading("type", text="类型")
        self.result_tree.heading("size", text="大小")
        self.result_tree.heading("count", text="文件数")
        self.result_tree.column("type", width=200)
        self.result_tree.column("size", width=150)
        self.result_tree.column("count", width=100)

        result_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=result_scrollbar.set)

        self.result_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # 总计
        total_frame = ttk.Frame(result_frame)
        total_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        ttk.Label(total_frame, text="总计可清理:").grid(row=0, column=0, padx=(0, 10))
        self.total_size_var = tk.StringVar(value="0 MB")
        ttk.Label(total_frame, textvariable=self.total_size_var, font=("微软雅黑", 12, "bold")).grid(row=0, column=1)

        # 按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        ttk.Button(btn_frame, text="扫描", command=self.start_scan).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="清理选中", command=self.cleanup_selected).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="全部清理", command=self.cleanup_all).grid(row=0, column=2, padx=5)

        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # 配置权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

    def format_size(self, size_bytes):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    def scan_temp_files(self):
        """扫描临时文件"""
        temp_dirs = [
            tempfile.gettempdir(),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp'),
            os.path.join(os.environ.get('TEMP', '')),
        ]

        total_size = 0
        file_count = 0

        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        try:
                            filepath = os.path.join(root, file)
                            size = os.path.getsize(filepath)
                            total_size += size
                            file_count += 1
                        except:
                            pass

        return total_size, file_count

    def scan_recycle_bin(self):
        """扫描回收站"""
        # 使用PowerShell获取回收站大小
        try:
            cmd = "powershell -Command \"(New-Object -ComObject Shell.Application).NameSpace(10).Items() | Measure-Object -Property Size -Sum | Select-Object -ExpandProperty Sum\""
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            if result.returncode == 0 and result.stdout.strip():
                size = int(result.stdout.strip())
                return size, 1  # 回收站算作1个项目
        except:
            pass

        return 0, 0

    def scan_browser_cache(self):
        """扫描浏览器缓存"""
        cache_dirs = [
            # Chrome
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data', 'Default', 'Code Cache'),
            # Edge
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Edge', 'User Data', 'Default', 'Code Cache'),
        ]

        total_size = 0
        file_count = 0

        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                for root, dirs, files in os.walk(cache_dir):
                    for file in files:
                        try:
                            filepath = os.path.join(root, file)
                            size = os.path.getsize(filepath)
                            total_size += size
                            file_count += 1
                        except:
                            pass

        return total_size, file_count

    def scan_system_logs(self):
        """扫描系统日志"""
        log_dirs = [
            os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Logs'),
            os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp'),
        ]

        total_size = 0
        file_count = 0

        for log_dir in log_dirs:
            if os.path.exists(log_dir):
                for root, dirs, files in os.walk(log_dir):
                    for file in files:
                        try:
                            filepath = os.path.join(root, file)
                            size = os.path.getsize(filepath)
                            total_size += size
                            file_count += 1
                        except:
                            pass

        return total_size, file_count

    def scan_update_cache(self):
        """扫描Windows更新缓存"""
        update_dir = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'SoftwareDistribution', 'Download')

        total_size = 0
        file_count = 0

        if os.path.exists(update_dir):
            for root, dirs, files in os.walk(update_dir):
                for file in files:
                    try:
                        filepath = os.path.join(root, file)
                        size = os.path.getsize(filepath)
                        total_size += size
                        file_count += 1
                    except:
                        pass

        return total_size, file_count

    def scan_thumbnails(self):
        """扫描缩略图缓存"""
        thumb_dir = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'Explorer')

        total_size = 0
        file_count = 0

        if os.path.exists(thumb_dir):
            for file in os.listdir(thumb_dir):
                if file.startswith('thumbcache'):
                    try:
                        filepath = os.path.join(thumb_dir, file)
                        size = os.path.getsize(filepath)
                        total_size += size
                        file_count += 1
                    except:
                        pass

        return total_size, file_count

    def start_scan(self):
        """开始扫描"""
        # 清空结果
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        self.status_var.set("正在扫描...")
        self.progress_var.set(0)

        # 在新线程中扫描
        self.scan_thread = threading.Thread(target=self.scan_worker)
        self.scan_thread.start()

    def scan_worker(self):
        """扫描工作线程"""
        total_size = 0
        scan_functions = {
            "temp_files": self.scan_temp_files,
            "recycle_bin": self.scan_recycle_bin,
            "browser_cache": self.scan_browser_cache,
            "system_logs": self.scan_system_logs,
            "update_cache": self.scan_update_cache,
            "thumbnails": self.scan_thumbnails,
        }

        for i, (key, func) in enumerate(scan_functions.items()):
            if self.option_vars[key].get():
                size, count = func()
                self.cleanup_options[key]["size"] = size
                total_size += size

                # 更新UI
                self.root.after(0, self.update_scan_result, key, size, count)
                self.root.after(0, self.progress_var.set, (i + 1) / len(scan_functions) * 100)

        # 更新总计
        self.root.after(0, self.total_size_var.set, self.format_size(total_size))
        self.root.after(0, self.status_var.set, "扫描完成")

    def update_scan_result(self, key, size, count):
        """更新扫描结果"""
        option = self.cleanup_options[key]
        self.result_tree.insert("", tk.END, values=(
            option["name"],
            self.format_size(size),
            count
        ))

    def cleanup_selected(self):
        """清理选中项目"""
        selected = self.result_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要清理的项目")
            return

        if not messagebox.askyesno("确认", "确定要清理选中的项目吗？此操作不可撤销。"):
            return

        # 执行清理
        for item in selected:
            values = self.result_tree.item(item, "values")
            type_name = values[0]

            # 找到对应的清理函数
            for key, option in self.cleanup_options.items():
                if option["name"] == type_name:
                    self.cleanup_by_type(key)
                    break

        # 重新扫描
        self.start_scan()
        messagebox.showinfo("完成", "清理完成！")

    def cleanup_all(self):
        """清理所有项目"""
        if not messagebox.askyesno("确认", "确定要清理所有垃圾文件吗？此操作不可撤销。"):
            return

        # 执行清理
        for key in self.cleanup_options:
            if self.option_vars[key].get():
                self.cleanup_by_type(key)

        # 重新扫描
        self.start_scan()
        messagebox.showinfo("完成", "清理完成！")

    def cleanup_by_type(self, type_key):
        """根据类型清理"""
        if type_key == "temp_files":
            self.cleanup_temp_files()
        elif type_key == "recycle_bin":
            self.cleanup_recycle_bin()
        elif type_key == "browser_cache":
            self.cleanup_browser_cache()
        elif type_key == "system_logs":
            self.cleanup_system_logs()
        elif type_key == "update_cache":
            self.cleanup_update_cache()
        elif type_key == "thumbnails":
            self.cleanup_thumbnails()

    def cleanup_temp_files(self):
        """清理临时文件"""
        temp_dirs = [
            tempfile.gettempdir(),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp'),
        ]

        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                for root, dirs, files in os.walk(temp_dir, topdown=False):
                    for file in files:
                        try:
                            filepath = os.path.join(root, file)
                            os.remove(filepath)
                        except:
                            pass
                    for dir in dirs:
                        try:
                            dirpath = os.path.join(root, dir)
                            shutil.rmtree(dirpath)
                        except:
                            pass

    def cleanup_recycle_bin(self):
        """清空回收站"""
        try:
            subprocess.run("powershell -Command \"Clear-RecycleBin -Force\"", shell=True)
        except:
            pass

    def cleanup_browser_cache(self):
        """清理浏览器缓存"""
        cache_dirs = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data', 'Default', 'Code Cache'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Edge', 'User Data', 'Default', 'Code Cache'),
        ]

        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                try:
                    shutil.rmtree(cache_dir)
                except:
                    pass

    def cleanup_system_logs(self):
        """清理系统日志"""
        log_dirs = [
            os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Logs'),
        ]

        for log_dir in log_dirs:
            if os.path.exists(log_dir):
                for root, dirs, files in os.walk(log_dir, topdown=False):
                    for file in files:
                        try:
                            filepath = os.path.join(root, file)
                            os.remove(filepath)
                        except:
                            pass

    def cleanup_update_cache(self):
        """清理Windows更新缓存"""
        update_dir = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'SoftwareDistribution', 'Download')

        if os.path.exists(update_dir):
            try:
                # 需要停止Windows Update服务
                subprocess.run("net stop wuauserv", shell=True)
                shutil.rmtree(update_dir)
                os.makedirs(update_dir)
                subprocess.run("net start wuauserv", shell=True)
            except:
                pass

    def cleanup_thumbnails(self):
        """清理缩略图缓存"""
        thumb_dir = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'Explorer')

        if os.path.exists(thumb_dir):
            for file in os.listdir(thumb_dir):
                if file.startswith('thumbcache'):
                    try:
                        filepath = os.path.join(thumb_dir, file)
                        os.remove(filepath)
                    except:
                        pass


def main():
    """主函数"""
    root = tk.Tk()
    app = SystemCleanupTool(root)
    root.mainloop()


if __name__ == "__main__":
    main()

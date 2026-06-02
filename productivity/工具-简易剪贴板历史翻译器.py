#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
小宝工具箱 - 简易剪贴板历史翻译器 (Clipboard History & Quick Translator)
功能：后台静默监听系统剪贴板，自动记录历史复制内容，提供一键翻译（中英互译，基于免 key 翻译 API）并一键写回剪贴板。
受众：阅读外文文献的学生、处理跨国业务/英文报告的办公族、频繁复制粘贴的人员。
"""

import urllib.request
import urllib.parse
import json
import threading
import tkinter as tk
from tkinter import messagebox

class ClipboardTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("剪贴板历史翻译器")
        self.root.geometry("450x450")
        self.root.resizable(False, False)
        
        self.history = []
        self.last_clipboard_text = ""
        self.is_monitoring = True
        
        self.setup_ui()
        self.monitor_clipboard()

    def setup_ui(self):
        # 头部横幅
        header = tk.Label(self.root, text="📋 剪贴板历史与极速翻译", font=("Helvetica", 14, "bold"), fg="#0969da")
        header.pack(pady=10)
        
        # 历史记录列表框
        list_frame = tk.LabelFrame(self.root, text=" 复制历史记录 (双击条目重新写入剪贴板) ", font=("Helvetica", 9, "bold"), padx=5, pady=5)
        list_frame.pack(padx=15, fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.history_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Helvetica", 10), height=8, selectmode="single")
        self.history_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # 绑定双击事件，一键复制历史
        self.history_listbox.bind("<Double-Button-1>", self.copy_selected_to_clipboard)
        
        # 翻译预览区
        trans_frame = tk.LabelFrame(self.root, text=" 智能中英互译结果 ", font=("Helvetica", 9, "bold"), padx=5, pady=5)
        trans_frame.pack(padx=15, fill="x", pady=10)
        
        self.trans_text = tk.Text(trans_frame, height=4, font=("Helvetica", 10), wrap="word")
        self.trans_text.pack(fill="x", expand=True)
        
        # 按钮控制区
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        translate_btn = tk.Button(btn_frame, text="⚡ 一键翻译选定项", font=("Helvetica", 10, "bold"), bg="#0969da", fg="white",
                                  relief="flat", activebackground="#0c54b6", command=self.translate_selected)
        translate_btn.grid(row=0, column=0, padx=10, ipady=3, ipadx=5)
        
        copy_trans_btn = tk.Button(btn_frame, text="✍ 复制翻译结果", font=("Helvetica", 10, "bold"), bg="#2da44e", fg="white",
                                   relief="flat", activebackground="#2c974b", command=self.copy_translation)
        copy_trans_btn.grid(row=0, column=1, padx=10, ipady=3, ipadx=5)
        
        clear_btn = tk.Button(btn_frame, text="🗑 清空历史", font=("Helvetica", 10), bg="#f6f8fa", relief="groove",
                              command=self.clear_history)
        clear_btn.grid(row=0, column=2, padx=10, ipady=2, ipadx=5)

    def monitor_clipboard(self):
        """主循环：每隔 500 毫秒轮询系统剪贴板，检测文本变更"""
        if self.is_monitoring:
            try:
                # 获取系统剪贴板内容
                clipboard_text = self.root.clipboard_get()
                clipboard_text = clipboard_text.strip()
                
                # 触发剪贴板文本新增
                if clipboard_text and clipboard_text != self.last_clipboard_text:
                    self.last_clipboard_text = clipboard_text
                    
                    # 避免重复
                    if clipboard_text not in self.history:
                        self.history.insert(0, clipboard_text)
                        
                        # 仅保留最近 25 条，保持清爽
                        if len(self.history) > 25:
                            self.history.pop()
                            
                        self.update_listbox()
            except Exception:
                # 剪贴板可能为空或非文本格式
                pass
            
            # 定时轮询
            self.root.after(500, self.monitor_clipboard)

    def update_listbox(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.history:
            # 缩略展示，避免单行太长
            display_item = item.replace('\n', ' ')
            if len(display_item) > 40:
                display_item = display_item[:37] + "..."
            self.history_listbox.insert(tk.END, display_item)

    def copy_selected_to_clipboard(self, event=None):
        """双击条目，重新将其完整复制回系统剪贴板"""
        try:
            selected_idx = self.history_listbox.curselection()[0]
            selected_text = self.history[selected_idx]
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)
            self.last_clipboard_text = selected_text # 避免自己触发监控
            messagebox.showinfo("成功", "已成功将该历史文本写回系统剪贴板！")
        except IndexError:
            pass

    def copy_translation(self):
        translation = self.trans_text.get(1.0, tk.END).strip()
        if translation and not translation.startswith("正在翻译"):
            self.root.clipboard_clear()
            self.root.clipboard_append(translation)
            self.last_clipboard_text = translation
            messagebox.showinfo("成功", "翻译结果已复制到剪贴板！")
        else:
            messagebox.showwarning("警告", "翻译结果为空，无法复制。")

    def clear_history(self):
        self.history.clear()
        self.last_clipboard_text = ""
        self.update_listbox()
        self.trans_text.delete(1.0, tk.END)

    def translate_selected(self):
        """多线程调用免费 MyMemory API 进行翻译，防 GUI 卡顿"""
        try:
            selected_idx = self.history_listbox.curselection()[0]
            selected_text = self.history[selected_idx]
            
            self.trans_text.delete(1.0, tk.END)
            self.trans_text.insert(tk.END, "正在翻译中，请稍候...")
            
            # 开启翻译守护线程
            thread = threading.Thread(target=self.run_translation, args=(selected_text,))
            thread.daemon = True
            thread.start()
        except IndexError:
            messagebox.showwarning("提示", "请先在历史记录列表中单击选定要翻译的文本。")

    def run_translation(self, text):
        """调用免费无限制的 MyMemory API 进行中英判定与翻译"""
        # 判断首个字符是否为汉字以决定翻译方向
        is_chinese = False
        for char in text[:5]:
            if '\u4e00' <= char <= '\u9fff':
                is_chinese = True
                break
                
        lang_pair = "zh-CN|en" if is_chinese else "en|zh-CN"
        
        try:
            url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair={lang_pair}"
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=8) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                translated_text = res_data["matches"][0]["translation"]
                
                # 剔除可能的空内容
                if not translated_text:
                    translated_text = "翻译接口未返回有效翻译，请重试。"
                    
                # 写入 GUI
                self.root.after(0, lambda: self.show_translation_result(translated_text))
        except Exception as e:
            self.root.after(0, lambda: self.show_translation_result(f"翻译服务请求失败，请检查网络。错误: {e}"))

    def show_translation_result(self, result):
        self.trans_text.delete(1.0, tk.END)
        self.trans_text.insert(tk.END, result)

if __name__ == "__main__":
    app_root = tk.Tk()
    app = ClipboardTranslatorApp(app_root)
    app_root.mainloop()

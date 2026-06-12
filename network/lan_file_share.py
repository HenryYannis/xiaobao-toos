#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
小宝工具箱 - 局域网极速文件共享器 (LAN File Share Server)
功能：一键将电脑上的指定目录化身局域网文件共享中心，局域网内的任何手机、平板、电脑只需输入网页地址，
     即可免流量、极速下载电脑上的文件，甚至支持直接在手机浏览器中向电脑上传文件。
受众：教育工作者、教师（一键分发课件）、日常跨平台（手机到电脑）临时传输大文件的办公人员。
"""

import os
import sys
import socket
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

# 终端彩色输出
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    """自定义 HTTP 请求处理器，在标准 SimpleHTTPRequestHandler 上提供文件上传能力"""
    def do_POST(self):
        """处理局域网内其他设备上传文件的 POST 请求"""
        try:
            # 解析 multipart/form-data 类型的 POST 请求
            boundary = self.headers.get_boundary().encode()
            remainbytes = int(self.headers['content-length'])
            line = self.rfile.readline()
            remainbytes -= len(line)
            if not boundary in line:
                self.send_error(400, "Content NOT begun with boundary")
                return
            
            # 读取文件头，提取文件名
            line = self.rfile.readline()
            remainbytes -= len(line)
            fn_index = line.find(b'filename=')
            if fn_index == -1:
                self.send_error(400, "Can't find out file name")
                return
            
            filename = line[fn_index + 10 : -2].decode('utf-8').strip('"')
            # 兼容不同浏览器对文件名的处理
            filename = os.path.basename(filename)
            if not filename:
                self.send_error(400, "Filename is empty")
                return
            
            # 读取后续空行
            line = self.rfile.readline()
            remainbytes -= len(line)
            line = self.rfile.readline()
            remainbytes -= len(line)
            
            # 写入本地文件
            out_filepath = os.path.join(self.directory, filename)
            try:
                out = open(out_filepath, 'wb')
            except IOError:
                self.send_error(404, "Can't create file to write, do you have permission?")
                return
            
            # 循环写入文件体
            preline = self.rfile.readline()
            remainbytes -= len(preline)
            while remainbytes > 0:
                line = self.rfile.readline()
                remainbytes -= len(line)
                if boundary in line:
                    preline = preline[0:-1]
                    if preline.endswith(b'\r'):
                        preline = preline[0:-1]
                    out.write(preline)
                    out.close()
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    # 返回上传成功的精致反馈页面
                    response_html = f"""
                    <html>
                    <head>
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <style>
                            body {{ font-family: -apple-system, sans-serif; text-align: center; padding: 40px; background-color: #f5f5f7; }}
                            .card {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); display: inline-block; max-width: 320px; }}
                            h2 {{ color: #34c759; }}
                            a {{ display: inline-block; margin-top: 20px; padding: 10px 20px; background: #007aff; color: white; text-decoration: none; border-radius: 6px; }}
                        </style>
                    </head>
                    <body>
                        <div class="card">
                            <h2>✓ 上传成功！</h2>
                            <p>文件 <b>{filename}</b> 已成功存入分享电脑！</p>
                            <a href="/">返回主页</a>
                        </div>
                    </body>
                    </html>
                    """
                    self.wfile.write(response_html.encode('utf-8'))
                    return
                else:
                    out.write(preline)
                    preline = line
            
            self.send_error(400, "Unexpected end of file")
        except Exception as e:
            self.send_error(500, f"Internal error: {e}")

    def list_directory(self, path):
        """重写目录列表生成方法，在页面顶部注入一个精致的文件上传 HTML 表单"""
        try:
            # 获取原生的目录页面对象
            dir_list = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None
        
        # 页面美化与上传表单注入
        r = []
        displaypath = self.path
        enc = sys.getfilesystemencoding()
        title = f"小宝极速局域网共享器: {displaypath}"
        
        r.append('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        r.append(f'<html>\n<head>\n<meta name="viewport" content="width=device-width, initial-scale=1">')
        r.append(f'<meta http-equiv="Content-Type" content="text/html; charset=utf-8">')
        r.append(f'<title>{title}</title>\n')
        # 注入高颜值的现代 CSS，适配手机端
        r.append("""
        <style>
            body { font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 20px; background-color: #f6f8fa; color: #24292f; }
            h2 { color: #0969da; border-bottom: 1px solid #d0d7de; padding-bottom: 8px; }
            .upload-box { background: white; border: 1px dashed #0969da; padding: 20px; border-radius: 8px; margin-bottom: 20px; text-align: center; }
            .file-list { background: white; border: 1px solid #d0d7de; border-radius: 8px; list-style: none; padding: 0; }
            .file-item { display: flex; align-items: center; padding: 12px 16px; border-bottom: 1px solid #d0d7de; }
            .file-item:last-child { border-bottom: none; }
            .file-item a { color: #0969da; text-decoration: none; font-weight: 500; flex-grow: 1; word-break: break-all; }
            .file-item a:hover { text-decoration: underline; }
            .btn { background-color: #2da44e; color: white; border: none; padding: 8px 16px; font-weight: 600; border-radius: 6px; cursor: pointer; }
            .btn:hover { background-color: #2c974b; }
            input[type="file"] { margin: 8px; }
        </style>
        """)
        r.append('</head>\n<body>')
        r.append(f'<h2>📂 局域网共享目录: {displaypath}</h2>\n')
        
        # 注入极速上传卡片
        r.append('<div class="upload-box">')
        r.append('<h3>📤 极速上传文件到此目录</h3>')
        r.append('<form ENCTYPE="multipart/form-data" METHOD="POST">')
        r.append('<input NAME="file" TYPE="file"/>')
        r.append('<input class="btn" TYPE="submit" VALUE="开始上传"/>')
        r.append('</form>')
        r.append('</div>')
        
        # 渲染文件列表
        r.append('<ul class="file-list">')
        # 提供返回上级目录
        if displaypath != "/":
            r.append('<li class="file-item"><a href="..">📁 .. (返回上级目录)</a></li>')
            
        for name in sorted(dir_list):
            if name.startswith('.'):
                continue
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # 文件夹加 Emoji 图标
            if os.path.isdir(fullname):
                displayname = f"📁 {name}/"
                linkname = f"{name}/"
            else:
                displayname = f"📄 {name}"
                
            r.append(f'<li class="file-item"><a href="{linkname}">{displayname}</a></li>')
            
        r.append('</ul>\n<hr>\n</body>\n</html>\n')
        
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        f = open(path, 'wb') # 占位空写
        f.close()
        
        self.send_response(200)
        self.send_header("Content-type", f"text/html; charset={enc}")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        
        self.wfile.write(encoded)
        return None

class LANShareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("小宝局域网极速共享器")
        self.root.geometry("450x420")
        self.root.resizable(False, False)
        
        self.server = None
        self.server_thread = None
        self.is_running = False
        self.share_dir = os.path.abspath(os.path.dirname(__file__))
        self.port = 8080
        self.local_ip = self.get_local_ip()
        
        self.setup_ui()

    def get_local_ip(self):
        """自动提取电脑所在的局域网真实 IP 地址"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # 并不需要真正建立连接即可获取出口 IP
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def setup_ui(self):
        # 头部横幅
        header = tk.Label(self.root, text="🌐 局域网极速文件共享器", font=("Helvetica", 16, "bold"), fg="#0969da")
        header.pack(pady=15)
        
        # 目录选择区
        dir_frame = tk.LabelFrame(self.root, text="选择需要分享的目录", font=("Helvetica", 10, "bold"), padx=10, pady=10)
        dir_frame.pack(padx=20, fill="x")
        
        self.dir_path_label = tk.Label(dir_frame, text=self.share_dir, wraplength=380, anchor="w", fg="#24292f")
        self.dir_path_label.pack(side="left", fill="x", expand=True)
        
        select_btn = tk.Button(dir_frame, text="选择目录", command=self.select_directory, bg="#f6f8fa", relief="groove")
        select_btn.pack(side="right", padx=5)

        # 参数配置区
        param_frame = tk.Frame(self.root)
        param_frame.pack(pady=15)
        
        tk.Label(param_frame, text="共享端口: ").grid(row=0, column=0, padx=5)
        self.port_entry = tk.Entry(param_frame, width=8, justify="center")
        self.port_entry.insert(0, str(self.port))
        self.port_entry.grid(row=0, column=1, padx=5)

        # 状态控制及指示
        self.status_label = tk.Label(self.root, text="● 已停止共享", font=("Helvetica", 11, "bold"), fg="#cf222e")
        self.status_label.pack(pady=5)
        
        self.url_text = tk.Text(self.root, height=2, width=45, state="disabled", font=("Courier", 10), bg="#f6f8fa", relief="flat")
        self.url_text.pack(pady=10, padx=20)
        
        # 核心启动按钮
        self.control_btn = tk.Button(self.root, text="启动共享服务", font=("Helvetica", 12, "bold"), bg="#2da44e", fg="white",
                                     relief="flat", activebackground="#2c974b", command=self.toggle_server)
        self.control_btn.pack(pady=15, ipadx=10, ipady=5)

    def select_directory(self):
        if self.is_running:
            messagebox.showwarning("警告", "共享服务运行期间无法修改分享目录，请先停止服务。")
            return
        selected = filedialog.askdirectory(initialdir=self.share_dir)
        if selected:
            self.share_dir = os.path.abspath(selected)
            self.dir_path_label.config(text=self.share_dir)

    def start_http_server(self):
        """开启 HTTP 共享服务的线程核心逻辑"""
        # 使用闭包或局部类进行目录挂载
        dir_to_share = self.share_dir
        class CustomHTTPHandler(CustomHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=dir_to_share, **kwargs)

        try:
            self.server = TCPServer(("", self.port), CustomHTTPHandler)
            print(f"{COLOR_GREEN}[SUCCESS]{COLOR_RESET} 局域网服务在端口 {self.port} 启动")
            self.server.serve_forever()
        except Exception as e:
            self.is_running = False
            self.root.after(0, lambda: messagebox.showerror("启动失败", f"无法启动服务端口被占用，错误: {e}"))
            self.root.after(0, self.reset_ui_to_stopped)

    def toggle_server(self):
        if not self.is_running:
            # 获取并验证端口号
            try:
                self.port = int(self.port_entry.get())
            except ValueError:
                messagebox.showerror("错误", "端口号必须是 1024 - 65535 之间的整数")
                return
            
            # 开启共享
            self.is_running = True
            self.status_label.config(text=f"● 共享中 (IP: {self.local_ip}:{self.port})", fg="#2da44e")
            self.control_btn.config(text="停止共享服务", bg="#cf222e", activebackground="#a40e26")
            self.port_entry.config(state="disabled")
            
            # 写入状态指示框
            access_url = f"http://{self.local_ip}:{self.port}"
            self.url_text.config(state="normal")
            self.url_text.delete(1.0, tk.END)
            self.url_text.insert(tk.END, f"局域网设备输入以下网址直接访问:\n{access_url}")
            self.url_text.config(state="disabled")
            
            # 开启后台守护线程，避免卡死 Tkinter UI
            self.server_thread = threading.Thread(target=self.start_http_server)
            self.server_thread.daemon = True
            self.server_thread.start()
        else:
            # 停止共享
            self.is_running = False
            if self.server:
                self.server.shutdown()
                self.server.server_close()
            self.reset_ui_to_stopped()

    def reset_ui_to_stopped(self):
        self.status_label.config(text="● 已停止共享", fg="#cf222e")
        self.control_btn.config(text="启动共享服务", bg="#2da44e", activebackground="#2c974b")
        self.port_entry.config(state="normal")
        self.url_text.config(state="normal")
        self.url_text.delete(1.0, tk.END)
        self.url_text.config(state="disabled")

if __name__ == "__main__":
    app_root = tk.Tk()
    app = LANShareApp(app_root)
    
    # 窗口关闭拦截，防端口泄露
    def on_app_closing():
        if app.is_running and app.server:
            app.server.shutdown()
            app.server.server_close()
        app_root.destroy()
        
    app_root.protocol("WM_DELETE_WINDOW", on_app_closing)
    app_root.mainloop()

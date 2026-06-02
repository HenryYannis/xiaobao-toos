import tkinter as tk
from tkinter import messagebox, simpledialog
import hashlib
import datetime
import random

class SecurityApp:
    def __init__(self, master):
        self.master = master
        master.title("安全设置")
        master.geometry("400x250")
        master.resizable(False, False)
        
        # 居中显示内容
        main_frame = tk.Frame(master)
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # 标题
        title_label = tk.Label(main_frame, text="安全问题设置", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 安全问题提示
        question_label = tk.Label(main_frame, text="请设置安全问题(例如: 您的注册手机号):")
        question_label.pack(pady=(0, 10))
        
        # 输入框
        self.security_entry = tk.Entry(main_frame, width=30, font=("Arial", 12))
        self.security_entry.pack(pady=(0, 20))
        self.security_entry.focus_set()
        
        # 确认按钮
        confirm_button = tk.Button(main_frame, text="确认", width=10, 
                                  command=self.set_security_question)
        confirm_button.pack()

    def set_security_question(self):
        security_answer = self.security_entry.get().strip()
        
        # 简单验证输入不为空
        if not security_answer:
            messagebox.showerror("错误", "安全问题不能为空!")
            return
            
        # 这里可以添加更复杂的验证逻辑，如手机号格式验证
        self.security_answer = security_answer
        
        # 关闭当前窗口，打开新窗口
        self.master.destroy()
        self.open_new_window()

    def open_new_window(self):
        new_window = tk.Tk()
        new_window.title("密码找回")
        new_window.geometry("400x300")
        NewPasswordWindow(new_window, self.security_answer)

class NewPasswordWindow:
    def __init__(self, master, security_answer):
        self.master = master
        self.security_answer = security_answer
        master.title("忘记密码")
        master.geometry("400x300")
        master.resizable(False, False)
        
        # 居中显示内容
        main_frame = tk.Frame(master)
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # 标题
        title_label = tk.Label(main_frame, text="密码找回", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 提示信息
        info_label = tk.Label(main_frame, text="请输入您设置的安全问题答案:")
        info_label.pack(pady=(0, 10))
        
        # 输入框
        self.answer_entry = tk.Entry(main_frame, width=30, font=("Arial", 12))
        self.answer_entry.pack(pady=(0, 20))
        self.answer_entry.focus_set()
        
        # 按钮框架
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # 找回密码按钮
        reset_button = tk.Button(button_frame, text="找回密码", width=12,
                                command=self.reset_password)
        reset_button.pack(side=tk.LEFT, padx=10)
        
        # 返回按钮
        back_button = tk.Button(button_frame, text="返回", width=12,
                               command=self.master.destroy)
        back_button.pack(side=tk.LEFT, padx=10)

    def reset_password(self):
        entered_answer = self.answer_entry.get().strip()
        
        if entered_answer != self.security_answer:
            messagebox.showerror("错误", "安全问题答案不正确!")
            return
            
        # 生成临时密码
        temp_password = self.generate_temp_password()
        
        # 获取当前时间
        current_time = datetime.datetime.now()
        expiration_time = current_time + datetime.timedelta(hours=24)
        
        # 显示临时密码和有效期
        message = f"您的临时密码已生成: {temp_password}\n"
        message += f"该密码将在 {expiration_time.strftime('%Y-%m-%d %H:%M:%S')} 过期"
        messagebox.showinfo("临时密码", message)

    def generate_temp_password(self):
        # 结合安全问题和当前时间生成种子
        seed = f"{self.security_answer}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 使用哈希算法生成随机数
        hash_obj = hashlib.sha256(seed.encode())
        hash_hex = hash_obj.hexdigest()
        
        # 转换为整数并取模，确保是8位数字
        random_num = int(hash_hex, 16) % 100000000
        
        # 格式化为8位数字，不足前面补0
        return f"{random_num:08d}"

if __name__ == "__main__":
    root = tk.Tk()
    app = SecurityApp(root)
    root.mainloop()
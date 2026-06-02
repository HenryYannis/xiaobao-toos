import tkinter as tk
from time import strftime

class FullscreenClock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')
        self.after_id = None
        
        # 创建时间标签（添加颜色安全校验）
        self.clock_label = tk.Label(
            self.root,
            font=('ds-digital', 200),
            bg='black',
            fg='white'  # 修改为浅灰色确保可见性
        )
        self.clock_label.pack(anchor='center', pady=200)
        
        self.root.bind('<Escape>', self.safe_exit)
        self.update_time()
        
    def update_time(self):
        current_time = strftime('%H:%M:%S')
        self.clock_label.config(text=current_time)
        
        h, m, s = map(int, current_time.split(':'))
        
        # 颜色状态机逻辑
        new_color = 'white'  # 默认颜色
        if m == 59 and s >= 57:
            new_color = 'red'
            
        # 仅在颜色变化时更新配置（优化性能）
        if self.clock_label.cget('foreground') != new_color:
            self.clock_label.config(fg=new_color)
        
        self.after_id = self.root.after(1000, self.update_time)
        
    def safe_exit(self, event=None):
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.root.destroy()

if __name__ == "__main__":
    app = FullscreenClock()
    app.root.mainloop()
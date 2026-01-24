import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("井字棋")
        self.master.resizable(False, False)
        
        # 游戏状态
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'  # 玩家是X，电脑是O
        self.game_over = False
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        # 标题标签
        self.title_label = tk.Label(
            self.master, 
            text="井字棋 - 你是 X", 
            font=('Arial', 16, 'bold')
        )
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # 游戏板按钮
        self.buttons = []
        for i in range(9):
            button = tk.Button(
                self.master,
                text=' ',
                font=('Arial', 30, 'bold'),
                width=4,
                height=2,
                bg='#f0f0f0',
                activebackground='#e0e0e0',
                command=lambda i=i: self.on_click(i)
            )
            row = (i // 3) + 1
            col = i % 3
            button.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(button)
        
        # 重置按钮
        self.reset_button = tk.Button(
            self.master,
            text="重新开始",
            font=('Arial', 12),
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            command=self.reset_game
        )
        self.reset_button.grid(row=4, column=0, columnspan=3, pady=10)
        
    def on_click(self, index):
        """处理玩家点击"""
        if self.board[index] == ' ' and not self.game_over and self.current_player == 'X':
            self.make_move(index, 'X')
            
            # 检查游戏是否结束
            if not self.game_over:
                # 电脑移动
                self.master.after(500, self.computer_move)
    
    def make_move(self, index, player):
        """在指定位置下棋"""
        self.board[index] = player
        self.buttons[index].config(
            text=player,
            state='disabled',
            disabledforeground='#333' if player == 'X' else '#FF5733'
        )
        
        # 检查胜负
        winner = self.check_winner()
        if winner:
            self.game_over = True
            if winner == 'X':
                messagebox.showinfo("游戏结束", "恭喜你赢了！")
            else:
                messagebox.showinfo("游戏结束", "电脑赢了！")
            self.disable_all_buttons()
        elif ' ' not in self.board:
            self.game_over = True
            messagebox.showinfo("游戏结束", "平局！")
            self.disable_all_buttons()
    
    def computer_move(self):
        """电脑AI移动"""
        if self.game_over:
            return
        
        # 策略1：检查电脑是否能赢
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                if self.check_winner() == 'O':
                    self.make_move(i, 'O')
                    return
                self.board[i] = ' '
        
        # 策略2：阻止玩家赢
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'X'
                if self.check_winner() == 'X':
                    self.board[i] = ' '
                    self.make_move(i, 'O')
                    return
                self.board[i] = ' '
        
        # 策略3：占中心
        if self.board[4] == ' ':
            self.make_move(4, 'O')
            return
        
        # 策略4：占角落
        corners = [0, 2, 6, 8]
        available_corners = [i for i in corners if self.board[i] == ' ']
        if available_corners:
            move = random.choice(available_corners)
            self.make_move(move, 'O')
            return
        
        # 策略5：随机占空位
        available_moves = [i for i in range(9) if self.board[i] == ' ']
        if available_moves:
            move = random.choice(available_moves)
            self.make_move(move, 'O')
    
    def check_winner(self):
        """检查是否有玩家获胜"""
        # 所有获胜组合
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 行
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 列
            [0, 4, 8], [2, 4, 6]              # 对角线
        ]
        
        for pattern in win_patterns:
            a, b, c = pattern
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return self.board[a]
        
        return None
    
    def disable_all_buttons(self):
        """禁用所有按钮"""
        for button in self.buttons:
            button.config(state='disabled')
    
    def reset_game(self):
        """重置游戏"""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        
        for button in self.buttons:
            button.config(
                text=' ',
                state='normal',
                bg='#f0f0f0'
            )
        
        self.title_label.config(text="井字棋 - 你是 X")

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()

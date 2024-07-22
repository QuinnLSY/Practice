
import tkinter as tk
from tkinter import messagebox

# 定义棋盘大小
BOARD_SIZE = 15

# 初始化棋盘
board = [['+' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# 定义棋子类型
EMPTY = '+'
BLACK = '●'
WHITE = '○'

# 定义当前落子方
current_player = BLACK

# 创建主窗口
root = tk.Tk()
root.title("五子棋")
root.geometry("500x500")

# 创建棋盘
canvas = tk.Canvas(root, width=480, height=480, bg='white')
canvas.pack()

# 绘制棋盘网格
for i in range(15):
    canvas.create_line(30, 30 + i * 30, 450, 30 + i * 30)
    canvas.create_line(30 + i * 30, 30, 30 + i * 30, 450)

# 绘制棋子
def draw_piece(row, col, player):
    x = 30 + col * 30
    y = 30 + row * 30
    if player == BLACK:
        canvas.create_oval(x - 13, y - 13, x + 13, y + 13, fill='black')
    else:
        canvas.create_oval(x - 13, y - 13, x + 13, y + 13, fill='white')

# 判断是否胜利
def is_win(row, col, player):
    # 判断横向是否胜利
    count = 0
    for i in range(BOARD_SIZE):
        if board[row][i] == player:
            count += 1
            if count == 5:
                return True
        else:
            count = 0

    # 判断纵向是否胜利
    count = 0
    for i in range(BOARD_SIZE):
        if board[i][col] == player:
            count += 1
            if count == 5:
                return True
        else:
            count = 0

    # 判断左上到右下是否胜利
    count = 0
    for i in range(-4, 5):
        if 0 <= row + i < BOARD_SIZE and 0 <= col + i < BOARD_SIZE:
            if board[row + i][col + i] == player:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0

    # 判断左下到右上是否胜利
    count = 0
    for i in range(-4, 5):
        if 0 <= row - i < BOARD_SIZE and 0 <= col + i < BOARD_SIZE:
            if board[row - i][col + i] == player:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0

    return False

# 落子事件处理函数
def place_piece(event, player):
    x = event.x
    y = event.y

    col = (x - 30) // 30
    row = (y - 30) // 30

    # 判断落子位置是否合法
    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE or board[row][col] != EMPTY:
        messagebox.showinfo("提示", "落子位置不合法，请重新落子！")
        return

    # 在棋盘上落子
    board[row][col] = player

    # 绘制棋子
    draw_piece(row, col, player)

    # 判断是否胜利
    if is_win(row, col, player):
        messagebox.showinfo("提示", f"{player}获胜！")
        root.quit()

    # 切换落子方
    player = WHITE if player == BLACK else BLACK

# 绑定落子事件
canvas.bind("<Button-1>", place_piece)

# 运行主循环
root.mainloop()
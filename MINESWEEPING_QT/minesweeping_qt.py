# -*- coding:utf-8 -*-
"""
:author: 单纯同学
:time: 2023-08-08
:software: pycharm
:commentary: 基于PyQt6的扫雷游戏
"""
import random
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import QtCore
import os

_Window_ = os.path.join("window.png")
_Cover_ = os.path.join("cover.png")
_Mine_ = os.path.join("bomb.png")
_Dead_ = os.path.join("dead.png")
_Flag_ = os.path.join("flag.png")
_Space_ = ""

_EASY_ROW = 10
_EASY_COL = 10
_EASY_NUM = 10

_NORMAL_ROW = 15
_NORMAL_COL = 15
_NORMAL_NUM = 30

_HARD_ROW = 20
_HARD_COL = 20
_HARD_NUM = 75


class Main_Window(QWidget):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.resize(400, 400)
        self.setWindowTitle('扫雷')
        # self.setWindowIcon(QIcon(os.path.join("bomb.png")))
        self.image = QPixmap(_Window_)
        self.Banner = QLabel(self)
        self.Banner.setPixmap(self.image)

        # 按钮菜单
        self.Menu = QLabel(self.Banner)
        self.Menu.resize(400, 200)
        self.Menu.move(0, 200)

        self.Easy_Button = QPushButton(self.Menu)
        self.Easy_Button.setFixedSize(100, 45)
        self.Easy_Button.setText("EASY")
        self.Easy_Button.clicked.connect(lambda: self.StartGame(_EASY_ROW, _EASY_COL, _EASY_NUM))

        self.Normal_Button = QPushButton(self.Menu)
        self.Normal_Button.setFixedSize(100, 45)
        self.Normal_Button.setText("NORMAL")
        self.Normal_Button.clicked.connect(lambda: self.StartGame(_NORMAL_ROW, _NORMAL_COL, _NORMAL_NUM))

        self.Hard_Button = QPushButton(self.Menu)
        self.Hard_Button.setFixedSize(100, 45)
        self.Hard_Button.setText("HARD")
        self.Hard_Button.clicked.connect(lambda: self.StartGame(_HARD_ROW, _HARD_COL, _HARD_NUM))

        # 设置按钮位置
        self.grid_menu = QGridLayout(self.Menu)  # 网格化布局
        self.grid_menu.addWidget(self.Easy_Button, 0, 1)
        self.grid_menu.addWidget(self.Normal_Button, 1, 1)
        self.grid_menu.addWidget(self.Hard_Button, 2, 1)

    # 对话框
    def messagebox(self, title, content):
        button = QMessageBox.question(self, title, content)
        if button == QMessageBox.StandardButton.Yes:
            self.restart()
        else:
            self.close()

    # 重新开始
    def restart(self):
        os.execl(sys.executable, sys.executable, *sys.argv)  # 固定格式

    # 游戏事件处理
    def playGame(self, button, row, col, num):
        x = self.getPosition(button)[0]
        y = self.getPosition(button)[1]
        get_btn = self.grid_board.itemAtPosition(x, y).widget()
        if self.Mine[x][y] == _Mine_:
            self.showMine(row, col)
            get_btn.setIcon(QIcon(_Dead_))
            self.messagebox("Game Over", "是否重新开始？")
        else:
            self.Num(x, y, row, col)
            if self.Num(x, y, row, col) == 0:
                self.outoReveal(x, y, row, col)
        if self.Win(row, col) == num:
            self.messagebox("Game Win!", "是否再次开始？")

    # 获胜
    def Win(self, row, col):
        count = 0
        for i in range(row):
            for j in range(col):
                if self.Grid[i][j] == _Cover_:
                    count += 1
        return count

    # 计算周围炸弹数
    def Num(self, x, y, row, col):
        get_btn = self.grid_board.itemAtPosition(x, y).widget()
        get_btn.setIcon(QIcon(_Space_))
        count = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i < 0 or i > row - 1 or j < 0 or j > col - 1:
                    continue
                else:
                    if self.Mine[i][j] == _Mine_:
                        count += 1
        if count == 0:
            self.Grid[x][y] = _Space_
        else:
            get_btn.setText(str(count))
            self.Grid[x][y] = count
        return count

    # 自动展开
    def outoReveal(self, x, y, row, col):
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i < 0 or i > row - 1 or j < 0 or j > col - 1:
                    continue
                if self.Grid[i][j] != _Cover_:
                    continue
                else:
                    self.Num(i, j, row, col)
                    if self.Num(i, j, row, col) == 0:
                        self.outoReveal(i, j, row, col)

    # 触发炸弹，显示所有炸弹
    def showMine(self, row, col):
        for i in range(row):
            for j in range(col):
                if self.Mine[i][j] == _Mine_:
                    mine_btn = self.grid_board.itemAtPosition(i, j).widget()
                    mine_btn.setIcon(QIcon(_Mine_))

    # 正式游戏界面初始化
    def StartGame(self, row, col, num):
        self.Grid = [[0 for i in range(row)] for j in range(col)]  # 按钮地基
        self.Mine = [[0 for i in range(row)] for j in range(col)]  # 雷区
        self.init(self.Grid, row, col)
        self.init(self.Mine, row, col)
        self.setMine(num, row, col)
        self.ShowBoard(row, col, num)

    # 初始化未开按钮
    def init(self, list, row, col):
        for i in range(row):
            for j in range(col):
                list[i][j] = _Cover_

    # 部雷
    def setMine(self, num, row, col):
        count = 0
        while count < num:
            x = random.randint(0, row - 1)
            y = random.randint(0, col - 1)
            if self.Mine[x][y] != _Mine_:
                self.Mine[x][y] = _Mine_
                count += 1

    # 显示面板
    def ShowBoard(self, row, col, num):
        self.Banner.close()
        self.grid_board = QGridLayout(self)
        self.grid_board.setSpacing(1)
        for i in range(row):
            for j in range(col):
                self.button = QPushButton(self)
                self.button.setFixedSize(30, 40)
                self.button.setIcon(QIcon(self.Grid[i][j]))
                btn = self.button
                self.button.clicked.connect(lambda playGame, button=btn: self.playGame(button, row, col, num))  # 关联点击事件
                self.grid_board.addWidget(self.button, i, j)

    # 获取按钮坐标
    def getPosition(self, button):
        btn_index = self.grid_board.indexOf(button)
        position = self.grid_board.getItemPosition(btn_index)
        return position


def main():
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

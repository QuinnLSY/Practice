# -*- coding:utf-8 -*-
import random

from Tetromino_List import *
import pygame
from Board import *

Game_Board = Board()


class Tetromino():
    def __init__(self) -> None:
        super().__init__()
        self.tetromino = random.choice(TETROMINO)  # 随机选择初始方块
        self.position = 3  # 初始横向位置
        self.rotation = 0  # 初始旋转样式
        self.dpos = 0  # 初始下落位置

    # 画方块，tetromino为三位数组，[旋转样式,方块行,方块列]
    def Draw(self, surface, tetromino):
        # 画出当前方块
        for i in range(len(tetromino[self.rotation][0])):  # 列
            for j in range(len(tetromino[self.rotation])):  # 行
                if tetromino[self.rotation][j][i] == '1':
                    pygame.draw.rect(surface, self.tetromino[4], ((i + self.position) * SIZE, (j + int(self.dpos)) * SIZE, SIZE - 1, SIZE - 1))
                    # 下方有堆积的方块时，记录当前方块位置在board上，并重新生成一个新的方块
                    if (j + int(self.dpos) + 1) < ROW and Game_Board.board[i + self.position][j + int(self.dpos) + 1]:
                        for x in range(len(tetromino[self.rotation])):
                            for y in range(len(tetromino[self.rotation][0])):
                                if tetromino[self.rotation][x][y] == '1':
                                    Game_Board.board[y + self.position][x + int(self.dpos)] = 1
                        self.Next_tetro()

        self.Put_into_board(tetromino, self.Bottom_Index(self.tetromino))
        # self.dpos += 1

    # 获取方块有色部分的左侧刻度
    def Left_Index(self, tetromino):
        for i in range(len(tetromino[self.rotation][0])):  # 列
            for j in range(len(tetromino[self.rotation])):  # 行
                if tetromino[self.rotation][j][i] == '1':
                    return i

    # 获取方块有色部分的右侧刻度
    def Right_Index(self, tetromino):
        right = 0
        for i in range(len(tetromino[self.rotation][0])):  # 列
            for j in range(len(tetromino[self.rotation])):  # 行
                if tetromino[self.rotation][j][i] == '1':
                    right = i
        return right

    # 获取方块有色部分的底部刻度
    def Bottom_Index(self, tetromino):
        bottom = 0
        for i in range(len(tetromino[self.rotation][0])):  # 列
            for j in range(len(tetromino[self.rotation])):  # 行
                if tetromino[self.rotation][j][i] == '1':
                    if bottom < j:
                        bottom = j
        return bottom

    # 左碰撞监测，左边(-1)有board记录的方块时不可左移
    def Collide_left(self, tetromino):
        for i in range(len(tetromino[self.rotation][0])):  # 列
            for j in range(len(tetromino[self.rotation])):  # 行
                if tetromino[self.rotation][j][i] == '1':
                    if i + self.position - 1 > 0 and Game_Board.board[i + self.position - 1][j + int(self.dpos)]:
                        return True

    # 右碰撞监测，右边(+1)有board记录的方块时不可右移
    def Collide_right(self, tetromino):
        for i in range(len(tetromino[self.rotation][0])):  # 列
            for j in range(len(tetromino[self.rotation])):  # 行
                if tetromino[self.rotation][j][i] == '1':
                    if i + self.position + 1 < COL and Game_Board.board[i + self.position + 1][j + int(self.dpos)]:
                        return True

    # 右旋转碰撞监测，以右旋的下一个样式是否与当前board重叠来判断是否可旋转(即self.rotation + 1)
    def Collide_rotation_L(self, tetromino):
        if self.rotation < 3:
            for i in range(len(tetromino[self.rotation + 1][0])):  # 列
                for j in range(len(tetromino[self.rotation + 1])):  # 行
                    if tetromino[self.rotation + 1][j][i] == '1' and Game_Board.board[i + self.position][j + int(self.dpos)]:
                        return True
        if self.rotation == 3:
            for i in range(len(tetromino[0][0])):  # 列
                for j in range(len(tetromino[0])):  # 行
                    if tetromino[0][j][i] == '1' and Game_Board.board[i + self.position][j + int(self.dpos)]:
                        return True

    # 左旋转碰撞监测，以左旋的上一个样式是否与当前board重叠来判断是否可旋转(即self.rotation - 1)
    def Collide_rotation_J(self, tetromino):
        if self.rotation <= 3:
            for i in range(len(tetromino[self.rotation - 1][0])):  # 列
                for j in range(len(tetromino[self.rotation - 1])):  # 行
                    if tetromino[self.rotation - 1][j][i] == '1' and Game_Board.board[i + self.position][j + int(self.dpos)]:
                        return True
        if self.rotation == 0:
            for i in range(len(tetromino[3][0])):  # 列
                for j in range(len(tetromino[3])):  # 行
                    if tetromino[3][j][i] == '1' and Game_Board.board[i + self.position][j + int(self.dpos)]:
                        return True

    # 触底保留方块
    def Put_into_board(self, tetromino, j):
        if j + int(self.dpos) == ROW - 1:  # 触底
            for x in range(len(tetromino[self.rotation])):  # 列
                for y in range(len(tetromino[self.rotation][0])):
                    if tetromino[self.rotation][x][y] == '1':
                        Game_Board.board[y + self.position][x + int(self.dpos)] = 1
            self.Next_tetro()

    # 生成新的方块
    def Next_tetro(self):
        # 重新初始化
        self.tetromino = random.choice(TETROMINO)
        self.position = 3
        self.rotation = 0
        self.dpos = 0

    def Update(self, surface):
        self.Draw(surface, self.tetromino)
        self.dpos += 0.1  # 用小数来避免刷新速度过快的问题，用转换为int的方法使方块以SIZE为单位移动(涮新十次才会移动一格)

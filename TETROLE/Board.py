# -*- coding:utf-8 -*-
import pygame
import numpy as np

COL = 10
ROW = 25
SIZE = 35  # 网格大小
SCORE_FIELD = 8  # 分数显示占格大小
COLOR_NONE = "#3c3c3c"
SCORE_POS = (int(COL + 0.5 * SCORE_FIELD) * SIZE, 2 * SIZE)
NOTE1_POS = (int(COL + 0.5 * SCORE_FIELD) * SIZE, 12 * SIZE)
NOTE2_POS = (int(COL + 0.5 * SCORE_FIELD) * SIZE, 13 * SIZE)
OPTION1_POS = (int(COL + 0.5 * SCORE_FIELD) * SIZE, 8 * SIZE)
OPTION2_POS = (int(COL + 0.5 * SCORE_FIELD) * SIZE, 9 * SIZE)
TIP_POS = (int(COL + SCORE_FIELD) * 0.5 * SIZE, 12 * SIZE)

class Board():
    def __init__(self):
        super().__init__()
        # self.score_font_rect = None
        # self.score_font = None
        self.board = np.zeros((COL, ROW))  # 注意⚠️：列在前，行在后，在画网格及Tetromino方法中极需注意
        self.score = 0

    # 加载底面网格
    def Load_Game(self, surface):
        for j in range(COL):
            for i in range(ROW):
                if self.board[j][i] == 0:
                    pygame.draw.rect(surface, COLOR_NONE, (j * SIZE, i * SIZE, SIZE - 1, SIZE - 1))  # x坐标依列j变化，y坐标依行i变化
                if self.board[j][i] == 1:
                    pygame.draw.rect(surface, 'red', (j * SIZE, i * SIZE, SIZE - 1, SIZE - 1))

    # 消除连成一线的行，并记一分
    def Get_score(self):
        for i in range(ROW):
            count = 0
            for j in range(COL):
                if self.board[j][i] == 1:
                    count += 1
            if count == COL:
                for j in range(COL):
                    self.board[j][i] = 0
                self.score += 1
                for m in range(i, 0, -1):  # 逆向遍历
                    for n in range(COL):
                        self.board[n][m] = self.board[n][m-1]

    # 加载侧边栏
    def Load_side(self, surface):
        for j in range(COL, COL + SCORE_FIELD):
            for i in range(ROW):
                pygame.draw.rect(surface, COLOR_NONE, (j * SIZE, i * SIZE, SIZE, SIZE))

        self.score_font = pygame.font.Font('cartoon.ttf', 80).render(str(self.score), True, 'white')
        self.score_rect = self.score_font.get_rect(center=SCORE_POS)
        surface.blit(self.score_font, self.score_rect)
        self.option1 = pygame.font.Font('cartoon.ttf', 20).render("A向左移动，D向右移动", True, 'green')
        self.option1_rect = self.option1.get_rect(center=OPTION1_POS)
        surface.blit(self.option1, self.option1_rect)
        self.option2 = pygame.font.Font('cartoon.ttf', 20).render("J向左旋转，L向右旋转", True, 'yellow')
        self.option2_rect = self.option2.get_rect(center=OPTION2_POS)
        surface.blit(self.option2, self.option2_rect)
        self.note1 = pygame.font.Font('cartoon.ttf', 20).render("按空格键暂停游戏", True, 'white')
        self.note1_rect = self.note1.get_rect(center=NOTE1_POS)
        surface.blit(self.note1, self.note1_rect)
        # self.note2 = pygame.font.Font('cartoon.ttf', 20).render("按回车键重新开始", True, 'white')
        # self.note2_rect = self.note2.get_rect(center=NOTE2_POS)
        # surface.blit(self.note2, self.note2_rect)

    # 判断游戏结束
    def Game_Over(self):
        for i in range(COL):
            if self.board[i][0] == 1:
                return True

    # 重新开始提示
    def Ask(self, surface):
        pygame.draw.rect(surface, 'black', (0, 9 * SIZE, 18 * SIZE, 6 * SIZE))
        self.tip = pygame.font.Font('cartoon.ttf', 76).render("按回车键重新开始", True, 'white')
        self.tip_rect = self.tip.get_rect(center=TIP_POS)
        surface.blit(self.tip, self.tip_rect)

    # 重新开始
    def Restart(self):
        self.board = np.zeros((COL, ROW))
        self.score = 0

    def Update(self, surface):
        self.Load_Game(surface)
        self.Load_side(surface)
        self.Get_score()

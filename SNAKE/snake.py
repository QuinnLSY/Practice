# -*- coding:utf-8 -*-
"""
:author: 单纯同学
:time: 2023-08-02
:software: pycharm
"""

import pygame
import random
import sys

FPS = 10
WEIGHT = 600
HEIGHT = 600
COLOR = [255, 255, 255]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
BLACK = [0, 0, 0]

pygame.init()
screen = pygame.display.set_mode((WEIGHT, HEIGHT))
pygame.display.set_caption('贪吃蛇')
clock = pygame.time.Clock()


# 显示文字
def draw_text(surf, text, size, x, y, color, font_bold=False, font_italic=False):
    # 获取系统字体，设置字体大小
    font = pygame.font.Font('font.ttf', size)
    # 是否加粗
    font.set_bold(font_bold)
    # 是否斜体
    font.set_italic(font_italic)

    surf_text = font.render(text, True, color)  # 渲染文字，获取文字对象
    text_rect = surf_text.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(surf_text, text_rect)


# 蛇类
class Snake(object):
    def __init__(self):
        self.dirction = pygame.K_RIGHT  # 初始方向
        self.body = []  # 组成块的起始坐标：25x25
        for i in range(3):
            self.addnode()

    def addnode(self):  # 增加身体
        left, top = (0, 0)
        if self.body:
            left, top = (self.body[0].left, self.body[0].top)
        node = pygame.Rect(left, top, 25, 25)
        if self.dirction == pygame.K_RIGHT:
            node.left += 25
        elif self.dirction == pygame.K_LEFT:
            node.left -= 25
        elif self.dirction == pygame.K_UP:
            node.top -= 25
        elif self.dirction == pygame.K_DOWN:
            node.top += 25
        self.body.insert(0, node)

    def delnode(self):  # 删除身体
        self.body.pop()

    def isdead(self):  # 判断死亡
        if self.body[0].x not in range(WEIGHT):
            return True
        if self.body[0].y not in range(HEIGHT):
            return True
        if self.body[0] in self.body[1:]:  # 撞自己
            return True
        return False

    def move(self):  # 移动,以区域亮起为前进，而不是将图形移动
        self.addnode()
        self.delnode()

    def change_dirc(self, press):  # 改变方向
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if press in LR + UD:
            if (press in LR) and (self.dirction in LR):
                return
            if (press in UD) and (self.dirction in UD):
                return
            self.dirction = press


# 食物类
class Food:
    def __init__(self):
        self.rect = pygame.Rect(-25, 0, 25, 25)  # 第一次默认位置，创建对象用

    def remove(self):
        self.rect.x = -25  # 移出画面以消失

    def set(self):  # 出现位置
        if self.rect.x == -25:
            allops = []  # 以25为单位，可出现坐标刻度(x，y通用)
            for pos in range(25, WEIGHT - 25, 25):
                allops.append(pos)
            self.rect.x = random.choice(allops)
            self.rect.y = random.choice(allops)


# snake = Snake()
# food = Food()

score = 0  # 得分
isdead = False  # 是否死亡
start = True  # 是否重开游戏的判断变量
running = True  # 设置运行变量，及时打断while循环，快速退出程序
while running:
    clock.tick(FPS)
    if start:
        score = 0
        snake = Snake()
        food = Food()
        start = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()  # 从系统层面直接退出，无循环卡顿问题
        if event.type == pygame.KEYDOWN:
            snake.change_dirc(event.key)
            if event.key == pygame.K_SPACE and isdead:  # 重新开始
                start = True

    screen.fill(COLOR)

    if not isdead:
        snake.move()
    # 绘制蛇身
    pygame.draw.rect(screen, [50, 50, 10], snake.body[0], 0)
    for rect in snake.body[1:]:
        pygame.draw.rect(screen, [20, 220, 39], rect, 0)

    isdead = snake.isdead()
    if isdead:
        draw_text(screen, 'YOU DEAD!', 60, WEIGHT / 2, HEIGHT / 3, RED)
        draw_text(screen, '按空格键重新开始...', 20, WEIGHT / 2, HEIGHT / 3 + 70, BLACK)

    #  吃到食物
    if food.rect == snake.body[0]:
        score += 50
        food.remove()
        snake.addnode()
    food.set()
    pygame.draw.rect(screen, RED, food.rect, 0)
    draw_text(screen, 'score:' + str(score), 20, WEIGHT / 2, 10, BLACK)

    pygame.display.update()
pygame.quit()

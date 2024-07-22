# -*- coding:utf-8 -*-
"""
:author: 单纯同学
:time: 2023-08-18
:software: pycharm
:commentary: 超级马里奥--工具及游戏主控
"""
import os

import pygame
import random
import sys
from SUPER_MARIO.source.constants import *
from SUPER_MARIO.source.setup import *
# pygame.font.init()
# # 定义颜色
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# show_popup = False
# # 创建字体
# font1 = pygame.font.Font(FONT, 24)
#
# # 弹框和按钮的布局
# popup_rect = pygame.Rect(SCREEN_W // 2 - 150, SCREEN_H // 2 - 75, 300, 150)
# yes_button_rect = pygame.Rect(SCREEN_W // 2 - 75, SCREEN_H // 2 - 25, 75, 30)
# no_button_rect = pygame.Rect(SCREEN_W // 2 + 25, SCREEN_H // 2 - 25, 75, 30)
#
#
# def draw_popup(SCREEN):
#     # 绘制弹框背景
#     pygame.draw.rect(SCREEN, BLACK, popup_rect, 2)  # 2 表示线条粗细
#
#     # 绘制文本
#     popup_text = font1.render("是否退出游戏？", True, WHITE)
#     SCREEN.blit(popup_text, (popup_rect.x + 10, popup_rect.y + 10))
#
#     # 绘制按钮
#     pygame.draw.rect(SCREEN, RED, yes_button_rect)
#     pygame.draw.rect(SCREEN, GREEN, no_button_rect)
#
#     # 绘制按钮文本
#     yes_text = font1.render("是", True, WHITE)
#     no_text = font1.render("否", True, WHITE)
#     SCREEN.blit(yes_text, (yes_button_rect.x + 10, yes_button_rect.y + 5))
#     SCREEN.blit(no_text, (no_button_rect.x + 10, no_button_rect.y + 5))

class Game:
    def __init__(self, state_dict, start_state):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()  # 为下面run中state.update顺利更新，需在前传入键值，否则无法更新
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]

    def update(self):
        if self.state.finished:
            game_info = self.state.game_info
            next_state = self.state.next
            self.state.finished = False
            self.state = self.state_dict[next_state]
            self.state.start(game_info)
        self.state.update(self.screen, self.keys)  # state是MainMenu()的当前界面对象，定义在main.py

    def run(self):
        global show_popup
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                    # if event.key == pygame.K_ESCAPE:
                    #     show_popup = True
                elif event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()
            # # 检测鼠标点击事件
            # mouse_pos = pygame.mouse.get_pos()
            # if show_popup:
            #     for button_rect in (yes_button_rect, no_button_rect):
            #         if button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            #             if button_rect == yes_button_rect:
            #                 self.state.next = 'main_menu'
            #                 self.state.finished = True
            #             else:
            #                 show_popup = False
            #
            # # 填充背景色
            # self.screen.fill(BLACK)
            #
            # # 绘制弹框
            # if show_popup:
            #     draw_popup(self.screen)

            # self.screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            # image = get_image(GRAPHICS['mario_bros'], 145, 32, 16, 16, (0, 0, 0), 5)
            # self.screen.blit(image, (300, 300))
            self.update()
            pygame.display.update()
            self.clock.tick(FPS)


# 载入图片
def load_graphics(path, accept=('.jpg', '.png', '.bmp', '.gif')):
    graphics = {}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)  # 拆成 文件名，后缀
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(path, pic))
            if img.get_alpha():  # 透明背景，加快图像渲染
                img = img.convert_alpha()
            else:
                img = img.convert()
            graphics[name] = img
    return graphics


# 画出图片
def get_image(sheet, x, y, width, height, colorkey, scale):
    """
    从给定的图像表中提取指定区域的图像，并应用颜色键和缩放。

    参数:
    sheet: 图像表，包含多个图像的Surface对象。
    x: 提取区域的左上角x坐标。
    y: 提取区域的左上角y坐标。
    width: 提取区域的宽度。
    height: 提取区域的高度。
    colorkey: 颜色键，用于透明化图像中指定颜色的像素。
    scale: 缩放因子，用于放大或缩小图像。

    返回:
    返回提取并处理后的图像Surface对象。
    """
    # 创建一个与提取区域大小相同的空白Surface对象,pygame.SRCALPHA表示创建的Surface对象支持透明,另一处在level创建背景时使用
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    # 从sheet中提取指定区域的图像，并将其复制到新创建的imageSurface上
    image.blit(sheet, (0, 0), (x, y, width, height))
    # 设置image的透明色，即colorkey参数指定的颜色
    image.set_colorkey(colorkey)
    # 对image进行缩放，使其大小变为原图的scale倍，并返回缩放后的图像
    image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
    return image


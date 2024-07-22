# -*- coding:utf-8 -*-
"""
:author: 单纯同学
:time: 2023-08-21
:software: pycharm
:commentary: 超级马里奥--载入游戏，正式开始游戏
"""
import pygame
from SUPER_MARIO.source.states.main_menu import *


class LoadScreen:
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'level'
        self.druation = 2000  # 持续显示时间
        self.timer = 0
        self.info = Info('load_screen', self.game_info)

    def update(self, surface, keys):
        self.draw(surface)
        if self.timer == 0:
            self.timer = pygame.time.get_ticks()  # 计时
        if pygame.time.get_ticks() - self.timer > 2000:  # 等待两秒后转入正式关卡界面
            self.finished = True
            self.game_info['start_time'] = pygame.time.get_ticks()
            self.game_info['play_time'] = 0
            self.timer = 0

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.info.update()  # 金币闪烁
        self.info.draw(surface)


class GameOver(LoadScreen):
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'main_menu'
        self.timer = 0
        self.druation = 4000
        self.info = Info('game_over', self.game_info)

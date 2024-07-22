# -*- coding:utf-8 -*-
"""
:author: 单纯同学
:time: 2023-08-18
:software: pycharm
:commentary: 超级马里奥--显示的文字信息
"""
import pygame
from SUPER_MARIO.source.constants import *
from SUPER_MARIO.source.components.coin import *
from SUPER_MARIO.source.components.player import *

pygame.font.init()


class Info:
    def __init__(self, state, game_info):
        self.state = state
        self.game_info = game_info
        self.create_state_labels()
        self.create_info_labels()
        self.flash_coin = FlashingCoin()
        self.i = 0

    # 游戏状态信息（主界面，过渡页...)
    def create_state_labels(self):
        self.state_labels = []
        if self.state == 'main_menu':
            self.state_labels.append((self.create_label('1 PLAYER GAME'), (272, 363)))
            self.state_labels.append((self.create_label('2 PLAYER GAME'), (272, 408)))
            self.state_labels.append((self.create_label('TOP-000000'), (290, 468)))
        elif self.state == 'load_screen':
            self.state_labels.append((self.create_label('WORLD'), (280, 200)))
            self.state_labels.append((self.create_label('1-1'), (430, 200)))
            self.state_labels.append((self.create_label('X  {}'.format(self.game_info['lives'])), (380, 280)))
            self.player_image = get_image(GRAPHICS['mario_bros'], 178, 32, 12, 16, (0, 0, 0), BG_MULTI)
        elif self.state == 'game_over':
            self.state_labels.append((self.create_label('GAME OVER'), (280, 300)))

    # 游戏过程信息(得分，时间，...)
    def create_info_labels(self):
        self.info_labels = []
        self.info_labels.append((self.create_label('MARIO'), (70, 30)))
        self.info_labels.append((self.create_label('WORLD'), (455, 30)))
        self.info_labels.append((self.create_label('TIME'), (625, 30)))
        self.info_labels.append((self.create_label('000000'), (70, 55)))
        self.info_labels.append((self.create_label('X00'), (305, 55)))
        self.info_labels.append((self.create_label('1-1'), (480, 55)))
        self.info_labels.append((self.create_label('{} S'.format(self.game_info['play_time'])), (625, 55)))
    # 上述两个方法通用调用方法

    def create_label(self, label, size=20, width_scale=1.25, height_scale=1):
        font = pygame.font.Font(FONT, size)
        label_image = font.render(label, True, (255, 255, 255))
        # 放大产生锯齿化效果
        rect = label_image.get_rect()
        label_image = pygame.transform.scale(label_image, (int(rect.width*width_scale), int(rect.height*height_scale)))
        label_image = label_image.convert_alpha()
        return label_image

    def update(self):
        self.flash_coin.update()
        # 如何实时更新play_time
        if self.state == 'level':
            # self.game_info['play_time'] = (pygame.time.get_ticks() - self.game_info['start_time'])/1000
            # 计算游戏已进行的时间（以秒为单位），并保留一位小数
            self.game_info['play_time'] = round((pygame.time.get_ticks() - self.game_info['start_time']) / 1000, 1)

            self.info_labels.remove(self.info_labels[5 + (++self.i)])
            self.info_labels.append((self.create_label('{} S'.format(self.game_info['play_time'])), (625, 55)))

    def draw(self, surface):
        for label in self.state_labels:
            surface.blit(label[0], label[1])
        for label in self.info_labels:
            surface.blit(label[0], label[1])
        surface.blit(self.flash_coin.image, self.flash_coin.rect)
        if self.state == 'load_screen':
            surface.blit(self.player_image, (300, 270))

# -*- coding:utf-8 -*-
"""
:author: 单纯同学
:time: 2023-08-21
:software: pycharm
:commentary: 超级马里奥--金币管理
"""
import pygame
from SUPER_MARIO.source.setup import *
from SUPER_MARIO.source.tools import *


class FlashingCoin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        self.frame_index = 0
        frame_rects = [(1, 160, 5, 8), (9, 160, 5, 8), (17, 160, 5, 8), (9, 160, 5, 8)]  # 多图切换,抠图位置及大小
        self.load_frames(frame_rects)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = 280  # 金币在主菜单的位置
        self.rect.y = 54
        self.timer = 0

    def load_frames(self, frame_rects):
        sheet = GRAPHICS['item_objects']
        for frame_rect in frame_rects:
            self.frames.append(get_image(sheet, *frame_rect, (0, 0, 0), BG_MULTI))

    def update(self):
        """
        更新角色动画的状态。

        该方法通过控制帧索引来实现动画效果。它根据当前时间与上一帧时间的差值来决定是否进入下一帧。
        如果时间差大于当前帧的持续时间，则帧索引增加，并循环回到开始，以实现动画的连续播放。
        """

        # 获取当前时间，用于计算时间差，以控制动画播放速度
        self.current_time = pygame.time.get_ticks()

        # 定义每一帧的持续时间，单位为毫秒
        frame_durations = [375, 125, 125, 125]

        # 如果计时器为0，初始化计时器为当前时间
        if self.timer == 0:
            self.timer = self.current_time
        # 如果当前时间与上一帧时间差大于当前帧应展示的时间
        elif self.current_time - self.timer > frame_durations[self.frame_index]:
            # 进入下一帧
            self.frame_index += 1
            # 确保帧索引不会超过帧总数
            self.frame_index %= 4
            # 更新计时器为当前时间，准备计算下一帧的时间差
            self.timer = self.current_time

        # 根据当前的帧索引更新角色图像
        self.image = self.frames[self.frame_index]


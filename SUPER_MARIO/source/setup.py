# -*- coding:utf-8 -*-
"""
:author: 单纯同学
:time: 2023-08-18
:software: pycharm
:commentary: 超级马里奥--游戏启动模块
"""
import pygame
from SUPER_MARIO.source.constants import *
from SUPER_MARIO.source.tools import *

pygame.init()
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("超级马里奥兄弟")

GRAPHICS = load_graphics('resources/graphics')
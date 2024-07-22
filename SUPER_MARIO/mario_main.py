# -*- coding:utf-8 -*-
"""
:author: 单纯同学
:time: 2023-08-18
:software: pycharm
:commentary: 超级马里奥--启动游戏
"""

import pygame

from SUPER_MARIO.source.states.main_menu import *
from SUPER_MARIO.source.tools import *
from SUPER_MARIO.source.setup import *
from SUPER_MARIO.source.states.load_screen import *
from SUPER_MARIO.source.states.level import *


def main():
    state_dict = {
        'main_menu': MainMenu(),
        'load_screen': LoadScreen(),
        'level': Level(),
        'game_over': GameOver()
    }
    game = Game(state_dict, 'main_menu')
    game.run()


if __name__ == '__main__':
    main()

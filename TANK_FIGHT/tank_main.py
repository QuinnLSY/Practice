# encoding : utf-8
from gameloop import *
from pygame import *
import pygame, sys, time

if __name__ == '__main__':
    player = game()  # 声明一个类对象
    # player.game_start('KEEP-GOING')  # 调用开始函数
    while player.playing:  # 进入游戏运行
        # player.new()  # 开始游戏
        player.game_start('KEEP-GOING')
    # screen.fill(black)
    # player.game_start('GAME-OVER')  # 游戏结束
    # time.sleep(1.5)  # 可以不要
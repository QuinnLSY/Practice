# -*- coding:utf-8 -*-
"""
:author: 单纯同学
:time: 2023-08-10
:software: pycharm
:commentary: 俄罗斯方块
"""

import pygame
import sys
from Board import *
from Tetromino import *

Game_On = True
SPACE = False

pygame.init()
screen = pygame.display.set_mode(((COL + SCORE_FIELD) * SIZE, ROW * SIZE))
clock = pygame.time.Clock()

My_Tetromino = Tetromino()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if Game_On:
                    if not SPACE:
                        SPACE = True
                    else:
                        SPACE = False
            if event.key == pygame.K_RETURN:
                if not Game_On:
                    Game_On = True
                    Game_Board.Restart()
            # 左右移动，边界判断
            if event.key == pygame.K_a and (My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) > 0 and not My_Tetromino.Collide_left(My_Tetromino.tetromino):
                My_Tetromino.position -= 1
            if event.key == pygame.K_d and (My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) < COL - 1 and not My_Tetromino.Collide_right(My_Tetromino.tetromino):
                My_Tetromino.position += 1
            # 旋转碰撞禁止
            if event.key == pygame.K_j:
                # 与边界的碰撞
                # L型方块
                if My_Tetromino.tetromino == L and My_Tetromino.rotation == 0 and (My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) == 0:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == L and My_Tetromino.rotation == 2 and (My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) == COL - 1:
                    My_Tetromino.rotation = My_Tetromino.rotation
                # J型方块
                elif My_Tetromino.tetromino == J and My_Tetromino.rotation == 0 and (My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) == 0:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == J and My_Tetromino.rotation == 2 and (My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) == 0:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == J and My_Tetromino.rotation == 2 and (My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) == COL - 1:
                    My_Tetromino.rotation = My_Tetromino.rotation
                # I型方块
                elif My_Tetromino.tetromino == I and My_Tetromino.rotation == 0 and (
                        My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) <= 1:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == I and My_Tetromino.rotation == 2 and (
                        My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) <= 1:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == I and My_Tetromino.rotation == 0 and (
                        My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) >= COL - 2:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == I and My_Tetromino.rotation == 2 and (
                        My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) >= COL - 2:
                    My_Tetromino.rotation = My_Tetromino.rotation
                # Z型方块
                elif My_Tetromino.tetromino == Z and My_Tetromino.rotation == 1 and (
                        My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) == 0:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == Z and My_Tetromino.rotation == 3 and (
                        My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) == COL - 1:
                    My_Tetromino.rotation = My_Tetromino.rotation
                # S型方块
                elif My_Tetromino.tetromino == S and My_Tetromino.rotation == 1 and (
                        My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) == 0:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == S and My_Tetromino.rotation == 3 and (
                        My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) == 0:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == S and My_Tetromino.rotation == 1 and (
                        My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) == COL - 1:
                    My_Tetromino.rotation = My_Tetromino.rotation
                # T型方块
                elif My_Tetromino.tetromino == T and My_Tetromino.rotation == 1 and (
                        My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) == 0:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == T and My_Tetromino.rotation == 3 and (
                        My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) == COL - 1:
                    My_Tetromino.rotation = My_Tetromino.rotation
                # 与其他方块的碰撞
                elif My_Tetromino.Collide_rotation_J(My_Tetromino.tetromino):
                    My_Tetromino.rotation = My_Tetromino.rotation
                else:
                    My_Tetromino.rotation = My_Tetromino.rotation - 1
                # 旋转循环
                if My_Tetromino.rotation < 0:
                    My_Tetromino.rotation = 3

            elif event.key == pygame.K_l:
                # 与边界的碰撞
                # L型方块
                if My_Tetromino.tetromino == L and My_Tetromino.rotation == 2 and (My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) == 0:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == L and My_Tetromino.rotation == 0 and (My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) == COL - 1:
                    My_Tetromino.rotation = My_Tetromino.rotation
                # J型方块
                elif My_Tetromino.tetromino == J and My_Tetromino.rotation == 0 and (My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) == 0:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == J and My_Tetromino.rotation == 2 and (My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) == 0:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == J and My_Tetromino.rotation == 0 and (My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) == COL - 1:
                    My_Tetromino.rotation = My_Tetromino.rotation
                # I型方块
                elif My_Tetromino.tetromino == I and My_Tetromino.rotation == 0 and (My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) == 0:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == I and My_Tetromino.rotation == 2 and (My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) <= 1:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == I and My_Tetromino.rotation == 0 and (My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) >= COL - 2:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == I and My_Tetromino.rotation == 2 and (My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) == COL - 1:
                    My_Tetromino.rotation = My_Tetromino.rotation
                # Z型方块
                # elif My_Tetromino.tetromino == Z and My_Tetromino.rotation == 1 and (My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) == 0:
                #     My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == Z and My_Tetromino.rotation == 3 and (My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) == 0:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == Z and My_Tetromino.rotation == 1 and (My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) == COL - 1:
                    My_Tetromino.rotation = My_Tetromino.rotation
                # elif My_Tetromino.tetromino == Z and My_Tetromino.rotation == 3 and (My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) == COL - 1:
                #     My_Tetromino.rotation = My_Tetromino.rotation
                # S型方块
                elif My_Tetromino.tetromino == S and My_Tetromino.rotation == 1 and (My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) == 0:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == S and My_Tetromino.rotation == 3 and (My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) == COL - 1:
                    My_Tetromino.rotation = My_Tetromino.rotation
                # T型方块
                elif My_Tetromino.tetromino == T and My_Tetromino.rotation == 1 and (My_Tetromino.Left_Index(My_Tetromino.tetromino) + My_Tetromino.position) == 0:
                    My_Tetromino.rotation = My_Tetromino.rotation
                elif My_Tetromino.tetromino == T and My_Tetromino.rotation == 3 and (My_Tetromino.Right_Index(My_Tetromino.tetromino) + My_Tetromino.position) == COL - 1:
                    My_Tetromino.rotation = My_Tetromino.rotation

                # 与其他方块的碰撞
                elif My_Tetromino.Collide_rotation_L(My_Tetromino.tetromino):
                    My_Tetromino.rotation = My_Tetromino.rotation
                else:
                    My_Tetromino.rotation = My_Tetromino.rotation + 1
                # 旋转循环
                if My_Tetromino.rotation > 3:
                    My_Tetromino.rotation = 0

    if Game_On:
        if not SPACE:
            screen.fill("#ffffff")
            Game_Board.Update(screen)
            My_Tetromino.Update(screen)
            # My_Tetromino.Draw(screen, My_Tetromino.tetromino)

            if Game_Board.Game_Over():
                Game_Board.Ask(screen)
                Game_On = False
            pygame.display.update()

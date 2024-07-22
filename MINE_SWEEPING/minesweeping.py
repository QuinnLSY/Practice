# -*- coding:utf-8 -*-
"""
:author: 单纯同学
:time: 2023-08-04
:software: pycharm
:commentary: 扫雷游戏主题
"""


import pygame
import os
import sys
from time import sleep
from tkinter import messagebox

class Game:
    def __init__(self, board, screenSize):
        self.board = board
        self.screenSize = screenSize
        self.pieceSize = (self.screenSize[0]//self.board.getSize()[1], (self.screenSize[1])//self.board.getSize()[0])
        self.loadImages()
        self.running = True

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize)
        # pygame.draw.rect(self.screen, [255, 255, 255], (0, 740, 800, 60), 0)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    rightClick = pygame.mouse.get_pressed()[2]
                    self.handleClick(position, rightClick)
            self.draw()
            pygame.display.flip()
            if self.board.getWon():
                sound = pygame.mixer.Sound("win.wav")
                sound.play()
                sleep(3)
                self.running = False
            if self.board.getLost():
                sound = pygame.mixer.Sound("lost.wav")
                sound.play()
                sleep(1)
                self.running = False
        pygame.quit()

    # 根据获取的图片绘制piece
    def draw(self):
        topLeft = (0, 0)
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                piece = self.board.getPiece((row, col))
                image = self.getImage(piece)
                self.screen.blit(image, topLeft)
                topLeft = (topLeft[0] + self.pieceSize[0], topLeft[1])
            topLeft = (0, topLeft[1] + self.pieceSize[1])

    # 加载图片
    def loadImages(self):
        self.images = {}
        for fileName in os.listdir("images"):
            if not fileName.endswith(".png"):
                continue
            image = pygame.image.load(r"images/"+fileName)
            image = pygame.transform.scale(image, self.pieceSize)
            self.images[fileName.split(".")[0]] = image

    # 获取坐标位置对应图片
    def getImage(self, piece):
        # string = "unclicked_bomb" if piece.getHasBomb() else str(piece.getNumAround())
        string = None
        if piece.getClicked():
            string = "bomb_at_clicked_block" if piece.getHasBomb() else str(piece.getNumAround())
        else:
            string = "flag" if piece.getFlagged() else "empty_block"
        return self.images[string]

    # 点击处理，调用board中方法
    def handleClick(self, position, rightClick):
        # if self.board.getLost():
        #     sound = pygame.mixer.Sound("lost.wav")
        #     sound.play()
        #     sleep(1)
        #     self.running = False
        index = (position[1]//self.pieceSize[1], position[0]//self.pieceSize[0])  # 获取行列坐标(左上角)
        piece = self.board.getPiece(index)
        self.board.handleClick(piece, rightClick)

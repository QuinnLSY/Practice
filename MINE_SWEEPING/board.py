from piece import Piece
from random import random


# 面板类，size[0] x size[1】大小的面板，以方块为单位
class Board:
    def __init__(self, size, prob):
        self.size = size
        self.prob = prob  # 该单元出现炸弹的概率
        self.lost = False
        self.won = False
        self.numClicked = 0
        self.numNonBombs = 0
        self.setBoard()

    # 初始化面板中piece的状态
    def setBoard(self):
        self.board = []
        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                hasBomb = random() < self.prob  # 是炸弹的概率
                if not hasBomb:
                    self.numNonBombs += 1
                piece = Piece(hasBomb)  # 标记为炸弹
                row.append(piece)
            self.board.append(row)
        self.setNeighbors()

    # 设置每一个piece的邻居，建立计算炸弹数量的关联关系
    def setNeighbors(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.getPiece((row, col))
                neighbors = self.getListOfNeighbors((row, col))
                piece.setNeighbors(neighbors)

    # 获取周围8个邻居
    def getListOfNeighbors(self, index):
        neighbors = []
        for row in range(index[0] - 1, index[0] + 2):
            for col in range(index[1] - 1, index[1] + 2):
                outOfBounds = row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]
                same = row == index[0] and col == index[1]
                if same or outOfBounds:
                    continue
                neighbors.append(self.getPiece((row, col)))
        return neighbors

    # 获取面板规格
    def getSize(self):
        return self.size

    # 获取对应坐标下的piece
    def getPiece(self, index):
        return self.board[index[0]][index[1]]

    # 处理点击事件
    def handleClick(self, piece, flag):
        if piece.getClicked() or (not flag and piece.getFlagged()):
            return
        if flag:
            piece.toggleFlag()
            return
        piece.click()
        if piece.getHasBomb():
            self.lost = True
            return
        self.numClicked += 1
        if piece.getNumAround() != 0:
            return
        for neighbor in piece.getNeighbors():  # 当周围都没有炸弹时，piece自动点击
            if not neighbor.getHasBomb() and not neighbor.getClicked():
                self.handleClick(neighbor, False)

    def getLost(self):
        return self.lost

    def getWon(self):
        return self.numNonBombs == self.numClicked

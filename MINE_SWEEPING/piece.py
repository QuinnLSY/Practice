# 按钮图片类
class Piece:
    def __init__(self, hasBomb):
        self.hasBomb = hasBomb
        self.clicked = False
        self.flagged = False

    def getHasBomb(self):
        return self.hasBomb

    def getClicked(self):
        return self.clicked

    def getFlagged(self):
        return self.flagged

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors
        self.setNumAround()

    def getNeighbors(self):
        return self.neighbors

    # 根据周围邻居是否被设置为炸弹，记录其周围炸弹数量
    def setNumAround(self):
        self.numAround = 0
        for piece in self.neighbors:
            if piece.getHasBomb():
                self.numAround += 1

    # 获取setNumaround后的炸弹数
    def getNumAround(self):
        return self.numAround

    # 点击右键后，flag建立和取消相互切换
    def toggleFlag(self):
        self.flagged = not self.flagged

    def click(self):
        self.clicked = True
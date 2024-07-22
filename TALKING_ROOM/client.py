from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *
import sys
import os
import socket
from threading import Thread


class Client(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # 窗口大小与位置
        self.setGeometry(600, 300, 360, 300)
        self.setWindowTitle("聊天室")
        # 背景
        palette = QtGui.QPalette()  # 面板
        bg = QtGui.QPixmap(os.path.join("background0.png"))
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(bg))
        self.setPalette(palette)
        self.ui()
        # 连接服务器
        self.client = socket.socket()
        self.client.connect(("127.0.0.1", 8989))
        self.work_thread()

    # 界面布局
    def ui(self):
        # 聊天显示框（多行文本框）
        self.content = QTextBrowser(self)
        self.content.setGeometry(30, 30, 300, 150)
        # 输入框（单行文本框）
        self.message = QLineEdit(self)
        self.message.setPlaceholderText(u"此处输入发送内容")
        self.message.setGeometry(30, 200, 300, 30)
        # 发送按钮
        self.button = QPushButton("发送", self)
        self.button.setFont(QFont("微软雅黑", 12, True))
        self.button.setGeometry(270, 250, 60, 30)

    # 发消息
    def send_msg(self):
        msg = self.message.text()
        self.client.send(msg.encode())
        if msg.upper() == "Q":
            self.client.close()
            self.destroy()
        self.message.clear()

    def recv_msg(self):
        while True:
            try:
                data = self.client.recv(1024).decode()
                data = data + "\n"
                self.content.append(data)
            except:
                exit()

    def btn_send(self):
        self.button.clicked.connect(self.send_msg)

    def work_thread(self):
        Thread(target=self.btn_send).start()
        Thread(target=self.recv_msg).start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec())

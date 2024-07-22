# -*- coding:utf-8 -*-
"""
:author: 单纯同学
:time: 2023-08-17
:software: pycharm
:commentary: 多人聊天室
"""

import socket
from threading import Thread
import time

class Server:
    def __init__(self):
        self.server = socket.socket()  # 空缺默认IPv4，tcp连接
        self.server.bind(("127.0.0.1", 8989))  # ip,端口号
        self.server.listen(5)  # 最多挂5个
        # 所有客户端
        self.clients = []
        # 用户名与ip的绑定信息
        self.clients_name_ip = {}
        self.get_connect()

    # 监听客户端连接
    def get_connect(self):
        while True:
            # 获取连接客户信息
            client, address = self.server.accept()
            print(address)
            data = "与服务器连接成功！请输入昵称开始聊天！"
            # server与client通信，client需要send()并encode，receive()并decode
            client.send(data.encode())
            # 连接的用户添加到服务器的用户列表中
            self.clients.append(client)
            # 服务器启动多线程处理每个客户端的消息
            Thread(target=self.get_mes, args=(client, self.clients, self.clients_name_ip, address)).start()

    # 对所有客户端消息进行处理
    def get_mes(self, client, clients, clients_name_ip, address):
        # 接收客户端发来的昵称
        name = client.recv(1024).decode()  # 1024=1kb
        # 昵称与ip绑定
        clients_name_ip[address] = name
        # 循环监听客户端消息
        while True:
            # 获取所有客户发送的消息
            try:
                recv_data = client.recv(1024).decode()
            except Exception as e:
                self.close_client(client, address)
                break

            if recv_data.upper() == "Q":
                self.close_client(client, address)
                break
            for c in clients:
                # 消息：谁在什么时候发送了什么消息
                c.send((clients_name_ip[address]+" "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n"+recv_data).encode())

    def close_client(self, client, address):
        self.clients.remove(client)
        client.close()

        print(self.clients_name_ip[address]+"已经离开聊天！")
        for c in self.clients:
            c.send((self.clients_name_ip[address]+"已经离开聊天！").encode())


if __name__ == '__main__':
    Server()

# -*- coding:utf-8 -*-
"""
:author: 单纯同学
:time: 2023-09-20
:software: pycharm
:commentary: 超级马里奥--杂项（石头/水管/检查点等类）只是加一个隐形轮廓，brick/box/enemy/player/coin都是需要抠图画到幕布上的实物
"""
import pygame


# 在level.py的setup_ground_items中调用
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, name):
        """
        初始化一个无实物游戏对象。

        这个方法是用来创建一个新的游戏对象的初始化函数。它设置了对象的位置、大小和名称。

        参数:
        x - 游戏对象的x坐标
        y - 游戏对象的y坐标
        w - 游戏对象的宽度
        h - 游戏对象的高度
        name - 游戏对象的名称，用于标识和区分不同的对象
        """
        # 初始化游戏精灵基类
        pygame.sprite.Sprite.__init__(self)

        # 创建一个表面，用于绘制游戏对象，相当于给地面水管等加一个隐形轮廓
        self.image = pygame.Surface((w, h)).convert()

        # 获取表面的矩形区域，用于碰撞检测和位置设置
        self.rect = self.image.get_rect()

        # 设置游戏对象在屏幕上的初始位置
        self.rect.x = x
        self.rect.y = y

        # 设置游戏对象的名称，用于标识和区分不同的对象
        self.name = name


class Checkpoint(Item):
    def __init__(self, x, y, w, h, checkpoint_type, enemy_groupid=None, name='checkpoint'):
        Item.__init__(self, x, y, w, h, name)
        self.checkpoint_type = checkpoint_type
        self.enemy_groupid = enemy_groupid


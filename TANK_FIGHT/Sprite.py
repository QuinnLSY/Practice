# encoding : utf-8

from setting import *
from pygame import *
import pygame, sys, time
import os
from random import *
from math import *

vec = pygame.math.Vector2  # 运用向量


class Player(pygame.sprite.Sprite):  # 玩家类
    Bullet_groups = pygame.sprite.Group()
    flag = 1  # 判断方向的flag 改变坦克方向，同时改变以射出子弹的方向

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("resource", "down.png")).convert()  # 图片的加载
        self.image.set_colorkey(white)  # 设置忽略白色
        self.rect = self.image.get_rect()
        self.radius = 15
        self.rect.center = (115, 130)

        self.pos = vec(115, 130)

        self.last_time = time.time()  # 记录上一次时间 用来设置子弹频率等

        self.die = 0

    def update(self):
        key_pressed = pygame.key.get_pressed()  # 按键获取
        if key_pressed[pygame.K_a]:
            self.image = pygame.image.load(os.path.join("resource", "left.png")).convert()
            self.image.set_colorkey(white)
            self.pos.x -= move_space  # 位置移动
            self.flag = 2
        if key_pressed[pygame.K_d]:
            self.image = pygame.image.load(os.path.join("resource", "right.png")).convert()
            self.image.set_colorkey(white)
            self.pos.x += move_space
            self.flag = 1
        if key_pressed[pygame.K_w]:
            self.image = pygame.image.load(os.path.join("resource", "up.png")).convert()
            self.image.set_colorkey(white)
            self.pos.y -= move_space
            self.flag = 3
        if key_pressed[pygame.K_s]:
            self.image = pygame.image.load(os.path.join("resource", "down.png")).convert()
            self.image.set_colorkey(white)
            self.pos.y += move_space
            self.flag = 4
        if key_pressed[pygame.K_SPACE]:
            self.shoot()
        self.rect.midbottom = self.pos

    def shoot(self):  # 开火
        self.now = time.time()  # 获取现在时间
        if self.now - self.last_time > 0.3:  # 子弹时间间隔
            # 这里显示错误了，应该在if 语句内 包含以下部分
            pygame.mixer.music.load(os.path.join("resource", "expl0.wav"))
            pygame.mixer.music.play()  # 音乐加载
            if self.flag == 1 or self.flag == 2:
                bullet = Bullet_LR(self.pos.x, self.pos.y, self.flag)
                self.Bullet_groups.add(bullet)
                self.Bullet_groups.update()
                self.last_time = self.now
            if self.flag == 3 or self.flag == 4:
                bullet = Bullet_UD(self.pos.x, self.pos.y, self.flag)
                self.Bullet_groups.add(bullet)
                self.Bullet_groups.update()
                self.last_time = self.now


class Platform(pygame.sprite.Sprite):  # 地图创建
    def __init__(self, x, y, w, h):  # x，y，宽，高
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))  # 砖块大小
        self.image.fill(yellow)  # 砖颜色
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Enemy(pygame.sprite.Sprite):  # 与player 相同
    Bullet_groups = pygame.sprite.Group()
    flag = 1

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("resource", "down.png")).convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.center = (315, 130)
        self.pos = vec(315, 130)
        self.bar = 100
        self.last_time = time.time()
        self.flag = 1
        self.die = 0

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT]:
            self.image = pygame.image.load(os.path.join("resource", "left.png")).convert()
            self.image.set_colorkey(white)
            self.pos.x -= move_space
            self.flag = 2
        if key_pressed[pygame.K_RIGHT]:
            self.image = pygame.image.load(os.path.join("resource", "right.png")).convert()
            self.image.set_colorkey(white)
            self.pos.x += move_space
            self.flag = 1
        if key_pressed[pygame.K_UP]:
            self.image = pygame.image.load(os.path.join("resource", "up.png")).convert()
            self.image.set_colorkey(white)
            self.pos.y -= move_space
            self.flag = 3
        if key_pressed[pygame.K_DOWN]:
            self.image = pygame.image.load(os.path.join("resource", "down.png")).convert()
            self.image.set_colorkey(white)
            self.pos.y += move_space
            self.flag = 4
        if key_pressed[pygame.K_p]:
            self.shoot()

        self.rect.midbottom = self.pos

    def shoot(self):
        self.now = time.time()
        if self.now - self.last_time > 0.3:
            pygame.mixer.music.load(os.path.join("resource", "expl1.wav"))
            pygame.mixer.music.play()
            if self.flag == 1 or self.flag == 2:
                bullet = Bullet_LR(self.pos.x, self.pos.y, self.flag)
                self.Bullet_groups.add(bullet)
                self.Bullet_groups.update()
                self.last_time = self.now
            if self.flag == 3 or self.flag == 4:
                bullet = Bullet_UD(self.pos.x, self.pos.y, self.flag)
                self.Bullet_groups.add(bullet)
                self.Bullet_groups.update()
                self.last_time = self.now


# 左右炮弹
class Bullet_LR(pygame.sprite.Sprite):  # 炮弹组
    def __init__(self, x, y, flag):  # 炮弹该有的位置 玩家周围
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("resource", "dot_lr.png")).convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = x  # 这里是准确的位置，未进行准确更改
        self.rect.bottom = y - 10
        self.speed = 5
        self.flag = flag

    def update(self):
        if self.flag == 1:  # right
            self.rect.x += self.speed
        if self.flag == 2:  # left
            self.rect.x -= self.speed
        # if self.flag == 3:  # up
        #     self.rect.y -= self.speed
        # if self.flag == 4:  # down
        #     self.rect.y += self.speed


# 上下炮弹
class Bullet_UD(pygame.sprite.Sprite):  # 炮弹组
    def __init__(self, x, y, flag):  # 炮弹该有的位置 玩家周围
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("resource", "dot_ud.png")).convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = x   # 这里是准确的位置，未进行准确更改
        self.rect.bottom = y
        self.speed = 5
        self.flag = flag

    def update(self):
        # if self.flag == 1:  # right
        #     self.rect1.x += self.speed
        # if self.flag == 2:  # left
        #     self.rect1.x -= self.speed
        if self.flag == 3:  # up
            self.rect.y -= self.speed
        if self.flag == 4:  # down
            self.rect.y += self.speed
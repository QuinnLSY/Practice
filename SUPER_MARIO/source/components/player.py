# -*- coding:utf-8 -*-
"""
:author: 单纯同学
:time: 2023-08-21
:software: pycharm
:commentary: 超级马里奥--玩家动作管理
"""
import pygame

from SUPER_MARIO.source.components.powerup import Fireball
from SUPER_MARIO.source.setup import *
from SUPER_MARIO.source.tools import *
import json
import os


class Player(pygame.sprite.Sprite):  # 在level中调用
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.load_data()
        self.setup_states()
        self.setup_velocities()
        self.setup_timers()
        self.load_images()

    def load_data(self):
        file_name = self.name + '.json'
        file_path = os.path.join('source/data/player', file_name)
        with open(file_path) as f:
            self.playe_data = json.load(f)
            
    # 设置状态
    def setup_states(self):
        self.state = 'stand'
        self.face_right = True
        self.dead = False
        self.big = False
        self.fire = False
        self.can_shoot = True
        self.can_jump = True
        self.hurt_immune = False

    # 各种速度
    def setup_velocities(self):
        speed = self.playe_data['speed']
        self.x_vel = 0  # 速度参数在level.py中调用
        self.y_vel = 0
        self.gravity = GRAVITY
        self.anti_gravity = ANTI_GRAVITY

        if self.big:
            self.max_walk_vel = 1.3*speed['max_walk_speed']  # 走的最大速度
            self.max_run_vel = 1.5*speed['max_run_speed']  # 跑的最大速度
            self.max_y_vel = 1.3*speed['max_y_velocity']
            self.jump_vel = 1.3*speed['jump_velocity']  # 跳的最大速度
            self.walk_accel = 0.8*speed['walk_accel']  # 走的加速度
            self.run_accel = 0.8*speed['run_accel']  # 跑的加速度
            self.turn_accel = 0.8*speed['turn_accel']  # 转向的加速度（即正向的减速度）
        else:
            self.max_walk_vel = speed['max_walk_speed']  # 走的最大速度
            self.max_run_vel = speed['max_run_speed']  # 跑的最大速度
            self.max_y_vel = speed['max_y_velocity']
            self.jump_vel = speed['jump_velocity']  # 跳的最大速度
            self.walk_accel = speed['walk_accel']  # 走的加速度
            self.run_accel = speed['run_accel']  # 跑的加速度
            self.turn_accel = speed['turn_accel']  # 转向的加速度（即正向的减速度）

        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel

    # 各状态计时器
    def setup_timers(self):
        self.walking_timer = 0
        self.transition_timer = 0  # 状态转换计时器，用于转换过程动画帧切换定位
        # TODO: big_power_timer fire_power_timer不一样，可以补充
        self.big_power_timer = 0  # 获得道具计时器，为0则是small_normal；不为0，即获得道具时的时间
        self.fire_power_timer = 0
        self.death_timer = 0  # 死亡时间
        self.hurt_immune_timer = 0  # 免疫伤害的计时器
        self.last_fireball_timer = 0  # 子弹发射间隔

    def load_images(self):
        """
        加载玩家角色的图像资源。

        从配置文件中获取玩家图像帧的矩形区域信息，根据这些信息加载并处理图像，
        包括正常大小和大尺寸的站立和行走动画帧，以及大尺寸的火球攻击动画帧。
        """
        # 从图形配置中获取马里奥兄弟的图形表
        sheet = GRAPHICS['mario_bros']
        # 从玩家数据中获取图像帧的矩形列表
        frame_rects = self.playe_data['image_frames']

        # 初始化不同状态下的图像帧列表
        # 包括正常和大尺寸，正常和火球状态，以及面向左右的方向
        self.right_small_normal_frames = []
        self.right_big_normal_frames = []
        self.right_big_fire_frames = []
        self.left_small_normal_frames = []
        self.left_big_normal_frames = []
        self.left_big_fire_frames = []

        # 组合不同状态的帧列表，用于快速切换玩家状态
        self.small_normal_frames = [self.right_small_normal_frames, self.left_small_normal_frames]
        self.big_normal_frames = [self.right_big_normal_frames, self.left_big_normal_frames]
        self.big_fire_frames = [self.right_big_fire_frames, self.left_big_fire_frames]

        # 创建包含所有状态帧的列表，用于遍历播放动画
        self.all_frames = [
            self.right_small_normal_frames,
            self.right_big_normal_frames,
            self.right_big_fire_frames,
            self.left_small_normal_frames,
            self.left_big_normal_frames,
            self.left_big_fire_frames,
        ]

        # 默认设置玩家面向右方的帧列表
        self.right_frames = self.right_small_normal_frames
        self.left_frames = self.left_small_normal_frames

        # 遍历帧矩形列表，根据不同的组别加载并处理图像
        for group, group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
                # 从图形表中加载单个帧图像
                right_image = get_image(sheet, frame_rect['x'], frame_rect['y'],
                                        frame_rect['width'], frame_rect['height'], (0, 0, 0), PLAYER_MULTI)
                # 对右向图像进行水平翻转，得到左向图像
                left_image = pygame.transform.flip(right_image, True, False)  # 镜像翻转
                # 根据组别，将图像添加到相应的列表中
                if group == 'right_small_normal':
                    self.right_small_normal_frames.append(right_image)
                    self.left_small_normal_frames.append(left_image)
                if group == 'right_big_normal':
                    self.right_big_normal_frames.append(right_image)
                    self.left_big_normal_frames.append(left_image)
                if group == 'right_big_fire':
                    self.right_big_fire_frames.append(right_image)
                    self.left_big_fire_frames.append(left_image)

        # 初始化当前帧索引和当前帧列表
        self.frame_index = 0
        self.frames = self.right_frames
        # 获取当前帧图像和其矩形区域
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

    def update(self, keys, level):
        self.current_time = pygame.time.get_ticks()
        self.handel_states(keys, level)
        self.is_hurt_immune()

    def handel_states(self, keys, level):
        self.can_jump_or_not(keys)
        if self.state == 'stand':
            self.stand(keys)
        elif self.state == 'walk':
            self.walk(keys)
        elif self.state == 'jump':
            self.jump(keys)
        elif self.state == 'fall':
            self.fall(keys)
        elif self.state == 'die':
            self.die(keys)
        elif self.state == 'big_normal2small_normal':
            self.big_normal2small_normal(keys)
        elif self.state == 'small_normal2big_normal':
            self.small_normal2big_normal(keys)
        elif self.state == 'big_normal2big_fire':
            self.big_normal2big_fire(keys)

        self.can_shoot_or_not(keys)
        if self.fire and self.can_shoot:
            if keys[pygame.K_SPACE]:
                self.shoot_fireball(level)

        if self.fire_power_timer != 0 and self.fire_power_timer >= self.big_power_timer and self.current_time - self.fire_power_timer > 150000:
            self.state = 'big_fire2big_normal'
            self.state = 'big_normal2small_normal'
        # 获得的能力可使用时间为10秒
        elif self.fire_power_timer != 0 and self.fire_power_timer < self.big_power_timer and self.current_time - self.big_power_timer > 150000:
            self.state = 'big_fire2big_normal'
        elif self.fire_power_timer == 0 and self.big_power_timer != 0 and self.current_time - self.big_power_timer > 10000:
            self.state = 'big_normal2small_normal'

        # 什么都不做，默认状态第一帧
        if self.face_right:
            self.frames = self.right_frames
            self.image = self.right_frames[self.frame_index]
        else:
            self.frames = self.left_frames
            self.image = self.left_frames[self.frame_index]

    def can_jump_or_not(self, keys):
        if not keys[pygame.K_UP]:
            self.can_jump = True

    def stand(self, keys):
        self.frame_index = 0
        self.x_vel = 0
        self.y_vel = 0
        if keys[pygame.K_RIGHT]:
            self.face_right = True
            self.state = 'walk'
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            self.state = 'walk'
        elif keys[pygame.K_UP] and self.can_jump:
            self.state = 'jump'
            self.y_vel = self.jump_vel

    def walk(self, keys):
        if keys[pygame.K_s]:
            self.max_x_vel = self.max_run_vel
            self.x_accel = self.run_accel
        else:
            self.max_x_vel = self.max_walk_vel
            self.x_accel = self.walk_accel

        if keys[pygame.K_UP] and self.can_jump:
            self.state = 'jump'
            self.y_vel = self.jump_vel

        if self.current_time - self.walking_timer > self.calc_frame_duration():
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time
        if keys[pygame.K_RIGHT]:
            self.face_right = True
            if self.x_vel < 0:
                self.frame_index = 5
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            if self.x_vel > 0:
                self.frame_index = 5
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
        else:
            if self.face_right:
                self.x_vel -= self.x_accel
                if self.x_vel < 0:
                    self.x_vel = 0
                    self.state = 'stand'
            else:
                self.x_vel += self.x_accel
                if self.x_vel > 0:
                    self.x_vel = 0
                    self.state = 'stand'

    def jump(self, keys):
        self.frame_index  = 4
        self.y_vel += self.anti_gravity
        self.can_jump = False

        if self.y_vel >= 0:
            self.state = 'fall'

        if keys[pygame.K_RIGHT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)

        if not keys[pygame.K_UP]:  # 长短跳，松开按键，短跳
            self.state = 'fall'

    def fall(self, keys):
        self.y_vel = self.calc_vel(self.y_vel, self.gravity, self.max_y_vel)

        if keys[pygame.K_RIGHT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)

    def die(self, keys):
        self.rect.y += self.y_vel
        self.y_vel += self.anti_gravity

    def go_die(self):
        self.dead = True
        self.y_vel = self.jump_vel
        self.frame_index = 6
        self.state = 'die'
        self.death_timer = self.current_time

    def big_normal2small_normal(self, keys):
        self.change(keys, [2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 'small_normal')
        self.big = False
        self.fire = False
        self.setup_velocities()
        self.big_power_timer = 0
        self.fire_power_timer = 0

    def small_normal2big_normal(self, keys):
        self.change(keys, [1, 0, 1, 0, 1, 2, 0, 1, 2, 0, 2], 'big_normal')
        self.fire = False
        self.big = True
        self.setup_velocities()
        self.fire_power_timer = 0

    def big_normal2big_fire(self, keys):
        self.change(keys, [0, 1, 0, 1, 2, 0, 1, 2, 0, 1, 0], 'big_fire')
        self.fire = True
        self.big = True
        self.setup_velocities()

    def shoot_fireball(self, level):
        if self.current_time - self.last_fireball_timer > 300:
            self.frame_index = 6
            if self.face_right:
                fireball = Fireball(self.rect.right, self.rect.centery + self.rect.height/2, 1)
            else:
                fireball = Fireball(self.rect.left, self.rect.centery + self.rect.height/2, 0)

            level.powerup_group.add(fireball)
            self.can_shoot = False
            self.last_fireball_timer = self.current_time

    # 检测一次一发
    def can_shoot_or_not(self, keys):
        if not keys[pygame.K_SPACE]:
            self.can_shoot = True

    def big_fire2big_normal(self, keys):
        self.change(keys, [0, 1, 0, 1, 2, 0, 1, 2, 0, 1, 0], 'big_fire_normal')
        self.fire = False
        self.big = True
        self.setup_velocities()
        self.fire_power_timer = 0

    def change(self, keys, sizes, goal):
        frame_dur = 50  # 状态转换时的每帧时间
        sizes = sizes  # 转换过程中经历的各造型
        # 不同的转换目标，需要在不同的帧造型组中寻找对应的帧造型
        if goal == 'small_normal':
            self.frames0 = self.small_normal_frames, 8
            self.frames1 = self.big_normal_frames, 8
            self.frames2 = self.big_normal_frames, 4
        elif goal == 'big_normal':
            self.frames0 = self.small_normal_frames, 0
            self.frames1 = self.small_normal_frames, 7
            self.frames2 = self.big_normal_frames, 0
        elif goal == 'big_fire':
            self.frames0 = self.big_fire_frames, 3
            self.frames1 = self.big_normal_frames, 3
            self.frames2 = self.small_normal_frames, 3
        elif goal == 'big_fire_normal':
            self.frames0 = self.big_normal_frames, 3
            self.frames1 = self.big_fire_frames, 3
            self.frames2 = self.small_normal_frames, 3
        # 转换过程在这三帧中切换，0是当前状态，1是过渡状态，2是目标状态
        frames_and_idx = [self.frames0, self.frames1, self.frames2]
        if self.transition_timer == 0:
            self.transition_timer = self.current_time
            self.changing_idx = 0  # 指向当前切换到那一帧
        elif self.current_time - self.transition_timer > frame_dur:  # transition_timer结合frame_dur计算帧切换时间
            self.transition_timer = self.current_time
            frames, idx = frames_and_idx[sizes[self.changing_idx]]
            self.change_player_image(frames, idx)  # 把mario图像转化为这一帧对应形象
            self.changing_idx += 1
            if self.changing_idx == len(sizes):  # 切换到最后一帧后，即达到目标状态
                self.transition_timer = 0  # 帧不再变化
                self.big_power_timer = self.current_time  # 开始计时获得能力的时长（实际不增长，0表示无能力，不为0表示有能力，不为0的时间超过10秒，该能力消失）
                self.fire_power_timer = self.current_time
                self.state = 'walk'  # 转为可操作状态
                self.right_frames = frames[0]  # 确定最终可用的帧造型组
                self.left_frames = frames[1]

    def change_player_image(self, frames, idx):
        self.frame_index = idx
        if self.face_right:
            self.right_frames = frames[0]
            self.image = self.right_frames[self.frame_index]
        else:
            self.left_frames = frames[1]
            self.image = self.left_frames[self.frame_index]
        # 以底部为中心转换状态，不然会钻土
        last_frame_bottom = self.rect.bottom
        last_frame_centerx = self.rect.centerx
        self.rect = self.image.get_rect()
        self.rect.bottom = last_frame_bottom
        self.rect.centerx = last_frame_centerx

    def calc_vel(self, vel, accel, max_vel, is_position=True):  # 计算速度
        if is_position:  # 正向（右）
            return min(vel + accel, max_vel)
        else:
            return max(vel - accel, -max_vel)

    def calc_frame_duration(self):  # 帧切换时间间隔,速度越快，帧率越快，帧时间间隔越短
        duration = -60 / self.max_run_vel * abs(self.x_vel) + 80
        return duration

    def is_hurt_immune(self):
        if self.hurt_immune:
            if self.hurt_immune_timer == 0:
                self.hurt_immune_timer = self.current_time
                self.blank_image = pygame.Surface((1, 1))  # 创建一个空白帧
            elif self.current_time - self.hurt_immune_timer < 2000:
                if (self.current_time - self.hurt_immune_timer) % 100 < 50:
                    self.image = self.blank_image  # 碰怪变小时的无敌帧闪烁，每100毫秒的前50毫秒闪烁一次
            else:
                self.hurt_immune = False
                self.hurt_immune_timer = 0



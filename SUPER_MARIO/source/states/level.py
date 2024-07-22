# -*- coding:utf-8 -*-
"""
:author: 单纯同学
:time: 2023-08-21
:software: pycharm
:commentary: 超级马里奥--进入关卡
"""
import pygame
from SUPER_MARIO.source.states.main_menu import *
from SUPER_MARIO.source.components.player import *
from SUPER_MARIO.source.components import stuff, brick, box, enemy
import json
import os


class Level:
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'game_over'
        self.info = Info('level', self.game_info)
        self.load_map_data()
        self.setup_background()
        self.setup_start_positions()
        self.setup_player()
        self.setup_ground_items()
        self.setup_bricks_and_boxs()
        self.setup_enemies()
        self.setup_checkpoints()

    def load_map_data(self):
        file_name = 'level_1.json'
        file_path = os.path.join('source/data/maps', file_name)
        with open(file_path) as f:
            self.map_data = json.load(f)

    def setup_background(self):
        """
        设置游戏背景。

        本方法通过读取地图数据中的背景图像名称，加载相应的图像资源，并根据屏幕尺寸调整背景图像的大小。
        同时，创建一个与背景相同大小的游戏地面Surface，用于后续的游戏对象绘制和碰撞检测。
        """
        # 从地图数据中获取背景图像的名称
        self.image_name = self.map_data['image_name']
        # 从GRAPHICS字典中加载背景图像
        self.background = GRAPHICS[self.image_name]
        # 获取背景图像的矩形区域
        rect = self.background.get_rect()
        # 根据BG_MULTI的倍数调整背景图像的大小
        self.background = pygame.transform.scale(self.background, (int(rect.width*BG_MULTI),
                                                                   int(rect.height*BG_MULTI)))
        # 更新调整大小后的背景图像的矩形区域
        self.background_rect = self.background.get_rect()
        # 获取游戏窗口的矩形区域
        self.game_window = SCREEN.get_rect()
        # 创建一个与背景相同大小的游戏地面Surface，pygame.SRCALPHA表示使用透明像素,tools.get_image同步使用，以确保mario等对象可以正确显示在背景上
        # 此处需要说明：去除pygame.SRCALPHA同样可以创建Surface对象，只要tools.get_image中使用的方法相同即可。
        # 这里使用pygame.SRCALPHA使用透明像素是因为，info.py中创建info信息时是现将文字转换为图片，而转换的图片默认是带透明像素的，
        # 要想在背景上正确显示info，而不是显示白条（即透明像素被填充），就需要将game_ground改为透明像素（即使用pygame.SRCALPHA)，因此需要同步使用tools.get_image。
        # #在main_menu和load_screen中不需要使用pygame.SRCALPHA，是因为他们直接截取图片（png）做背景或设置RGB为背景，本身就是透明像素，
        # 而这里的背景是画在同大小的surface（game_ground）上的，然后game_ground画到主surface(tools中的self.screen)上，最后再将info
        # 画到主surface上覆盖game_ground对应区域，使用如果game_ground不使用pygame.SRCALPHA，无透明像素，则info.py中创建的info信息会
        # 被无透明像素叠底，从而显示白条。（也即，所有的实物和文字图片对象都必须与surface统一格式）
        self.game_ground = pygame.surface.Surface((self.background_rect.width, self.background_rect.height), pygame.SRCALPHA)

    def setup_start_positions(self):
        self.positions = []
        for data in self.map_data['maps']:
            self.positions.append((data['start_x'], data['end_x'], data['player_x'], data['player_y']))
        self.start_x, self.end_x, self.player_x, self.player_y = self.positions[0]

    def setup_player(self):
        self.player = Player('mario')
        self.player.rect.x = self.game_window.x + self.player_x
        self.player.rect.bottom = self.player_y

    def setup_ground_items(self):
        """
        初始化场景中的地面物品组。

        这个方法通过遍历地图数据，为每种类型的地面物品（如地面、管道、台阶）创建一个精灵对象，
        并将这些精灵对象添加到一个组中。这样可以在游戏的后续过程中方便地对这些物品进行管理
        和渲染。

        地面物品的属性（如位置、宽度、高度）是从地图数据中获取的，每个物品的类型由其在
        数据中的名称决定。
        """
        # 创建一个用于存储所有地面物品的精灵组
        self.ground_items_group = pygame.sprite.Group()
        # 遍历地图数据中定义的所有地面物品类型
        for name in ['ground', 'pipe', 'step']:
            # 对于每种类型的物品，遍历其在地图数据中的所有实例
            for item in self.map_data[name]:
                # 根据每个物品的属性创建一个对应的精灵对象，并添加到物品组中
                self.ground_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item['height'], name))

    def setup_bricks_and_boxs(self):
        self.brick_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()

        if 'brick' in self.map_data:
            for brick_data in self.map_data['brick']:
                x = brick_data['x']
                y = brick_data['y']
                brick_type = brick_data['type']
                if brick_type == 0:
                    if 'brick_num' in brick_data:
                        # TODO: batch bricks
                        pass
                    else:
                        self.brick_group.add(brick.Brick(x, y, brick_type, None))
                elif brick_type == 1:
                    self.brick_group.add(brick.Brick(x, y, brick_type, self.coin_group))
                else:
                    self.brick_group.add(brick.Brick(x, y, brick_type, self.powerup_group))

        if 'box' in self.map_data:
            for box_data in self.map_data['box']:
                x = box_data['x']
                y = box_data['y']
                box_type = box_data['type']
                if box_type == 1:
                    self.box_group.add(box.Box(x, y, box_type, self.coin_group))
                else:
                    self.box_group.add(box.Box(x, y, box_type, self.powerup_group))

    def setup_enemies(self):
        self.shell_group = pygame.sprite.Group()  # 待复活组，乌龟压扁后未再次碰撞
        self.dying_group = pygame.sprite.Group()  # 死亡组
        self.enemy_group = pygame.sprite.Group()  # 遇到检查点，将该点敌人添加到该组
        self.enemy_group_dict = {}
        for enemy_group_data in self.map_data['enemy']:
            group = pygame.sprite.Group()
            for enemy_group_id, enemy_list in enemy_group_data.items():
                for enemy_data in enemy_list:
                    group.add(enemy.create_enemy(enemy_data))
                self.enemy_group_dict[enemy_group_id] = group

    def setup_checkpoints(self):
        self.checkpoint_group = pygame.sprite.Group()
        for item in self.map_data['checkpoint']:
            x, y, w, h = item['x'], item['y'], item['width'], item['height']
            checkpoint_type = item['type']
            enemy_groupid = item.get('enemy_groupid')
            self.checkpoint_group.add(stuff.Checkpoint(x, y, w, h, checkpoint_type, enemy_groupid))

    def update(self, surface, keys):
        self.current_time = pygame.time.get_ticks()
        self.player.update(keys, self)
        # self.game_info['play_time'] = (self.current_time - self.game_info['start_time'])//1000
        if self.player.dead:
            if self.current_time - self.player.death_timer > 3000:
                self.finished = True
                self.update_game_info()
        elif self.is_frozen():  # 状态转换时其它场景不刷新
            pass
        else:
            """更新动态方法"""
            self.update_player_position()
            self.check_checkpoints()
            self.check_if_go_die()
            self.update_game_window()
            """更新画面组件"""
            self.info.update()  # 金币闪烁
            self.powerup_group.update(self)
            self.coin_group.update()
            self.brick_group.update()
            self.box_group.update()
            # for enemy_group in self.enemy_group_dict.values():
            #     enemy_group.update(self)  # 无检查点，野怪全部刷新
            self.enemy_group.update(self)  # enemy类中引入了level，以使用level中的移动方法，所有更新时需传入self
            self.dying_group.update(self)
            self.shell_group.update(self)

            # self.info.draw(surface)
        self.draw(surface)

    def is_frozen(self):
        return self.player.state in ['big_normal2small_normal', 'small_normal2big_normal']

    def update_player_position(self):  # 位置移动，速度参数在player.py中
        self.player.rect.x += self.player.x_vel
        if self.player.rect.x < self.start_x:
            self.player.rect.x = self.start_x

        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x
        self.check_x_collisions()
        """ 没死才需要垂直检测，死了就不需要碰撞了"""
        if not self.player.dead:
            self.player.rect.y += self.player.y_vel
            self.check_y_collisions()

    def check_x_collisions(self):
        check_group = pygame.sprite.Group(self.brick_group, self.ground_items_group, self.box_group)
        colloded_sprite = pygame.sprite.spritecollideany(self.player, check_group)
        if colloded_sprite:
            self.adjust_player_x(colloded_sprite)

        enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)
        if self.player.hurt_immune:
            return
        """自己挂了"""
        if enemy and self.player.y_vel == 0:
            if self.player.big:
                self.player.state = 'big_normal2small_normal'
                self.player.hurt_immune = True  # 变小无敌免疫，player中的is_hurt_immune执行免疫操作
            else:
                self.player.go_die()

        shell = pygame.sprite.spritecollideany(self.player, self.shell_group)
        if shell:
            if shell.state == 'slide':
                self.player.go_die()
            else:
                if self.player.rect.x < shell.rect.x:
                    shell.x_vel = 10
                    shell.rect.x += 40
                    shell.direction = 1
                else:
                    shell.x_vel = -10
                    shell.rect.x -= 40
                    shell.direction = 0
                shell.state = 'slide'

        powerup = pygame.sprite.spritecollideany(self.player, self.powerup_group)
        if powerup:
            if powerup.name == 'fireball':
                pass
            if powerup.name == 'mushroom':
                self.player.state = 'small_normal2big_normal'
                powerup.kill()
            elif powerup.name == 'fireFlower':
                self.player.state = 'big_normal2big_fire'
                powerup.kill()
            elif powerup.name == 'life_mushroom':
                self.player.state = 'blond_up'
                powerup.kill()
            elif powerup.name == 'star':
                pass

    def check_y_collisions(self):
        ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)
        box = pygame.sprite.spritecollideany(self.player, self.box_group)  # 碰撞检测顺序有先后
        brick = pygame.sprite.spritecollideany(self.player, self.brick_group)
        enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)

        if brick and box:
            to_brick = abs(self.player.rect.centerx - brick.rect.centerx)
            to_box = abs(self.player.rect.centerx - box.rect.centerx)
            if to_brick < to_box:
                box = None
            else:
                brick = None

        if ground_item:
            self.adjust_player_y(ground_item)
        elif box:
            self.adjust_player_y(box)
        elif brick:
            self.adjust_player_y(brick)
        # 弄死敌人
        elif enemy:
            if self.player.hurt_immune:
                return  # 免疫状态不做处理
            self.enemy_group.remove(enemy)
            if enemy.name == 'koopa':
                self.shell_group.add(enemy)
            else:
                self.dying_group.add(enemy)

            if self.player.y_vel < 0:  # 上顶
                how = 'bumped'
            else:  # 下压
                how = 'trampled'
                """压死野怪后自动小跳"""
                self.player.state = 'jump'
                self.player.rect.bottom = enemy.rect.top
                self.player.y_vel = self.player.jump_vel * 0.8
            enemy.go_die(how, 1 if self.player.face_right else -1)
        self.check_will_fall(self.player)

    def adjust_player_x(self, sprite):
        if self.player.rect.x < sprite.rect.x:
            self.player.rect.right = sprite.rect.left
        else:
            self.player.rect.left = sprite.rect.right
        self.player.x_vel = 0

    def adjust_player_y(self, sprite):
        """
        调整玩家角色与特定精灵之间的垂直位置关系。

        当玩家角色的底部位置低于精灵的底部位置时，认为玩家角色应停留在精灵的顶部，
        否则，认为玩家角色应继续下落。这个函数主要用于处理玩家角色与平台之间的交互，
        确保玩家角色能够正确地站在平台上或者从平台上掉落。

        参数:
        - self: 类的实例，用于访问和操作类的属性和方法。
        - sprite: 一个表示特定精灵的对象，这里用来与玩家角色进行位置比较。

        无返回值。
        """
        # 检查玩家角色的底部是否低于精灵的底部
        if self.player.rect.bottom < sprite.rect.bottom:  # 下降碰到
            # 如果是，则停止玩家角色的垂直运动
            self.player.y_vel = 0
            # 将玩家角色的底部与精灵的顶部对齐
            self.player.rect.bottom = sprite.rect.top  # 此处当角色移出碰撞范围后，无法修改y坐标导致凌空，需要使用check_will_fall来检查下落状态
            # 设置玩家角色的状态为行走
            self.player.state = 'walk'
        else:  # 上升撞到
            # 如果不是，则加速玩家角色的垂直下落
            self.player.y_vel = 7
            # 将玩家角色的顶部与精灵的底部对齐
            self.player.rect.top = sprite.rect.bottom
            # 设置玩家角色的状态为下落
            self.player.state = 'fall'
            # 检测顶碎砖块时，上方是否有敌人，有的话顶碎砖块同时顶死敌人
            self.is_enemy_on(sprite)

            if sprite.name == 'box':
                if sprite.state == 'rest':
                    sprite.go_bumped()
            if sprite.name == 'brick':
                if self.player.big and sprite.brick_type == 0:
                    sprite.smashed(self.dying_group)  # 变大状态下空箱子顶碎
                else:
                    sprite.go_bumped()

    def is_enemy_on(self, sprite):
        """
        检查敌人是否站在砖块上。
        """
        sprite.rect.y -= 1
        enemy = pygame.sprite.spritecollideany(sprite, self.enemy_group)
        if enemy:
            self.enemy_group.remove(enemy)
            self.dying_group.add(enemy)
            if sprite.rect.centerx > enemy.rect.centerx:  # 在砖块右边，向右被击飞，左边向左杯击飞
                enemy.go_die('bumped', -1)
            else:
                enemy.go_die('bumped', 1)
        sprite.rect.y += 1


    def check_will_fall(self, sprite):
        """
        检查精灵是否即将下落。

        通过短暂向上移动精灵并检测是否与其它东西碰撞来判断精灵的下落状态。
        如果精灵没有碰撞且当前状态不是跳跃，则将其状态设置为下落。

        参数:
        - sprite: 要检查的精灵对象。
        """
        # 模拟精灵向下移动一小段距离，用于检测是否与其它东西接触
        sprite.rect.y += 1
        # 创建一个临时组，包含所有地面物品，用于碰撞检测
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)
        # 检查精灵是否与地面组中的任何物品发生碰撞
        collided_sprite = pygame.sprite.spritecollideany(sprite, check_group)
        # 如果没有发生碰撞且精灵当前状态不是跳跃，则将其状态设置为下落
        if not collided_sprite and sprite.state != 'jump' and not self.is_frozen():  # 下落过程中转换形态时，不能进行下落检测，否则会直接从转换形态的状态变为下落态，导致形态转换失败
            sprite.state = 'fall'
        # 恢复精灵的原始位置，撤销之前的模拟移动
        sprite.rect.y -= 1

    def check_checkpoints(self):
        checkpoint = pygame.sprite.spritecollideany(self.player, self.checkpoint_group)
        if checkpoint:
            if checkpoint.checkpoint_type == 0:
                self.enemy_group.add(self.enemy_group_dict[str(checkpoint.enemy_groupid)])
            checkpoint.kill()

    def check_if_go_die(self):
        if self.player.rect.y > SCREEN_H:
            self.player.go_die()

    def update_game_window(self):
        """
        更新游戏窗口的位置。

        如果玩家向右移动，并且玩家的中心点超过窗口宽度的三分之一，且游戏窗口的右边界未达到结束位置，
        则将游戏窗口向右移动玩家的水平速度。这用于实现游戏窗口随着玩家移动的效果，创建滚动背景的错觉。
        """
        # 计算游戏窗口宽度的三分之一，用于确定玩家移动时窗口是否应该跟随移动
        third = self.game_window.x + self.game_window.width/2
        fourth = self.game_window.x + self.game_window.width/4

        # 检查玩家是否向右移动，且玩家中心点超过窗口宽度的三分之一，同时游戏窗口的右边界未达到结束位置
        if self.player.x_vel > 0 and self.player.rect.centerx > third and self.game_window.right < self.end_x:
            # 更新游戏窗口的位置，使其向右移动玩家的水平速度
            self.game_window.x += self.player.x_vel
            # 更新游戏窗口的起始位置，用于后续判断窗口是否需要移动
            # self.start_x = self.game_window.x
        if self.player.x_vel < 0 and self.player.rect.centerx < fourth and self.game_window.left > self.start_x:
            self.game_window.x += self.player.x_vel
            # self.start_x = self.game_window.x

    def update_game_info(self):
        if self.player.dead:
            self.game_info['lives'] -= 1
        if self.game_info['lives'] == 0:
            self.finished = True
            self.next = 'game_over'
        else:
            self.next = 'load_screen'

    def draw(self, surface):
        self.game_ground.blit(self.background,  self.game_window, self.game_window)
        self.game_ground.blit(self.player.image, self.player.rect)
        self.powerup_group.draw(self.game_ground)
        self.coin_group.draw(self.game_ground)
        self.brick_group.draw(self.game_ground)
        self.box_group.draw(self.game_ground)
        # for enemy_group in self.enemy_group_dict.values():
        #     enemy_group.draw(self.game_ground)
        self.enemy_group.draw(self.game_ground)
        self.dying_group.draw(self.game_ground)
        self.shell_group.draw(self.game_ground)

        # surface.blit(self.game_ground, (0, 0), self.game_window)
        surface.blit(self.game_ground, (0, 0), self.game_window)
        self.info.draw(surface)
        # self.info.update(surface)  # 金币闪烁

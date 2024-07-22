import math

import pygame
from .. import tools, setup
from SUPER_MARIO.source.constants import *


def create_powerup(centerx, centery, type):
    # if type == 'mushroom':
    #     return Mushroom(centerx, centery)
    # elif type == 'fireFlower':
    #     return FireFlower(centerx, centery)
    return FireFlower(centerx, centery)


class Powerup(pygame.sprite.Sprite):
    def __init__(self, centerx, centery, name, frame_rects):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        self.frame_index = 0
        self.name = name
        for frame_rect in frame_rects:
            if self.name == 'fireball':
                self.frames.append(tools.get_image(setup.GRAPHICS['item_objects'], *frame_rect, (0, 0, 0), 5))
            else:
                self.frames.append(tools.get_image(setup.GRAPHICS['item_objects'], *frame_rect, (0, 0, 0), 2.5))
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery - self.rect.height
        self.origin_y = centery

        self.x_vel = 0
        self.direction = 1
        self.y_vel = -5
        self.gravity = GRAVITY - 0.8
        self.max_y_vel = 8

    def update_position(self, level):
        self.rect.x += self.x_vel
        self.check_x_collisions(level)
        self.rect.y += self.y_vel
        self.check_y_collisions(level)

        if self.rect.x < 0 or self.rect.y > SCREEN_H:
            self.kill()

    def check_x_collisions(self, level):
        sprite = pygame.sprite.spritecollideany(self, level.ground_items_group)
        if sprite:
            if self.direction:
                self.direction = 0
                self.rect.right = sprite.rect.left
            else:
                self.direction = 1
                self.rect.left = sprite.rect.right
            self.x_vel *= -1

    def check_y_collisions(self, level):
        check_group = pygame.sprite.Group(level.ground_items_group, level.box_group, level.brick_group)
        sprite = pygame.sprite.spritecollideany(self, check_group)
        if sprite:
            if self.rect.top < sprite.rect.top:
                self.rect.bottom = sprite.rect.top
                self.y_vel = 0
                self.state = 'walk'
        level.check_will_fall(self)


class Mushroom(Powerup):
    def __init__(self, centerx, centery):
        Powerup.__init__(self, centerx, centery, 'mushroom', [(0, 0, 16, 16)])
        self.x_vel = 1
        self.state = 'grow'
        self.name = 'mushroom'

    def update(self, level):
        if self.state == 'grow':
            self.rect.y += self.y_vel
            if self.rect.centery < self.origin_y - 1.5 * self.rect.height:
                self.state = 'walk'
        elif self.state == 'walk':
            pass
        elif self.state == 'fall':
            if self.y_vel < self.max_y_vel:
                self.y_vel += (++self.gravity)
            else:
                self.y_vel = self.max_y_vel

        if self.state != 'grow':
            self.update_position(level)


class FireFlower(Powerup):
    def __init__(self, centerx, centery):
        frame_rects = [(0, 32, 16, 16), (16, 32, 16, 16), (32, 32, 16, 16), (48, 32, 16, 16)]
        Powerup.__init__(self, centerx, centery, 'fireFlower', frame_rects)
        self.x_vel = 0
        self.state = 'grow'
        self.name = 'fireFlower'
        self.timer = 0

    def update(self, level):
        if self.state == 'grow':
            self.rect.y += self.y_vel
            if self.rect.centery < self.origin_y - 1.5 * self.rect.height:
                self.state = 'rest'
        elif self.state == 'rest':
            pass
        elif self.state == 'fall':
            if self.y_vel < self.max_y_vel:
                self.y_vel += (++self.gravity)
            else:
                self.y_vel = self.max_y_vel
        if self.state != 'grow':
            self.update_position(level)

        self.current_time = pygame.time.get_ticks()

        if self.timer == 0:
            self.timer = self.current_time
        if self.current_time - self.timer > 30:
            self.frame_index += 1
            self.frame_index %= len(self.frames)
            self.image = self.frames[self.frame_index]
            self.timer = self.current_time


class Fireball(Powerup):
    def __init__(self, centerx, centery, direction):
        frame_rect = [(96, 144, 8, 8), (104, 144, 8, 8), (96, 152, 8, 8), (104, 152, 8, 8),  # 旋转
                      (112, 144, 16, 16), (122, 160, 16, 16), (112, 176, 16, 16)  # 爆炸
                      ]
        Powerup.__init__(self, centerx, centery, 'fireball', frame_rect)
        self.name = 'fireball'
        self.direction = direction
        self.centerx = centerx
        self.x_vel = -5 if direction == 0 else 5
        self.y_vel = -10
        self.gravity = GRAVITY
        self.state = 'fly'
        self.timer = 0

    def update(self, level):
        self.current_time = pygame.time.get_ticks()
        if self.state == 'fly':
            self.y_vel += self.gravity
            if self.current_time - self.timer > 50:
                self.frame_index += 1
                self.frame_index %= 4
                self.image = self.frames[self.frame_index]
                self.timer = self.current_time
            self.update_position(level)
        elif self.state == 'explode':
            if self.frame_index <= 3:
                self.frame_index = 3
            if self.current_time - self.timer > 50:
                if self.frame_index < 6:
                    self.frame_index += 1
                    self.timer = self.current_time
                    self.image = self.frames[self.frame_index]
                else:
                    self.kill()

    def update_position(self, level):
        self.rect.x += self.x_vel
        self.check_x_collisions(level)
        self.rect.y += self.y_vel
        self.check_y_collisions(level)

        # 屏幕外消失
        if self.rect.x < 0 or abs(self.rect.x - self.centerx) > SCREEN_W*3/4 or self.rect.y > SCREEN_H:
            self.kill()

    def check_x_collisions(self, level):
        check_infrangible = pygame.sprite.Group(level.ground_items_group, level.box_group)
        infrangible = pygame.sprite.spritecollideany(self, check_infrangible)
        if infrangible:
            self.state = 'explode'

        enemy = pygame.sprite.spritecollideany(self, level.enemy_group)
        if enemy:
            enemy.go_die('bumped', -1 if self.direction == 0 else 1)
            level.enemy_group.remove(enemy)
            level.dying_group.add(enemy)
            self.state = 'explode'

        brick = pygame.sprite.spritecollideany(self, level.brick_group)
        if brick:
            if brick.brick_type == 0:
                brick.smashed(level.dying_group)
                self.state = 'explode'
            else:
                self.state = 'explode'

    def check_y_collisions(self, level):
        check_group = pygame.sprite.Group(level.ground_items_group, level.box_group, level.brick_group)
        sprite = pygame.sprite.spritecollideany(self, check_group)
        if sprite:
            if self.rect.top < sprite.rect.top:
                self.rect.bottom = sprite.rect.top
                self.y_vel = -self.y_vel

        enemy = pygame.sprite.spritecollideany(self, level.enemy_group)
        if enemy:
            enemy.go_die('bumped', -1 if self.direction == 0 else 1)
            level.enemy_group.remove(enemy)
            level.dying_group.add(enemy)
            self.state = 'explode'


class LifeMushroom(Powerup):
    def __init__(self, centerx, centery):
        Powerup.__init__(self, centerx, centery, [(32, 0, 16, 16)])


class Star(Powerup):
    def __init__(self, centerx, centery):
        Powerup.__init__(self, centerx, centery, [(48, 0, 16, 16)])

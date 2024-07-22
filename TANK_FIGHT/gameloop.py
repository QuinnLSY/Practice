# encoding : utf-8

from setting import *
from pygame import *
from Sprite import *
import pygame, sys
import os

vec = pygame.math.Vector2
pygame.init()  # pygame 初始化
pygame.display.set_caption("Keep-Going")  # 游戏窗口 左上角名称
screen = pygame.display.set_mode((width, height))  # 游戏窗口的大小

# 爆炸图片，字典
expl_anim = {'sm': [], 'player': []}
for i in range(9):
    expl_img = pygame.image.load(os.path.join("resource", f"expl{i}.png")).convert()
    expl_img.set_colorkey(black)
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = pygame.image.load(os.path.join("resource", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(black)
    expl_anim['player'].append(player_expl_img)


class game:  # 游戏类 包含循环等
    def __init__(self):  # 初始化
        self.FpsClock = pygame.time.Clock()  # 设置游戏的刷新率
        self.playing = True  # 进入游戏的状态
        self.running = True  # 游戏运行的状态
        self.stop = False  # 退出游戏状态
        self.exit = False  # 确认退出
        self.Pblood = 100  # 玩家血量
        self.Eblood = 100  # 敌人血量
        self.player_die = 0
        self.enemy_die = 0
        self.player = Player()  # 声明一个游戏玩家对象
        self.enemy = Enemy()  # 声明一个敌人对象
        self.all_groups = pygame.sprite.Group()  # 通过pygame自带的 group 来判断碰撞检测
        self.player_groups = pygame.sprite.Group()
        self.Map_groups = pygame.sprite.Group()
        self.Enemy_groups = pygame.sprite.Group()
        self.Explosion = pygame.sprite.Group()

    def new(self):  # 开始一个游戏
        self.player_groups.add(self.player)  # 将玩家添加到玩家组
        self.all_groups.add(self.player)  # 将玩家添加到 所有组

        self.Enemy_groups.add(self.enemy)
        self.all_groups.add(self.enemy)

        for platforms in Map1:  # 地图
            p = Platform(*platforms)  # 取出所有值
            self.Map_groups.add(p)
            self.all_groups.add(p)
        self.run()  # 调用函数运行游戏

    def run(self):
        show_init = True
        while self.running:
            if show_init:
                if self.stop:
                    # self.exit = True
                    self.game_start("GAME_OVER")
                    break  # 获取游戏退出状态，打断循环以关闭窗口
                show_init = False
            self.FpsClock.tick(Fps)  # 设置帧率
            self.events()
            print(self.exit)  # 获取事件
            self.draw_pic()  # 画出图片
            self.update()

    def game_start(self, text):  # 游戏的开始界面
        self.text_draw(width / 2, height / 4, 64, text)  # 文本
        self.text_draw(width / 2, height * 3 / 4, 25, 'Press any key to continue', )  # 文本
        pygame.display.update()  # 更新展示
        waiting = True
        if self.exit == False:
            while waiting:  # 实现 按键等待开始效果
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        self.running = False
                        self.playing = False
                        sys.exit()
                        self.stop = True
                        self.exit = True
                    if event.type == pygame.KEYDOWN:
                        self.Pblood = 100  # 玩家血量
                        self.Eblood = 100  # 敌人血量
                        self.new()
                        waiting = False
                        self.stop = False
                        self.running = True
                        self.playing = True

    def update(self):  # 画面更新
        self.Map_groups.update()
        self.player_groups.update()
        # self.enemy.Bullet_groups.update(self.enemy.flag)  # 通过按键判断子弹方向
        # self.player.Bullet_groups.update(self.player.flag)
        self.enemy.Bullet_groups.update()
        self.player.Bullet_groups.update()
        self.Enemy_groups.update()
        self.Explosion.update()

        # player炮弹撞墙
        hit = pygame.sprite.groupcollide(self.player.Bullet_groups, self.Map_groups, True, False)
        for h in hit:
            expl1 = Explosion(h.rect.center, 'sm')  # 炮弹撞墙爆炸
            self.Explosion.add(expl1)
            self.all_groups.add(self.Explosion)
        # enemy炮弹撞墙
        hit = pygame.sprite.groupcollide(self.enemy.Bullet_groups, self.Map_groups, True, False)
        for h in hit:
            expl1 = Explosion(h.rect.center, 'sm')  # 炮弹撞墙爆炸
            self.Explosion.add(expl1)
            self.all_groups.add(self.Explosion)

        PMC = pygame.sprite.spritecollide(self.player, self.Map_groups, False)  # 撞墙
        if PMC:
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_a]:
                self.player.pos.x = self.player.pos.x + gap
            if key_pressed[pygame.K_d]:
                self.player.pos.x = self.player.pos.x - gap
            if key_pressed[pygame.K_w]:
                self.player.pos.y = self.player.pos.y + gap
            if key_pressed[pygame.K_s]:
                self.player.pos.y = self.player.pos.y - gap

        EMC = pygame.sprite.spritecollide(self.enemy, self.Map_groups, False)  # 撞墙
        if EMC:
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_LEFT]:
                self.enemy.pos.x = self.enemy.pos.x + gap
            if key_pressed[pygame.K_RIGHT]:
                self.enemy.pos.x = self.enemy.pos.x - gap
            if key_pressed[pygame.K_UP]:
                self.enemy.pos.y = self.enemy.pos.y + gap
            if key_pressed[pygame.K_DOWN]:
                self.enemy.pos.y = self.enemy.pos.y - gap

    def text_draw(self, x, y, size, text):  # 文本展示函数
        self.font = pygame.font.Font('font.ttf', size)  # 字体，大小
        self.text_surf = self.font.render(text, True, red)  # 颜色
        self.text_rect = self.text_surf.get_rect()  # 矩形
        self.text_rect.center = (x, y)  # 位置
        screen.blit(self.text_surf, self.text_rect)  # 覆盖展示

    def bar_draw(self, x, y, pct):  # 血条函数
        # draw a bar
        if pct <= 0:
            pct = 0
        Bar_Lenth = 100
        Bar_Height = 10
        Fill_Lenth = (pct / 100) * Bar_Lenth
        Out_rect = pygame.Rect(x, y, Bar_Lenth, Bar_Height)
        Fill_rect = pygame.Rect(x, y, Fill_Lenth, Bar_Height)
        pygame.draw.rect(screen, green, Fill_rect)
        pygame.draw.rect(screen, red, Out_rect, 2)

    def draw_pic(self):
        # 右侧显示区域 按序
        screen.fill(white)  # 背景
        self.text_draw(900, 50, 30, "KEEP")  # 文本
        self.text_draw(900, 100, 30, "GOING")

        self.text_draw(820, 150, 20, "P1:")
        self.text_draw(970, 150, 16, str(self.Pblood))
        self.text_draw(820, 200, 20, "P2:")
        self.text_draw(970, 200, 16, str(self.Eblood))

        self.text_draw(900, 250, 20, "P1死亡："+str(self.player_die)+"次")
        self.text_draw(900, 300, 20, "P1死亡："+str(self.enemy_die)+"次")
        # self.text_draw(900, 350, 20, "Be Control!")

        # 子弹与玩家碰撞事件，P2打P1
        self.bar_draw(850, 145, self.Pblood)  # 血条
        hit = pygame.sprite.groupcollide(self.enemy.Bullet_groups, self.player_groups, True, False,pygame.sprite.collide_circle)  # 血条减少
        for h in hit:
            self.Pblood = self.Pblood - randint(10, 15)
            expl1 = Explosion(h.rect.center, 'sm')  # 炮弹打坦克后炮弹爆炸
            self.Explosion.add(expl1)
            self.all_groups.add(self.Explosion)
            if self.Pblood <= 0:
                self.Pblood = 0
                self.player_die += 1
                expl2 = Explosion(self.player.rect.center, 'player')  # 玩家爆炸
                self.Explosion.add(expl2)
                self.all_groups.add(self.Explosion)
                self.player.kill()

                screen.fill(black)
                self.game_start('P2 WIN!')
                self.running = False
            self.bar_draw(850, 145, self.Pblood)

        # 子弹与玩家碰撞事件，P1打P2
        self.bar_draw(850, 195, self.Eblood)
        hit = pygame.sprite.groupcollide(self.player.Bullet_groups, self.Enemy_groups, True, False)
        for h in hit:
            self.Eblood = self.Eblood - randint(10, 15)
            expl1 = Explosion(h.rect.center, 'sm')  # 炮弹打坦克后炮弹爆炸
            self.Explosion.add(expl1)
            self.all_groups.add(self.Explosion)
            if self.Eblood <= 0:
                self.Eblood = 0
                self.enemy_die += 1
                expl2 = Explosion(self.enemy.rect.center, 'player')  # 玩家爆炸
                self.Explosion.add(expl2)
                self.all_groups.add(self.Explosion)
                self.enemy.kill()

                screen.fill(black)
                self.game_start('P1 WIN!')
                self.running = False
            self.bar_draw(850, 195, self.Eblood)

        self.Map_groups.draw(screen)  # 画出图片
        self.player_groups.draw(screen)
        self.Enemy_groups.draw(screen)
        self.player.Bullet_groups.draw(screen)
        self.enemy.Bullet_groups.draw(screen)
        self.Explosion.draw(screen)
        self.all_groups.draw(screen)

        pygame.display.update()

    def events(self):  # 事件
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                self.stop = True
                self.running = False
                self.playing = False


# 爆炸类
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        # 以上为游戏控制对象固定格式
        self.size = size
        self.image = expl_anim[self.size][0]

        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0  # 帧数，切换爆炸流程
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

# -*- coding:UTF-8 -*-
import pygame
import random
import os  # 可获取相对路径
import pathlib  # 获取绝对路径

FPS = 60
WIDTH = 500
HEIGHT = 601
COLOR = (255, 255, 255)  # 背景颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
rock_num = 10  # 陨石数量
# #游戏初始化
pygame.init()
pygame.mixer.init()  # 声音混合初始化
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 窗口大小
pygame.display.set_caption('飞机大战')  # 标题
clock = pygame.time.Clock()  # 刷新时钟

# 获取绝对路径
folder = pathlib.Path(__file__).parent.resolve()

# 获取图片
background = pygame.image.load(os.path.join(folder, "img", "background.png")).convert()
background_img = pygame.transform.scale(background, (500, 602))

player_img = pygame.image.load(os.path.join(folder, "img", "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (20, 20))  # 制作生命条数图标
player_mini_img.set_colorkey(BLACK)

pygame.display.set_icon(player_mini_img)  # 设置开始图标

bullet_img = pygame.image.load(os.path.join(folder, "img", "bullet.png")).convert()

# rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join(folder, "img", f"rock{i}.png")).convert())
    # 格式化按顺序取值

expl_anim = {}  # 爆炸图片，字典
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join(folder, "img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = pygame.image.load(os.path.join(folder, "img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)

power_imgs = {}  # 宝箱图片
power_imgs['shield'] = pygame.image.load(os.path.join(folder, "img", "shield.png")).convert()
power_imgs['twogun'] = pygame.image.load(os.path.join(folder, "img", "gun.png")).convert()

# 获取声音
shoot_sound = pygame.mixer.Sound(os.path.join(folder, "sound", "shoot.wav"))
expl_sound = [
    pygame.mixer.Sound(os.path.join(folder, "sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join(folder, "sound", "expl1.wav"))
]
die_sound = pygame.mixer.Sound(os.path.join(folder, "sound", "rumble.ogg"))
shield_sound = pygame.mixer.Sound(os.path.join(folder, "sound", "pow0.wav"))
gun_sound = pygame.mixer.Sound(os.path.join(folder, "sound", "pow1.wav"))
pygame.mixer.music.load(os.path.join(folder, "sound", "background.ogg"))  # 载入背景音乐
pygame.mixer.music.set_volume(0.3)  # 调节背景音乐音量

# 设置字体
# font_name = pygame.font.match_font('arial')
font_name = os.path.join(folder, 'font.ttf')


# 绘制分数
def draw_text(surf, text, size, x, y):  # 载体，内容，大小，x坐标，y坐标
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)  # 渲染：内容，是否反锯齿，颜色
    text_rect = text_surface.get_rect()  # 获取矩形框
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)  # 绘制


# 绘制血量条
def draw_health(surf, hp, x, y):  # 载体，血量，x坐标，y坐标
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


# 绘制生命条数
def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 25 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_init():
    screen.blit(background_img, (0, 0))
    draw_text(screen, '飞机大战', 62, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, '<-：左移 ->：右移，空格键发射子弹', 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, '任意键开始', 18, WIDTH / 2, HEIGHT / 4 * 3)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False


# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 以上为游戏控制对象固定格式
        # self.image = pygame.Surface((50,40)) #图片大小
        # self.image.fill((0,255,0)) #填充颜色
        self.image = pygame.transform.scale(player_img, (50, 50))  # 载入图片并设置大小
        self.image.set_colorkey(BLACK)  # 去除黑色像素
        self.rect = self.image.get_rect()  # 获取图片对象的长方形轮廓范围
        # self.rect.center = (WIDTH/2,HEIGHT/2) #居中位置
        # 画圆检验碰撞范围
        self.radius = 25
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius) #要在定位前画出
        # 初始位置
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 10 * 9

        self.speedx = 8  # 左右移速
        self.speedy = 8  # 上下移速

        self.health = 100  # 生命值
        self.lives = 3  # 生命数
        self.gun = 1  # 枪的数量
        self.hidden = False

    def update(self):
        # 获取键盘事件
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedy
        # 控制边界（x，y为左上角点;top，bottom正常逻辑指向对象）
        if self.rect.left < 0:
            self.rect.x = 0
        if self.rect.right > WIDTH:
            self.rect.x = WIDTH - self.rect.width
        # if self.rect.top < 0:
        #     self.rect.y = 0
        if self.rect.bottom > HEIGHT:
            self.rect.y = HEIGHT - self.rect.height
        # if self.rect.right > WIDTH:
        #     self.rect.right = WIDTH
        # if self.rect.left < 0:
        #     self.rect.left = 0
        # if self.rect.top < 0:
        #     self.rect.top = 0
        # if self.rect.bottom > HEIGHT:
        #     self.rect.bottom = HEIGHT
        # 隐藏状态处理
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.health = 100
            self.rect.centerx = WIDTH / 2
            self.rect.centery = HEIGHT / 10 * 9

        if self.gun >= 2 and self.gun <= 4 and pygame.time.get_ticks() - self.get_time > 5000:
            self.gun = 1
        if self.gun > 4 and pygame.time.get_ticks() - self.get_time > 1000:
            self.gun = 1

    def shoot(self):
        if not (self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.y)
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif self.gun >= 2 and self.gun <= 4:
                bullet1 = Bullet(self.rect.centerx - 10, self.rect.y)
                bullet2 = Bullet(self.rect.centerx + 10, self.rect.y)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
            elif self.gun > 4:
                for i in range(50):
                    bullet = Bullet(0 + 10 * i, HEIGHT)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
            shoot_sound.play()

    def gunup(self):
        self.gun += 1
        self.get_time = pygame.time.get_ticks()
        if self.gun > 50:
            self.gun = 50

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()

        self.rect.center = (WIDTH / 2, HEIGHT - 1000)


# 陨石类
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 以上为游戏控制对象固定格式
        # self.image = pygame.Surface((30,30)) #图片大小
        # self.image.fill((255,0,0)) #填充颜色
        # 保存一份原始图片，消除旋转造成的角度累计误差
        # self.image_origin = pygame.transform.scale(rock_img,(45,40))
        self.image_origin = random.choice(rock_imgs)
        self.image_origin.set_colorkey(BLACK)

        self.image = self.image_origin.copy()
        self.rect = self.image.get_rect()  # 获取长方形对象
        # self.rect.center = (WIDTH/2,HEIGHT/2)#居中位置

        self.radius = self.rect.width / 2.2
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -self.rect.height)

        self.speedx = random.randrange(-3, 3)  # 左右移速
        self.speedy = random.randrange(2, 4)  # 上下移速

        self.rot_degree = random.randrange(-3, 3)  # 单次旋转角度
        self.total_degree = 0  # 累计旋转角度

    # 旋转函数
    def ratate(self):
        self.total_degree = (self.total_degree + self.rot_degree) % 360
        self.image = pygame.transform.rotate(self.image_origin, self.total_degree)  # 数字为旋转速度，旋转默认相对左上角固定
        # 旋转是固定旋转中心
        center = self.rect.center  # 图片已经旋转，但框还没有改变
        self.rect = self.image.get_rect()  # 获取旋转后图片的框
        self.rect.center = center  # 将旋转后图片框的中心位置固定在旋转前的位置上，以此实现原地旋转

    def update(self):
        # 执行旋转命令
        self.ratate()
        # 控制边界
        # self.rect.x += self.speedx * random.sample([-10,10],1)[0]
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-200, -self.rect.height)

            self.speedx = random.randrange(-3, 3)  # 左右移速
            self.speedy = random.randrange(2, 6)  # 上下移速


# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # 以上为游戏控制对象固定格式
        # self.image = pygame.Surface((10,20)) #图片大小
        # self.image.fill((255,255,0)) #填充颜色
        self.image = pygame.transform.scale(bullet_img, (13, 54))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  # 获取长方形对象
        # self.rect.center = (WIDTH/2,HEIGHT/2)  # 居中位置
        self.rect.centerx = x
        self.rect.bottom = y

        self.speedy = -10  # 上下移速

    def update(self):
        # 控制边界
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


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


# 宝箱类
class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        # 以上为游戏控制对象固定格式
        self.type = random.choice(['shield', 'twogun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        if self.type == 'shield':
            shield_sound.play()
        else:
            gun_sound.play()
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.speedy = 3  # 上下移速

    def update(self):
        # 控制边界
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


# 游戏控制对象
# all_sprites = pygame.sprite.Group() #所有对象列表，pygame自带对象列表
# rocks = pygame.sprite.Group() #所有陨石列表
# bullets = pygame.sprite.Group() #所有子弹列表
# powers = pygame.sprite.Group() #所有宝箱列表
#
# player = Player()
# all_sprites.add(player)
# for i in range(rock_num): #加入6个陨石对象
#     rock = Rock()
#     all_sprites.add(rock)
#     rocks.add(rock)
# score = 0
# pygame.mixer.music.play(-1) #播放背景音乐，-1无限循环

# 游戏窗口显示运行
init_h1 = 0
init_h2 = -602
running = True
show_init = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break  # 打断重复执行，使得能够直接在初始化界面退出
        show_init = False
        # 对象初始化
        all_sprites = pygame.sprite.Group()  # 所有对象列表，pygame自带对象列表
        rocks = pygame.sprite.Group()  # 所有陨石列表
        bullets = pygame.sprite.Group()  # 所有子弹列表
        powers = pygame.sprite.Group()  # 所有宝箱列表

        player = Player()
        all_sprites.add(player)
        for i in range(rock_num):  # 加入6个陨石对象
            rock = Rock()
            all_sprites.add(rock)
            rocks.add(rock)
        score = 0
        pygame.mixer.music.play(-1)  # 播放背景音乐，-1无限循环

    clock.tick(FPS)  # 刷新频率：每秒FPS次
    for event in pygame.event.get():  # 循环获取事件
        if event.type == pygame.QUIT:  # 监测关闭窗口事件
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # 更新游戏对象
    all_sprites.update()
    # 子弹与陨石碰撞
    hits_rock_and_bullet = pygame.sprite.groupcollide(rocks, bullets, True, True)  # groupcollide群组碰撞检测
    for hit in hits_rock_and_bullet:
        random.choice(expl_sound).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        r = Rock()
        all_sprites.add(r)  # 陨石消失后重新生成
        rocks.add(r)
        if random.random() > 0.8:  # 概率产生宝箱
            p = Power(hit.rect.center)
            all_sprites.add(p)
            powers.add(p)
        score += int(hit.radius)
    # 玩家与宝箱碰撞
    hits_player_and_power = pygame.sprite.spritecollide(player, powers, True)  # spritecollide单体碰撞检测
    for get in hits_player_and_power:
        if get.type == 'shield':
            shield_sound.play()
            player.health += 20
            if player.health > 100:
                player.health = 100
        elif get.type == 'twogun':
            gun_sound.play()
            player.gunup()
    # 陨石与玩家碰撞
    hits_player_and_rock = pygame.sprite.spritecollide(player, rocks, True,
                                                       pygame.sprite.collide_circle)  # spritecollide单体碰撞检测
    for attack in hits_player_and_rock:  # ⬆️按圆形边界判定
        random.choice(expl_sound).play()
        player.health -= int(attack.radius / 2)
        rr = Rock()
        all_sprites.add(rr)  # 陨石消失后重新生成
        rocks.add(rr)
        expl1 = Explosion(attack.rect.center, 'sm')  # 陨石碰撞飞机后陨石爆炸
        all_sprites.add(expl1)
        if player.health <= 0:  # 玩家死亡
            die_sound.play()
            expl2 = Explosion(player.rect.center, 'player')  # 玩家爆炸
            all_sprites.add(expl2)
            player.health = 0
            player.lives -= 1
            player.hide()
        if player.lives == 0:
            # running = False
            show_init = True

    # 显示画面
    screen.fill(COLOR)  # 屏幕颜色(白)
    screen.blit(background_img, (0, init_h1))
    init_h1 += 2
    if init_h1 >= 602:
        init_h1 = -602

    screen.blit(background_img, (0, init_h2))
    init_h2 += 2
    if init_h2 >= 602:
        init_h2 = -602

    all_sprites.draw(screen)
    draw_text(screen, '得分:' + str(score), 18, WIDTH / 2, 0)
    draw_lives(screen, player.lives, player_mini_img, 0, 0)
    draw_health(screen, player.health, 0, 20)
    draw_text(screen, '血量:' + str(player.health), 18, 35, 30)
    draw_text(screen, '枪管数:' + str(player.gun), 18, WIDTH - 45, 0)

    pygame.display.update()  # 刷新
pygame.quit()  # 退出

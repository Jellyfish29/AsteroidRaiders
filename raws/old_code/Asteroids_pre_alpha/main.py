import pygame
from pygame.locals import *
import random
import math
import numpy as np
import os


pygame.init()
Clock = pygame.time.Clock()
winwidth = 1920
winheight = 1080
white = (255, 255, 255)
black = (0, 0, 0)
fps = 63
win = pygame.display.set_mode((winwidth, winheight), pygame.FULLSCREEN)
# win = pygame.display.set_mode((winwidth, winheight))


def Angles(speed):
    return {idx: i for idx, i in enumerate(
        [(speed * (i / 100), -speed) for i in range(0, 100, 10)] +
        [(speed, -speed * (-i / 100)) for i in range(-100, 0, 10)] +
        [(speed, speed * (i / 100)) for i in range(0, 100, 10)] +
        [(speed * (-i / 100), speed) for i in range(-100, 0, 10)] +
        [(-speed * (i / 100), speed) for i in range(0, 100, 10)] +
        [(-speed, speed * (-i / 100)) for i in range(-100, 0, 10)] +
        [(-speed, -speed * (i / 100)) for i in range(0, 100, 10)] +
        [(-speed * (-i / 100), -speed) for i in range(-100, 0, 10)])}


def Angles_shot_player(speed):
    return {idx: i for idx, i in enumerate(
        [(speed, speed * (-i / 100)) for i in np.arange(0, 100, 2.23)] +
        [(speed * (-i / 100), -speed) for i in np.arange(-100, 0, 2.23)] +
        [(-speed * (i / 100), - speed) for i in np.arange(0, 100, 2.23)] +
        [(-speed, -speed * (-i / 100)) for i in np.arange(-100, 0, 2.23)] +
        [(-speed, speed * (i / 100)) for i in np.arange(0, 100, 2.23)] +
        [(-speed * (-i / 100), speed) for i in np.arange(-100, 0, 2.23)] +
        [(speed * (i / 100), speed) for i in np.arange(0, 100, 2.23)] +
        [(speed, speed * (-i / 100)) for i in np.arange(-100, 0, 2.23)])}


def Degrees():
    rel_x, rel_y = pygame.mouse.get_pos()[0] - Player.hitbox.center[0], pygame.mouse.get_pos()[1] - Player.hitbox.center[1]
    angle = -math.atan2(rel_y, rel_x)
    angle = math.degrees(angle)
    if angle < 0:
        angle += 360
    return int(angle)

def directions(speed):
    return {"up": (0, -speed),
              "down": (0, speed),
              "right": (speed, 0),
              "left": (-speed, 0),
              "right up": (speed * 0.8, -speed * 0.8),
              "right down": (speed * 0.8, speed * 0.8),
              "left up": (-speed * 0.8, -speed * 0.8),
              "left down": (-speed * 0.8, speed * 0.8),
              "idle": (0, 0)}       


class Gfx:

    def __init__(self, kind):
        self.pathes = [os.path.join(os.getcwd(), f"Gfx\\{kind}\\" + file) for file in os.listdir(os.path.join(os.getcwd(), f"Gfx\\{kind}"))]
        self.pictures = {
            idx: pygame.image.load(img).convert_alpha() for idx, img in enumerate(sorted(self.pathes))}

    def get_pictures(self):
        return self.pictures


class Background:

    bg = Gfx("background").get_pictures()
    y = 0

    def update():
        Background.y += 0.5
        win.blit(Background.bg[0], (0, Background.y - winheight))
        win.blit(Background.bg[0], (0, Background.y))
        if Background.y == winheight:
            Background.y = 0


class Interface:

    bg = Gfx("background").get_pictures()
    y = 0

    def __init__(self, text, color, location):
        self.font = pygame.font.SysFont("arial", 30)
        self.text = text
        self.color = color
        self.location = location

    def draw(self):
        text = self.font.render(self.text, True, self.color, (50, 50, 50))
        rect = text.get_rect()
        rect.topleft = self.location
        win.blit(text, rect)

    def update():
        pygame.draw.rect(win, (50, 50, 50), pygame.Rect(0, 0, winwidth, 50))
        for text, color, location in [(f"SCORE = {Levels.display_score}", (255, 0, 0), (20, 10)),
                                      (f"LIVES = {Player.health}", (0, 255, 0), (250, 10)),
                                      (f"LEVEL = {Levels.level}", (0, 120, 120), (450, 10)),
                                      (f"Rapid Fire = {Power_ups.super_shot_amount}", (0, 0, 255), (700, 10)),  # super_shot
                                      (f"Star Fire = {Power_ups.star_shot_amount}", (255, 0, 0), (1050, 10)),  # star_shot
                                      (f"Nukes = {Turret.rocket_ammo}", (120, 0, 0), (1400, 10))]:  # Turret.rocket
            Interface(text, color, location).draw()


class Player:

    health = 3
    hitbox = pygame.Rect(winwidth / 2, winheight / 2, 50, 50)
    speed = 3
    direction = "idle"
    directions = directions(speed)
    gfx_idx = {
        "up": 0, "down": 2, "right": 4, "left": 6, "right up": 8, "right down": 10, "left up": 12, "left down": 14, "idle": 16}
    borders = [pygame.Rect(-100, -100, winwidth + 200, 10),  # Top
               pygame.Rect(-100, winheight + 100, winwidth + 200, 10),  # Bot
               pygame.Rect(-100, -100, 10, winheight + 200),  # Left
               pygame.Rect(winwidth + 100, -100, 10, winheight + 200)]  # Right
    gfx_pictures = Gfx("player_ship").get_pictures()
    gfx_counter = 0

    def move(direction):
        Player.direction = direction

    def hit():
        Player.health -= 1 
        if Player.health == 0:  # Game Over
            pygame.quit()
            exit()

    def speed_boost(boost):
        if boost:
            Player.directions = directions(Player.speed * 2)
        else:
            Player.directions = directions(Player.speed)

    def gfx_animation(idx):
        if Player.gfx_counter < 3:
            win.blit(Player.gfx_pictures[Player.gfx_idx[idx]], (Player.hitbox.topleft[0] - 18, Player.hitbox.topleft[1] - 25))
            Player.gfx_counter += 1
        else:
            win.blit(Player.gfx_pictures[Player.gfx_idx[idx] + 1], (Player.hitbox.topleft[0] - 18, Player.hitbox.topleft[1] - 25))
            Player.gfx_counter += 1
        if Player.gfx_counter == 6:
            Player.gfx_counter = 0

    def update():
        # Methode for main gameloop, everithing that needs to be updated every tick

        # Player: move and draw
        Player.hitbox.move_ip(Player.directions[Player.direction])
        # pygame.draw.rect(win, (0, 0, 0), Player.hitbox)
        #  Player: border draw and player out of bounds
        for border in Player.borders:
            # pygame.draw.rect(win, white, border)
            if Player.hitbox.colliderect(border):
                pygame.quit()
                exit()  # Game ove
        Player.gfx_animation(Player.direction)


class Turret:

    shot_lst = []
    angle = 0
    projectile_size = 6
    projectile_speed = 15
    firing = False
    direction = None
    normal_fire_rate = [30, 10]
    fire_rate = normal_fire_rate[0]
    ammunition = normal_fire_rate[1]
    fire_limiter = 0
    star_shot_limiter = 0
    super_shot_limiter = 0
    star_shot_ammo = 30
    super_shot_ammo = 50
    super_shot_fire_rate = [5, 100]
    rocket_ammo = 1
    rocket_fired = False
    rocket = pygame.Rect(-1000, -1000, 1, 1)  # Placeholer rect out of sigth
    angles = Angles_shot_player(projectile_speed)
    rocket_angles = Angles_shot_player(3)
    gun_draw_angles = Angles_shot_player(20)
    gfx_shot_pictures = Gfx("projectile").get_pictures()
    gfx_explosion_pictures = Gfx("explosions").get_pictures()
    gfx_counter = 0
    gfx_counter_ex = 0
    explo = True

    def fire(fire):
        Turret.firing = fire

    def level_up():
        if Levels.level < 13:
            Turret.normal_fire_rate[0] -= 2
        if Levels.level % 10 == 0 and Levels.level < 41:
            Turret.super_shot_fire_rate[0] -= 1
        if Levels.level % 4 and Levels.level != 0:
            Power_ups.star_shot_tubes += 1
        Turret.star_shot_ammo += 1
        Turret.super_shot_ammo += 1

    def rocket_fire():
        Turret.rocket_fired = True
        Turret.rocket_ammo -= 1
        Turret.rocket = pygame.Rect(Player.hitbox.center[0], Player.hitbox.center[1], 10, 10)

    def rocket_reload():
        Turret.rocket_ammo += 1

    def gfx_rocket(arg):
        if arg:
            if Turret.gfx_counter < 3:
                win.blit(Turret.gfx_shot_pictures[4], (Turret.rocket.topleft[0] - 18, Turret.rocket.topleft[1] - 25))
                Turret.gfx_counter += 1
            else:
                win.blit(Turret.gfx_shot_pictures[5], (Turret.rocket.topleft[0] - 18, Turret.rocket.topleft[1] - 25))
                Turret.gfx_counter += 1
            if Turret.gfx_counter == 6:
                Turret.gfx_counter = 0

    def gfx_rocket_explosion():
        if Turret.gfx_counter_ex < 10:
            win.blit(Turret.gfx_explosion_pictures[0], (Turret.rocket.center[0] - 50, Turret.rocket.center[1] - 50))
            Turret.gfx_counter_ex += 1
        elif Turret.gfx_counter_ex < 20:
            win.blit(Turret.gfx_explosion_pictures[1], (Turret.rocket.center[0] - 100, Turret.rocket.center[1] - 100))
            Turret.gfx_counter_ex += 1
        elif Turret.gfx_counter_ex < 30:
            win.blit(Turret.gfx_explosion_pictures[2], (Turret.rocket.center[0] - 250, Turret.rocket.center[1] - 250))
            Turret.gfx_counter_ex += 1
        else:
            win.blit(Turret.gfx_explosion_pictures[3], (Turret.rocket.center[0] - 400, Turret.rocket.center[1] - 400))

    def gfx_shot_animation(shot):
        if Power_ups.super_shot:
            win.blit(Turret.gfx_shot_pictures[1], (shot.topleft[0] - 10, shot.topleft[1] - 10))
        elif Power_ups.star_shot:
            win.blit(Turret.gfx_shot_pictures[2], (shot.topleft[0] - 10, shot.topleft[1] - 10))
        else:
            win.blit(Turret.gfx_shot_pictures[0], (shot.topleft[0] - 10, shot.topleft[1] - 10))

    def gun_draw():
        for ang, loca in [(i, Turret.gun_draw_angles[i]) for i in range(0, 360, 1)]:
            # print(ang, loca)
            if Degrees() <= ang:
                pygame.draw.circle(win, (255, 0, 0), (Player.hitbox.center[0] + int(loca[0]), Player.hitbox.center[1] + int(loca[1])), 4)
                break

    def update():
        # Method for main gameloop, everithing that needs to be updated every tick
        # Gun indicator
        Turret.gun_draw()
        # Shot creation
        if Turret.firing:
            Turret.fire_limiter += 1
            if Turret.fire_limiter > Turret.fire_rate:
                # star_shot
                if Power_ups.star_shot:
                    # Turret.star_shot()
                    Turret.angle = 0
                    Turret.star_shot_limiter += 1
                    Turret.ammunition = 1000
                    if Turret.star_shot_limiter > Turret.star_shot_ammo:
                        Turret.ammunition = Turret.normal_fire_rate[1]
                        Turret.star_shot_limiter = 0
                        Power_ups.star_shot = False
                    for i in range(0, 360, int(360 / Power_ups.star_shot_tubes)):
                        Turret.shot_lst.append(
                            (pygame.Rect(Player.hitbox.center[0], Player.hitbox.center[1], Turret.projectile_size, Turret.projectile_size), Turret.angles[Turret.angle + i]))
                # super_shot
                elif Power_ups.super_shot:
                    # Turret.super_shot()
                    Turret.fire_rate, Turret.ammunition = Turret.super_shot_fire_rate
                    Turret.super_shot_limiter += 1
                    if Turret.super_shot_limiter >= Turret.super_shot_ammo:
                        Turret.fire_rate, Turret.ammunition = Turret.normal_fire_rate
                        Turret.super_shot_limiter = 0
                        Power_ups.super_shot = False
                # normal shot
                Turret.shot_lst.append(
                    (pygame.Rect(Player.hitbox.center[0], Player.hitbox.center[1], Turret.projectile_size, Turret.projectile_size), Turret.angles[Degrees()]))
                Turret.fire_limiter = 0
        if len(Turret.shot_lst) > Turret.ammunition:
            del(Turret.shot_lst)[Turret.ammunition]

        # Shot draw and border collision
        for shot, direction in Turret.shot_lst:
            shot.move_ip(direction)
           # pygame.draw.rect(win, (255, 255, 0), shot)
            Turret.gfx_shot_animation(shot)
            for border in Player.borders:
                try:                                # wierd index bug
                    if shot.colliderect(border):
                        Turret.shot_lst.remove((shot, direction))
                except ValueError:
                    pass
        # Rocket

        Turret.gfx_rocket(Turret.explo)
        if Turret.rocket_fired:
            Turret.rocket.move_ip(Turret.rocket_angles[Degrees()])
            # pygame.draw.circle(win, (150, 0, 0), (Turret.rocket.center[0], Turret.rocket.center[1]), 6)
            # pygame.draw.rect(win, (150, 0, 0), Turret.rocket)
            if abs(Player.hitbox.center[0] - Turret.rocket.center[0]) > 400 or abs(Player.hitbox.center[1] - Turret.rocket.center[1]) > 400:
                Turret.explo = False
                Turret.rocket.inflate_ip(20, 20)
                Turret.gfx_rocket_explosion()
                if abs(Turret.rocket.topleft[0] - Turret.rocket.center[0]) > 400:
                    Turret.rocket = pygame.Rect(-1000, -1000, 1, 1)
                    Turret.rocket_fired = False
                    Turret.gfx_counter_ex = 0
                    Turret.explo = True


class Enemy:

    enemy_lst = []
    speed = [2, 6]
    direction = (0, 79)
    size = (lambda speed=speed[1]: {speed + 1 - i: i * 15 for i in range(1, speed + 1)})()  # oof
    spawn_point = (1, 4)
    gfx_pictures = Gfx("asteroids").get_pictures()
    print(gfx_pictures)

    def __init__(self, direction, speed, spawn_point):
        self.spawn_points = {1: (random.randint(50, winwidth - 50), -50),  # Top
                             2: (random.randint(0, winwidth), winheight + 50),  # Bot
                             3: (-50, random.randint(0, winheight)),  # Left
                             4: (winwidth + 50, random.randint(0, winheight))}  # Right
        self.direction = direction
        self.directions = Angles(speed)
        self.hitbox = pygame.Rect(
            self.spawn_points[spawn_point][0], self.spawn_points[spawn_point][1], 60, 60)
        self.health = 4
        self.score_amount = speed
        self.speed = speed
        self.gfx_idx = 0
        self.animation_counter = 0
        self.animation_speed = Enemy.size[speed]

    def draw(self):
        self.hitbox.move_ip(self.directions[self.direction])
       # pygame.draw.rect(win, (255, 0, 0), self.hitbox)

    def border_collide(self):
        for border in Player.borders:
            if self.hitbox.colliderect(border):
                return True

    def player_collide(self):
        return self.hitbox.colliderect(Player.hitbox)

    def hit_detection(self):
        if self.hitbox.colliderect(Turret.rocket):
            Levels.interval_score += self.score_amount
            Levels.display_score += self.score_amount
            Power_ups.score += self.score_amount
            return True
        for shot, _ in Turret.shot_lst:
            if self.hitbox.colliderect(shot):
                Turret.shot_lst.remove((shot, _))
                self.health -= 1
                if self.health == 0:
                    Levels.interval_score += self.score_amount
                    Levels.display_score += self.score_amount
                    Power_ups.score += self.score_amount
                    return True

    def gfx_animation(self):
        self.animation_counter += 1
        if self.animation_counter == (self.animation_speed * len(Enemy.gfx_pictures)):  # 480
            self.animation_counter = 0
            self.gfx_idx = 0
        if self.animation_counter % self.animation_speed == 0 and self.animation_counter != 0:  # 60
            self.gfx_idx += 1
        win.blit(Enemy.gfx_pictures[self.gfx_idx], (self.hitbox.topleft[0] - 8, self.hitbox.topleft[1] - 15))

    def update():
        # Methode for main gameloop, everithing that needs to be updated every tick

        # Enemy instance creation
        if not Levels.boss_fight:
            for _ in range(Levels.level_up()):
                while len(Enemy.enemy_lst) < Levels.enemy_amount:
                    Enemy.enemy_lst.append(Enemy(
                        random.randint(Enemy.direction[0], Enemy.direction[1]),
                        random.randint(Enemy.speed[0], Enemy.speed[1]),
                        random.randint(Enemy.spawn_point[0], Enemy.spawn_point[1])))

        # Enemy draw and collision detection Border/Player/Shot
        for enemy in Enemy.enemy_lst:
            enemy.draw()
            enemy.gfx_animation()
            if enemy.border_collide() or enemy.hit_detection():
                Enemy.enemy_lst.remove(enemy)
            elif enemy.player_collide():
                Enemy.enemy_lst.remove(enemy)
                Player.hit()


class Bosses:

    boss_lst = []
    boss_shot_lst = []
    limiter = 0
    kills = 0
    health = 50
    gfx_pictures = Gfx("boss_ship").get_pictures()
    gfx_shot_pictures = Gfx("projectile").get_pictures()
    shot_angles = Angles_shot_player(3)
    shot_tubes = 3

    def __init__(self, speed, spawn_point, health):
        self.spawn_points = {1: (winwidth * 0.5 - 200 / 2, -500),
                             2: (winwidth * 0.25 - 200 / 2, -500),
                             3: (winwidth * 0.75 - 200 / 2, -500),
                             4: (winwidth * 0.5 - 200 / 2, -1000),
                             5: (winwidth * 0.25 - 200 / 2, -1000),
                             6: (winwidth * 0.75 - 200 / 2, -1000)}
        self.speed = speed
        self.health = health
        self.score_amount = 20
        self.spawn_point = spawn_point
        self.hitbox = pygame.Rect(self.spawn_points[spawn_point][0], self.spawn_points[spawn_point][1], 100, 330)
        self.limiter = 0
        self.img_idx = random.choice([0, 2])
        self.gfx_counter = 0

    def draw(self):
        self.hitbox.move_ip(0, self.speed)
       # pygame.draw.rect(win, (200, 200, 200), self.hitbox)

    def gfx_animation(self):
        if self.gfx_counter < 2:
            win.blit(Bosses.gfx_pictures[self.img_idx], (self.hitbox.topleft[0] - 30, self.hitbox.topleft[1] - 15))
            self.gfx_counter += 1
        else:
            win.blit(Bosses.gfx_pictures[self.img_idx + 1], (self.hitbox.topleft[0] - 30, self.hitbox.topleft[1] - 15))
            self.gfx_counter += 1
        if self.gfx_counter == 4:
            self.gfx_counter = 0

    def gfx_shot_animation(shot):
        win.blit(Bosses.gfx_shot_pictures[3], (shot.topleft[0] - 10, shot.topleft[1] - 10))

    def collide_border(self):
        if self.hitbox.colliderect(Player.borders[1]):
            return True

    def collide_player(self):
        if self.hitbox.colliderect(Player.hitbox):
            return True

    def boss_shot_create(self):
        self.limiter += 1
        if self.limiter > 80:
            for i in range(0, 360, int(360 / Bosses.shot_tubes)):
                Bosses.boss_shot_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1], 15, 15), Bosses.shot_angles[0 + i]))
            self.limiter = 0

    def boss_fire(self):
        for shot, direction in Bosses.boss_shot_lst:
            shot.move_ip(direction)
            # pygame.draw.rect(win, (255, 0, 0), shot)
            Bosses.gfx_shot_animation(shot)

    def hit_detection(self):
        if self.hitbox.colliderect(Turret.rocket):
            self.health -= 1
        for shot, _ in Turret.shot_lst:
            if self.hitbox.colliderect(shot):
                Turret.shot_lst.remove((shot, _))
                self.health -= 1
                if Power_ups.super_shot and Levels.level > 40:
                    self.health -= 1
        if self.health < 0:
            Levels.interval_score += self.score_amount
            Levels.display_score += self.score_amount
            Power_ups.score += self.score_amount
            Turret.rocket_reload()
            return True

    def boss_create():
        for i in range(Levels.boss_amount):
            Bosses.boss_lst.append(Bosses(1, i + 1, Bosses.health))

    def update():
        if Levels.boss():
            Bosses.boss_create()
            Levels.boss_fight = True
        if Levels.boss_fight:
            for boss in Bosses.boss_lst:
                boss.draw()
                boss.gfx_animation()
                boss.boss_shot_create()
                boss.boss_fire()
                if boss.collide_player():
                    Player.hit()
                elif boss.collide_border():
                    Bosses.kills += 1
                    Player.hit()
                    Bosses.boss_lst.remove(boss)
                elif boss.hit_detection():
                    Bosses.kills += 1

                    Bosses.boss_lst.remove(boss)
                if Bosses.kills == Levels.boss_amount:
                    Levels.boss_fight = False
                    Bosses.kills = 0

            for shot, di in Bosses.boss_shot_lst:
                if shot.colliderect(Player.hitbox):
                    Player.hit()
                    Bosses.boss_shot_lst.remove((shot, di))
            if len(Bosses.boss_shot_lst) > 70:
                del(Bosses.boss_shot_lst)[0]
        else:
            Bosses.boss_lst.clear()
            Bosses.boss_shot_lst.clear()


class Blocker():

    block_lst = []
    gfx_pictures = Gfx("blockers").get_pictures()

    def __init__(self):
        self.hitbox = pygame.Rect((random.randint(-50, winwidth - 50), -400, 250, 250))
        self.speed = 1

    def draw(self):
        self.hitbox.move_ip(0, self.speed)
        pygame.draw.rect(win, (70, 70, 70), self.hitbox)

    def collision(self):
        return self.hitbox.colliderect(Player.borders[1])

    def player_collision(self):
        return self.hitbox.colliderect(Player.hitbox)

    def hit_detection(self):
        for shot, _ in Turret.shot_lst:
            if self.hitbox.colliderect(shot):
                Turret.shot_lst.remove((shot, _))

    def create():
        if not Levels.boss_fight:
            for i in range(Levels.blocker_amount):
                Blocker.block_lst.append(Blocker())

    def gfx_animation(self):
        win.blit(Blocker.gfx_pictures[0], self.hitbox)

    def update():
        if len(Blocker.block_lst) == 0:
            Blocker.create()
        for blocker in Blocker.block_lst:
            blocker.draw()
            blocker.gfx_animation()
            blocker.hit_detection()
            if blocker.collision():
                Blocker.block_lst.remove(blocker)
            elif blocker.player_collision():
                Player.hit()


class Levels:

    interval_score = 0
    display_score = 0
    level = 0
    level_interval = 20
    enemy_amount = 5  # at Start
    enemys_per_level = 1
    boss_amount = 1
    blocker_amount = 1
    boss_fight = False

    def level_up():
        if Levels.interval_score > Levels.level_interval:
            Levels.enemy_amount += Levels.enemys_per_level
            Levels.level += 1
            Levels.level_interval += 5
            Levels.interval_score = 0
            Bosses.health += 2
            Turret.level_up()
            Player.level_up()
        return Levels.enemy_amount

    def boss():
        if Levels.level % 3 == 0 and Levels.level != 0:
            Levels.level += 1
            Bosses.shot_tubes += 1
            for lvl, amount in [(i * 10, i) for i in range(1, 6)]:
                if Levels.level > lvl:
                    Levels.boss_amount = amount + 1
            return True


class Power_ups:

    power_up_lst = []
    super_shot = False
    star_shot = False
    super_shot_amount = 0
    star_shot_amount = 0
    star_shot_tubes = 3
    heal_ammount = 1
    score = 0

    def __init__(self, typ):
        self.hitbox = pygame.Rect(random.randint(100, winwidth - 100), -50, 50, 50)
        self.typ = typ

    def collision(self):
        if self.hitbox.colliderect(Player.hitbox):
            if self.typ == "heal":
                Player.health += Power_ups.heal_ammount
            elif self.typ == "super_shot":
                Turret.super_shot_limiter = 0  # reset bei erneutem einsammeln
                Power_ups.super_shot_amount += 1
            elif self.typ == "star_shot":
                Turret.super_star_limiter = 0
                Power_ups.star_shot_amount += 1
            return True
        elif self.hitbox.colliderect(Player.borders[1]):
            return True

    def use(pup_name):
        if pup_name == "super_shot":
            if Power_ups.super_shot_amount > 0:
                Power_ups.super_shot = True
                Power_ups.super_shot_amount -= 1
        elif pup_name == "star_shot":
            if Power_ups.star_shot_amount > 0:
                Power_ups.star_shot = True
                Power_ups.star_shot_amount -= 1

    def draw(self):
        self.hitbox.move_ip(0, 1)
        if self.typ == "heal":
            pygame.draw.rect(win, (0, 255, 0), self.hitbox)  # green
        elif self.typ == "super_shot":
            pygame.draw.rect(win, (0, 0, 255), self.hitbox)  # blue
        elif self.typ == "star_shot":
            pygame.draw.rect(win, (255, 0, 0), self.hitbox)  # red

    def spawn():
        if Power_ups.score > 30:
            Power_ups.score = 0
            return True

    def update():
        if Power_ups.spawn():
            Power_ups.power_up_lst.append(Power_ups(random.choice(["heal", "super_shot", "star_shot"])))
        for power_up in Power_ups.power_up_lst:
            power_up.draw()
            if power_up.collision():
                Power_ups.power_up_lst.remove(power_up)


def main():

    right, left, up, down = [False, False, False, False]

    def move_condition(bool_1, str_1, bool_2, str_2, str_3):
        if bool_1:
            Player.move(str_1)
        elif bool_2:
            Player.move(str_2)
        else:
            Player.move(str_3)

    while True:
        # print(Clock.get_fps())
        # print(Player.gfx_pictures)
        win.fill(black)
        Background.update()
        Player.update()
        Turret.update()
        Power_ups.update()
        Enemy.update()
        Bosses.update()
        # Blocker.update()
        Interface.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_d:
                    right = True
                    move_condition(up, "right up", down, "right down", "right")
                elif event.key == K_a:
                    left = True
                    move_condition(up, "left up", down, "left down", "left")
                elif event.key == K_w:
                    up = True
                    move_condition(left, "left up", right, "right up", "up")
                elif event.key == K_s:
                    down = True
                    move_condition(left, "left down", right,
                                   "right down", "down")
                elif event.key == K_1:
                    Power_ups.use("super_shot")
                elif event.key == K_2:
                    Power_ups.use("star_shot")
                elif event.key == K_LSHIFT:
                    Player.speed_boost(True)
                if Turret.rocket_ammo > 0 and not Turret.rocket_fired:
                    if event.key == K_LCTRL:
                        Turret.rocket_fire()
            elif event.type == MOUSEBUTTONDOWN:
                Turret.fire(True)
            elif event.type == KEYUP:
                if event.key == K_w:
                    up = False
                elif event.key == K_s:
                    down = False
                elif event.key == K_d:
                    right = False
                elif event.key == K_a:
                    left = False
                elif event.key == K_SPACE:
                    Turret.fire(False)
                elif event.key == K_a or event.key == K_d:
                    Turret.turn(None, False)
                elif event.key == K_LSHIFT:
                    Player.speed_boost(False)
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    exit()

                if [up, down, left, right].count(True) < 2:
                    for con, cmd in [(up, "up"),
                                     (down, "down"),
                                     (right, "right"),
                                     (left, "left"),
                                     (not any([up, down, right, left]), "idle")]:
                        if con:
                            Player.move(cmd)
            elif event.type == MOUSEBUTTONUP:
                Turret.fire(False)
            elif event.type == QUIT:
                pygame.quit()
                exit()
        Clock.tick(fps)
        pygame.display.update()


if __name__ == "__main__":
    main()

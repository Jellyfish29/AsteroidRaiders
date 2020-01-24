import pygame
from pygame.locals import *
import random
import math
import numpy as np
import os
import time

# Title: "Asteroid Raider"
# Author: Clemens Lütge
# CC-BY-NC-SA 4.0

pygame.init()
Clock = pygame.time.Clock()
winwidth = 1920
winheight = 1080
white = (255, 255, 255)
black = (0, 0, 0)
fps = 60
win = pygame.display.set_mode((winwidth, winheight), pygame.FULLSCREEN | pygame.DOUBLEBUF)
# win = pygame.display.set_mode((winwidth, winheight))
pygame.mouse.set_visible(False)


def Angles(speed):
    return {idx: i for idx, i in enumerate(
        [(speed * (i / 100), -speed) for i in range(0, 100, 10)] +
        [(speed, -speed * (-i / 100)) for i in range(-100, 0, 10)] +
        [(speed, speed * (i / 100)) for i in range(0, 100, 10)] +
        [(speed * (-i / 100), speed) for i in range(-100, 0, 10)] +
        [(-speed * (i / 100), speed) for i in range(0, 100, 10)] +
        [(-speed, speed * (-i / 100)) for i in range(-100, 0, 10)] +
        [(-speed, -speed * (i / 100)) for i in range(0, 100, 10)] +
        [(-speed * (-i / 100), -speed) for i in range(-100, 0, 10)]
    )}


def Angles_shot_player(speed):
    return {idx: i for idx, i in enumerate(
        [(speed, speed * (-i / 100)) for i in np.arange(0, 100, 2.23)] +
        [(speed * (-i / 100), -speed) for i in np.arange(-100, 0, 2.23)] +
        [(-speed * (i / 100), - speed) for i in np.arange(0, 100, 2.23)] +
        [(-speed, -speed * (-i / 100)) for i in np.arange(-100, 0, 2.23)] +
        [(-speed, speed * (i / 100)) for i in np.arange(0, 100, 2.23)] +
        [(-speed * (-i / 100), speed) for i in np.arange(-100, 0, 2.23)] +
        [(speed * (i / 100), speed) for i in np.arange(0, 100, 2.23)] +
        [(speed, speed * (-i / 100)) for i in np.arange(-100, 0, 2.23)]
    )}


def Degrees():
    rel_x, rel_y = pygame.mouse.get_pos()[0] - Player.hitbox.center[0], pygame.mouse.get_pos()[1] - Player.hitbox.center[1]
    angle = -math.atan2(rel_y, rel_x)
    angle = math.degrees(angle)
    if angle < 0:
        angle += 360
    return int(angle)


def directions(speed):
    return {
        "up": (0, -speed),
        "down": (0, speed),
        "right": (speed, 0),
        "left": (-speed, 0),
        "right up": (speed * 0.8, -speed * 0.8),
        "right down": (speed * 0.8, speed * 0.8),
        "left up": (-speed * 0.8, -speed * 0.8),
        "left down": (-speed * 0.8, speed * 0.8),
        "idle": (0, 0)
    }


def get_images(kind):
    pathes = [os.path.join(os.getcwd(), f"Gfx\\{kind}\\" + file) for file in os.listdir(os.path.join(os.getcwd(), f"Gfx\\{kind}"))]
    return {idx: pygame.image.load(img).convert_alpha() for idx, img in enumerate(sorted(pathes))}


def rect_not_on_sreen(rect, bot=False):
    if rect.center[0] > winwidth + 120 or rect.center[0] < - 100:
        return True
    if bot:
        if rect.center[1] > winheight + 250:
            return True
    if not bot:
        if rect.center[1] > winheight + 150 or rect.center[1] < - 150:
            return True
    else:
        return False


class Gfx:

    gfx_cursor = get_images("cursor")
    bg = get_images("background")
    y = 0

    def cursor():
        rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0, 0)
        win.blit(Gfx.gfx_cursor[2], (rect.topleft[0] - 17, rect.topleft[1] - 17))

    def background():
        Gfx.y += 0.5
        win.blit(Gfx.bg[0], (0, Gfx.y - winheight))
        win.blit(Gfx.bg[0], (0, Gfx.y))
        if Gfx.y == winheight:
            Gfx.y = 0


class Interface:

    gfx_pictures = get_images("icons")
    inter_lst = []

    def __init__(self, color, location, icon_idx):
        self.font = pygame.font.SysFont("arial", 30, 20)
        self.text = ""
        self.color = color
        self.text_render = self.font.render(self.text, True, color)
        self.location = location
        self.icon_idx = icon_idx
        self.rect = pygame.Rect(self.location[0], self.location[1], 1, 1)

    def draw(self):
        self.text_render = self.font.render(self.text, True, self.color)
        win.blit(self.text_render, self.rect)
        win.blit(Interface.gfx_pictures[self.icon_idx], (self.rect.topleft[0] - 70, self.rect.topleft[1] - 8))

    def create():
        for color, location, icon_idx in[
                ((255, 255, 255), (170, 5), 5),  # Score
                ((255, 255, 255), (170, 40), 5),  # Level
                ((255, 255, 255), (1075, 15), 3),  # health
                ((255, 255, 255), (1340, 15), 3),   # repair
                ((255, 255, 255), (1460, 15), 3),  # shield
                ((255, 255, 255), (1580, 15), 1),  # super_shot
                ((255, 255, 255), (1700, 15), 2),  # star_shot
                ((255, 255, 255), (1820, 15), 4)  # Turret.rocket
        ]:
            Interface.inter_lst.append(Interface(color, location, icon_idx))
        """ Player.speed                 +=
            Player.max_health           +=
            Player.damage               +=
            Turret.fire_rate            -=
            Turret.super_shot_ammo      +=
            Turret.star_shot_ammo       +=
            Power_ups.star_shot_tubes   +="""

    def upgrades(upgrades_pressed):
        pygame.mouse.set_visible(True)
        font = pygame.font.SysFont("arial", 30)
        rects = [pygame.Rect(winwidth / 2 - 350 / 2, (winheight - 300) / 2 + i, 350, 30) for i in range(0, 451, 50)]
        texts = [
            f"Skill Points = {Levels.skill_points}",
            f"{Player.speed}        Speed                           + 15 % ",  # len 57
            f"{Player.max_health}        Max Health                   + 1",
            f"{Player.damage}        Damage                         + 20% ",
            f"{Turret.fire_rate}      Fire Rate                      + 10% ",
            f"{Turret.super_shot_ammo}    Rapid Fire Ammo         + 40 ",
            f"{Turret.star_shot_ammo}      Star Shot Ammo           + 10 ",
            f"{Power_ups.star_shot_tubes}        Star Shot Tubes           + 2 ",
            f"{Power_ups.shield_time / 60}s       Shield Duration         + 2s"
        ]
        render_lst = [(idx, font.render(text, True, (255, 255, 255)), rect) for idx, rect, text in zip([i for i in range(len(rects))], rects, texts)]
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == KEYDOWN:
                    if event.key == K_TAB:
                        pygame.mouse.set_visible(False)
                        main()
            mouse_pos = pygame.mouse.get_pos()
            # print(mouse_pos)
            for idx, text, rect in render_lst:
                win.blit(text, rect)
                if Levels.skill_points > 0:
                    if pygame.mouse.get_pressed()[0] == 1:
                        if rect.collidepoint(mouse_pos):
                            if idx == 1:
                                Player.speed += 0.5
                                Player.directions = directions(Player.speed)
                            elif idx == 2:
                                Player.max_health += 1
                                Player.health += 1
                            elif idx == 3:
                                Player.damage += Player.base_damage * 0.2
                            elif idx == 4:
                                if Turret.fire_rate >= 10:
                                    Turret.fire_rate -= 3
                                    Turret.normal_fire_rate[0] -= 3
                            elif idx == 5:
                                Turret.super_shot_ammo += 40
                            elif idx == 6:
                                Turret.star_shot_ammo += 10
                            elif idx == 7:
                                if Power_ups.star_shot_tubes < 8:
                                    Power_ups.star_shot_tubes += 2
                            elif idx == 8:
                                Power_ups.shield_time += 120
                            Levels.skill_points -= 1
                            main()
            Clock.tick(fps)
            pygame.display.update()

            # time.sleep(10)
            # break

    def update():
        win.blit(Interface.gfx_pictures[0], (pygame.Rect(0, -20, winwidth, 50)))
        for inter, text in zip(Interface.inter_lst, [
                f"Score= {Levels.display_score}",
                f"Level  = {Levels.display_level}",
                f"{Player.health}/{Player.max_health}",
                f"{Power_ups.heal_ammount}",
                f"{Power_ups.shield_amount}",
                f"{Power_ups.super_shot_amount}",
                f"{Power_ups.star_shot_amount}",
                f"{Turret.rocket_ammo}"
        ]):
            setattr(inter, "text", text)
            inter.draw()
        # Red Alert
        if Levels.boss_fight:
            win.blit(Interface.gfx_pictures[6], (pygame.Rect(395, 2, 1, 1)))
        if Levels.skill_points > 0:
            pygame.draw.rect(win, (255, 255, 0), pygame.Rect(35, 20, 30, 30))


class Player:

    health = 4
    max_health = 4
    hitbox = pygame.Rect(winwidth / 2, winheight / 2, 50, 50)
    speed = 3
    base_damage = 1
    damage = base_damage
    direction = "idle"
    directions = directions(speed)
    gfx_idx = {
        "up": 0, "down": 2, "right": 4, "left": 6, "right up": 8, "right down": 10, "left up": 12, "left down": 14, "idle": 16}
    gfx_pictures = get_images("player_ship")
    gfx_hit_effect_pictures = get_images("hit_effects")
    gfx_counter = 0

    def move(direction):
        Player.direction = direction

    def hit(sure_death=False):
        if sure_death:
            Player.health = 0
        elif not Power_ups.shield:
            Player.health -= 1
            Player.gfx_hit_effect()
        if Player.health == 0:
            with open("score.txt", "a")as f:
                f.write(time.strftime("%H:%M:%S") + "   " + time.strftime("%d/%m/%Y") + "\nScore = " + str(Levels.display_score) + "\n")
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

    def gfx_hit_effect():
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect(0, 0, winwidth, winheight))
        win.blit(Player.gfx_hit_effect_pictures[3], (Player.hitbox.topleft[0] - 20, Player.hitbox.topleft[1] - 20))

    def update():
        # Methode for main gameloop, everithing that needs to be updated every tick

        # Player: move and draw
        Player.hitbox.move_ip(Player.directions[Player.direction])
        # pygame.draw.rect(win, (0, 0, 0), Player.hitbox)
        #  Player: border draw and player out of bounds
        if rect_not_on_sreen(Player.hitbox):
            pygame.quit()
            exit()  # Game over
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
    super_shot_fire_rate = [5, 100]
    super_shot_ammo = super_shot_fire_rate[1]
    rocket_ammo = 1
    rocket_fired = False
    rocket = pygame.Rect(-1000, -1000, 1, 1)  # Placeholer rect out of sigth
    angles = Angles_shot_player(projectile_speed)
    rocket_angles = Angles_shot_player(3)
    rocket_degree = 0
    gun_draw_angles = Angles_shot_player(20)
    gfx_shot_pictures = get_images("projectile")
    gfx_explosion_pictures = get_images("explosions")
    gfx_hit_pictures = get_images("hit_effects")
    gfx_counter = 0
    gfx_counter_ex = 0
    explosion = True

    def fire(fire):
        Turret.firing = fire

    def rocket_fire():
        Turret.rocket_fired = True
        Turret.rocket_ammo -= 1
        Turret.rocket = pygame.Rect(Player.hitbox.center[0], Player.hitbox.center[1], 10, 10)
        Turret.rocket_degree = Degrees()

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

    def gfx_hit_effect(shot):
        win.blit(Turret.gfx_hit_pictures[random.choice([0, 1, 2])], (shot.topleft[0] - 10, shot.topleft[1] - 10))

    def gun_draw():
        for ang, loca in [(i, Turret.gun_draw_angles[i]) for i in range(0, 360, 1)]:
            if Degrees() <= ang:
                pygame.draw.circle(win, (255, 0, 0), (Player.hitbox.center[0] + int(loca[0]), Player.hitbox.center[1] + int(loca[1])), 2)
                # win.blit(Turret.gfx_gun[0], (pygame.Rect(Player.hitbox.center[0] + int(loca[0]) - 10, Player.hitbox.center[1] + int(loca[1]) - 5, 1, 1)))
                break

    def update():
        # Method for main gameloop, everything that needs to be updated every tick

        # Gun indicator
        Turret.gun_draw()
        # Shot creation
        if Turret.firing:
            Turret.fire_limiter += 1
            if Turret.fire_limiter > Turret.fire_rate:
                # star_shot
                if Power_ups.star_shot:
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
            if rect_not_on_sreen(shot):
                Turret.shot_lst.remove((shot, direction))
        # Rocket
        Turret.gfx_rocket(Turret.explosion)
        if Turret.rocket_fired:
            Turret.rocket.move_ip(Turret.rocket_angles[Turret.rocket_degree])
            # pygame.draw.rect(win, (150, 0, 0), Turret.rocket)
            if abs(Player.hitbox.center[0] - Turret.rocket.center[0]) > 400 or abs(Player.hitbox.center[1] - Turret.rocket.center[1]) > 400:
                Turret.explosion = False
                Turret.rocket.inflate_ip(20, 20)
                Turret.gfx_rocket_explosion()
                if abs(Turret.rocket.topleft[0] - Turret.rocket.center[0]) > 400:
                    Turret.rocket = pygame.Rect(-1000, -1000, 1, 1)
                    Turret.rocket_fired = False
                    Turret.gfx_counter_ex = 0
                    Turret.explosion = True


class Enemy:

    enemy_lst = []
    speed = [2, 7]
    health = 2.6
    direction = (0, 79)
    size = (lambda speed=speed[1]: {speed + 1 - i: i * 15 for i in range(1, speed + 1)})()  # oof
    spawn_point = (1, 4)
    gfx_pictures_ast = get_images("asteroids")
    spez_gfx = get_images("spez")

    def __init__(self, direction, speed, spawn_point, health):
        self.spawn_points = {
            1: [random.randint(100, winwidth - 50), random.randint(-150, -50)],  # Top
            2: [random.randint(100, winwidth - 50), random.randint(winheight + 50, winheight + 100)],  # Bot
            3: [random.randint(-150, -100), random.randint(0, winheight)],  # random.randint(0, winheight)),  # Left
            4: [random.randint(winwidth, winwidth + 50), random.randint(0, winheight)]  # Right
        }
        self.spawn_point = spawn_point
        self.direction = direction
        self.angles = Angles(speed)
        self.hitbox = pygame.Rect(
            self.spawn_points[spawn_point][0], self.spawn_points[spawn_point][1], 70, 70)
        self.health = health
        self.max_health = self.health
        self.healthbar_len = 70
        self.healthbar_max_len = self.healthbar_len
        self.score_amount = speed + 1
        self.speed = speed
        self.gfx_idx = 0
        self.animation_counter = 0
        self.animation_speed = Enemy.size[speed]
        self.typ = "normal"

    def draw(self):
        self.hitbox.move_ip(self.angles[int(self.direction)])
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)

    def gfx_health_bar(self):
        if self.health < self.max_health:
            pygame.draw.rect(win, (200, 0, 0), (pygame.Rect(self.hitbox.topleft[0], self.hitbox.topleft[1] - 30, 70, 2)))
            pygame.draw.rect(win, (0, 200, 0), (pygame.Rect(self.hitbox.topleft[0], self.hitbox.topleft[1] - 30, self.healthbar_len, 2)))

    def border_collide(self):
        return rect_not_on_sreen(self.hitbox)

    def player_collide(self):
        return self.hitbox.colliderect(Player.hitbox)

    def hit_detection(self):
        if self.hitbox.colliderect(Turret.rocket):
            self.health -= 1
            self.healthbar_len -= self.healthbar_max_len / self.max_health
        for shot, _ in Turret.shot_lst:
            if self.hitbox.colliderect(shot):
                Turret.gfx_hit_effect(shot)
                Turret.shot_lst.remove((shot, _))
                self.health -= Player.damage
                self.healthbar_len -= (self.healthbar_max_len / (self.max_health / Player.damage))
        if self.health <= 0:
            Levels.interval_score += self.score_amount
            Levels.display_score += self.score_amount
            Power_ups.score += self.score_amount
            return True

    def gfx_animation(self):
        if self.typ == "seeker" or self.typ == "shooter":
            if self.animation_counter < 3:
                win.blit(Enemy.spez_gfx[self.gfx_idx[0]], (self.hitbox.center[0] - 40, self.hitbox.center[1] - 50))
                self.animation_counter += 1
            else:
                win.blit(Enemy.spez_gfx[self.gfx_idx[1]], (self.hitbox.center[0] - 40, self.hitbox.center[1] - 50))
                self.animation_counter += 1
            if self.animation_counter == 6:
                self.animation_counter = 0
        else:
            self.animation_counter += 1
            if self.animation_counter == (self.animation_speed * len(Enemy.gfx_pictures_ast)):  # 480
                self.animation_counter = 0
                self.gfx_idx = 0
            if self.animation_counter % self.animation_speed == 0 and self.animation_counter != 0:  # 60
                self.gfx_idx += 1
            win.blit(Enemy.gfx_pictures_ast[self.gfx_idx], (self.hitbox.topleft[0] - 8, self.hitbox.topleft[1] - 15))

    def update():
        # Method for main gameloop

        # Enemy instance creation
        if not Levels.boss_fight:
            while len(Enemy.enemy_lst) < Levels.enemy_amount:
                Enemy.enemy_lst.append(Enemy(
                    random.randint(Enemy.direction[0], Enemy.direction[1]),
                    random.randint(Enemy.speed[0], Enemy.speed[1]),
                    random.randint(Enemy.spawn_point[0], Enemy.spawn_point[1]),
                    Enemy.health
                ))
        # Enemy draw and collision detection Border/Player/Shot
        for enemy in Enemy.enemy_lst:
            enemy.draw()
            enemy.gfx_animation()
            enemy.gfx_health_bar()
            if enemy.border_collide() or enemy.hit_detection():
                Enemy.enemy_lst.remove(enemy)
            elif enemy.player_collide():
                if Power_ups.shield:
                    enemy.health = 0
                else:
                    Player.hit()
                    Enemy.enemy_lst.remove(enemy)


class Spez_enemy(Enemy):

    lst = []
    shot_lst = []
    amount = 6
    health = 2
    shot_gfx = get_images("projectile")

    def __init__(self, typ, spawn):
        self.typ = typ
        self.score_amount = 10
        if self.typ == "seeker":
            super().__init__(1, 4, spawn, Spez_enemy.health + 1)  # direction, speed, spawnpoint, health
            # self.animation_speed = 5
            # self.gfx_idx = (0, 1, 2, 3)
            self.angles = Angles_shot_player(self.speed)
            self.gfx_idx = (8, 9)
            self.typ = typ
            self.score_amount += 2
        elif self.typ == "jumper":
            super().__init__(random.randint(1, 79), 7, spawn, Spez_enemy.health)
            # self.gfx_idx = (4, 5, 6, 7)
            self.distance_count = 0
            self.dir_change_interval = random.randint(5, 40)
            self.typ = typ
            self.score_amount += 4
        elif self.typ == "shooter":
            super(). __init__(1, random.randint(4, 6), spawn, Spez_enemy.health + 2)
            for sp, direction, gfx_idx in [(1, 40, (2, 3)), (2, 79, (6, 7)), (3, 20, (0, 1)), (4, 60, (4, 5))]:
                if self.spawn_point == sp:
                    self.direction = direction
                    self.gfx_idx = gfx_idx
            self.shot_angle = 0
            self.shot_angles = Angles_shot_player(7)
            self.fire_rate = random.randint(60, 100)
            self.limiter = 0
            self.typ = typ
            self.score_amount += 3

    def skills(self):
        # Seeker
        if self.typ == "seeker":
            rel_x, rel_y = Player.hitbox.center[0] - self.spawn_points[self.spawn_point][0], Player.hitbox.center[1] - self.spawn_points[self.spawn_point][1]
            self.direction = -math.atan2(rel_y, rel_x)
            self.direction = math.degrees(self.direction)
            if self.direction < 0:
                self.direction += 360
            if abs(Player.hitbox.center[0] - self.hitbox.center[0]) > 20 or abs(Player.hitbox.center[1] - self.hitbox.center[1]) > 20:
                self.spawn_points[self.spawn_point][0] = self.hitbox.center[0]
                self.spawn_points[self.spawn_point][1] = self.hitbox.center[1]
        # jumper
        elif self.typ == "jumper":
            self.distance_count += 1
            if self.distance_count >= self.dir_change_interval:
                self.direction = random.randint(0, 79)
                self.distance_count = 0
        # shooter
        elif self.typ == "shooter":
            rel_x, rel_y = Player.hitbox.center[0] - self.hitbox.center[0], Player.hitbox.center[1] - self.hitbox.center[1]
            self.shot_angle = -math.atan2(rel_y, rel_x)
            self.shot_angle = math.degrees(self.shot_angle)
            if self.shot_angle < 0:
                self.shot_angle += 360
            self.limiter += 1
            if self.limiter > self.fire_rate:
                Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1], 7, 7), self.shot_angles[int(self.shot_angle)]))
                self.limiter = 0

    def gfx_shot(rect):
        win.blit(Spez_enemy.shot_gfx[6], (rect))

    def spez_event(kind):
        if not Levels.boss_fight:
            Levels.spez_event_trigger = 0
            spawn = random.randint(1, 4)
            if kind == "wave":
                for i in range(15):
                    Enemy.enemy_lst.append(Enemy(40, 5, 1, Enemy.health))
            elif kind == "jumper":
                for i in range(10 + Levels.level):
                    Spez_enemy.lst.append(Spez_enemy(kind, spawn))
            elif kind == "shooter":
                for i in range(3 + int(Levels.level / 6)):
                    Spez_enemy.lst.append(Spez_enemy(kind, spawn))
            elif kind == "seeker":
                for i in range(2 + int(Levels.level / 10)):
                    Spez_enemy.lst.append(Spez_enemy(kind, spawn))

    def update():
        # create instances
        if not Levels.boss_fight:
            while len(Spez_enemy.lst) < Spez_enemy.amount:
                Spez_enemy.lst.append(Spez_enemy(random.choice(["shooter", "seeker", "jumper"]), random.randint(1, 4)))  # "seeker", random.randint(1, 4)))
        # draw, update, skills, ...
        for spez in Spez_enemy.lst:
            spez.draw()
            spez.gfx_animation()
            spez.skills()
            spez.gfx_health_bar()
            if spez.border_collide() or spez.hit_detection():
                Spez_enemy.lst.remove(spez)
            elif spez.player_collide():
                Spez_enemy.lst.remove(spez)
                Player.hit()
        # Shot draw / hitdetection
        for shot, angle in Spez_enemy.shot_lst:
            shot.move_ip(angle)
            Spez_enemy.gfx_shot(shot)
            # pygame.draw.rect(win, (255, 0, 0), shot)
            if shot.colliderect(Player.hitbox):
                Player.hit()
                Spez_enemy.shot_lst.remove((shot, angle))
            if rect_not_on_sreen(shot):
                Spez_enemy.shot_lst.remove((shot, angle))


class Bosses:

    boss_lst = []
    boss_shot_lst = []
    kills = 0
    health = 50
    gfx_pictures = get_images("boss_ship")
    gfx_shot_pictures = get_images("projectile")
    shot_angles = Angles_shot_player(3)
    shot_tubes = 3
    border = pygame.Rect(-100, winheight + 350, winwidth + 200, 10)
    fire_rate = 100

    def __init__(self, speed, spawn_point, health):
        self.spawn_points = {
            1: (winwidth * 0.5 - 200 / 2, random.randint(-600, -500)),
            2: (winwidth * 0.25 - 200 / 2, random.randint(-600, -500)),
            3: (winwidth * 0.75 - 200 / 2, random.randint(-600, -500)),
            4: (winwidth * 0.5 - 200 / 2, random.randint(-1200, -1000)),
            5: (winwidth * 0.25 - 200 / 2, random.randint(-1200, -1000)),
            6: (winwidth * 0.75 - 200 / 2, random.randint(-1200, -1000))
        }
        self.speed = speed
        self.health = health
        self.max_health = health
        self.healthbar_len = 100
        self.healthbar_max_len = self.healthbar_len
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

    def gfx_health_bar(self):
        pygame.draw.rect(win, (200, 0, 0), pygame.Rect(self.hitbox.topleft[0], self.hitbox.topleft[1] - 40, 100, 3))
        pygame.draw.rect(win, (0, 200, 0), pygame.Rect(self.hitbox.topleft[0], self.hitbox.topleft[1] - 40, self.healthbar_len, 3))

    def collide_border(self):
        return rect_not_on_sreen(self.hitbox, True)

    def collide_player(self):
        if self.hitbox.colliderect(Player.hitbox):
            return True

    def boss_shot_create(self):
        self.limiter += 1
        if self.limiter > Bosses.fire_rate:
            for i in range(0, 360, int(360 / int(Bosses.shot_tubes))):
                Bosses.boss_shot_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1], 15, 15), Bosses.shot_angles[0 + i]))
            self.limiter = 0

    def hit_detection(self):
        if self.hitbox.colliderect(Turret.rocket):
            if not Turret.explosion:
                self.health -= 1
                self.healthbar_len -= self.healthbar_max_len / self.max_health
        for shot, _ in Turret.shot_lst:
            if self.hitbox.colliderect(shot):
                Turret.gfx_hit_effect(shot)
                Turret.shot_lst.remove((shot, _))
                self.health -= Player.damage
                self.healthbar_len -= (self.healthbar_max_len / (self.max_health / Player.damage))
        if self.health < 0:
            Levels.interval_score += self.score_amount
            Levels.display_score += self.score_amount
            Power_ups.score += self.score_amount
            return True

    def boss_create():
        for i in range(Levels.boss_amount):
            Bosses.boss_lst.append(Bosses(1, i + 1, Bosses.health))

    def update():
        # Methode for main game loop
        # if Levels.boss_trigger():

        #     Levels.boss_fight = True
        if Levels.boss_fight:
            for boss in Bosses.boss_lst:
                boss.draw()
                boss.gfx_animation()
                boss.boss_shot_create()
                boss.gfx_health_bar()
                if boss.collide_player():
                    Player.hit(True)
                elif boss.collide_border():
                    Bosses.kills += 1
                    Player.hit()
                    Bosses.boss_lst.remove(boss)
                elif boss.hit_detection():
                    Bosses.kills += 1
                    Bosses.boss_lst.remove(boss)
                    Bosses.fire_rate -= 20
                if Bosses.kills == Levels.boss_amount:
                    Levels.boss_fight = False
                    Bosses.kills = 0
                    Turret.rocket_reload()
                    Enemy.enemy_lst.clear()  # Reset

            for shot, direction in Bosses.boss_shot_lst:
                shot.move_ip(direction)
                Bosses.gfx_shot_animation(shot)
                if shot.colliderect(Player.hitbox):
                    Player.hit()
                    Bosses.boss_shot_lst.remove((shot, direction))
                elif rect_not_on_sreen(shot):
                    Bosses.boss_shot_lst.remove((shot, direction))
            if len(Bosses.boss_shot_lst) > 100:
                del(Bosses.boss_shot_lst)[0]
        else:
            Bosses.boss_lst.clear()
            Bosses.boss_shot_lst.clear()
            Bosses.fire_rate = 100


class Blocker():

    block_lst = []
    gfx_pictures = get_images("blockers")

    def __init__(self):
        self.hitbox = pygame.Rect((random.randint(-50, winwidth - 50), random.randint(-1500, -400), 250, 250))
        self.speed = 1
        self.gfx_idx = random.choice([0, 1])

    def draw(self):
        self.hitbox.move_ip(0, self.speed)
        # pygame.draw.rect(win, (70, 70, 70), self.hitbox)

    def collision(self):
        return self.hitbox.colliderect(Bosses.border)

    def player_collision(self):
        return self.hitbox.colliderect(Player.hitbox)

    def hit_detection(self):
        for shot, _ in Spez_enemy.shot_lst:
            if self.hitbox.colliderect(shot):
                Spez_enemy.shot_lst.remove((shot, _))
        for shot, _ in Turret.shot_lst:
            if self.hitbox.colliderect(shot):
                Turret.gfx_hit_effect(shot)
                Turret.shot_lst.remove((shot, _))

    def create():
        if not Levels.boss_fight:
            for i in range(Levels.blocker_amount):
                Blocker.block_lst.append(Blocker())

    def gfx_animation(self):
        win.blit(Blocker.gfx_pictures[self.gfx_idx], (self.hitbox.topleft[0] - 30, self.hitbox.topleft[1] - 40))

    def update():
        # methode for main game loop

        if len(Blocker.block_lst) == 0:
            Blocker.create()
        for blocker in Blocker.block_lst:
            blocker.draw()
            blocker.gfx_animation()
            blocker.hit_detection()
            if blocker.collision():
                Blocker.block_lst.remove(blocker)
            elif blocker.player_collision():
                Player.hit(True)


class Levels:

    interval_score = 0
    display_score = 0
    display_level = 1
    level = 1
    level_interval = 20
    enemy_amount = 4  # at Start
    enemys_per_level = 1
    boss_amount = 1
    blocker_amount = 1
    boss_fight = False
    skill_points = 0
    spez_event_trigger = 0

    def level_up():
        if Levels.interval_score > Levels.level_interval:
            # Levels.enemy_amount += Levels.enemys_per_level
            Levels.level += 1
            Levels.display_level += 1
            Levels.level_interval += 15
            Power_ups.interval += 3
            Levels.skill_points += 1
            Levels.spez_event_trigger = random.randint(1, 4)
            Levels.boss_trigger()
            Levels.enemy_scaling()
            Levels.interval_score = 0

    def boss_trigger():
        if Levels.level % 4 == 0 and Levels.level != 0:
            # Levels.level += 1
            Bosses.shot_tubes += 0.4
            for lvl, amount in [(i * 10, i) for i in range(1, 6)]:
                if Levels.level > lvl:
                    Levels.boss_amount = amount + 1
            Levels.boss_fight = True
            Bosses.boss_create()

    def enemy_scaling():
        Enemy.health += 0.2
        Spez_enemy.health += 0.3
        if Levels.level % 10 == 0:
            Spez_enemy.amount += 1
        elif Levels.level % 3 == 0:
            Levels.enemy_amount += 1
        elif Levels.level % 15 == 0:
            Levels.blocker_amount += 1
        print(Levels.enemy_amount)


class Power_ups:

    power_up_lst = []
    super_shot = False
    star_shot = False
    shield = False
    super_shot_amount = 0
    star_shot_amount = 0
    shield_amount = 0
    heal_ammount = 1
    shield_counter = 0
    shield_time = 240
    star_shot_tubes = 2
    score = 0
    interval = 30
    gfx_pictures = get_images("power_ups")

    def __init__(self, typ):
        self.hitbox = pygame.Rect(random.randint(100, winwidth - 100), -200, 50, 240)
        self.typ = typ
        self.gfx_counter = 0
        if typ == "star_shot":
            self.gfx_idx = (0, 1)
        elif typ == "super_shot":
            self.gfx_idx = (2, 3)
        elif typ == "heal":
            self.gfx_idx = (4, 5)
        elif typ == "shield":
            self.gfx_idx = (0, 1)

    def collision(self):
        if self.hitbox.colliderect(Player.hitbox):
            if self.typ == "heal":
                Power_ups.heal_ammount += 1
            elif self.typ == "super_shot":
                Turret.super_shot_limiter = 0  # reset bei erneutem einsammeln
                Power_ups.super_shot_amount += 1
            elif self.typ == "star_shot":
                Turret.super_star_limiter = 0
                Power_ups.star_shot_amount += 1
            elif self.typ == "shield":
                Power_ups.shield_amount += 1
            return True
        return rect_not_on_sreen(self.hitbox, True)

    def use(pup_name):
        if pup_name == "super_shot":
            if Power_ups.super_shot_amount > 0:
                Power_ups.super_shot = True
                Power_ups.super_shot_amount -= 1
        elif pup_name == "star_shot":
            if Power_ups.star_shot_amount > 0:
                Power_ups.star_shot = True
                Power_ups.star_shot_amount -= 1
        elif pup_name == "shield":
            if Power_ups.shield_amount > 0:
                Power_ups.shield_amount -= 1
                Power_ups.shield_counter = 0
                Power_ups.shield = True
        elif pup_name == "heal":
            if Power_ups.heal_ammount > 0:
                Power_ups.heal_ammount -= 1
                Player.health += 2
                if Player.health > Player.max_health:
                    Player.health = Player.max_health

    def draw(self):
        self.hitbox.move_ip(0, 1)
        if self.typ == "shield":
            pygame.draw.rect(win, (0, 255, 255), self.hitbox)  # green
        # elif self.typ == "super_shot":
        #     pygame.draw.rect(win, (0, 0, 255), self.hitbox)  # blue
        # elif self.typ == "star_shot":
        #     pygame.draw.rect(win, (255, 0, 0), self.hitbox)  # red

    def gfx_animation(self):
        if self.gfx_counter < 4:
            win.blit(Power_ups.gfx_pictures[self.gfx_idx[0]], (self.hitbox.topleft[0], self.hitbox.topleft[1]))
            self.gfx_counter += 1
        else:
            win.blit(Power_ups.gfx_pictures[self.gfx_idx[1]], (self.hitbox.topleft[0], self.hitbox.topleft[1]))
            self.gfx_counter += 1
        if self.gfx_counter == 8:
            self.gfx_counter = 0

    def draw_shield():
        shield_rect = pygame.Rect(Player.hitbox.topleft[0] - 25, Player.hitbox.topleft[1] - 25, 100, 100)
        pygame.draw.rect(win, (0, 240, 220), shield_rect)

    def spawn():
        if Power_ups.score > Power_ups.interval:
            Power_ups.score = 0
            return True

    def update():
        if Power_ups.spawn():
            Power_ups.power_up_lst.append(Power_ups(random.choice(["heal", "super_shot", "star_shot", "shield"])))
        for power_up in Power_ups.power_up_lst:
            power_up.draw()
            power_up.gfx_animation()
            if power_up.collision():
                Power_ups.power_up_lst.remove(power_up)
        if Power_ups.shield:
            Power_ups.draw_shield()
            Power_ups.shield_counter += 1
            if Power_ups.shield_counter > Power_ups.shield_time:
                Power_ups.shield = False
                Power_ups.shield_counter = 0


def main():

    right, left, up, down = [False, False, False, False]

    def move_condition(bool_1, str_1, bool_2, str_2, str_3):
        if bool_1:
            Player.move(str_1)
        elif bool_2:
            Player.move(str_2)
        else:
            Player.move(str_3)

    shooter_event, jumper_event, seeker_event, wave_event = [pygame.USEREVENT + i for i in range(1, 5)]

    event_conditions = [
        (lambda: Levels.spez_event_trigger == 1, pygame.event.Event(shooter_event)),
        (lambda: Levels.spez_event_trigger == 2, pygame.event.Event(jumper_event)),
        (lambda: Levels.spez_event_trigger == 3, pygame.event.Event(seeker_event)),
        (lambda: Levels.spez_event_trigger == 4, pygame.event.Event(wave_event))
    ]

    Interface.create()

    while True:
        # print(Clock.get_fps())
        # win.fill(black)
        Gfx.background()
        Blocker.update()
        Power_ups.update()
        Player.update()
        Turret.update()
        Enemy.update()
        Spez_enemy.update()
        Bosses.update()
        Interface.update()
        Levels.level_up()
        for spez_event in map(pygame.event.post, [event for (condition, event) in event_conditions if condition()]):
            spez_event
        for event in pygame.event.get():
            for typ, kind in [
                (shooter_event, "shooter"),
                (jumper_event, "jumper"),
                (seeker_event, "seeker"),
                (wave_event, "wave")
            ]:
                if event.type == typ:
                    Spez_enemy.spez_event(kind)
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
                    move_condition(left, "left down", right, "right down", "down")
                elif event.key == K_1:
                    Power_ups.use("heal")
                elif event.key == K_2:
                    Power_ups.use("shield")
                elif event.key == K_3:
                    Power_ups.use("super_shot")
                elif event.key == K_4:
                    Power_ups.use("star_shot")
                elif event.key == K_TAB:
                    Interface.upgrades(True)
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
                elif event.key == K_LSHIFT:
                    Player.speed_boost(False)
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    exit()

                if [up, down, left, right].count(True) < 2:
                    for con, cmd in [
                        (up, "up"),
                        (down, "down"),
                        (right, "right"),
                        (left, "left"),
                        (not any([up, down, right, left]), "idle")
                    ]:
                        if con:
                            Player.move(cmd)
            elif event.type == MOUSEBUTTONUP:
                Turret.fire(False)
            elif event.type == QUIT:
                pygame.quit()
                exit()
        Gfx.cursor()
        Clock.tick(fps)
        pygame.display.update()


if __name__ == "__main__":
    main()

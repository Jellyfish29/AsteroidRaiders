import pygame
from pygame.locals import *
import random
import math
import numpy as np


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
    print("ooF")

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


class Score_board:

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
            Score_board(text, color, location).draw()


class Player:

    health = 3
    hitbox = pygame.Rect(winwidth / 2, winheight / 2, 50, 50)
    speed = 3
    angles = Angles_shot_player(3)
    direction = "idle"
    invu_time = 41
    # directions = {"right": (speed, 0), "left": (-speed, 0), "idle": (0, 0)}
    borders = [pygame.Rect(-100, -100, winwidth + 200, 10),  # Top
               pygame.Rect(-100, winheight + 100, winwidth + 200, 10),  # Bot
               pygame.Rect(-100, -100, 10, winheight + 200),  # Left
               pygame.Rect(winwidth + 100, -100, 10, winheight + 200)]  # Right

    def strafe(direction):  # strafe
        Player.direction = direction

    def move(direction):
        Player.direction = direction

    def hit():
        Player.health -= 1
        if Player.health == 0:  # Game Over
            pygame.quit()
            exit()

    def update():
        # Methode for main gameloop, everithing that needs to be updated every tick

        # Player: move and draw
        if Player.direction == "forward":
            Player.hitbox.move_ip(Player.angles[Degrees()])
        elif Player.direction == "backward":
            if Degrees() < 180:
                Player.hitbox.move_ip(Player.angles[Degrees() + 180])
            else:
                Player.hitbox.move_ip(Player.angles[Degrees() - 180])
        elif Player.direction == "left":
            if Degrees() > 270:
                Player.hitbox.move_ip(Player.angles[Degrees() - 270])
                print(Degrees() - 270)
            else:
                Player.hitbox.move_ip(Player.angles[Degrees() + 89])
        elif Player.direction == "right":
            if Degrees() < 90:
                Player.hitbox.move_ip(Player.angles[Degrees() + 270])
            else:
                Player.hitbox.move_ip(Player.angles[Degrees() - 90])
        elif Player.direction == "idle":
            Player.hitbox.move_ip(0, 0)
        pygame.draw.rect(win, (255, 0, 0), Player.hitbox)
        #  Player: border draw and player out of bounds
        for border in Player.borders:
            pygame.draw.rect(win, white, border)
            if Player.hitbox.colliderect(border):
                pygame.quit()
                exit()  # Game ove


class Turret:

    shot_lst = []
    angle = 0
    projectile_size = 6
    projectile_speed = 15
    firing = False
    turning = False
    turn_rate = 0.5
    turn_limiter = 0
    direction = None
    normal_fire_rate = [30, 25]
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

    def turn(direction, turning):
        Turret.turning = turning
        Turret.direction = direction

    def fire(fire):
        Turret.firing = fire

    def level_up():
        if Levels.level < 20:
            Turret.normal_fire_rate[0] -= 1
        if Levels.level == 10 or Levels.level == 20 or Levels.level == 30:
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

    def gun_draw():
        for ang, loca in [(i, Turret.gun_draw_angles[i]) for i in range(0, 360, 1)]:
            # print(ang, loca)
            if Degrees() <= ang:
                pygame.draw.circle(win, (230, 230, 0), (Player.hitbox.center[0] + int(loca[0]), Player.hitbox.center[1] + int(loca[1])), 4)
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
        # Turret turning
        if Turret.turning:
            # print(Turret.angle)
            Turret.turn_limiter += 1  # get_time_rate()
            if Turret.turn_limiter > Turret.turn_rate:
                if Turret.direction == "right":
                    Turret.angle += 1
                    if Turret.angle == len(Turret.angles):
                        Turret.angle = 0
                elif Turret.direction == "left":
                    Turret.angle -= 1
                    if Turret.angle == -1:
                        Turret.angle = len(Turret.angles) - 1
                Turret.turn_limiter = 0
        # Shot draw and border collision
        for shot, direction in Turret.shot_lst:
            shot.move_ip(direction)
            pygame.draw.rect(win, (255, 255, 0), shot)
            for border in Player.borders:
                try:                                # wierd index bug
                    if shot.colliderect(border):
                        Turret.shot_lst.remove((shot, direction))
                except ValueError:
                    pass
        # Rocket
        if Turret.rocket_fired:
            Turret.rocket.move_ip(Turret.rocket_angles[Degrees()])
            # pygame.draw.circle(win, (150, 0, 0), (Turret.rocket.center[0], Turret.rocket.center[1]), 6)
            pygame.draw.rect(win, (150, 0, 0), Turret.rocket)
            if abs(Player.hitbox.center[0] - Turret.rocket.center[0]) > 400 or abs(Player.hitbox.center[1] - Turret.rocket.center[1]) > 400:
                Turret.rocket.inflate_ip(20, 20)
                if abs(Turret.rocket.topleft[0] - Turret.rocket.center[0]) > 400:
                    Turret.rocket = pygame.Rect(-1000, -1000, 1, 1)
                    Turret.rocket_fired = False


class Enemy:

    enemy_lst = []
    speed = [2, 6]
    direction = (0, 79)
    size = (lambda speed=speed[1]: {speed + 1 - i: i * 15 for i in range(1, speed + 1)})()  # oof
    spawn_point = (1, 4)

    def __init__(self, direction, speed, spawn_point):
        self.spawn_points = {1: (random.randint(50, winwidth - 50), -50),  # Top
                             2: (random.randint(0, winwidth), winheight + 50),  # Bot
                             3: (-50, random.randint(0, winheight)),  # Left
                             4: (winwidth + 50, random.randint(0, winheight))}  # Right
        self.direction = direction
        self.directions = Angles(speed)
        self.hitbox = pygame.Rect(
            self.spawn_points[spawn_point][0], self.spawn_points[spawn_point][1], Enemy.size[speed], Enemy.size[speed])
        self.health = int(Enemy.size[speed] / 15)
        self.score_amount = int(Enemy.size[speed] / 15)

    def draw(self):
        self.hitbox.move_ip(self.directions[self.direction])
        pygame.draw.rect(win, white, self.hitbox)

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

    def __init__(self, size, speed, spawn_point, health):
        self.spawn_points = {1: (winwidth * 0.5 - size / 2, -500),
                             2: (winwidth * 0.25 - size / 2, -500),
                             3: (winwidth * 0.75 - size / 2, -500),
                             4: (winwidth * 0.5 - size / 2, -1000),
                             5: (winwidth * 0.25 - size / 2, -1000),
                             6: (winwidth * 0.75 - size / 2, -1000)}
        self.speed = speed
        self.health = health
        self.score_amount = 20
        self.spawn_point = spawn_point
        self.angles = Angles(3)
        self.hitbox = pygame.Rect(self.spawn_points[spawn_point][0], self.spawn_points[spawn_point][1], size, size)
        self.limiter = 0

    def draw(self):
        self.hitbox.move_ip(0, self.speed)
        pygame.draw.rect(win, (200, 200, 200), self.hitbox)

    def collide(self):
        if self.hitbox.colliderect(Player.hitbox) or self.hitbox.colliderect(Player.borders[1]):
            return True

    def boss_shot_create(self):
        self.limiter += 1
        if self.limiter > 80:
            for i in range(0, 79, 10):
                Bosses.boss_shot_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1], 15, 15), self.angles[0 + i]))
            self.limiter = 0

    def boss_fire(self):
        for shot, direction in Bosses.boss_shot_lst:
            shot.move_ip(direction)
            pygame.draw.rect(win, (255, 0, 0), shot)

    def hit_detection(self):
        if self.hitbox.colliderect(Turret.rocket):
            self.health -= 30
        for shot, _ in Turret.shot_lst:
            if self.hitbox.colliderect(shot):
                Turret.shot_lst.remove((shot, _))
                self.health -= 1
        if self.health < 0:
            Levels.interval_score += self.score_amount
            Levels.display_score += self.score_amount
            Power_ups.score += self.score_amount
            Turret.rocket_reload()
            return True

    def boss_create():
        for i in range(Levels.boss_amount):
            Bosses.boss_lst.append(Bosses(400, 1, i + 1, Bosses.health))

    def update():
        if Levels.boss():
            Bosses.boss_create()
            Levels.boss_fight = True
        if Levels.boss_fight:
            for boss in Bosses.boss_lst:
                boss.draw()
                boss.boss_shot_create()
                boss.boss_fire()
                if boss.collide():
                    Player.hit()
                    Bosses.boss_shot_lst.remove(boss)
                elif boss.hit_detection():
                    Bosses.kills += 1
                    if Bosses.kills == Levels.boss_amount:
                        Levels.boss_fight = False
                        Bosses.kills = 0
                    Bosses.boss_lst.remove(boss)
            for shot, di in Bosses.boss_shot_lst:
                if shot.colliderect(Player.hitbox):
                    Player.hit()
                    Bosses.boss_shot_lst.remove((shot, di))
            if len(Bosses.boss_shot_lst) > 70:
                del(Bosses.boss_shot_lst)[0]
        else:
            Bosses.boss_lst.clear()
            Bosses.boss_shot_lst.clear()


class Levels:

    interval_score = 0
    display_score = 0
    level = 0
    level_interval = 20
    enemy_amount = 5  # at Start
    enemys_per_level = 1
    boss_amount = 0
    boss_fight = False

    def level_up():
        if Levels.interval_score > Levels.level_interval:
            Levels.enemy_amount += Levels.enemys_per_level
            Levels.level += 1
            Levels.level_interval += 5
            Levels.interval_score = 0
            Bosses.health += 2
            Turret.level_up()
        return Levels.enemy_amount

    def boss():
        if Levels.level % 3 == 0 and Levels.level != 0:
            Levels.level += 1
            for lvl, amount in [(i * 10, i) for i in range(1, 6)]:
                if Levels.level > lvl:
                    Levels.boss_amount = amount + 1
                    break
            else:
                Levels.boss_amount = 1
            return True


class Power_ups:

    power_up_lst = []
    super_shot = False
    star_shot = False
    super_shot_amount = 1
    star_shot_amount = 0
    star_shot_tubes = 0
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
    # for i in range(315, 360, 1):
    #     print(Angles_shot_player(1)[i])

    right, left, forward, backward = [False, False, False, False]

    # move_condition(if, move, elif, move ,"(else)" move)

    while True:
        # print(Clock.get_fps())
        # print(Degrees())
        win.fill(black)
        Player.update()
        Turret.update()
        Power_ups.update()
        Enemy.update()
        Bosses.update()
        Score_board.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_d:
                    right = True
                    Player.move("right")
                elif event.key == K_a:
                    Player.move("left")
                    left = True
                elif event.key == K_w:
                    forward = True
                    Player.move("forward")
                elif event.key == K_s:
                    backward = True
                    Player.move("backward")
                elif event.key == K_LEFT:
                    Turret.turn("left", True)
                elif event.key == K_RIGHT:
                    Turret.turn("right", True)

                elif event.key == K_1:
                    Power_ups.use("super_shot")
                elif event.key == K_2:
                    Power_ups.use("star_shot")
                if Turret.rocket_ammo > 0 and not Turret.rocket_fired:
                    if event.key == K_LCTRL:
                        Turret.rocket_fire()
            elif event.type == MOUSEBUTTONDOWN:
                Turret.fire(True)
            elif event.type == KEYUP:
                if event.key == K_w:
                    forward = False
                elif event.key == K_s:
                    backward = False
                elif event.key == K_d:
                    right = False
                elif event.key == K_a:
                    left = False
                elif event.key == K_SPACE:
                    Turret.fire(False)
                elif event.key == K_LEFT or event.key == K_RIGHT:
                    Turret.turn(None, False)
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    exit()

                if [forward, backward, left, right].count(True) < 2:
                    for con, cmd in [(forward, "forward"),
                                     (backward, "backward"),
                                     (right, "right"),
                                     (left, "left"),
                                     (not any([forward, backward, right, left]), "idle")]:
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

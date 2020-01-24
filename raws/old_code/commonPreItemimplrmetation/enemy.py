import pygame
from pygame.locals import *
import random

from init import *
from astraid_funcs import *
from Gfx import Gfx
import player as pl
import turret as tr
import levels as lvl
import power_ups as pup
""" Gfx class:
        Methods: shot_hit_effect(), create_effect()
    Player class:
        Attributes: Player.hitbox, Player.damage
        Methods: Player.hit()
    Turret class:
        Attributes: Turret.shot_lst, Turret.missile_lst, Turret.pd_lst, Turret.nuke
        Methods:  Turret.missile_aquisition()
    Levels class:
        Attributes: Levels.display_score , Levels.interval_score, Levels.boss_fight, Levels.enemy_amount
    Power_ups class:
        Attributes: Power_ups-score, Power_ups.shield
"""


class Enemy:

    enemy_lst = []
    speed = [2, 7]
    health = 2.6
    direction = (0, 79)
    size = (lambda speed=speed[1]: {speed + 1 - i: i * 15 for i in range(1, speed + 1)})()  # oof
    spawn_point = (1, 4)
    gfx_pictures_ast = get_images("asteroids")
    spez_gfx = get_images("spez")
    boss_gfx = get_images("boss_ship")

    def __init__(self, direction, speed, spawn_point, health):
        self.spawn_points = {
            1: [random.randint(100, winwidth - 50), random.randint(-150, -50)],  # Top
            2: [random.randint(100, winwidth - 50), random.randint(winheight + 50, winheight + 100)],  # Bot
            3: [random.randint(-150, -100), random.randint(0, winheight)],  # random.randint(0, winheight)),  # Left
            4: [random.randint(winwidth, winwidth + 50), random.randint(0, winheight)]  # Right
        }
        self.spawn_point = spawn_point
        self.direction = direction
        self.angles = angles_80(speed)
        self.hitbox = pygame.Rect(
            self.spawn_points[spawn_point][0], self.spawn_points[spawn_point][1], 70, 70)
        self.health = health
        self.max_health = self.health
        self.healthbar_len = 70
        self.healthbar_height = 1
        self.healthbar_max_len = self.healthbar_len
        self.score_amount = speed + 1
        self.speed = speed
        self.gfx_idx = 0
        self.animation_speed = Enemy.size[speed]
        self.typ = "normal"
        self.skill = "normal"
        self.enemy_tc = Time_controler()

    def draw(self):
        self.hitbox.move_ip(self.angles[int(self.direction)])
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)

    def gfx_health_bar(self):
        if self.health < self.max_health:
            pygame.draw.rect(win, (200, 0, 0), (pygame.Rect(self.hitbox.topleft[0], self.hitbox.topleft[1] - 30, self.healthbar_max_len, self.healthbar_height)))
            pygame.draw.rect(win, (0, 200, 0), (pygame.Rect(self.hitbox.topleft[0], self.hitbox.topleft[1] - 30, self.healthbar_len, self.healthbar_height)))

    def border_collide(self):
        return rect_not_on_sreen(self.hitbox, bot=False, strict=False)

    def player_collide(self):
        if self.hitbox.colliderect(pl.Player.hitbox):
            Gfx.create_effect("enexplo", 5, (self.hitbox.topleft[0] - 20, self.hitbox.topleft[1] - 30))
            return True

    def hit_detection(self, missile_hit):
        for missile in tr.Turret.missile_lst:
            if self.hitbox.colliderect(missile):
                self.health -= pl.Player.damage * 4
                self.healthbar_len -= (self.healthbar_max_len / (self.max_health / (pl.Player.damage * 4)))
                Gfx.create_effect("shot_hit", 7, (missile.topleft[0] - 10, missile.topleft[1] - 10))
                tr.Turret.missile_lst.remove(missile)
        if self.hitbox.colliderect(tr.Turret.nuke):
            self.health -= 1.5
            self.healthbar_len -= (self.healthbar_max_len / (self.max_health / 2))
        for shot, _ in tr.Turret.shot_lst:
            if self.hitbox.colliderect(shot):
                Gfx.shot_hit_effect(shot)
                tr.Turret.shot_lst.remove((shot, _))
                self.health -= pl.Player.damage
                self.healthbar_len -= (self.healthbar_max_len / (self.max_health / pl.Player.damage))
        if self.skill == "seeker" or self.skill == "jumper":
            for shot, _ in tr.Turret.pd_lst:
                if shot.colliderect(self.hitbox):
                    Gfx.shot_hit_effect(shot)
                    self.health -= 1
                    self.healthbar_len -= (self.healthbar_max_len / (self.max_health / 1))
                    tr.Turret.pd_lst.remove((shot, _))
        if self.health <= 0:
            lvl.Levels.display_score += self.score_amount
            lvl.Levels.interval_score += self.score_amount
            pup.Power_ups.score += self.score_amount
            Gfx.create_effect("enexplo", 5, (self.hitbox.topleft[0] - 20, self.hitbox.topleft[1] - 30))
            return True

    def gfx_animation(self):
        if self.typ == "normal":
            animation_ticker = self.enemy_tc.animation_ticker(self.animation_speed * len(Enemy.gfx_pictures_ast))
            if animation_ticker == (self.animation_speed * len(Enemy.gfx_pictures_ast)):  # 480
                self.gfx_idx = 0
            if animation_ticker % self.animation_speed == 0:
                self.gfx_idx += 1
                if self.gfx_idx == len(Enemy.gfx_pictures_ast):
                    self.gfx_idx = 0
            win.blit(Enemy.gfx_pictures_ast[self.gfx_idx], (self.hitbox.topleft[0] - 8, self.hitbox.topleft[1] - 15))
        elif self.typ == "seeker" or self.typ == "shooter" or self.typ == "add":
            animation_ticker = self.enemy_tc.animation_ticker(6)
            if animation_ticker < 3:
                win.blit(Enemy.spez_gfx[self.gfx_idx[0]], (self.hitbox.center[0] - self.gfx_hook[0], self.hitbox.center[1] - self.gfx_hook[1]))
            else:
                win.blit(Enemy.spez_gfx[self.gfx_idx[1]], (self.hitbox.center[0] - self.gfx_hook[0], self.hitbox.center[1] - self.gfx_hook[1]))
        elif self.typ != "normal" or self.typ != "seeker" or self.typ != "shooter":
            animation_ticker = self.enemy_tc.animation_ticker(10)
            if animation_ticker < 5:
                win.blit(Enemy.boss_gfx[self.gfx_idx[0]], (self.hitbox.center[0] - self.gfx_hook[0], self.hitbox.center[1] - self.gfx_hook[1]))
            else:
                win.blit(Enemy.boss_gfx[self.gfx_idx[1]], (self.hitbox.center[0] - self.gfx_hook[0], self.hitbox.center[1] - self.gfx_hook[1]))

    def update():
        # Method for main gameloop

        # Enemy instance creation
        if not lvl.Levels.boss_fight:
            while len(Enemy.enemy_lst) < lvl.Levels.enemy_amount:
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
            tr.Turret.missile_aquisition(enemy)
            if enemy.border_collide() or enemy.hit_detection(False):
                Enemy.enemy_lst.remove(enemy)
            elif enemy.player_collide():
                if pup.Power_ups.shield:
                    enemy.health = 0
                else:
                    pl.Player.hit(1)
                    Enemy.enemy_lst.remove(enemy)

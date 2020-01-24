import pygame
import random

from init import *
from astraid_funcs import *
from Gfx import Gfx
import enemy as en
import player as pl
import turret as tr
import levels as lvl
""" Enemy class: (Inheritace)
    Player class:
        Attributes: Player.hitbox
        Methods: Player.hit()
    Turret class:
        Methods: Turret.point_defence(), Turret.missile_aquisition()
    Levels class:
        Attributes: Levels.boss_fight, Levels.level, Levels.spez_event_trigger
"""


class Spez_enemy(en.Enemy):

    lst = []
    shot_lst = []
    amount = 1
    health = 2
    shot_gfx = get_images("projectile")

    def __init__(self, typ, spawn):
        self.typ = typ
        self.score_amount = 10
        self.spez_tc = Time_controler()
        self.gfx_hook = (40, 50)
        if self.typ == "seeker":
            super().__init__(1, 4, spawn, Spez_enemy.health + 1)  # direction, speed, spawnpoint, health
            self.angles = angles_360(self.speed)
            self.gfx_idx = (8, 9)
            self.skill, self.typ = typ, typ
            self.score_amount += 2
        elif self.typ == "jumper":
            super().__init__(random.randint(0, 359), 7, spawn, Spez_enemy.health)
            self.dir_change_interval = random.randint(5, 40)
            self.skill, self.typ = typ, "normal"
            self.score_amount += 4
            self.gfx_idx = (12,13)
        elif self.typ == "shooter":
            super(). __init__(1, random.randint(4, 6), spawn, Spez_enemy.health + 2)
            for sp, direction, gfx_idx in [(1, 90, (2, 3)), (2, 270, (6, 7)), (3, 359, (0, 1)), (4, 180, (4, 5))]:
                if self.spawn_point == sp:
                    self.direction = direction
                    self.gfx_idx = gfx_idx
            self.shot_angle = 0
            self.shot_angles = angles_360(7)
            self.fire_rate = random.randint(60, 100)
            self.skill, self.typ = typ, typ
            self.score_amount += 3
        elif self.typ == "strafer":
            super().__init__(random.randint(0, 359), 8, spawn, Spez_enemy.health)
            self.shot_angles = angles_360(20)
            self.skill, self.typ = typ, typ
            self.gfx_idx = (2,3)
        elif self.typ == "gravity_well" or self.typ == "repair_station":
            super().__init__(random.randint(0, 359), 1, 1, Spez_enemy.health)
            self.gfx_idx = (10, 11)
            self.skill = typ
            self.typ = "phenomenon"
            self.direction = 90

    def skills(self):
        # Seeker
        if self.skill == "seeker":
            self.direction = degrees(pl.Player.hitbox.center[0], self.spawn_points[self.spawn_point][0], pl.Player.hitbox.center[1], self.spawn_points[self.spawn_point][1])
            if abs(pl.Player.hitbox.center[0] - self.hitbox.center[0]) > 20 or abs(pl.Player.hitbox.center[1] - self.hitbox.center[1]) > 20:
                self.spawn_points[self.spawn_point][0] = self.hitbox.center[0]
                self.spawn_points[self.spawn_point][1] = self.hitbox.center[1]
        # jumper
        elif self.skill == "jumper":
            if self.spez_tc.trigger_1(self.dir_change_interval):
                self.direction = random.randint(0, 359)
        # shooter
        elif self.skill == "shooter":
            self.shot_angle = degrees(pl.Player.hitbox.center[0], self.hitbox.center[0], pl.Player.hitbox.center[1], self.hitbox.center[1])
            if self.spez_tc.trigger_2(self.fire_rate):
                Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1], 7, 7), self.shot_angles[int(self.shot_angle)]))
        elif self.skill == "strafer":
            if self.spez_tc.trigger_2(15):
                Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1], 7, 7), self.shot_angles[self.direction]))
        elif self.skill == "gravity_well":
            envelope = pygame.Rect(self.hitbox.center[0] - 300 , self.hitbox.center[1] -300 , 600, 600)
            if envelope.colliderect(pl.Player.hitbox):
                pl.Player.directions = directions(2)
            else:
                pl.Player.directions = directions(pl.Player.speed)
            for enemy in en.Enemy.enemy_lst:
                if enemy.hitbox.colliderect(envelope):
                    enemy.angles = angles_360(2)
                else:
                    enemy.anles = angles_360(enemy.speed)
            # pygame.draw.rect(win, (0,20,40), envelope)
            pygame.draw.rect(win, (0,20,230), self.hitbox)
        elif self.skill == "repair_station":
            if abs(self.hitbox.center[0] - pl.Player.hitbox.center[0]) < 300 or abs(self.hitbox.center[1] - pl.Player.hitbox.center[1]) < 300:
                if self.tc.trigger_2(300):
                    if pl.Player.health < pl.Player.max_health:
                        pl.Player.health += 1
            pygame.draw.rect(win, (0,230,20), self.hitbox)

    def gfx_shot(rect):
        win.blit(Spez_enemy.shot_gfx[6], (rect))

    def spez_event(kind):
        if not lvl.Levels.boss_fight and not lvl.Levels.after_boss:
            lvl.Levels.spez_event_trigger = 0
            spawn = random.randint(1, 4)
            if kind == "wave":
                for i in range(15):
                    en.Enemy.enemy_lst.append(en.Enemy(90, 5, 1, en.Enemy.health))
            elif kind == "jumper":
                for i in range(10 + lvl.Levels.level):
                    Spez_enemy.lst.append(Spez_enemy(kind, spawn))
            elif kind == "shooter":
                for i in range(3 + int(lvl.Levels.level / 6)):
                    Spez_enemy.lst.append(Spez_enemy(kind, spawn))
            elif kind == "seeker":
                for i in range(2 + int(lvl.Levels.level / 10)):
                    Spez_enemy.lst.append(Spez_enemy(kind, spawn))

    def update():
        # create instances
        if not lvl.Levels.boss_fight and not lvl.Levels.after_boss and not lvl.Levels.elite_fight:
            # if not any(lvl.Levels.boss_fight, lvl.Levels.elite_fight, lvl.Levels.after_boss):
            while len(Spez_enemy.lst) < Spez_enemy.amount:
                Spez_enemy.lst.append(Spez_enemy("gravity_well", 1))#random.choice(["shooter", "seeker", "jumper", "strafer"]), random.randint(1, 4)))  # "seeker", random.randint(1, 4)))
        # draw, update, skills, ...
        for spez in Spez_enemy.lst:
            spez.draw()
            spez.gfx_animation()
            spez.skills()
            spez.gfx_health_bar()
            if spez.skill == "seeker" or spez.skill == "jumper":
                tr.Turret.point_defence(spez.hitbox)
            tr.Turret.missile_aquisition(spez)
            if spez.border_collide():
                Spez_enemy.lst.remove(spez)
            if spez.typ != "phenomenon":
                if spez.hit_detection(False):
                    Spez_enemy.lst.remove(spez)
            elif spez.player_collide():
                Spez_enemy.lst.remove(spez)
                pl.Player.hit(1)
        # Shot draw / hitdetection
        for shot, angle in Spez_enemy.shot_lst:
            shot.move_ip(angle)
            Spez_enemy.gfx_shot(shot)
            # pygame.draw.rect(win, (255, 0, 0), shot)
            if shot.colliderect(pl.Player.hitbox):
                pl.Player.hit(1)
                Gfx.shot_hit_effect(shot)
                Spez_enemy.shot_lst.remove((shot, angle))
            if rect_not_on_sreen(shot, bot=False, strict=False):
                Spez_enemy.shot_lst.remove((shot, angle))

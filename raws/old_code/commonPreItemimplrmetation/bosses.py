import pygame
import random

from init import *
from astraid_funcs import *
import turret as tr
import spez_enemy as spez
import player as pl
import enemy as en
import levels as lvl
from Gfx import Gfx
""" creates and handels Bosses Objects

    Turret class:
        Attributes: Turret.shot_lst, Turret.pd_lst, Turret.nuke
        methods: Turret.point_defence(), Turret.missile_aquisition(), Turret.nuke_reload()
    Levels class:
        Attributes: Levels.boss_fight, Levels.skill_points
    Player class:
        Attributes: Player.hitbox
        methods: Player.hit()
    Enemy class:
        Attributes: Enemy.boss_gfx
    Spez_enemy class: (Inheritance)
        Attributes: Spez_enemy.shot_lst, Spez_enemy.shot_gfx
"""


class Bosses(spez.Spez_enemy):

    shot_lst = []
    mine_lst = []
    missile_lst = []
    main_gun_lst = []
    boss_lst = []

    def __init__(self, typ, health, speed, fire_rate, boss_skill, move_pattern, size, gfx_idx, gfx_hook):
        self.checkpoints = {
            0: (winwidth / 2, 300),             # topmid
            1: (300, 300),                      # topleft
            2: (winwidth - 300, 300),           # topright
            3: (300, winheight / 2),             # midleft
            4: (winwidth - 300, winheight / 2),   # midright
            5: (300, winheight - 300),             # leftbot
            6: (winwidth - 300, winheight - 300),  # rightbot
            7: (winwidth / 2, winheight - 100),   # midbot
            8: (winwidth / 2, 600),
            9: (winwidth / 2, 610)
        }
        self.orig_gfx_idx = gfx_idx
        self.gfx_idx = gfx_idx
        self.gfx_hook = gfx_hook
        self.enemy_tc = Time_controler()
        self.cp_ticker = 0
        self.direction = 0
        self.healthbar_len = 100
        self.healthbar_height = 5
        self.healthbar_max_len = self.healthbar_len
        self.shot_angle = 0
        self.shot_angles = angles_360(7)  # projectilespeed
        self.spez_tc = Time_controler()
        self.score_amount = 400
        self.health = health
        self.max_health = self.health
        self.speed = speed
        self.fire_rate = fire_rate
        self.boss_skill = boss_skill
        self.skill = "shooter"
        self.move_pattern = move_pattern
        self.typ = typ
        self.size = size
        self.directions = angles_360(self.speed)
        self.hitbox = pygame.Rect(winwidth / 2, -250, size[0], size[1])
        self.enrage_trigger = self.health * 0.15
        if "mines" in self.boss_skill:
            self.mine_tc = Time_controler()
            self.mine_trigger = 220
            self.mine_angles = angles_360(10)
        if "seeker_missiles" in self.boss_skill:
            self.missile_tc = Time_controler()
            self.missile_duration = 480
            self.missile_angles = angles_360(6)
            self.missile_retarget_trigger = 90
            self.missile_direction = 270
        if "salvo" in self.boss_skill:
            self.salvo_tc = Time_controler()
        if "volley" in self.boss_skill:
            self.volley_tc = Time_controler()
        if "main_gun" in self.boss_skill:
            self.mg_angle = 0
            self.main_gun_tc = Time_controler()
            self.main_gun_angles = angles_360(35)
        if "jumpdrive" in self.boss_skill:
            self.jumpdrive_tc = Time_controler()
            self.jump_charge = False
            self.jump_point = 0
            self.jump_chance = 1100
        if self.typ == "CA":
            self.add_respawn_time = 720
        if self.typ == "BB":
            self.add_respawn_time = 600

    def gfx_direction(self):
        if self.direction > 45 and self.direction < 135:  # up
            self.gfx_idx = self.orig_gfx_idx
        elif self.direction > 135 and self.direction < 225:  # left
            self.gfx_idx = [i + 2 for i in self.orig_gfx_idx]
        elif self.direction > 225 and self.direction < 315:  # down
            self.gfx_idx = [i + 4 for i in self.orig_gfx_idx]
        elif self.direction < 45 or self.direction > 315:  # right
            self.gfx_idx = [i + 6 for i in self.orig_gfx_idx]

    def move(self):
        rel_x, rel_y = self.checkpoints[self.move_pattern[self.cp_ticker]][0] - self.hitbox.center[0], self.checkpoints[self.move_pattern[self.cp_ticker]][1] - self.hitbox.center[1]
        self.direction = -math.atan2(rel_y, rel_x)
        self.direction = math.degrees(self.direction)
        if self.direction < 0:
            self.direction += 360
        self.hitbox.move_ip(self.directions[int(self.direction)])
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        if self.hitbox.collidepoint(self.checkpoints[self.move_pattern[self.cp_ticker]]):
            self.cp_ticker += 1
            if self.cp_ticker > len(self.move_pattern) - 1:
                self.cp_ticker = 0

    def enrage(self):
        if self.health < self.enrage_trigger:
            self.fire_rate -= self.fire_rate * 0.5
            self.speed += 2
            self.directions = angles_360(self.speed)
            if "mines" in self.boss_skill:
                self.mine_trigger -= 100
            if "seeker_missiles" in self.boss_skill:
                self.missile_retarget_trigger -= 45
            if "jumpdrive" in self.boss_skill:
                self.jump_chance -= 250
            if "adds" in self.boss_skill:
                self.add_respawn_time -= 120
            self.enrage_trigger = -10

    def boss_skills(self):
        # mines
        if "mines" in self.boss_skill:
            if self.mine_tc.trigger_1(self.mine_trigger):
                Bosses.mine_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1], 20, 20), pygame.Rect(self.hitbox.center[0] - 175, self.hitbox.center[1] - 175, 350, 350)))
                if len(Bosses.mine_lst) > 15:
                    del Bosses.mine_lst[15]
            for mine, envelope in Bosses.mine_lst:
                tr.Turret.point_defence(mine)
                # pygame.draw.rect(win, (100, 100, 0), envelope)
                # pygame.draw.rect(win, (100, 0, 0), mine)
                win.blit(spez.Spez_enemy.shot_gfx[12], (mine.topleft[0] - 5, mine.topleft[1] - 5))
                win.blit(spez.Spez_enemy.shot_gfx[13], (envelope.topleft[0] - 27, envelope.topleft[1] - 27))
                if envelope.colliderect(pl.Player.hitbox):
                    mine_direction = degrees(pl.Player.hitbox.center[0], mine.center[0], pl.Player.hitbox.center[1], mine.center[1])
                    mine.move_ip(self.mine_angles[int(mine_direction)])
                    envelope.move_ip(self.mine_angles[int(mine_direction)])
                    if mine.colliderect(pl.Player.hitbox):
                        Gfx.shot_hit_effect(mine)
                        pl.Player.hit(1)
                        Bosses.mine_lst.remove((mine, envelope))
                for shot, _ in tr.Turret.shot_lst + tr.Turret.pd_lst:
                    if mine.colliderect(shot):
                        Gfx.shot_hit_effect(shot)
                        try:
                            Bosses.mine_lst.remove((mine, envelope))
                            tr.Turret.shot_lst.remove((shot, _))
                        except ValueError:
                            pass
                if mine.colliderect(tr.Turret.nuke):
                    Bosses.mine_lst.remove((mine, envelope))
        # seeker missile
        if "seeker_missiles" in self.boss_skill:
            if self.missile_tc.trigger_1(self.missile_duration) or len(Bosses.missile_lst) == 0:
                Bosses.missile_lst.clear()
                self.missile_direction = 270
                Bosses.missile_lst.append(pygame.Rect(self.hitbox.center[0], self.hitbox.center[1], 20, 20))
            for missile in Bosses.missile_lst:
                tr.Turret.point_defence(missile)
                # pygame.draw.rect(win, (230, 40, 0), missile)
                if self.missile_tc.trigger_2(self.missile_retarget_trigger):
                    if abs(pl.Player.hitbox.center[0] - missile.center[0]) > 1 or abs(pl.Player.hitbox.center[1] - missile.center[1]) > 1:
                        self.missile_direction = degrees(pl.Player.hitbox.center[0], missile.center[0], pl.Player.hitbox.center[1], missile.center[1])
                win.blit(gfx_rotate(spez.Spez_enemy.shot_gfx[11], self.missile_direction - 90), (missile.topleft[0] - 10, missile.topleft[1] - 10))
                missile.move_ip(self.missile_angles[self.missile_direction])
                if missile.colliderect(pl.Player.hitbox):
                    Gfx.shot_hit_effect(missile)
                    pl.Player.hit(1)
                    Bosses.missile_lst.remove(missile)
                elif rect_not_on_sreen(missile, strict=True):
                    Bosses.missile_lst.remove(missile)
                for shot, _ in tr.Turret.pd_lst:
                    if shot.colliderect(missile):
                        try:
                            Bosses.missile_lst.remove(missile)
                            tr.Turret.pd_lst.remove((shot, _))
                        except ValueError:
                            pass
            if len(Bosses.missile_lst) > 1:
                del Bosses.missile_lst[1]
        # salvo fire
        if "salvo" in self.boss_skill:
            if self.salvo_tc.trigger_1(self.fire_rate * 5):
                for i in range(135, 225, 15):
                    spez.Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0] - self.size[0] / 2, self.hitbox.center[1], 7, 7), self.shot_angles[i]))
                for i in range(0, 45, 15):
                    spez.Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0] + self.size[0] / 2, self.hitbox.center[1], 7, 7), self.shot_angles[i]))
                for i in range(315, 360, 15):
                    spez.Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0] + self.size[0] / 2, self.hitbox.center[1], 7, 7), self.shot_angles[i]))
        # volley fire
        if "volley" in self.boss_skill:
            if self.volley_tc.trigger_1(self.fire_rate * 3):
                for i in range(-20, 20, 20):
                    try:
                        spez.Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0] - self.size[0] / 2, self.hitbox.center[1], 7, 7), self.shot_angles[self.shot_angle + i]))
                    except KeyError:
                        if i < 0:
                            spez.Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0] - self.size[0] / 2, self.hitbox.center[1], 7, 7), self.shot_angles[self.shot_angle + i + 360]))
                        else:
                            spez.Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0] - self.size[0] / 2, self.hitbox.center[1], 7, 7), self.shot_angles[self.shot_angle + i - 360]))
        # main Gun
        if "main_gun" in self.boss_skill:
            if self.main_gun_tc.delay(True, self.fire_rate * 6):
                Bosses.main_gun_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1] + self.size[1] / 2, 4, 4), False, 7))
                if "main_gun_2"in self. boss_skill:
                    Bosses.main_gun_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1] - self.size[1] / 2, 4, 4), False, 7))
                if self.main_gun_tc.trigger_2(100):
                    Bosses.main_gun_lst.clear()
                    Bosses.main_gun_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1] + self.size[1] / 2, 30, 30), True, 8))
                    if "main_gun_2"in self. boss_skill:
                        Bosses.main_gun_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1] - self.size[1] / 2, 30, 30), True, 8))
                    self.main_gun_tc.delay(False)
            for idx, (main_gun, fire, gfx_idx) in enumerate(Bosses.main_gun_lst):
                # if not fire:
                if "main_gun_2" in self.boss_skill:
                    if idx % 2 == 0:
                        self.mg_angle = degrees(pl.Player.hitbox.center[0], self.hitbox.center[0], pl.Player.hitbox.center[1], (self.hitbox.center[1] + self.size[1] / 2))
                    else:
                        self.mg_angle = degrees(pl.Player.hitbox.center[0], self.hitbox.center[0], pl.Player.hitbox.center[1], (self.hitbox.center[1] - self.size[1] / 2))
                else:
                    self.mg_angle = degrees(pl.Player.hitbox.center[0], self.hitbox.center[0], pl.Player.hitbox.center[1], (self.hitbox.center[1] + self.size[1] / 2))
                if fire:
                    if main_gun.colliderect(pl.Player.hitbox):
                        pl.Player.hit(1)
                if rect_not_on_sreen(main_gun):
                    Bosses.main_gun_lst.remove((main_gun, fire, gfx_idx))
                main_gun.move_ip(self.main_gun_angles[self.mg_angle])
                win.blit(spez.Spez_enemy.shot_gfx[gfx_idx], (main_gun.topleft[0], main_gun.topleft[1] - 8))
                # pygame.draw.rect(win, (255, 0, 0), main_gun)
        if "jumpdrive" in self.boss_skill:
            if not self.jump_charge:
                jumpdrive_trigger = random.randint(1, self.jump_chance)
                if jumpdrive_trigger == 1:
                    self.jump_point = self.checkpoints[random.choice([1, 2, 3, 4])]
                    jumpdrive_trigger = 0
                    self.jump_charge = True
            if self.jump_charge:
                # pygame.draw.rect(win, (0, 0, 100), pygame.Rect(self.jump_point, self.size))
                if self.typ == "CA":
                    win.blit(en.Enemy.boss_gfx[40], self.jump_point)
                elif self.typ == "BB":
                    win.blit(en.Enemy.boss_gfx[41], self.jump_point)
                if self.jumpdrive_tc.trigger_1(60):
                    Gfx.create_effect("jump", 2, (self.hitbox.topleft[0] - 40, self.hitbox.topleft[1] - 40))
                    self.hitbox.topleft = self.jump_point
                    self.jump_charge = False
        if "adds" in self.boss_skill:
            if self.typ == "CA":
                Boss_adds.create(1, self.add_respawn_time, [])
            elif self.typ == "BB":
                Boss_adds.create(2, self.add_respawn_time, ["volley"])

    def create(lvl):
        # typ, health, speed, fire_rate, boss_skill, move_pattern, size(), gfx_idx(), gfx_hook() // Skills: "mines", "seeker_missiles", "salvo", "volley", "main_gun", "main_gun_2"
        if lvl == 5:  # The Corvette
            Bosses.boss_lst.append(Bosses("corv", 250, 5, 90, ["mines", "volley"], (0, 1, 2, 3, 4, 5, 6), (80, 180), [0, 1], (50, 120)))
        elif lvl == 10:  # The Frigate
            Bosses.boss_lst.append(Bosses("FF", 350, 3, 60, ["seeker_missiles", "salvo", "volley"], (0, 1, 2, 3), (100, 220), (8, 9), (65, 120)))
        elif lvl == 15:  # The Destroyerd
            Bosses.boss_lst.append(Bosses("DD", 600, 2, 60, ["seeker_missiles", "mines", "salvo", "volley"], (0, 7), (120, 260), (16, 17), (70, 140)))
        elif lvl == 20:  # The Cruiser
            Bosses.boss_lst.append(Bosses("CA", 1000, 1, 50, ["seeker_missiles", "salvo", "main_gun", "jumpdrive", "adds"], (8, 9), (130, 240), (24, 25), (80, 180)))
        elif lvl == 25:  # The Batleship
            Bosses.boss_lst.append(Bosses("BB", 1600, 1, 70, ["salvo", "volley", "main_gun", "main_gun_2", "jumpdrive", "seeker_missiles", "adds"], (8, 9), (140, 360), (32, 33), (80, 220)))

    def update():
        if lvl.Levels.boss_fight:
            for boss in Bosses.boss_lst:
                boss.move()
                boss.skills()
                boss.boss_skills()
                boss.gfx_direction()
                boss.gfx_animation()
                boss.gfx_health_bar()
                boss.enrage()
                tr.Turret.missile_aquisition(boss)
                if boss.player_collide():
                    pl.Player.hit(1)
                if boss.hit_detection(False):
                    Bosses.boss_lst.remove(boss)
                    Bosses.mine_lst.clear()
                    Bosses.missile_lst.clear()
                    tr.Turret.nuke_reload(True)
                    lvl.Levels.skill_points += 2
                    lvl.Levels.boss_fight = False


class Boss_adds(Bosses):

    add_lst = []
    tc = Time_controler()

    def __init__(self, move_pattern, skills):
        Bosses.__init__(self, "add", 2, 5, 120, skills, move_pattern, (20, 50), 0, 0)
        self.checkpoints = {
            0: (400, 750),
            1: (700, 750),
            2: (700, 850),
            3: (400, 850),
            4: (winwidth - 400, 750),
            5: (winwidth - 700, 750),
            6: (winwidth - 700, 850),
            7: (winwidth - 400, 850)
        }
        self.score_amount = 10
        self.gfx_idx = (10, 11)
        self.gfx_hook = (17, 30)
        self.healthbar_len = 50
        self.healthbar_max_len = 50
        self.healthbar_height = 1

    def create(amount, respawn_speed, skills):
        if Boss_adds.tc.trigger_1(respawn_speed) and len(Boss_adds.add_lst) < amount:
            Boss_adds.add_lst.append(Boss_adds((0, 1, 2, 3, 4, 5, 6, 7), skills))
            if amount == 2 and len(Boss_adds.add_lst) < amount:
                Boss_adds.add_lst.append(Boss_adds((7, 6, 5, 4, 3, 2, 1, 0), skills))

    def update():
        for add in Boss_adds.add_lst:
            add.move()
            add.skills()
            add.boss_skills()
            add.gfx_health_bar()
            add.gfx_animation()
            tr.Turret.missile_aquisition(add)
            if add.player_collide():
                Boss_adds.add_lst.remove(add)
                pl.Player.hit(1)
            if add.hit_detection(False):
                Boss_adds.add_lst.remove(add)

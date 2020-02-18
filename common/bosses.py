import pygame
import random

from init import *
from astraid_funcs import *
from enemys import Enemy, Shooter
from projectiles import Wave
from boss_skills import Boss_skills
from items_misc import Item_upgrade_point_crate, Item_heal_crate, Item_supply_crate
from Gfx import Gfx, Background
import astraid_data as data


class Bosses(Shooter, Boss_skills):

    shot_sprites = get_images("projectile")

    def __init__(self):
        # Movement
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
        self.orig_checkpoints = self.checkpoints
        self.cp_ticker = 0
        self.direction = 0
        self.angles = angles_360(self.speed)
        self.orig_angles = self.angles
        self.snared = False
        # Gfx
        self.orig_gfx_idx = self.gfx_idx
        self.sprites = data.ENEMY.boss_sprites
        self.rotate = False
        self.buffer_hp = 0
        self.bg_change = True
        self.muzzle_effect_timer = (i for i in range(1))
        self.guns = [{"pos": [0, 0], "sprites": [2, 3]}]
        self.gun_idx = 0
        # Shooting
        self.shot_angle = 0
        self.shot_angles = angles_360(8)  # projectilespeed
        self.score_amount = 400
        self.projectile_speed = 20
        self.special_attack = False
        self.special_skills_lst = []
        Boss_skills.__init__(self)
        Timer.__init__(self)
        # Health
        self.max_health = self.health
        self.healthbar_len = self.size[0]
        self.healthbar_max_len = self.healthbar_len
        self.healthbar_height = 5
        self.kill = False
        self.hitable = True
        self.special_take_damage = None
        # General Attributes
        self.hitbox = pygame.Rect(winwidth / 2, -700, self.size[0], self.size[1])
        self.flag = "boss"
        # Phases
        self.phase_triggers = [self.health * 0.9, self.health * 0.5, self.health * 0.2]
        self.special_move = False
        self.special_gfx = False
        self.hide_health_bar = False
        self.engine = {
            "right": (-105, -10),
            "down": (-19, -153),
            "up": (-15, 90),
            "left": (70, -10)
        }

    def gfx_animation(self):
        if self.angles[0][0] > 0:
            if self.direction > 338 or self.direction < 22:
                # rechts
                if self.timer_trigger(20):
                    Gfx.create_effect(
                        "engine", 3, anchor=self.hitbox, rot=90,
                        x=self.engine["right"][0], y=self.engine["right"][1], layer=3
                    )
            elif 23 <= self.direction <= 67:
                # right down
                if self.timer_trigger(20):
                    Gfx.create_effect(
                        "engine", 3, anchor=self.hitbox, rot=90,
                        x=self.engine["right"][0], y=self.engine["right"][1], layer=3
                    )
                if self.timer_trigger(20):
                    Gfx.create_effect(
                        "engine2", 5, anchor=self.hitbox, rot=360,
                        x=self.engine["down"][0] - 33, y=self.engine["down"][1] - 20, layer=3
                    )
            elif 67 <= self.direction <= 112:
                # down
                if self.timer_trigger(20):
                    Gfx.create_effect(
                        "engine2", 5, anchor=self.hitbox, rot=360,
                        x=self.engine["down"][0] - 33, y=self.engine["down"][1] - 20, layer=3
                    )
            elif 112 <= self.direction <= 157:
                # leftdown
                if self.timer_trigger(20):
                    Gfx.create_effect(
                        "engine", 3, anchor=self.hitbox, rot=270,
                        x=self.engine["left"][0], y=self.engine["left"][1], layer=3
                    )
                if self.timer_trigger(20):
                    Gfx.create_effect(
                        "engine2", 5, anchor=self.hitbox, rot=360,
                        x=self.engine["down"][0] - 33, y=self.engine["down"][1] - 20, layer=3
                    )
            elif 157 <= self.direction <= 202:
                # links
                if self.timer_trigger(20):
                    Gfx.create_effect(
                        "engine", 3, anchor=self.hitbox, rot=270,
                        x=self.engine["left"][0], y=self.engine["left"][1], layer=3
                    )
            elif 202 <= self.direction <= 247:
                # leftup
                if self.timer_trigger(20):
                    Gfx.create_effect(
                        "engine", 3, anchor=self.hitbox, rot=270,
                        x=self.engine["left"][0], y=self.engine["left"][1], layer=3
                    )
                if self.timer_trigger(20):
                    Gfx.create_effect(
                        "engine", 3, anchor=self.hitbox, rot=180,
                        x=self.engine["up"][0], y=self.engine["up"][1], layer=3
                    )
            elif 247 <= self.direction <= 292:
                # up
                if self.timer_trigger(20):
                    Gfx.create_effect(
                        "engine", 3, anchor=self.hitbox, rot=180,
                        x=self.engine["up"][0], y=self.engine["up"][1], layer=3
                    )
            elif 292 <= self.direction <= 338:
                # riht up
                if self.timer_trigger(20):
                    Gfx.create_effect(
                        "engine", 3, anchor=self.hitbox, rot=90,
                        x=self.engine["right"][0], y=self.engine["right"][1], layer=3
                    )
                if self.timer_trigger(20):
                    Gfx.create_effect(
                        "engine", 3, anchor=self.hitbox, rot=180,
                        x=self.engine["up"][0], y=self.engine["up"][1], layer=3
                    )

        animation_ticker = self.timer_animation_ticker(120)
        if animation_ticker <= 60:
            win.blit(
                self.sprites[self.gfx_idx[0]],
                (self.hitbox.center[0] + self.gfx_hook[0],
                 self.hitbox.center[1] + self.gfx_hook[1])
            )
        else:
            win.blit(
                self.sprites[self.gfx_idx[1]],
                (self.hitbox.center[0] + self.gfx_hook[0],
                 self.hitbox.center[1] + self.gfx_hook[1])
            )
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)

    def guns_gfx_animation(self):
        gfx_angle = degrees(
            data.PLAYER.hitbox.center[1],
            self.hitbox.center[1],
            data.PLAYER.hitbox.center[0],
            self.hitbox.center[0]
        )
        for gun in self.guns:
            win.blit(rot_center(
                Gfx.gun_sprites[gun["sprites"][self.gun_idx]], gfx_angle),
                (self.hitbox.center[0] + gun["pos"][0],
                 self.hitbox.center[1] + gun["pos"][1])
            )

    def gun_gfx_idx_update(self):
        if next(self.muzzle_effect_timer, "stop") == "stop":
            self.gun_idx = 0
        else:
            self.gun_idx = 1

    def special_gfx_animation(self):
        pass

    def move(self):
        # self.direction = 96
        # self.hitbox.move_ip(self.angles[self.direction])
        self.direction = degrees(
            self.checkpoints[self.move_pattern[self.cp_ticker]][0],
            self.hitbox.center[0],
            self.checkpoints[self.move_pattern[self.cp_ticker]][1],
            self.hitbox.center[1]
        )
        self.hitbox.move_ip(self.angles[self.direction])
        if self.hitbox.collidepoint(self.checkpoints[self.move_pattern[self.cp_ticker]]):
            self.cp_ticker += 1
            if self.cp_ticker > len(self.move_pattern) - 1:
                self.cp_ticker = 0

    def phase_1(self):
        pass

    def phase_2(self):
        pass

    def phase_3(self):
        pass

    def special_death(self):
        pass

    def phases(self):
        if self.health < self.phase_triggers[0]:
            self.phase_1()
            self.phase_triggers[0] = - 100
        elif self.health < self.phase_triggers[1]:
            self.phase_2()
            self.phase_triggers[1] = - 100
        elif self.health < self.phase_triggers[2]:
            self.phase_3()
            self.phase_triggers[2] = - 100

    def boss_skills(self):
        for skill in self.skills_lst:
            try:
                skill()
            except TypeError:
                skill(self)

    def boss_special_skills(self):
        for skill in self.special_skills_lst:
            skill()

    def death(self):
        Gfx.create_effect("explosion_3", 2,
                          (self.hitbox.topleft[0] - 300, self.hitbox.topleft[1] - 300),
                          explo=True)

        if self.__class__.__name__ == "Elites":
            data.LEVELS.interval_score += data.LEVELS.level
        data.LEVELS.display_score += self.score_amount

        data.ITEMS.drop((800, 500), amount=self.drop_amount)
        data.ITEMS.drop((800, 500), target=Item_upgrade_point_crate((100, 100, 100), level=2))
        data.ITEMS.drop((800, 500), target=Item_supply_crate((100, 100, 100), level=2))
        data.ITEMS.drop((800, 500), target=Item_heal_crate((0, 255, 0), level=3))

        data.ENEMY_PROJECTILE_DATA.clear()
        data.LEVELS.boss_fight = False
        data.LEVELS.after_boss = True
        self.special_death()
        self.kill = True

    def set_snared(self):
        self.snared = True

    def snare_effect(self):
        if self.snared:
            self.angles = angles_360(0)
            if self.timer_key_trigger(300, key="snare"):
                self.angels = angles_360(self.speed)
                self.snared = False

    def border_collide(self):
        pass

    def tick(self):
        self.phases()
        self.snare_effect()
        self.player_collide()
        if not self.hide_health_bar:
            self.gfx_health_bar()
        if not self.snared:
            if not self.special_attack:
                self.skill()
                self.boss_skills()
            else:
                self.boss_special_skills()
        if not self.special_move:
            self.move()
        if not self.special_gfx:
            self.gfx_animation()
        else:
            self.special_gfx_animation()
        if not any([self.get_name() == "Elites",
                    self.get_name() == "Boss_scout"]):
            self.guns_gfx_animation()
            self.gun_gfx_idx_update()
        if self.hitable:
            data.TURRET.missile_aquisition(self)
        if any([self.get_name() == "Boss_turret",
                self.get_name() == "Boss_weakspot"]):
            data.TURRET.point_defence(self.hitbox)
        if self.health <= 0:
            self.death()

        if not any([self.get_name() == "Boss_turret",
                    self.get_name() == "Boss_weakspot",
                    self.get_name() == "Elites"]):
            # if self.bg_change:
            Background.bg_color_change(color=(40, 0, 30))
            # self.bg_change = False

        self.timer_tick()


data.BOSS = Bosses


class Boss_weakspot(Enemy):

    def __init__(self, health, boss, location, death_effect=None, size=(50, 50)):
        super().__init__(0, 0, 1, health, size, (6, 6), (-27, -27), data.ENEMY.spez_sprites)
        self.boss = boss
        self.boss.hitable = False
        self.location = location
        self.flag = "boss"
        self.death_effect = death_effect

    def move(self):
        self.hitbox.center = (self.boss.hitbox.center[0] + self.location[0],
                              self.boss.hitbox.center[1] + self.location[1])

    def death(self):
        if len([wp for wp in data.ENEMY_DATA if wp.__class__.__name__ == "Boss_weakspot"]) <= 1:
            self.boss.hitable = True
        if self.death_effect is not None:
            self.death_effect()
        self.kill = True

    def gfx_animation(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        animation_ticker = self.timer_animation_ticker(8)
        if animation_ticker < 4:
            win.blit
            (self.sprites[self.gfx_idx[0]],
             (self.hitbox.center[0] + self.gfx_hook[0],
              self.hitbox.center[1] + self.gfx_hook[1])
             )
        else:
            win.blit(
                self.sprites[self.gfx_idx[1]],
                (self.hitbox.center[0] + self.gfx_hook[0],
                 self.hitbox.center[1] + self.gfx_hook[1])
            )

    def border_collide(self):
        pass


class Boss_turret(Shooter):

    def __init__(self, health, boss, location):
        super().__init__()
        self.boss = boss
        self.health = health
        self.max_health = self.health
        self.location = location
        self.flag = "boss"
        self.fire_rate = 150
        self.target = data.PLAYER.hitbox
        self.special_take_damage = boss.special_take_damage
        self.gfx_idx = 0
        self.guns = [{"pos": [-50, -50], "sprites": [6, 7]}]
        self.gun_idx = 0
        self.score_amount = 0

    def move(self):
        self.hitbox.center = self.location

    def set_sp_dmg(self):
        self.special_take_damage = self.boss.special_take_damage

    def guns_gfx_animation(self):
        gfx_angle = degrees(
            data.PLAYER.hitbox.center[1],
            self.hitbox.center[1],
            data.PLAYER.hitbox.center[0],
            self.hitbox.center[0]
        )
        for gun in self.guns:
            win.blit(rot_center(
                Gfx.gun_sprites[gun["sprites"][self.gun_idx]], gfx_angle),
                (self.hitbox.center[0] + gun["pos"][0],
                 self.hitbox.center[1] + gun["pos"][1])
            )

    def gun_gfx_idx_update(self):
        if next(self.muzzle_effect_timer, "stop") == "stop":
            self.gun_idx = 0
        else:
            self.gun_idx = 1

    def gfx_animation(self):
        pass


class Boss_main_gun_battery(Bosses):

    def __init__(self, boss, target):
        self.size = (10, 10)
        Boss_skills.__init__(self)
        Timer.__init__(self)
        self.boss = boss
        self.hitbox = self.hitbox = pygame.Rect(winwidth / 2, -250, 0, 0)
        self.kill = False
        self.target = target
        self.flag = "boss"
        self.fire_rate = 1
        self.hitable = False
        self.location = random.choice([
            lambda: self.boss.hitbox.center,
            lambda: self.boss.hitbox.topleft,
            lambda: self.boss.hitbox.topright,
            lambda: self.boss.hitbox.bottomright,
            lambda: self.boss.hitbox.bottomleft,
        ])

    def tick(self):
        self.hitbox.center = self.location()
        self.skill_main_gun(target=self.target, static=True, gun_trigger=30, damage=2)
        self.timer_tick()


class Boss_laser_battery(Bosses):

    def __init__(self, boss):
        self.size = (10, 10)
        Boss_skills.__init__(self)
        Timer.__init__(self)
        self.boss = boss
        self.hitbox = self.hitbox = pygame.Rect(winwidth / 2, -250, 0, 0)
        self.kill = False
        self.flag = "boss"
        self.fire_rate = random.randint(20, 60)
        self.hitable = False
        self.fire = False
        self.target = (random.randint(0, 1800), random.randint(0, 1000))
        self.fixed_angle = 90

    def tick(self):
        self.hitbox.center = self.boss.hitbox.center
        if not self.fire:
            if self.timer_trigger(self.fire_rate):
                self.fire = True
                self.target = (random.randint(0, 1800), random.randint(0, 1000))
                self.fixed_angle += random.randint(5, 15)
                if self.fixed_angle >= 270:
                    self.fixed_angle = 90
        else:
            data.ENEMY_PROJECTILE_DATA.append(Wave(
                speed=25,
                size=(5, 5),
                start_point=self.boss.hitbox.center,
                damage=1,
                gfx_idx=16,
                # target=self.target,
                curve_size=2,
                fixed_angle=self.fixed_angle
            ))
            if self.timer_trigger(7):
                self.fire = False
        self.timer_tick()


class Boss_repair_ship(Enemy):
    # direction, speed, spawn_point, health, size, gfx_idx, gfx_hook, sprites

    def __init__(self, boss):
        self.boss = boss
        self.flag = "boss"
        super().__init__(0, 4, random.randint(1, 4), Enemy.health + 8,
                         (80, 80), (0, 1), (0, 0), Enemy.spez_sprites)
        self.gfx_hook = (-10, -20)
        self.gfx_idx = (11, 12)
        self.target = self.boss.hitbox.center

    def move(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        self.target = self.boss.hitbox.center
        self.hitbox.move_ip(self.angles[degrees(
            self.boss.hitbox.center[0],
            self.hitbox.center[0],
            self.boss.hitbox.center[1],
            self.hitbox.center[1]
        )])
        if self.hitbox.colliderect(self.boss.hitbox):
            # gfx_effect -->
            self.boss.set_health(-self.boss.max_health * 0.1, (0, 255, 0))
            self.kill = True


class Boss_shield_bubble(Timer):

    def __init__(self, pos, boss):
        Timer.__init__(self)
        self.hitbox = pygame.Rect(pos[0], pos[1], 150, 150)
        self.hitable = False
        self.kill = False
        self.boss = boss

    def hit(self, player):
        if self.hitbox.colliderect(player.hitbox):
            player.hitable = False
        else:
            player.hitable = True

    def destroy(self):
        if self.boss.health <= 0:
            self.kill = True
        return self.kill

    def tick(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        if self.timer_trigger(17):
            Gfx.create_effect(
                "shield2", 3,
                anchor=(self.hitbox.topleft[0] - 25, self.hitbox.topleft[1] - 25)
            )
        self.timer_tick()

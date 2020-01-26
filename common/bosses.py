import pygame
import random

from init import *
from astraid_funcs import *
from enemys import Enemy, Shooter
from projectiles import Impactor, Wave
from boss_skills import Boss_skills
from items import Item_upgrade_point_crate, Item_heal_crate, Item_supply_crate
from Gfx import Gfx
import astraid_data as data


class Bosses(Shooter, Boss_skills):

    shot_sprites = get_images("projectile")

    def __init__(self):  # , typ="", health=0, speed=0, fire_rate=0, boss_skill=[0], move_pattern=(0), size=(0, 0), gfx_idx=(0, 0), gfx_hook=(0, 0), drop_amount=0, wp_locations=None):
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
        self.cp_ticker = 0
        self.direction = 0
        self.angles = angles_360(self.speed)
        self.orig_angles = self.angles
        # Gfx
        self.orig_gfx_idx = self.gfx_idx
        self.sprites = data.ENEMY.boss_sprites
        self.rotate = False
        # Shooting
        self.shot_angle = 0
        self.shot_angles = angles_360(8)  # projectilespeed
        self.score_amount = 400
        self.projectile_speed = 16
        self.special_attack = False
        self.special_skills_lst = []
        Boss_skills.__init__(self)
        Timer.__init__(self)
        # Health
        self.max_health = self.health
        self.healthbar_len = 100
        self.healthbar_max_len = self.healthbar_len
        self.healthbar_height = 5
        self.kill = False
        self.hitable = True
        self.special_take_damage = None
        # General Attributes
        self.hitbox = pygame.Rect(winwidth / 2, -250, self.size[0], self.size[1])
        self.flag = "boss"
        # Phases
        self.phase_triggers = [self.health * 0.9, self.health * 0.5, self.health * 0.2]
        self.special_move = False
        self.special_gfx = False
        self.hide_health_bar = False

    def gfx_animation(self):
        if self.direction > 45 and self.direction < 135:  # up
            self.gfx_idx = self.orig_gfx_idx
        elif self.direction > 135 and self.direction < 225:  # left
            self.gfx_idx = [i + 2 for i in self.orig_gfx_idx]
        elif self.direction > 225 and self.direction < 315:  # down
            self.gfx_idx = [i + 4 for i in self.orig_gfx_idx]
        elif self.direction < 45 or self.direction > 315:  # right
            self.gfx_idx = [i + 6 for i in self.orig_gfx_idx]

        animation_ticker = self.timer_animation_ticker(8)
        if animation_ticker < 4:
            win.blit(self.sprites[self.gfx_idx[0]], (self.hitbox.center[0] + self.gfx_hook[0], self.hitbox.center[1] + self.gfx_hook[1]))
        else:
            win.blit(self.sprites[self.gfx_idx[1]], (self.hitbox.center[0] + self.gfx_hook[0], self.hitbox.center[1] + self.gfx_hook[1]))

    def move(self):
        rel_x, rel_y = self.checkpoints[self.move_pattern[self.cp_ticker]][0] - self.hitbox.center[0], self.checkpoints[self.move_pattern[self.cp_ticker]][1] - self.hitbox.center[1]
        self.direction = -math.atan2(rel_y, rel_x)
        self.direction = math.degrees(self.direction)
        if self.direction < 0:
            self.direction += 360
        self.hitbox.move_ip(self.angles[degrees(self.checkpoints[self.move_pattern[self.cp_ticker]][0], self.hitbox.center[0], self.checkpoints[self.move_pattern[self.cp_ticker]][1], self.hitbox.center[1])])
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
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
            skill()

    def boss_special_skills(self):
        for skill in self.special_skills_lst:
            skill()

    def death(self):
        Gfx.create_effect("explosion_3", 3, (self.hitbox.topleft[0] - 300, self.hitbox.topleft[1] - 300), explo=True)
        data.LEVELS.display_score += self.score_amount

        data.ITEMS.drop(self.hitbox.center, amount=self.drop_amount)
        data.ITEMS.drop(self.hitbox.center, target=Item_upgrade_point_crate((100, 100, 100)))
        data.ITEMS.drop(self.hitbox.center, target=Item_heal_crate((0, 255, 0)))

        data.ENEMY_PROJECTILE_DATA.clear()
        data.LEVELS.boss_fight = False
        data.LEVELS.after_boss = True
        self.special_death()
        self.kill = True

    def border_collide(self):
        pass

    def tick(self):
        self.phases()
        self.player_collide()
        if not self.hide_health_bar:
            self.gfx_health_bar()
        if not self.special_attack:
            self.skill()
            self.boss_skills()
        else:
            self.boss_special_skills()
        if not self.special_move:
            self.move()
        if not self.special_gfx:
            self.gfx_animation()
        if self.hitable:
            data.TURRET.missile_aquisition(self)
        if self.__class__.__name__ == "Boss_turret" or self.__class__.__name__ == "Boss_weakspot":
            data.TURRET.point_defence(self.hitbox)
        if self.health <= 0:
            self.death()
        self.timer_tick()

    @classmethod
    def create(cls, lvl):
        if lvl == 55:
            data.ENEMY_DATA.append(Boss_mine_boat())
        elif lvl == 5:
            data.ENEMY_DATA.append(Boss_frigatte())
        elif lvl == 15:
            data.ENEMY_DATA.append(Boss_corvette())
        elif lvl == 20:
            data.ENEMY_DATA.append(Boss_destroyer())
        elif lvl == 25:
            data.ENEMY_DATA.append(Boss_cruiser())
        elif lvl == 30:
            data.ENEMY_DATA.append(Boss_battleship())
        elif lvl == 35:
            data.ENEMY_DATA.append(Boss_carrier())


data.BOSS = Bosses


class Boss_mine_boat(Bosses):

    def __init__(self):
        self.health = 170
        self.speed = 4
        self.fire_rate = 90
        self.move_pattern = (0, 1, 2, 3, 4, 5, 6)
        self.size = (80, 180)
        self.gfx_idx = (0, 1)
        self.gfx_hook = (-50, -120)
        self.drop_amount = 1
        self.skills_lst = [self.skill_mines]
        super().__init__()

    def phase_1(self):
        self.angles = angles_360(5)
        # self.special_gfx = True
        self.special_move = True
        data.ENEMY_DATA.append(Boss_weakspot(self.max_health * 0.15, self, (0, -110)))
        self.skills_lst.append(self.skill_chaser)

    def phase_2(self):
        for loc in [(-50, 50), (50, 50)]:
            data.ENEMY_DATA.append(Boss_weakspot(self.max_health * 0.2, self, loc, death_effect=lambda: self.skills_lst.remove(self.skill_missile)))
        self.skills_lst.append(self.skill_missile)

    def phase_3(self):
        Gfx.bg_move = True
        self.agles = self.angles = angles_360(7)
        self.fire_rate -= 25
        self.set_health(-50, (0, 255, 0))
        self.skills_lst.append(self.skill_mines)


class Boss_frigatte(Bosses):

    def __init__(self):
        self.health = 700
        self.speed = 3
        self.fire_rate = 60
        self.move_pattern = (0, 1, 2, 3)
        self.size = (100, 220)
        self.gfx_idx = (8, 9)
        self.gfx_hook = (-65, -120)
        self.drop_amount = 1
        self.wp_locations = ((-50, 50), (50, 50), (0, -100))
        self.skills_lst = [self.skill_missile]
        super().__init__()

    def phase_1(self):

        self.skills_lst.append(self.skill_turret_defence_matrix)
        for i in range(2):
            spawn_loaction = (random.randint(300, 1700), random.randint(150, 900))
            data.ENEMY_PROJECTILE_DATA.append(Impactor(
                speed=4,
                start_point=self.hitbox.center,
                flag="enemy",
                target=spawn_loaction,
                impact_effect=lambda loc=spawn_loaction: data.ENEMY_DATA.append(Boss_turret(self.max_health * 0.05, self, loc))
            ))

    def phase_2(self):

        self.skills_lst += [self.skill_turret_defence_matrix, self.skill_salvo_alpha]
        for i in range(4):
            spawn_loaction = (random.randint(300, 1700), random.randint(150, 900))
            data.ENEMY_PROJECTILE_DATA.append(Impactor(
                speed=4,
                start_point=self.hitbox.center,
                flag="enemy",
                target=spawn_loaction,
                impact_effect=lambda loc=spawn_loaction: data.ENEMY_DATA.append(Boss_turret(self.max_health * 0.05, self, loc))
            ))

    def phase_3(self):

        self.skills_lst += [self.skill_turret_defence_matrix, self.skill_star_shot]
        for i in range(6):
            spawn_loaction = (random.randint(300, 1700), random.randint(150, 900))
            data.ENEMY_PROJECTILE_DATA.append(Impactor(
                speed=4,
                start_point=self.hitbox.center,
                flag="enemy",
                target=spawn_loaction,
                impact_effect=lambda loc=spawn_loaction: data.ENEMY_DATA.append(Boss_turret(self.max_health * 0.05, self, loc))
            ))


class Boss_corvette(Bosses):

    def __init__(self):

        self.health = 900
        self.speed = 4
        self.fire_rate = 30
        self.move_pattern = [random.randint(0, 9) for _ in range(40)]
        self.size = (80, 180)
        self.gfx_idx = (0, 1)
        self.gfx_hook = (-50, -120)
        self.drop_amount = 1
        self.skills_lst = [self.skill_volley]
        super().__init__()

    def phase_1(self):

        Gfx.bg_move = True
        Gfx.scroll_speed += 2
        self.speed += 2
        self.angles = angles_360(self.speed)
        self.skills_lst.append(self.skill_jumpdrive)

    def phase_2(self):

        self.speed += 2
        Gfx.scroll_speed += 2
        self.angles = angles_360(self.speed)
        self.fire_rate -= 10
        self.skills_lst.append(self.skill_jumpdrive)
        self.skills_lst.append(self.skill_speed_boost)

    def phase_3(self):

        Gfx.scroll_speed += 4
        self.speed += 4
        self.angles = angles_360(self.speed)
        self.fire_rate -= 10
        self.skills_lst.append(self.skill_jumpdrive)

    def special_death(self):
        Gfx.bg_move = False
        Gfx.scroll_speed -= 8


class Boss_destroyer(Bosses):

    def __init__(self):
        self.health = 1200
        self.speed = 2
        self.fire_rate = 60
        self.move_pattern = (0, 7, 0, 1, 2)
        self.size = (120, 260)
        self.gfx_idx = (16, 17)
        self.gfx_hook = (-70, -140)
        self.skills_lst = [self.skill_volley, self.skill_missile, self.skill_mines]
        self.drop_amount = 1
        super().__init__()

    def phase_1(self):

        self.special_attack = True
        self.special_skills_lst.append(self.skill_missile_barrage)
        self.skills_lst.append(self.skill_salvo_alpha)
        for loc in [(0, 0), (0, -100), (0, 100)]:
            data.ENEMY_DATA.append(Boss_weakspot(self.max_health * 0.05, self, loc, size=(120, 50)))

    def phase_2(self):

        self.special_attack = True
        self.special_skills_lst.append(self.skill_main_gun_salvo)
        self.skills_lst.append(self.skill_jumpdrive)
        for loc in [(0, 0), (0, -100), (0, 100)]:
            data.ENEMY_DATA.append(Boss_weakspot(self.max_health * 0.05, self, loc, size=(120, 50)))
        for _ in range(10):
            target = (random.randint(0, winwidth), random.randint(0, winheight))
            data.ENEMY_DATA.append(Boss_main_gun_battery(self, target))

    def phase_3(self):

        self.speed += 3
        self.set_health(-100, (0, 255, 0))
        self.fire_rate -= 25
        self.special_attack = True
        self.special_skills_lst.append(self.skill_laser_storm)
        for loc in [(0, 0), (0, -100), (0, 100)]:
            data.ENEMY_DATA.append(Boss_weakspot(self.max_health * 0.05, self, loc, size=(120, 50)))
        for _ in range(5):
            data.ENEMY_DATA.append(Boss_laser_battery(self))


class Boss_cruiser(Bosses):

    def __init__(self):
        self.health = 2500
        self.speed = 2
        self.fire_rate = 50
        self.move_pattern = (8, 9)
        self.size = (130, 240)
        self.gfx_idx = (24, 25)
        self.gfx_hook = (-80, -180)
        self.skills_lst = [self.skill_volley, self.skill_missile, self.skill_salvo_charlie]  # self.skill_salvo_alpha
        self.drop_amount = 1
        super().__init__()

    def phase_1(self):

        self.move_pattern = (0, 7, 0, 1, 2)
        # self.angles = angles_360(3)
        self.skills_lst.append(self.skill_dart_missiles)
        for _ in range(4):
            data.ENEMY_DATA.append(Boss_repair_ship(self))

    def phase_2(self):

        self.move_pattern = [random.randint(0, 9) for _ in range(40)]
        self.angles = angles_360(4)
        self.skills_lst.append(self.skill_salvo_alpha)
        for _ in range(6):
            data.ENEMY_DATA.append(Boss_repair_ship(self))

    def phase_3(self):

        self.special_attack = True
        self.special_skills_lst.append(self.skill_dart_missile_last_stand)
        for _ in range(8):
            data.ENEMY_DATA.append(Boss_repair_ship(self))


class Boss_battleship(Bosses):

    def __init__(self):
        self.health = 2400
        self.speed = 2
        self.fire_rate = 70
        self.move_pattern = (8, 9)
        self.size = (140, 360)
        self.gfx_idx = (32, 33)
        self.gfx_hook = (-80, -220)
        self.skills_lst = [self.skill_volley, self.skill_missile, self.skill_salvo_alpha, self.skill_star_shot, self.skill_main_gun]
        self.phase_skills = [[self.skill_main_gun], [self.skill_jumpdrive, self.skill_salvo_bravo]]
        self.drop_amount = 1
        super().__init__()


class Boss_carrier(Bosses):

    def __init__(self):
        self.health = 7000
        self.speed = 2
        self.fire_rate = 160
        self.boss_skill = ["adds"]
        self.move_pattern = (8, 9)
        self.size = (140, 360)
        self.gfx_idx = (32, 33)
        self.gfx_hook = (-80, -220)
        self.skills_lst = [self.skill_adds]
        self.phase_skills = [[], []]
        self.drop_amount = 1
        super().__init__()


class Elites(Bosses):

    health = 20
    sprites = get_images("elites")

    def __init__(self, health=0, speed=0, fire_rate=0, skill=[], gfx_idx=(0, 1), gfx_hook=(-30, -30)):
        self.health = health
        self.speed = speed
        self.fire_rate = fire_rate
        self.move_pattern = [random.randint(0, 9) for _ in range(40)]
        self.size = (100, 100)
        self.gfx_idx = gfx_idx
        self.gfx_hook = gfx_hook
        self.drop_amount = 0
        self.elite_skill = skill
        self.score_amount = 100
        self.flag = "elite"
        super().__init__()
        self.sprites = Elites.sprites

    def phases(self):
        pass

    def death(self):
        Gfx.create_effect("explosion_3", 3, (self.hitbox.topleft[0] - 300, self.hitbox.topleft[1] - 300), explo=True)
        data.LEVELSelite_fight = False
        if random.randint(0, 100) > 95:
            data.ITEMS.drop((self.hitbox.topleft), amount=1)
        else:
            random.choice([
                lambda: data.ITEMS.drop((self.hitbox.topleft), target=Item_supply_crate((100, 100, 100))),
                lambda: data.ITEMS.drop((self.hitbox.topleft), target=Item_heal_crate((100, 100, 100))),
                lambda: data.ITEMS.drop((self.hitbox.topleft), target=Item_upgrade_point_crate((100, 100, 100)))
            ])()
        self.kill = True

    def boss_skills(self):
        self.elite_skill(self)

    def gfx_animation(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        animation_ticker = self.timer_animation_ticker(8)
        gfx_angle = degrees(data.PLAYER.hitbox.center[1], self.hitbox.center[1], data.PLAYER.hitbox.center[0], self.hitbox.center[0])
        if animation_ticker < 4:
            win.blit(gfx_rotate(self.sprites[self.gfx_idx[0]], gfx_angle), (self.hitbox.topleft[0] + self.gfx_hook[0], self.hitbox.topleft[1] + self.gfx_hook[1]))
        else:
            win.blit(gfx_rotate(self.sprites[self.gfx_idx[1]], gfx_angle), (self.hitbox.topleft[0] + self.gfx_hook[0], self.hitbox.topleft[1] + self.gfx_hook[1]))

    @classmethod
    def spawn(cls):
        data.ENEMY_DATA.append(random.choice([
            lambda: Elites(health=Elites.health, speed=2, fire_rate=170, skill=Boss_skills.skill_mines, gfx_idx=(8, 9)),
            lambda: Elites(health=Elites.health + Elites.health * 0.2, speed=4, fire_rate=120, skill=Boss_skills.skill_missile, gfx_idx=(2, 3)),
            lambda: Elites(health=Elites.health - Elites.health * 0.2, speed=8, fire_rate=80, skill=Boss_skills.skill_jumpdrive, gfx_idx=(4, 5)),
            lambda: Elites(health=Elites.health + Elites.health, speed=3, fire_rate=100, skill=Boss_skills.skill_salvo_delta, gfx_idx=(6, 7)),
            lambda: Elites(health=Elites.health + Elites.health * 0.1, speed=2, fire_rate=100, skill=Boss_skills.skill_main_gun, gfx_idx=(0, 1)),
            lambda: Elites(health=Elites.health + Elites.health * 0.1, speed=6, fire_rate=100, skill=Boss_skills.skill_wave_motion_gun, gfx_idx=(10, 11))
        ])())


data.ELITES = Elites


class Boss_weakspot(Enemy):

    def __init__(self, health, boss, location, death_effect=None, size=(50, 50)):
        super().__init__(0, 0, 1, health, size, (14, 14), (-27, -27), data.ENEMY.spez_sprites)
        self.boss = boss
        self.boss.hitable = False
        self.location = location
        self.flag = "boss"
        self.death_effect = death_effect

    def move(self):
        self.hitbox.center = (self.boss.hitbox.center[0] + self.location[0], self.boss.hitbox.center[1] + self.location[1])
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)

    def death(self):
        if len([wp for wp in data.ENEMY_DATA if wp.__class__.__name__ == "Boss_weakspot"]) == 1:
            self.boss.hitable = True
            if self.death_effect is not None:
                self.death_effect()
        self.kill = True

    def gfx_animation(self):
        animation_ticker = self.timer_animation_ticker(8)
        if animation_ticker < 4:
            win.blit(self.sprites[self.gfx_idx[0]], (self.hitbox.center[0] + self.gfx_hook[0], self.hitbox.center[1] + self.gfx_hook[1]))
        else:
            win.blit(self.sprites[self.gfx_idx[1]], (self.hitbox.center[0] + self.gfx_hook[0], self.hitbox.center[1] + self.gfx_hook[1]))

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
        self.gfx_idx = (19, 19)

    def move(self):
        self.hitbox.center = self.location

    def set_sp_dmg(self):
        self.special_take_damage = self.boss.special_take_damage

    def gfx_animation(self):
        gfx_angle = degrees(self.target[1], self.hitbox.center[1], self.target[0], self.hitbox.center[0])
        win.blit(rot_center(self.sprites[self.gfx_idx[0]], gfx_angle), (self.hitbox.topleft[0] + self.gfx_hook[0], self.hitbox.topleft[1] + self.gfx_hook[1]))


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
        self.skill_main_gun(target=self.target)


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
                speed=15,
                size=(5, 5),
                start_point=self.boss.hitbox.center,
                damage=1,
                gfx_idx=1,
                # target=self.target,
                curve_size=1.5,
                fixed_angle=self.fixed_angle
            ))
            if self.timer_trigger(7):
                self.fire = False
        self.timer_tick()


class Boss_repair_ship(Enemy):
    #direction, speed, spawn_point, health, size, gfx_idx, gfx_hook, sprites

    def __init__(self, boss):
        self.boss = boss
        self.flag = "boss"
        super().__init__(0, 4, random.randint(1, 4), Enemy.health + 8, (100, 60), (0, 1), (0, 0), Enemy.spez_sprites)
        self.gfx_hook = (-70, -30)

    def move(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        self.hitbox.move_ip(self.angles[degrees(self.boss.hitbox.center[0], self.hitbox.center[0], self.boss.hitbox.center[1], self.hitbox.center[1])])
        if self.hitbox.colliderect(self.boss.hitbox):
            # gfx_effect -->
            self.boss.set_health(-self.boss.max_health * 0.1, (0, 255, 0))
            self.kill = True

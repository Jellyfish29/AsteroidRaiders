import pygame
import random

from init import *
from astraid_funcs import *
from enemys import Enemy, Shooter
from projectiles import Impactor, Wave
from boss_skills import Boss_skills
from items import Item_upgrade_point_crate, Item_heal_crate, Item_supply_crate
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
        self.healthbar_len = self.size[0]
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
        pass

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
            skill()

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
        data.ITEMS.drop((800, 500), target=Item_upgrade_point_crate((100, 100, 100)))
        data.ITEMS.drop((800, 500), target=Item_heal_crate((0, 255, 0)))

        data.ENEMY_PROJECTILE_DATA.clear()
        Background.bg_move = True
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
        self.guns_gfx_animation()
        if self.hitable:
            data.TURRET.missile_aquisition(self)
        if any([self.__class__.__name__ == "Boss_turret",
                self.__class__.__name__ == "Boss_weakspot"]):
            data.TURRET.point_defence(self.hitbox)
        if self.health <= 0:
            self.death()

        if not any([self.__class__.__name__ == "Boss_turret",
                    self.__class__.__name__ == "Boss_weakspot",
                    self.__class__.__name__ == "Elites"]):
            if self.bg_change:
                if Background.bg_color_change(color=0, c_value=40):
                    self.bg_change = False

        self.timer_tick()

    @classmethod
    def create(cls, lvl):
        if lvl == 6:
            data.ENEMY_DATA.append(Boss_mine_boat())
        elif lvl == 12:
            data.ENEMY_DATA.append(Boss_frigatte())
        elif lvl == 18:
            data.ENEMY_DATA.append(Boss_corvette())
        elif lvl == 24:
            data.ENEMY_DATA.append(Boss_destroyer())
        elif lvl == 30:
            data.ENEMY_DATA.append(Boss_cruiser())
        elif lvl == 36:
            data.ENEMY_DATA.append(Boss_scout())
        elif lvl == 42:
            data.ENEMY_DATA.append(Boss_battleship())
        # elif lvl == 35:
        #     data.ENEMY_DATA.append(Boss_carrier())


data.BOSS = Bosses


class Boss_mine_boat(Bosses):

    def __init__(self):
        self.health = 170
        self.speed = 4
        self.fire_rate = 90
        self.move_pattern = [random.randint(0, 9) for _ in range(40)]
        self.size = (80, 200)
        self.gfx_idx = (0, 1)
        self.gfx_hook = (-130, -120)
        self.drop_amount = 1
        self.skills_lst = [self.skill_mines]
        super().__init__()
        self.engine = {
            "right": (-78, -10),
            "down": (-19, -153),
            "up": (-15, 90),
            "left": (32, -10)
        }

    def phase_1(self):
        self.angles = angles_360(5)
        # self.special_gfx = True
        self.special_move = True
        data.ENEMY_DATA.append(Boss_weakspot(self.max_health * 0.15, self, (0, -110)))
        self.skills_lst.append(self.skill_chaser)

    def phase_2(self):
        for loc, effect in [
            ((-50, 50), None),
            ((50, 50), lambda: self.skills_lst.remove(self.skill_missile))
        ]:
            data.ENEMY_DATA.append(Boss_weakspot(
                self.max_health * 0.2,
                self,
                loc,
                death_effect=effect)
            )
        self.skills_lst.append(self.skill_missile)

    def phase_3(self):
        Background.bg_move = True
        self.agles = self.angles = angles_360(7)
        self.fire_rate -= 25
        self.set_health(-25, (0, 255, 0))
        self.skills_lst.append(self.skill_mines)


class Boss_frigatte(Bosses):

    def __init__(self):
        self.health = 700
        self.speed = 3
        self.fire_rate = 60
        self.move_pattern = [0, 1, 2, 3]
        self.size = (120, 220)
        self.gfx_idx = (2, 3)
        self.gfx_hook = (-130, -120)
        self.drop_amount = 1
        self.wp_locations = ((-50, 50), (50, 50), (0, -100))
        self.skills_lst = [self.skill_missile]
        super().__init__()
        self.engine = {
            "right": (-108, -10),
            "down": (-19, -153),
            "up": (-18, 90),
            "left": (67, -10)
        }

    def phase_1(self):

        self.skills_lst.append(self.skill_turret_defence_matrix)
        for i in range(2):
            spawn_loaction = (random.randint(300, 1700), random.randint(150, 900))
            data.ENEMY_PROJECTILE_DATA.append(Impactor(
                speed=4,
                start_point=self.hitbox.center,
                flag="enemy",
                target=spawn_loaction,
                impact_effect=lambda loc=spawn_loaction:
                data.ENEMY_DATA.append(Boss_turret(self.max_health * 0.05, self, loc))
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
                impact_effect=lambda loc=spawn_loaction:
                data.ENEMY_DATA.append(Boss_turret(self.max_health * 0.05, self, loc))
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
                impact_effect=lambda loc=spawn_loaction:
                data.ENEMY_DATA.append(Boss_turret(self.max_health * 0.05, self, loc))
            ))


class Boss_corvette(Bosses):

    def __init__(self):

        self.health = 800
        self.speed = 4
        self.fire_rate = 30
        self.move_pattern = [random.randint(0, 9) for _ in range(40)]
        self.size = (80, 200)
        self.gfx_idx = (4, 5)
        self.gfx_hook = (-130, -120)
        self.drop_amount = 1
        self.skills_lst = [self.skill_volley]
        super().__init__()
        self.engine = {
            "right": (-80, -10),
            "down": (-19, -153),
            "up": (-10, 100),
            "left": (40, -10)
        }

    def phase_1(self):

        Background.bg_move = True
        Background.scroll_speed = 1
        self.speed += 1
        self.angles = angles_360(self.speed)
        self.skills_lst.append(self.skill_jumpdrive)

    def phase_2(self):

        self.speed += 1
        Background.scroll_speed = 2
        self.angles = angles_360(self.speed)
        self.fire_rate -= 10
        self.skills_lst.append(self.skill_jumpdrive)
        self.skills_lst.append(self.skill_speed_boost)

    def phase_3(self):

        Background.scroll_speed = 3
        self.speed += 2
        self.angles = angles_360(self.speed)
        self.fire_rate -= 10
        self.skills_lst.append(self.skill_jumpdrive)

    def special_death(self):
        Background.bg_move = False
        Background.scroll_speed = 1


class Boss_destroyer(Bosses):

    def __init__(self):
        self.health = 2400
        self.speed = 2
        self.fire_rate = 60
        self.move_pattern = [0, 7, 0, 1, 2]
        self.size = (150, 230)
        self.gfx_idx = (6, 7)
        self.gfx_hook = (-130, -130)
        self.skills_lst = [self.skill_volley, self.skill_missile]
        self.drop_amount = 1
        self.turn_angles = (359 - i for i in range(0, 91))
        self.turn_angle = 359
        super().__init__()
        self.engine = {
            "right": (-105, -10),
            "down": (-19, -153),
            "up": (-15, 90),
            "left": (70, -10)
        }

    def phase_1(self):

        self.special_attack = True
        self.special_skills_lst.append(self.skill_missile_barrage)
        self.skills_lst.append(self.skill_salvo_alpha)
        for loc, size in [((0, 0), (180, 50)),
                          ((0, -100), (80, 50)),
                          ((0, 100), (80, 50))
                          ]:
            data.ENEMY_DATA.append(
                Boss_weakspot(self.max_health * 0.05, self, loc, size=size)
            )

    def phase_2(self):

        self.special_attack = True
        self.special_skills_lst.append(self.skill_main_gun_salvo)
        self.skills_lst.append(self.skill_jumpdrive)
        for loc, size in [((0, 0), (180, 50)),
                          ((0, -100), (80, 50)),
                          ((0, 100), (80, 50))
                          ]:
            data.ENEMY_DATA.append(
                Boss_weakspot(self.max_health * 0.05, self, loc, size=size)
            )
        data.PLAYER.hitbox.center
        for _ in range(8):
            target = random.choice([
                (random.randint(0, winwidth),
                 random.randint(0, winheight),
                 data.PLAYER.hitbox.center)
            ])
            data.ENEMY_DATA.append(Boss_main_gun_battery(self, target))

    def phase_3(self):

        self.speed += 3
        self.set_health(-100, (0, 255, 0))
        self.fire_rate -= 25
        self.special_attack = True
        self.special_skills_lst.append(self.skill_laser_storm_laststand)
        for _ in range(5):
            data.ENEMY_DATA.append(Boss_laser_battery(self))

    def special_gfx_animation(self):
        if self.timer_trigger(3):
            self.turn_angle = next(self.turn_angles, 270)
        win.blit(rot_center(
            self.sprites[self.gfx_idx[0]], self.turn_angle),
            (self.hitbox.center[0] + self.gfx_hook[0],
             self.hitbox.center[1] + self.gfx_hook[1])
        )


class Boss_cruiser(Bosses):

    def __init__(self):
        self.health = 5000
        self.speed = 2
        self.fire_rate = 50
        self.move_pattern = [8, 9]
        self.size = (130, 230)
        self.gfx_idx = (8, 9)
        self.gfx_hook = (-130, -130)
        self.skills_lst = [self.skill_volley, self.skill_missile, self.skill_salvo_charlie]
        self.turn_angles = (359 - i for i in range(0, 91))
        self.turn_angle = 359
        self.drop_amount = 1
        super().__init__()
        self.engine = {
            "right": (-105, -10),
            "down": (-19, -153),
            "up": (-15, 90),
            "left": (70, -10)
        }

    def phase_1(self):

        self.move_pattern = [0, 7, 0, 1, 2]
        # self.angles = angles_360(3)
        self.skills_lst.append(self.skill_dart_missiles)
        for _ in range(2):
            data.ENEMY_DATA.append(Boss_repair_ship(self))

    def phase_2(self):

        self.move_pattern = [random.randint(0, 9) for _ in range(40)]
        self.angles = angles_360(4)
        self.skills_lst.append(self.skill_salvo_charlie)
        for _ in range(4):
            data.ENEMY_DATA.append(Boss_repair_ship(self))

    def phase_3(self):

        self.angles = angles_360(4)
        self.special_attack = True
        self.special_skills_lst.append(self.skill_dart_missile_last_stand)
        for _ in range(6):
            data.ENEMY_DATA.append(Boss_repair_ship(self))

    def special_gfx_animation(self):
        if self.timer_trigger(3):
            self.turn_angle = next(self.turn_angles, 270)
        win.blit(rot_center(
            self.sprites[self.gfx_idx[0]], self.turn_angle),
            (self.hitbox.center[0] + self.gfx_hook[0],
             self.hitbox.center[1] + self.gfx_hook[1])
        )


class Boss_scout(Bosses):

    def __init__(self):
        self.health = 2000
        self.speed = 6
        self.fire_rate = 70
        self.move_pattern = [random.randint(0, 9) for _ in range(40)]
        self.size = (170, 100)
        self.gfx_idx = (14, 14)
        self.gfx_hook = (-50, -50)
        self.skills_lst = [self.skill_salvo_delta]
        self.drop_amount = 1
        self.gfx_angle = 0
        self.force_field_rate = 22
        self.phase_triggers = [self.health * 0.8, self.health * 0.5, self.health * 0.15]
        super().__init__()
        self.hitbox = pygame.Rect(winwidth / 2, 1200, self.size[0], self.size[1])
        # self.engine = {"right": (-105, -10), "down": (-19, -153), "up": (-15, 90), "left": (70, -10)}

    def gfx_animation(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        animation_ticker = self.timer_animation_ticker(8)
        self.gfx_angle = degrees(
            data.PLAYER.hitbox.center[1],
            self.hitbox.center[1],
            data.PLAYER.hitbox.center[0],
            self.hitbox.center[0]
        )
        if animation_ticker < 4:
            win.blit(gfx_rotate(
                self.sprites[self.gfx_idx[0]],
                self.gfx_angle),
                (self.hitbox.topleft[0] + self.gfx_hook[0],
                 self.hitbox.topleft[1] + self.gfx_hook[1])
            )
        else:
            win.blit(gfx_rotate(
                self.sprites[self.gfx_idx[1]],
                self.gfx_angle),
                (self.hitbox.topleft[0] + self.gfx_hook[0],
                 self.hitbox.topleft[1] + self.gfx_hook[1])
            )

    def phase_1(self):

        self.special_attack = True
        self.special_skills_lst.append(self.skill_scout_hunt)

    def phase_2(self):

        pass

    def phase_3(self):

        self.force_field_rate -= 8

    @run_limiter
    def special_gfx_animation(self, limiter):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        if self.gfx_angle == 180:
            if limiter.run_block_once():
                Background.scroll_speed = 10
                self.special_skills_lst.append(self.skill_scout_force_field_fire)
                self.gfx_idx = (12, 13)
        elif self.gfx_angle > 180:
            if self.timer_trigger(1):
                self.gfx_angle -= 1
        elif self.gfx_angle < 180:
            if self.timer_trigger(1):
                self.gfx_angle += 1

        animation_ticker = self.timer_animation_ticker(8)
        if animation_ticker < 4:
            win.blit(rot_center(
                self.sprites[self.gfx_idx[0]],
                self.gfx_angle),
                (self.hitbox.center[0] - 90,
                 self.hitbox.center[1] - 90)
            )
        else:
            win.blit(rot_center(
                self.sprites[self.gfx_idx[1]],
                self.gfx_angle),
                (self.hitbox.center[0] - 90,
                 self.hitbox.center[1] - 90)
            )

    def snare_effect(self):
        if self.snared:
            self.hitable = True
            self.hide_health_bar = False
            Background.bg_move = False
            self.gfx_idx = (14, 14)
            if self.timer_key_trigger(300, key="snare"):
                self.hitable = False
                self.hide_health_bar = True
                Background.bg_move = True
                self.gfx_idx = (12, 13)
                self.snared = False

    def special_death(self):
        Background.bg_move = False
        Background.scroll_speed = 1


class Boss_battleship(Bosses):

    def __init__(self):
        self.health = 8000
        self.speed = 2
        self.fire_rate = 70
        self.move_pattern = [0, 7, 0, 1, 2]
        self.size = (180, 240)
        self.gfx_idx = (10, 11)
        self.gfx_hook = (-130, -130)
        self.skills_lst = [self.skill_main_gun_fire_position,
                           self.skill_missile,
                           self.skill_main_gun]
        self.drop_amount = 1
        self.turn_angles_1 = (359 - i for i in range(0, 91))
        self.turn_angles_2 = (270 + i for i in range(0, 91))
        self.turn_angle = 359
        super().__init__()
        self.engine = {
            "right": (-105, -10),
            "down": (-19, -153),
            "up": (-15, 90),
            "left": (70, -10)
        }
        self.gun_position = [-33, 30]  # turned position = [-83, -33]

    def phase_1(self):

        self.special_attack = True
        self.special_skills_lst.append(self.skill_radar_guided_gun)

    def phase_2(self):

        self.special_gfx = False
        self.special_attack = False
        self.angles = angles_360(2)
        self.special_skills_lst.remove(self.skill_radar_guided_gun)
        self.special_skills_lst.remove(self.skill_point_defence)
        self.skills_lst.remove(self.skill_missile)
        self.skills_lst += [self.skill_dart_missiles,
                            self.skill_salvo_charlie,
                            self.skill_wave_motion_gun]

    def phase_3(self):

        self.special_attack = True
        self.special_skills_lst.append(self.skill_death_wave)
        for loc, size, death_effect in [
            ((-100, 0), (10, 50), lambda: data.ENEMY_DATA.append(
                Boss_shield_bubble(data.PLAYER.hitbox.topleft, self))),  # left
            ((100, 0), (10, 50), lambda: data.ENEMY_DATA.append(
                Boss_shield_bubble(data.PLAYER.hitbox.topleft, self))),  # right
            ((0, -130), (50, 10), lambda: data.ENEMY_DATA.append(
                Boss_shield_bubble(data.PLAYER.hitbox.topleft, self))),  # top
            ((0, 130), (50, 10), lambda: data.ENEMY_DATA.append(
                Boss_shield_bubble(data.PLAYER.hitbox.topleft, self)))  # bot
        ]:
            data.ENEMY_DATA.append(Boss_weakspot(
                self.max_health * 0.05, self, loc,
                death_effect=death_effect, size=size)
            )

    def guns_gfx_animation(self):
        gfx_angle = degrees(
            data.PLAYER.hitbox.center[1],
            self.hitbox.center[1],
            data.PLAYER.hitbox.center[0],
            self.hitbox.center[0]
        )
        win.blit(rot_center(
            data.ENEMY.spez_sprites[19], gfx_angle),
            (self.hitbox.center[0] + self.gun_position[0],
             self.hitbox.center[1] + self.gun_position[1])
        )


# class Boss_carrier(Bosses):

#     def __init__(self):
#         self.health = 7000
#         self.speed = 2
#         self.fire_rate = 160
#         self.boss_skill = ["adds"]
#         self.move_pattern = (8, 9)
#         self.size = (140, 360)
#         self.gfx_idx = (32, 33)
#         self.gfx_hook = (-80, -220)
#         self.skills_lst = [self.skill_adds]
#         self.phase_skills = [[], []]
#         self.drop_amount = 1
#         super().__init__()


class Elites(Bosses):

    health = 20
    sprites = get_images("elites")

    def __init__(
            self,
            health=0,
            speed=0,
            fire_rate=0,
            skill=[],
            gfx_idx=(0, 1),
            gfx_hook=(-30, -30)
    ):
        self.health = health
        self.speed = speed
        self.fire_rate = fire_rate
        self.elite_skill = skill
        self.gfx_idx = gfx_idx
        self.gfx_hook = gfx_hook

        self.move_pattern = [random.randint(0, 9) for _ in range(40)]
        self.size = (100, 100)
        self.drop_amount = 0
        self.score_amount = 100
        self.flag = "elite"
        super().__init__()
        self.sprites = Elites.sprites

    def phases(self):
        pass

    def death(self):
        Gfx.create_effect("explosion_3", 2,
                          (self.hitbox.topleft[0] - 300, self.hitbox.topleft[1] - 300),
                          explo=True)
        data.LEVELSelite_fight = False
        if random.randint(0, 100) > 90:
            data.ITEMS.drop((self.hitbox.topleft), amount=1)
        else:
            random.choice([
                lambda: data.ITEMS.drop(
                    (self.hitbox.topleft), target=Item_supply_crate((100, 100, 100))),
                lambda: data.ITEMS.drop(
                    (self.hitbox.topleft), target=Item_heal_crate((100, 100, 100))),
                lambda: data.ITEMS.drop(
                    (self.hitbox.topleft), target=Item_upgrade_point_crate((100, 100, 100)))
            ])()
        self.kill = True

    def boss_skills(self):
        self.elite_skill(self)

    def gfx_animation(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        animation_ticker = self.timer_animation_ticker(8)
        gfx_angle = degrees(
            data.PLAYER.hitbox.center[1],
            self.hitbox.center[1],
            data.PLAYER.hitbox.center[0],
            self.hitbox.center[0]
        )
        if animation_ticker < 4:
            win.blit(gfx_rotate(
                self.sprites[self.gfx_idx[0]], gfx_angle),
                (self.hitbox.topleft[0] + self.gfx_hook[0],
                 self.hitbox.topleft[1] + self.gfx_hook[1])
            )
        else:
            win.blit(gfx_rotate(
                self.sprites[self.gfx_idx[1]], gfx_angle),
                (self.hitbox.topleft[0] + self.gfx_hook[0],
                 self.hitbox.topleft[1] + self.gfx_hook[1])
            )

    @classmethod
    def spawn(cls):
        data.ENEMY_DATA.append(random.choice([
            lambda: Elites(
                health=Elites.health, speed=2, fire_rate=120,
                skill=Boss_skills.skill_salvo_charlie, gfx_idx=(8, 9)),
            lambda: Elites(
                health=Elites.health + Elites.health * 0.2, speed=4, fire_rate=120,
                skill=Boss_skills.skill_missile, gfx_idx=(2, 3)),
            lambda: Elites(
                health=Elites.health - Elites.health * 0.2, speed=8, fire_rate=80,
                skill=Boss_skills.skill_jumpdrive, gfx_idx=(4, 5)),
            lambda: Elites(
                health=Elites.health + Elites.health * 0.7, speed=3, fire_rate=100,
                skill=Boss_skills.skill_salvo_delta, gfx_idx=(6, 7)),
            lambda: Elites(
                health=Elites.health + Elites.health * 0.1, speed=2, fire_rate=100,
                skill=Boss_skills.skill_main_gun, gfx_idx=(0, 1)),
            lambda: Elites(
                health=Elites.health + Elites.health * 0.1, speed=6, fire_rate=100,
                skill=Boss_skills.skill_wave_motion_gun, gfx_idx=(10, 11))
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
        self.hitbox.center = (self.boss.hitbox.center[0] + self.location[0],
                              self.boss.hitbox.center[1] + self.location[1])

    def death(self):
        if len([wp for wp in data.ENEMY_DATA if wp.__class__.__name__ == "Boss_weakspot"]) == 1:
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
        self.gfx_idx = (19, 19)

    def move(self):
        self.hitbox.center = self.location

    def set_sp_dmg(self):
        self.special_take_damage = self.boss.special_take_damage

    def gfx_animation(self):
        gfx_angle = degrees(
            self.target[1],
            self.hitbox.center[1],
            self.target[0],
            self.hitbox.center[0]
        )
        win.blit(rot_center(
            self.sprites[self.gfx_idx[0]], gfx_angle),
            (self.hitbox.topleft[0] + self.gfx_hook[0],
             self.hitbox.topleft[1] + self.gfx_hook[1])
        )


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
                speed=20,
                size=(5, 5),
                start_point=self.boss.hitbox.center,
                damage=1,
                gfx_idx=16,
                # target=self.target,
                curve_size=1.5,
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
        self.gfx_idx = (20, 21)
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

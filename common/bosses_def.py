import pygame
import random
from bosses import *
from ui import *
import astraid_data as data
from items_misc import Item_upgrade_point_crate, Item_heal_crate, Item_supply_crate
from projectiles import Impactor
from Gfx import Gfx, Background


class Boss_mine_boat(Bosses):

    def __init__(self):
        self.health = 240
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
        self.guns = [{"pos": [-50, -50], "sprites": [2, 3]}]

    def phase_1(self):
        self.angles = angles_360(5)
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
        self.agles = angles_360(7)
        self.fire_rate -= 25
        self.set_health(-25, (0, 255, 0))
        self.skills_lst.append(self.skill_mines)


class Boss_frigatte(Bosses):

    def __init__(self):
        self.health = 1200
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
        self.guns = [{"pos": [-50, -50], "sprites": [4, 5]}]

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

        self.angles = angles_360(2)
        self.skills_lst += [self.skill_turret_defence_matrix]
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

        self.health = 1600
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
        self.guns = [{"pos": [-30, -30], "sprites": [2, 3]},
                     {"pos": [-70, -30], "sprites": [2, 3]}
                     ]

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
        self.health = 3000
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
        self.guns = [{"pos": [-20, -50], "sprites": [4, 5]},
                     {"pos": [-80, -50], "sprites": [4, 5]}
                     ]

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

        self.speed += 2
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
        for _ in range(6):
            target = random.choice([
                (random.randint(0, winwidth),
                 random.randint(0, winheight),
                 data.PLAYER.hitbox.center)
            ])
            data.ENEMY_DATA.append(Boss_main_gun_battery(self, target))

    def phase_3(self):

        # self.speed += 3
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
        self.health = 7000
        self.speed = 2
        self.fire_rate = 65
        self.move_pattern = [8, 9]
        self.size = (130, 230)
        self.gfx_idx = (8, 9)
        self.gfx_hook = (-130, -130)
        self.skills_lst = [self.skill_volley, self.skill_salvo_charlie]
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
        self.guns = [{"pos": [-20, -40], "sprites": [4, 5]},
                     {"pos": [-80, -40], "sprites": [4, 5]},
                     {"pos": [-50, -100], "sprites": [2, 3]},
                     {"pos": [-50, 0], "sprites": [2, 3]},
                     ]

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
        self.health = 3000
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
        self.health = 15000
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
        self.guns = [{"pos": [-53, 20], "sprites": [6, 7]},
                     {"pos": [29, -20], "sprites": [2, 3]},
                     {"pos": [-133, -20], "sprites": [2, 3]}]

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


# class Boss_carrier(Bosses):

#     def __init__(self):
#         self.health = 20000
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
            elite_skill=[],
            gfx_idx=(0, 1),
            gfx_hook=(-30, -30),
            drop=True,
            special_spawn=None,
            special_dest=None
    ):
        self.health = health
        self.speed = speed
        self.fire_rate = fire_rate
        self.gfx_idx = gfx_idx
        self.gfx_hook = gfx_hook
        self.drop = drop
        self.move_pattern = [random.randint(0, 9) for _ in range(40)]
        self.size = (100, 100)
        self.drop_amount = 0
        self.score_amount = 100
        self.flag = "elite"
        super().__init__()
        self.skills_lst = []
        self.skills_lst.append(elite_skill)
        if special_spawn is not None:
            self.hitbox.center = special_spawn
            self.special_move = True
            self.speed = Background.scroll_speed
            self.skills_lst.append(self.skill_hold_position)
            self.drop = False
        if special_dest is not None:
            self.checkpoints = {0: special_dest}
            self.move_pattern = [0, 0]
            self.drop = False
            self.skills_lst.append(self.skill_zone_capture)
        self.sprites = Elites.sprites

    def phases(self):
        pass

    def death(self):
        Gfx.create_effect("explosion_3", 2,
                          (self.hitbox.topleft[0] - 300, self.hitbox.topleft[1] - 300),
                          explo=True)
        data.LEVELS.elite_fight = False

        if self.drop:
            if random.randint(0, 100) > 90:
                data.ITEMS.drop((self.hitbox.topleft), amount=1)
            else:
                random.choice([
                    lambda:data.ITEMS.drop(
                        (self.hitbox.topleft), target=Item_supply_crate((100, 100, 100))),
                    lambda: data.ITEMS.drop(
                        (self.hitbox.topleft), target=Item_heal_crate((100, 100, 100))),
                    lambda: data.ITEMS.drop(
                        (self.hitbox.topleft), target=Item_upgrade_point_crate((100, 100, 100)))
                ])()
        self.kill = True

    # def boss_skills(self):
    #     self.elite_skill(self)

    def gfx_animation(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        animation_ticker = self.timer_animation_ticker(8)
        if len(data.PLAYER_DATA) == 1:
            gfx_angle = degrees(
                data.PLAYER_DATA[random.randint(0, len(data.PLAYER_DATA) - 1)].hitbox.center[1],
                self.hitbox.center[1],
                data.PLAYER_DATA[random.randint(0, len(data.PLAYER_DATA) - 1)].hitbox.center[0],
                self.hitbox.center[0]
            )
        else:
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

    def guns_gfx_animation(self):
        pass

    def gun_gfx_idx_update(self):
        pass

    @classmethod
    def spawn(cls, special_spawn=None, special_dest=None, drop=True):
        data.ENEMY_DATA.append(random.choice([
            lambda: Elites(
                health=Elites.health, speed=2, fire_rate=120,
                elite_skill=Boss_skills.skill_salvo_charlie, gfx_idx=(12, 13),
                special_spawn=special_spawn, special_dest=special_dest, drop=drop),
            lambda: Elites(
                health=Elites.health + Elites.health * 0.2, speed=6, fire_rate=120,
                elite_skill=Boss_skills.skill_missile, gfx_idx=(3, 4),
                special_spawn=special_spawn, special_dest=special_dest, drop=drop),
            lambda: Elites(
                health=Elites.health - Elites.health * 0.2, speed=8, fire_rate=80,
                elite_skill=Boss_skills.skill_jumpdrive, gfx_idx=(6, 7),
                special_spawn=special_spawn, special_dest=special_dest, drop=drop),
            lambda: Elites(
                health=Elites.health + Elites.health * 0.7, speed=3, fire_rate=100,
                elite_skill=Boss_skills.skill_salvo_delta, gfx_idx=(9, 10),
                special_spawn=special_spawn, special_dest=special_dest, drop=drop),
            lambda: Elites(
                health=Elites.health + Elites.health * 0.1, speed=2, fire_rate=100,
                elite_skill=Boss_skills.skill_main_gun, gfx_idx=(0, 1),
                special_spawn=special_spawn, special_dest=special_dest, drop=drop),
            lambda: Elites(
                health=Elites.health + Elites.health * 0.1, speed=4, fire_rate=100,
                elite_skill=Boss_skills.skill_wave_motion_gun, gfx_idx=(15, 16),
                special_spawn=special_spawn, special_dest=special_dest, drop=drop)
        ])())


data.ELITES = Elites

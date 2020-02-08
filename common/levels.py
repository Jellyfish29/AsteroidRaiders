import random
import pickle
# import pygame

from astraid_funcs import *
import astraid_data as data
from phenomenon import *
from enemys import *
from bosses_def import *
import Gfx as gfx
from items import Active_Items


class Levels:

    interval_score = 0
    display_score = 0
    display_level = 1
    level = 1
    level_interval = 35
    enemy_amount = 3  # at Start
    skill_points = 1
    # elite/Elites
    elite_wait = False
    elite_spawn_time = 0
    boss_fight = False
    after_boss = False
    elite_fight = False
    elite_max_spawn_time = 4000
    second_elite_chance = 100
    second_elite = False
    death_score_panalties = {
        1: 30,
        6: 50,
        12: 80,
        18: 150,
        24: 250,
        30: 370,
        36: 500,
        42: 700
    }
    # Events
    event_trigger_time = (3600, 5000)
    event_id = 0

    @classmethod
    def scaling(cls):
        data.ENEMY.health += 0.5
        Elites.health += Elites.health * 0.1
        cls.event_trigger_time = (cls.event_trigger_time[0] - 60, cls.event_trigger_time[1] - 75)
        if cls.event_trigger_time[0] <= 200:
            cls.event_trigger_time = (200, 500)
        cls.second_elite_chance -= 1.5
        if cls.second_elite_chance < 40:
            cls.second_elite_chance = 40
        if cls.level % 6 == 0:
            cls.enemy_amount += 1
            cls.elite_max_spawn_time -= 100
        if cls.level % 6 == 0:
            cls.spez_add()
            # data.BOSS.create(cls.level)
            cls.boss_spawn()
            cls.boss_fight = True
            gfx.Background.bg_move = False
            cls.save_game()

    @classmethod
    @timer
    def elite_spawn(cls, timer):
        if not any((cls.after_boss, cls.boss_fight)):
            if cls.level not in [i - 1 for i in range(6, 49, 6)]:
                if not cls.elite_wait:
                    cls.elite_spawn_time = cls.elite_max_spawn_time
                    cls.elite_wait = True
                if cls.elite_wait:
                    if timer.trigger(int(cls.elite_spawn_time)):
                        Elites.spawn()
                        if cls.level > 10 and random.randint(0, 100) > cls.second_elite_chance:
                            cls.second_elite = True
                        cls.elite_wait = False
        if cls.second_elite:
            if timer.trigger(240):
                cls.second_elite = False
                Elites.spawn()

    @classmethod
    def boss_spawn(cls):
        if cls.level == 6:
            data.ENEMY_DATA.append(Boss_mine_boat())
        elif cls.level == 12:
            data.ENEMY_DATA.append(Boss_frigatte())
        elif cls.level == 18:
            data.ENEMY_DATA.append(Boss_corvette())
        elif cls.level == 24:
            data.ENEMY_DATA.append(Boss_destroyer())
        elif cls.level == 30:
            data.ENEMY_DATA.append(Boss_cruiser())
        elif cls.level == 36:
            data.ENEMY_DATA.append(Boss_scout())
        elif cls.level == 42:
            data.ENEMY_DATA.append(Boss_battleship())

    @classmethod
    def spez_add(cls):
        data.ENEMY.spez_spawn_time -= 18
        data.PHENOM.spawn_time -= 15
        if data.ENEMY.spez_spawn_time < 60:
            data.ENEMY.spez_spawn_time = 60
        if cls.level == 1:
            data.ENEMY.set_spawn_table(Seeker)
            data.ENEMY.set_spawn_table(Jumper)
            data.PHENOM.set_spawn_table(Planet)
        if cls.level == 6:
            data.ENEMY.set_spawn_table(Shooter)
            # data.PHENOM.set_spawn_table(Gravity_well)
        elif cls.level == 12:
            data.ENEMY.set_spawn_table(Mine_layer)
            data.PHENOM.set_spawn_table(Repair_station)
        elif cls.level == 18:
            data.ENEMY.set_spawn_table(Strafer)
            # data.PHENOM.set_spawn_table(Anti_gravity_well)
        elif cls.level == 24:
            pass
            # data.ENEMY.get_spawn_table().append(en.Miner)
            # data.PHENOM.set_spawn_table(Nabulae_aoe_damage)
        elif cls.level == 30:
            pass
            # data.PHENOM.set_spawn_table(Nebulae_fire_rate_plus)
        elif cls.level == 36:
            pass

    @classmethod
    def execute_event(cls, event_id):
        spawn = random.randint(1, 4)
        if event_id == 1:
            for i in range(4 + int(cls.level / 2)):
                data.ENEMY_DATA.append(Asteroid(spawn=spawn))
        elif event_id == 2:
            for i in range(2 + int(cls.level / 2)):
                data.ENEMY_DATA.append(Jumper(spawn=spawn))
        elif event_id == 3:
            for i in range(2 + int(cls.level / 10)):
                data.ENEMY_DATA.append(Shooter(spawn=spawn))
        elif event_id == 4:
            for i in range(2 + int(cls.level / 10)):
                data.ENEMY_DATA.append(Seeker(spawn=spawn))
        elif event_id == 5:
            for i in range(3 + int(cls.level / 10)):
                data.ENEMY_DATA.append(Strafer(spawn=spawn))
        elif event_id == 6:
            for i in range(3):
                data.ENEMY_DATA.append(Mine_layer(spawn=spawn))

    @classmethod
    def save_game(cls):
        with open(os.path.join(os.getcwd()[:-7], f"save_games\\saves"), "wb") as file:
            pickle.dump(STAGE_SAVE(), file)

    @classmethod
    def load_game(cls):
        with open(os.path.join(os.getcwd()[:-7], f"save_games\\saves"), "rb") as file:
            return pickle.load(file)

    @classmethod
    @timer
    def update(cls, timer):

        if not any((cls.boss_fight, cls.after_boss, cls.elite_fight)):
            if timer.trigger(random.randint(cls.event_trigger_time[0], cls.event_trigger_time[1])):
                cls.execute_event(random.randint(1, 6))  # choices

        cls.elite_spawn()

        if cls.interval_score > cls.level_interval:
            cls.level += 1
            cls.display_level += 1
            cls.level_interval += 3
            cls.skill_points += 1
            cls.scaling()
            cls.interval_score = 0


data.LEVELS = Levels


class STAGE_SAVE():

    def __init__(self):
        self.items = data.ITEMS.inventory_dic
        self.pl_health = data.PLAYER.health
        self.pl_max_health = data.PLAYER.max_health
        self.pl_heal_amount = data.PLAYER.heal_amount
        self.pl_raw_health = data.PLAYER.raw_max_health
        self.skill_points = Levels.skill_points
        self.upgrade_points = data.ITEMS.upgrade_points
        self.pl_angles = data.PLAYER.angles
        self.pl_speed = data.PLAYER.speed
        self.pl_raw_speed = data.PLAYER.raw_speed
        self.pl_dmg = data.PLAYER.damage
        self.pl_crit = data.PLAYER.crit_chance
        self.pl_raw_crit = data.PLAYER.raw_crit_chance
        self.pl_fire_rate = data.TURRET.fire_rate
        self.pl_raw_fire_rate = data.TURRET.raw_fire_rate
        self.pl_cd = Active_Items.cd_reduction
        self.pl_jump = data.PLAYER.jumpdrive
        self.pl_shield = data.PLAYER.shield
        self.lvl = Levels.level
        self.display_level = Levels.display_level
        self.score = Levels.display_score
        self.interval_score = Levels.level_interval
        self.boss_fight = Levels.boss_fight
        self.enemy_health = data.ENEMY.health
        self.elite_health = Elites.health
        self.enemy_amount = Levels.enemy_amount
        self.second_elite_chance = Levels.second_elite_chance
        self.enemy_table = data.ENEMY.spez_spawn_table
        self.phenomenon_spawn_table = data.PHENOM.phenomenon_spawn_table
        self.bg_speed = gfx.Background.scroll_speed
        self.bg_move = gfx.Background.bg_move
        self.overdrive_count = data.TURRET.overdrive_count
        self.elite_sp_time = Levels.elite_max_spawn_time

    def load_save(self):
        data.ENEMY_DATA.clear()
        data.ENEMY_PROJECTILE_DATA.clear()
        data.PLAYER_PROJECTILE_DATA.clear()
        data.PHENOMENON_DATA.clear()
        data.PLAYER_DATA.clear()
        data.ITEMS.dropped_lst.clear()

        Levels.after_boss = False
        Levels.interval_score = 0
        Levels.level = self.lvl
        Levels.display_level = self.display_level
        Levels.display_score = self.score
        Levels.level_interval = self.interval_score
        data.ITEMS.inventory_dic = self.items
        data.PLAYER.health = self.pl_health
        data.PLAYER.max_health = self.pl_max_health
        data.PLAYER.heal_amount = self.pl_heal_amount
        data.PLAYER.raw_max_health = self.pl_raw_health
        data.PLAYER.hitbox.center = (1000, 900)
        Levels.skill_points = self.skill_points
        data.ITEMS.upgrade_points = self.upgrade_points
        data.PLAYER.angles = self.pl_angles
        data.PLAYER.speed = self.pl_speed
        data.PLAYER.raw_speed = self.pl_raw_speed
        data.PLAYER.damage = self.pl_dmg
        data.PLAYER.crit_chance = self.pl_crit
        data.PLAYER.raw_crit_chance = self.pl_raw_crit
        data.TURRET.fire_rate = self.pl_fire_rate
        data.TURRET.raw_fire_rate = self.pl_raw_fire_rate
        Active_Items.cd_reduction = self.pl_cd
        data.PLAYER.jumpdrive = self.pl_jump
        data.PLAYER.shield = self.pl_shield
        Levels.boss_fight = self.boss_fight
        data.ENEMY.health = self.enemy_health
        Elites.health = self.elite_health
        Levels.enemy_amount = self.enemy_amount
        Levels.second_elite_chance = self.second_elite_chance
        data.ENEMY.spez_spawn_table = self.enemy_table
        data.PHENOM.phenomenon_spawn_table = self.phenomenon_spawn_table
        gfx.Background.scroll_speed = self.bg_speed
        gfx.Background.bg_move = self.bg_move
        data.TURRET.overdrive_count = self.overdrive_count
        Levels.elite_max_spawn_time = self.elite_sp_time
        if self.boss_fight:
            self.spawn_boss()

    def spawn_boss(self):
        data.BOSS.create(self.lvl)

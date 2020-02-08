import random
import pickle
# import pygame

from astraid_funcs import *
import astraid_data as data
from phenomenon import *
from enemys import *
from bosses_def import *
from Gfx import Gfx, Background
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
    elite_max_spawn_time = 4000
    second_elite_chance = 100
    elite_spawn_time = 0
    # Flags
    elite_wait = False
    boss_fight = False
    after_boss = False
    elite_fight = False
    special_events = False
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
    special_event_queue = []
    events_disabled = False
    event_id = 0
    special_event_triggered = 0
    special_event_didnt_trigger = 0
    special_event_amount = 2

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
        if cls.level % 12 == 0:
            cls.self.special_event_amount += 1
            if cls.self.special_event_amount > 5:
                self.special_event_amount = 5
        if cls.level % 6 == 0:
            cls.enemy_amount += 1
            cls.elite_max_spawn_time -= 100
            cls.spez_add()
            cls.boss_spawn()
            cls.boss_fight = True
            Background.bg_move = False
            cls.special_event_triggered = 0
            cls.special_event_didnt_trigger = 0
            cls.save_game()
        else:
            if not cls.events_disabled:
                if cls.special_event_triggered < cls.special_event_amount:
                    if random.randint(1, 100) > 50 or cls.special_event_didnt_trigger > 1:
                        cls.special_event_triggered += 1
                        cls.execute_special_event()
                    else:
                        cls.special_event_didnt_trigger += 1

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
            data.ENEMY.set_spawn_table(Comet)
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
            data.ENEMY.set_spawn_table(Miner)
            # data.PHENOM.set_spawn_table(Nabulae_aoe_damage)
        elif cls.level == 30:
            pass
            # data.PHENOM.set_spawn_table(Nebulae_fire_rate_plus)
        elif cls.level == 36:
            pass

    @classmethod
    def execute_event(cls, event_id):
        if event_id == 1:
            Events.event_wave(
                enemy=Asteroid, spawn=random.randint(1, 4), amount=4, scaling=int(cls.level / 2))
        elif event_id == 2:
            Events.event_wave(
                enemy=Jumper, spawn=random.randint(1, 4), amount=2, scaling=int(cls.level / 2))
        elif event_id == 3:
            Events.event_wave(
                enemy=Shooter, spawn=random.randint(1, 4), amount=2, scaling=int(cls.level / 8))
        elif event_id == 4:
            Events.event_wave(
                enemy=Seeker, spawn=random.randint(1, 4), amount=2, scaling=int(cls.level / 8))
        elif event_id == 5:
            Events.event_wave(
                enemy=Strafer, spawn=random.randint(1, 4), amount=3, scaling=int(cls.level / 8))
        elif event_id == 6:
            Events.event_wave(
                enemy=Mine_layer, spawn=random.randint(1, 4), amount=3, scaling=0)
        elif event_id == 7:
            Events.event_wave(
                enemy=Miner, spawn=random.randint(1, 4), amount=3, scaling=0)

    @classmethod
    def execute_special_event(cls):
        cls.special_events = True
        cls.special_event_queue.append(random.choice([
            Events.event_comet_storm
        ]))

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

        if not any((cls.boss_fight, cls.after_boss, cls.elite_fight, cls.special_events)):
            if timer.trigger(random.randint(cls.event_trigger_time[0], cls.event_trigger_time[1])):
                cls.execute_event(random.randint(1, 7))  # choices

        cls.elite_spawn()

        for event in cls.special_event_queue:
            if event():
                cls.special_event_queue.remove(event)

        if len(cls.special_event_queue) == 0:
            cls.special_events = False

        if cls.interval_score > cls.level_interval:
            cls.level += 1
            cls.display_level += 1
            cls.level_interval += 3
            cls.skill_points += 1
            cls.scaling()
            cls.interval_score = 0


data.LEVELS = Levels


class Events():

    change_bg = True

    @classmethod
    def event_wave(cls, enemy=None, spawn=None, amount=None, scaling=None):
        for _ in range(amount + scaling):
            data.ENEMY_DATA.append(enemy(spawn=spawn))

    @classmethod
    def set_bg_color(cls):
        Background.bg_color_change(color=(20, 20, 0), speed=3)

    @classmethod
    @timer
    def event_comet_storm(cls, timer):
        if not timer.trigger(1200):
            cls.set_bg_color()
            if timer.trigger(25):
                data.ENEMY_PROJECTILE_DATA.append(Comet())
        else:
            # cls.change_bg = True
            return True


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
        self.bg_speed = Background.scroll_speed
        self.bg_move = Background.bg_move
        self.overdrive_count = data.TURRET.overdrive_count
        self.elite_sp_time = Levels.elite_max_spawn_time
        self.special_event_amount = Levels.special_event_amount

    def load_save(self):
        data.ENEMY_DATA.clear()
        data.ENEMY_PROJECTILE_DATA.clear()
        data.PLAYER_PROJECTILE_DATA.clear()
        data.PHENOMENON_DATA.clear()
        data.PLAYER_DATA.clear()
        data.ITEMS.dropped_lst.clear()

        Levels.after_boss = False
        Levels.interval_score = 0
        Levels.special_event_triggered = 0
        Levels.special_event_didnt_trigger = 0
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
        Background.scroll_speed = self.bg_speed
        Background.bg_move = self.bg_move
        data.TURRET.overdrive_count = self.overdrive_count
        Levels.elite_max_spawn_time = self.elite_sp_time
        Levels.special_event_amount = self.special_event_amount
        if self.boss_fight:
            Levels.boss_spawn()

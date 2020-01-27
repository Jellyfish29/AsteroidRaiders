import random
import pickle

from astraid_funcs import *
import astraid_data as data
from phenomenon import *
from enemys import *
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
    spez_event_trigger = 0
    # elite/Elites
    elite_wait = False
    elite_spawn_time = 0
    event_trigger_time = (3600, 5000)
    boss_fight = False
    after_boss = False
    elite_fight = False
    second_elite_chance = 100
    second_elite = False

    @classmethod
    def scaling(cls):
        data.ENEMY.health += 0.4
        data.ELITES.health += data.ELITES.health * 0.1
        cls.second_elite_chance -= 1.5
        if cls.level % 5 == 0:
            cls.enemy_amount += 1
        if cls.level % 5 == 0:
            cls.spez_add()
            data.BOSS.create(cls.level)
            cls.boss_fight = True
            gfx.Gfx.scroll_speed += 1
            gfx.Gfx.bg_move = False
            cls.save_game()

    @classmethod
    @timer
    def elite_spawn(cls, timer):
        if not any((cls.after_boss, cls.boss_fight)):
            if cls.level not in [i - 1 for i in range(5, 41, 5)]:
                if not cls.elite_wait:
                    cls.elite_spawn_time = 3600
                    cls.elite_wait = True
                if cls.elite_wait:
                    if timer.trigger(int(cls.elite_spawn_time)):
                        data.ELITES.spawn()
                        if cls.level > 10 and random.randint(0, 100) > cls.second_elite_chance:
                            cls.second_elite = True
                        cls.elite_wait = False
        if cls.second_elite:
            if timer.trigger(240):
                cls.second_elite = False
                data.ELITES.spawn()

    @classmethod
    def spez_add(cls):
        data.ENEMY.spez_spawn_time -= 15
        data.PHENOM.spawn_time -= 15
        if data.ENEMY.spez_spawn_time < 60:
            data.ENEMY.spez_spawn_time = 60
        if cls.level == 1:
            data.ENEMY.set_spawn_table(Seeker)
            data.ENEMY.set_spawn_table(Jumper)
            data.PHENOM.set_spawn_table(Planet)
            # data.PHENOM.set_spawn_table(Gravity_well)
        if cls.level == 5:
            data.ENEMY.set_spawn_table(Shooter)
            data.PHENOM.set_spawn_table(Gravity_well)
        elif cls.level == 10:
            data.ENEMY.set_spawn_table(Mine_layer)
            data.PHENOM.set_spawn_table(Repair_station)
        elif cls.level == 15:
            data.ENEMY.set_spawn_table(Strafer)
            data.PHENOM.set_spawn_table(Anti_gravity_well)
        elif cls.level == 20:
            # data.ENEMY.get_spawn_table().append(en.Miner)
            data.PHENOM.set_spawn_table(Nabulae_aoe_damage)
        elif cls.level == 25:
            data.PHENOM.set_spawn_table(Nebulae_fire_rate_plus)

    @classmethod
    def spez_event(cls, flag):
        cls.spez_event_trigger = 0
        if flag == "wave":
            for i in range(4 + int(cls.level / 2)):
                data.ENEMY_DATA.append(Asteroid())
        elif flag == "jumper":
            for i in range(2 + int(cls.level / 2)):
                data.ENEMY_DATA.append(Jumper())
        elif flag == "shooter":
            for i in range(2 + int(cls.level / 10)):
                data.ENEMY_DATA.append(Shooter())
        elif flag == "seeker":
            for i in range(2 + int(cls.level / 10)):
                data.ENEMY_DATA.append(Seeker())

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
                cls.spez_event_trigger = random.randint(1, 4)

        cls.elite_spawn()

        if cls.interval_score > cls.level_interval:
            cls.event_trigger_time = (cls.event_trigger_time[0] - 50, cls.event_trigger_time[1] - 75)
            cls.level += 1
            cls.display_level += 1
            cls.level_interval += 4
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
        self.elite_health = data.ELITES.health
        self.enemy_amount = Levels.enemy_amount
        self.second_elite_chance = Levels.second_elite_chance
        self.enemy_table = data.ENEMY.spez_spawn_table
        self.phenomenon_spawn_table = data.PHENOM.phenomenon_spawn_table
        self.bg_speed = gfx.Gfx.scroll_speed
        self.bg_move = gfx.Gfx.bg_move

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
        data.ELITES.health = self.elite_health
        Levels.enemy_amount = self.enemy_amount
        Levels.second_elite_chance = self.second_elite_chance
        data.ENEMY.spez_spawn_table = self.enemy_table
        data.PHENOM.phenomenon_spawn_table = self.phenomenon_spawn_table
        gfx.Gfx.scroll_speed = self.bg_speed
        gfx.Gfx.bg_move = self.bg_move
        if self.boss_fight:
            self.spawn_boss()

    def spawn_boss(self):
        data.BOSS.create(self.lvl)

import random
import pickle

from astraid_funcs import *
import astraid_data as data
from phenomenon import *
from enemys import *
from allies import *
from bosses_def import *
from ui import *
from Gfx import Gfx, Background
from items import Active_Items


class Levels:

    interval_score = 0
    display_score = 0
    display_level = 1
    level = 1
    level_interval = 35
    asteroid_enemy_amount = 2  # at Start
    extractor_enemy_amount = 2
    mining_ast_enemy_amount = 1
    skill_points = 0
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
    death_score_panalties = {0: 30, 6: 40, 12: 60, 18: 100,
                             24: 150, 30: 210, 36: 320, 42: 450}
    # Events
    event_trigger_time = (2700, 3700)
    special_event_queue = []
    special_events_lst = []
    events_disabled = False
    event_id = 0
    special_event_triggered = 0
    special_event_didnt_trigger = 0
    special_event_amount = 2

    @classmethod
    def scaling(cls):
        data.ENEMY.health += 0.3
        Elites.health += Elites.health * 0.1
        cls.event_trigger_time = (cls.event_trigger_time[0] - 60, cls.event_trigger_time[1] - 75)

        if cls.event_trigger_time[0] <= 200:
            cls.event_trigger_time = (200, 500)

        cls.second_elite_chance -= 1.5
        if cls.second_elite_chance < 40:
            cls.second_elite_chance = 40

        if cls.level % 12 == 0:
            cls.asteroid_enemy_amount += 1
            cls.mining_ast_enemy_amount += 1

        if cls.level % 6 == 0:
            cls.extractor_enemy_amount += 1
            # cls.elite_max_spawn_time -= 80
            cls.spez_add()
            cls.boss_spawn()
            cls.special_events_lst = [e[0] for e in data.EVENTS.get_special_events_lst() if e[1] == cls.level]
            cls.boss_fight = True
            Background.bg_move = False
            cls.special_event_triggered = 0
            cls.special_event_didnt_trigger = 0
            cls.save_game()
            Gui.add(Gui_tw_text(text=data.BOSS_TEXT[str(cls.level)], text_size=20,
                                anchor=data.PLAYER.hitbox, anchor_x=80))
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
        if not any((cls.after_boss, cls.boss_fight, cls.special_events)):
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
                # Elites.spawn()

    @classmethod
    def boss_spawn(cls):
        for enemy in data.ENEMY_DATA:
            if rect_not_on_sreen(enemy.hitbox, strict=True):
                enemy.kill = True

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
            data.ENEMY.set_spawn_table(Jumper)
        #     data.ENEMY.set_spawn_table(Shooter)
        #     data.ENEMY.set_spawn_table(Mine_layer)
        #     data.ENEMY.set_spawn_table(Strafer)
        #     data.ENEMY.set_spawn_table(Miner)
        if cls.level == 6:
            data.ENEMY.set_spawn_table(Seeker)
        elif cls.level == 12:
            data.ENEMY.set_spawn_table(Shooter)
        elif cls.level == 18:
            data.ENEMY.set_spawn_table(Strafer)
        elif cls.level == 24:
            data.ENEMY.set_spawn_table(Mine_layer)
        elif cls.level == 30:
            data.ENEMY.set_spawn_table(Miner)
            pass
        elif cls.level == 36:
            pass

    @classmethod
    def execute_event(cls, event_id):
        if event_id == 1:
            data.EVENTS.event_wave(
                enemy=Asteroid, spawn=random.randint(1, 4), amount=4, scaling=int(cls.level / 2))
        elif event_id == 2:
            data.EVENTS.event_wave(
                enemy=Jumper, spawn=random.randint(1, 4), amount=2, scaling=int(cls.level / 4))
        elif event_id == 3:
            data.EVENTS.event_wave(
                enemy=Shooter, spawn=random.randint(1, 4), amount=2, scaling=0)
        elif event_id == 4:
            data.EVENTS.event_wave(
                enemy=Seeker, spawn=random.randint(1, 4), amount=2, scaling=int(cls.level / 8))
        elif event_id == 5:
            data.EVENTS.event_wave(
                enemy=Strafer, spawn=random.randint(1, 4), amount=2, scaling=0)
        elif event_id == 6:
            data.EVENTS.event_wave(
                enemy=Mine_layer, spawn=random.randint(1, 4), amount=3, scaling=0)
        elif event_id == 7:
            data.EVENTS.event_wave(
                enemy=Miner, spawn=random.randint(1, 4), amount=2, scaling=0)

    @classmethod
    def execute_special_event(cls):
        for enemy in data.ENEMY_DATA:
            if rect_not_on_sreen(enemy.hitbox, strict=True):
                enemy.kill = True

        cls.special_events = True
        cls.special_event_queue.append(
            cls.special_events_lst.pop(random.randint(0, len(cls.special_events_lst) - 1)))

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
            if event() == "stop_event":
                cls.special_event_queue.remove(event)
                cls.special_events = False

        if len(cls.special_event_queue) == 0:
            cls.special_events = False

        if cls.special_events:
            cls.interval_score = 0

        if cls.interval_score > cls.level_interval:
            cls.level += 1
            cls.display_level += 1
            cls.level_interval += 3
            cls.scaling()
            cls.interval_score = 0


data.LEVELS = Levels


class STAGE_SAVE():

    def __init__(self):
        for _, item in data.ITEMS.inventory_dic.items():
            if item is not None:
                item.end_effect()
        self.items = data.ITEMS.inventory_dic
        self.pl_health = data.PLAYER.health
        self.pl_max_health = data.PLAYER.max_health
        self.pl_heal_amount = data.PLAYER.heal_amount
        self.pl_raw_health = data.PLAYER.raw_max_health
        self.skill_points = Levels.skill_points
        self.upgrade_points = data.ITEMS.upgrade_points
        self.pl_angles = data.PLAYER.angles
        self.pl_raw_speed = data.PLAYER.raw_speed
        self.pl_dmg = data.PLAYER.damage
        self.pl_raw_crit = data.PLAYER.raw_crit_chance
        self.pl_raw_fire_rate = data.TURRET.raw_fire_rate
        self.pl_jump = data.PLAYER.jumpdrive
        self.pl_shield = data.PLAYER.shield
        self.lvl = Levels.level
        self.display_level = Levels.display_level
        self.score = Levels.display_score
        self.interval_score = Levels.level_interval
        self.boss_fight = Levels.boss_fight
        self.enemy_health = data.ENEMY.health
        self.elite_health = Elites.health
        self.asteroid_enemy_amount = Levels.asteroid_enemy_amount
        self.extractor_enemy_amount = Levels.extractor_enemy_amount
        self.mining_ast_enemy_amount = Levels.mining_ast_enemy_amount
        self.second_elite_chance = Levels.second_elite_chance
        self.enemy_table = data.ENEMY.spez_spawn_table
        self.phenomenon_spawn_table = data.PHENOM.phenomenon_spawn_table
        self.bg_speed = Background.scroll_speed
        self.bg_move = Background.bg_move
        self.overdrive_count = data.TURRET.overdrive_count
        self.elite_sp_time = Levels.elite_max_spawn_time
        self.special_event_amount = Levels.special_event_amount
        self.raw_cd = Active_Items.raw_cd_reduction

    def load_save(self):
        Levels.level = self.lvl
        data.ENEMY_DATA.clear()
        data.ENEMY_PROJECTILE_DATA.clear()
        data.PLAYER_PROJECTILE_DATA.clear()
        data.PHENOMENON_DATA.clear()
        data.PLAYER_DATA.clear()
        data.ITEMS.dropped_lst.clear()
        data.ITEMS.active_flag_lst.clear()
        data.GUI_DATA.clear()
        Levels.special_events_lst.clear()
        Levels.special_event_queue.clear()
        data.EVENTS.all_reset()
        data.PLAYER.indicator_slots = {i: None for i in range(4)}
        Levels.special_events_lst = [e[0] for e in data.EVENTS.get_special_events_lst() if e[1] == Levels.level]

        Levels.after_boss = False
        Levels.special_events = False
        Levels.interval_score = 0
        Levels.special_event_triggered = 0
        Levels.special_event_didnt_trigger = 0
        Levels.display_level = self.display_level
        Levels.display_score = self.score
        Levels.level_interval = self.interval_score
        data.ITEMS.inventory_dic = self.items
        data.PLAYER.health = self.pl_health
        data.PLAYER.heal_amount = self.pl_heal_amount
        data.PLAYER.raw_max_health = self.pl_raw_health
        data.PLAYER.hitbox.center = (1000, 900)
        Levels.skill_points = self.skill_points
        data.ITEMS.upgrade_points = self.upgrade_points
        data.PLAYER.angles = self.pl_angles
        data.PLAYER.raw_speed = self.pl_raw_speed
        data.PLAYER.damage = self.pl_dmg
        data.PLAYER.raw_crit_chance = self.pl_raw_crit
        data.TURRET.raw_fire_rate = self.pl_raw_fire_rate
        data.PLAYER.jumpdrive = self.pl_jump
        data.PLAYER.shield = self.pl_shield
        Levels.boss_fight = self.boss_fight
        data.ENEMY.health = self.enemy_health
        Elites.health = self.elite_health
        Levels.asteroid_enemy_amount = self.asteroid_enemy_amount
        Levels.extractor_enemy_amount = self.extractor_enemy_amount
        Levels.mining_ast_enemy_amount = self.mining_ast_enemy_amount
        Levels.second_elite_chance = self.second_elite_chance
        data.ENEMY.spez_spawn_table = self.enemy_table
        data.PHENOM.phenomenon_spawn_table = self.phenomenon_spawn_table
        Background.scroll_speed = self.bg_speed
        Background.bg_move = self.bg_move
        data.TURRET.overdrive_count = self.overdrive_count
        Levels.elite_max_spawn_time = self.elite_sp_time
        Levels.special_event_amount = self.special_event_amount

        data.PLAYER.set_player_speed(0)
        data.PLAYER.set_player_health(0)
        data.PLAYER.set_player_crit_chance(0)
        data.TURRET.set_fire_rate(0)
        data.ACTIVE_ITEMS.set_cd_reduction(0)

        data.UP_MENU.reset_item_bar()

        if self.boss_fight:
            Levels.boss_spawn()

    # @classmethod
    # def execute_special_event(cls):
    #     cls.special_events = True
    #     if len(cls.special_events_lst) == 0:
    #         cls.special_events_lst = [e[0] for e in data.EVENTS.get_special_events_lst() if e[1] < csl.level]
    #         data.EVENTS.get_special_events_lst().copy()

    #     event = cls.special_events_lst[random.randint(0, len(cls.special_events_lst) - 1)]
    #     if event[1] < cls.level:
    #         cls.special_events_lst.remove(event)
    #         cls.special_event_queue.append(event[0])
    #     else:
    #         for i in range(len(cls.special_events_lst)):
    #             event = cls.special_events_lst[random.randint(0, len(cls.special_events_lst) - 1)]
    #             if event[1] < cls.level:
    #                 cls.special_events_lst.remove(event)
    #                 cls.special_event_queue.append(event[0])
    #                 break
    #         else:
    #             cls.special_events_lst. += data.EVENTS.get_special_events_lst()
    #             cls.execute_special_event()

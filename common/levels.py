import random
import pickle
# import pygame

from astraid_funcs import *
import astraid_data as data
from phenomenon import *
from enemys import *
from allies import *
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
    special_events_lst = []
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
            cls.special_event_amount += 1
            if cls.special_event_amount > 5:
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

            # data.ENEMY.set_spawn_table(Comet)
            # data.ENEMY.set_spawn_table(Shooter)
            # data.ENEMY.set_spawn_table(Mine_layer)
            # data.ENEMY.set_spawn_table(Strafer)
            # data.ENEMY.set_spawn_table(Miner)
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
        if len(cls.special_events_lst) == 0:
            cls.special_events_lst = special_events_lst.copy()
        cls.special_event_queue.append(cls.special_events_lst.pop(
            random.randint(0, len(cls.special_events_lst) - 1)))

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

        if cls.special_events:
            cls.interval_score = 0

        if cls.interval_score > cls.level_interval:
            cls.level += 1
            cls.display_level += 1
            cls.level_interval += 3
            cls.skill_points += 1
            cls.scaling()
            cls.interval_score = 0


data.LEVELS = Levels


class Events():

    # Convoy escort
    convoy_set_up = True
    convoy_amount = (i for i in range(3))
    convoy_ship_amount = (i for i in range(4))
    convoy_points = 0
    # Convoy attack

    # Station hack

    # Minefield
    mine_field_set_up = True
    mine_amount = 8
    mine_field_stage = 0
    mine_field_max_stages = 5

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

    @classmethod
    @timer
    def event_convoy_escort(cls, timer):
        cls.set_bg_color()

        if cls.convoy_set_up:
            cls.station_dest = (200, random.randint(400, 800))
            data.PLAYER_DATA.append(Space_station_allie(spawn_point=(200, -100), target=cls.station_dest))
            cls.convoy_set_up = False

        if not Background.bg_move:
            if timer.trigger(300):
                event_id = random.choice([3, 5, 6])
                Levels.execute_event(event_id)
            if timer.trigger(60):
                if next(cls.convoy_ship_amount, "stop") != "stop":
                    data.PLAYER_DATA.append(Convoy_ship_allie(
                        spawn_point=(2000, random.randint(200, 800)),
                        target=cls.station_dest
                    ))

            if timer.trigger(1200):
                wave = next(cls.convoy_amount, "stop")
                if wave != "stop":
                    cls.convoy_ship_amount = (i for i in range(4))
                if wave == 2:
                    Elites.spawn()

            if timer.timer_key_delay(limit=3600, key="end"):
                if len([s for s in data.PLAYER_DATA if isinstance(s, Convoy_ship_allie)]) == 0:
                    cls.convoy_set_up = True
                    # timer.timer_key_delay(reset=True, key="end")
                    timer.timer_reset()
                    return True

    @classmethod
    @timer
    def event_convoy_atack(cls, timer):
        pass

    @classmethod
    @timer
    def event_station_hack(cls, timer):
        pass

    @classmethod
    @timer
    def event_mine_field(cls, timer):
        cls.set_bg_color()
        if cls.mine_field_set_up:
            data.PLAYER.jumpdrive_disabled = True
            cls.spawn_mine_field()
            cls.mine_field_set_up = False
        if timer.trigger(400):
            Background.bg_move = False
        if not Background.bg_move:
            if data.PLAYER.hitbox.colliderect(pygame.Rect(0, -10, winwidth, 15)):
                data.PLAYER.hitbox.center = (data.PLAYER.hitbox.center[0], winheight)

                data.ENEMY_PROJECTILE_DATA.clear()
                data.PHENOMENON_DATA.clear()
                data.ITEMS.dropped_lst.clear()

                cls.mine_field_stage += 1
                cls.mine_amount += 1

                if cls.mine_field_stage == cls.mine_field_max_stages - 1:
                    sp = get_random_point()
                    random.choice([
                        lambda: data.ITEMS.drop(
                            sp, target=Item_supply_crate((100, 100, 100), level=3)),
                        lambda: data.ITEMS.drop(
                            sp, target=Item_heal_crate((100, 100, 100), level=3)),
                        lambda: data.ITEMS.drop(
                            sp, target=Item_upgrade_point_crate((100, 100, 100), level=3))
                    ])()

                if cls.mine_field_stage >= cls.mine_field_max_stages:
                    Background.bg_move = True
                    Background.y += 1080
                    cls.mine_amount = 10
                    cls.mine_field_stage = 0
                    cls.mine_field_set_up = True
                    data.PLAYER.jumpdrive_disabled = False

                    return True

                else:
                    cls.spawn_mine_field(start=False)

    @classmethod
    def spawn_mine_field(cls, start=True):
        mine_amount = (i for i in range(cls.mine_amount))
        t = next(mine_amount, "stop")
        while t != "stop":
            if start:
                y_cord = random.randint(-600, -200)
                x_cord = random.randint(-100, winwidth + 100)
            else:
                y_cord = random.randint(-200, 700)
                x_cord = random.randint(-100, winwidth + 100)
            t = next(mine_amount, "stop")
            data.ENEMY_PROJECTILE_DATA.append(Mine(
                speed=30,
                start_point=(x_cord, y_cord),
                damage=2,
                flag="neutral",
                oob_check=False,
                moving=True,
                fuse_delay=0
            ))


data.EVENTS = Events

special_events_lst = [
    Events.event_convoy_escort,
    Events.event_comet_storm,
    Events.event_mine_field
]


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
        self.special_events_lst = Levels.special_events_lst

    def load_save(self):
        data.ENEMY_DATA.clear()
        data.ENEMY_PROJECTILE_DATA.clear()
        data.PLAYER_PROJECTILE_DATA.clear()
        data.PHENOMENON_DATA.clear()
        data.PLAYER_DATA.clear()
        data.ITEMS.dropped_lst.clear()

        Levels.after_boss = False
        Levels.special_events = False
        Levels.special_event_queue.clear()
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
        Levels.special_events_lst = self.special_events_lst
        if self.boss_fight:
            Levels.boss_spawn()

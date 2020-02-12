from init import *

from astraid_funcs import *
import astraid_data as data
from phenomenon import *
from enemys import *
from allies import *
from bosses_def import Elites
from Gfx import Gfx, Background


class Events():

    special_events_lst = []
    # Comet Storm
    comet_storm_set_up = True
    # Minefield
    mine_field_set_up = True
    mine_amount = 8
    mine_field_stage = 0
    mine_field_max_stages = 5
    # Convoy escort
    convoy_set_up = True
    convoy_wave = 0
    convoy_wave_amount = 4
    convoy_ship_amount = (i for i in range(4))
    convoy_points = 0
    # Battleship defence
    battleship_defence_set_up = True
    bs_defence_bs_disabled = True
    bs_heals = 0
    bs_defence_wave_trigger = 700
    bs_defence_wave_strength = 2
    bs_defence_wave_counter = 0
    # Convoy attack
    convoy_attack_set_up = True
    convoy_attack_ship_amount = 6
    convoy_attack_c_length = (i for i in range(convoy_attack_ship_amount))
    convoy_attack_wave_amount = 5
    convoy_attack_wave_counter = 0
    convoy_attack_c_destroyed = 0

    # Station hack

    @classmethod
    def event_wave(cls, enemy=None, spawn=None, amount=None, scaling=None):
        for _ in range(amount + scaling):
            data.ENEMY_DATA.append(enemy(spawn=spawn))

    @classmethod
    @timer
    def event_comet_storm(cls, timer):
        if cls.comet_storm_set_up:
            data.PHENOMENON_DATA.append(Planet())
            cls.comet_storm_set_up = False
        if not timer.trigger(1400):
            cls.set_bg_color()
            if timer.trigger(17):
                data.ENEMY_PROJECTILE_DATA.append(Comet())
        else:
            cls.comet_storm_set_up = True
            data.ITEMS.drop(
                (1000, 400), target=Item_supply_crate((100, 100, 100), level=random.randint(0, 1)))
            return "stop_event"

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

                Background.bg_objs.clear()
                Background.y += 1080
                Background.bg_objs.append(Background(y=random.randint(100, 800)))

                # Destruction Effects >>>

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
                    cls.mine_field_reset()
                    data.PLAYER.jumpdrive_disabled = False

                    return "stop_event"

                else:
                    cls.spawn_mine_field(start=False)

    @classmethod
    def mine_field_reset(cls):
        cls.mine_field_set_up = True
        cls.mine_amount = 8
        cls.mine_field_stage = 0

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

    @classmethod
    @timer
    def event_convoy_escort(cls, timer):
        cls.set_bg_color()

        if cls.convoy_set_up:
            cls.station_dest = (250, random.randint(400, 700))
            data.PLAYER_DATA.append(Space_station_allie(spawn_point=(200, -200), target=cls.station_dest))
            cls.convoy_set_up = False

        if not Background.bg_move:
            if timer.trigger(260):
                event_id = random.choice([3, 5, 6])
                data.LEVELS.execute_event(event_id)
            if timer.trigger(60):
                if next(cls.convoy_ship_amount, "stop") != "stop":
                    data.PLAYER_DATA.append(Convoy_ship_allie(
                        spawn_point=(2000, random.randint(200, 800)),
                        target=cls.station_dest
                    ))

            if timer.trigger(1200):
                cls.convoy_wave += 1
                if cls.convoy_wave <= cls.convoy_wave_amount:
                    cls.convoy_ship_amount = (i for i in range(4))
                if cls.convoy_wave == 3:
                    Elites.spawn()
                # wave = next(cls.convoy_wave_amount, "stop")
                # if wave != "stop":
                #     cls.convoy_ship_amount = (i for i in range(4))
                # if wave == 1:
                #     Elites.spawn()

            if cls.convoy_wave >= cls.convoy_wave_amount:
                if len([s for s in data.PLAYER_DATA if isinstance(s, Convoy_ship_allie)]) == 0:
                    cls.convoy_escort_reset()
                    timer.timer_reset()

                    return "stop_event"

    @classmethod
    def convoy_escort_reset(cls):
        cls.convoy_set_up = True
        cls.convoy_wave = 0
        cls.convoy_wave_amount = 4
        cls.convoy_ship_amount = (i for i in range(4))

    @classmethod
    @timer
    def event_battleship_defence(cls, timer):
        cls.set_bg_color()
        if cls.battleship_defence_set_up:
            cls.bs_dest = (950, 400)
            data.PLAYER_DATA.append(Battleship_allie(spawn_point=(950, -200), target=cls.bs_dest))
            for _ in range(cls.bs_defence_wave_strength):
                data.ENEMY_DATA.append(Event_shooter(get_random_point(), spawn=1))
            timer.ticker.update({"wave_timer": 600})
            cls.battleship_defence_set_up = False

        if not Background.bg_move:
            if cls.bs_defence_bs_disabled:
                if timer.timer_key_trigger(cls.bs_defence_wave_trigger, key="wave_timer"):
                    spawn = random.randint(1, 4)
                    for _ in range(cls.bs_defence_wave_strength):
                        data.ENEMY_DATA.append(Event_shooter(get_random_point(), spawn=spawn))
                    cls.bs_defence_wave_trigger -= 60
                    cls.bs_defence_wave_counter += 1
                    cls.bs_defence_wave_strength += 1
                    if cls.bs_defence_wave_counter == 4:
                        Elites.spawn()

                if timer.trigger(1000):
                    data.LEVELS.execute_event(5)

                if cls.bs_defence_wave_counter == 5:
                    cls.bs_defence_bs_disabled = False

        else:
            if len(data.PLAYER_DATA) == 0:
                cls.bs_defence_reset()
                for enemy in [e for e in data.ENEMY_DATA if e.get_name() == "Event_shooter"]:
                    enemy.reset()

                return "stop_event"

    @classmethod
    def bs_defence_reset(cls):
        cls.battleship_defence_set_up = True
        cls.bs_defence_bs_disabled = True
        cls.bs_defence_wave_trigger = 700
        cls.bs_defence_wave_strength = 2
        cls.bs_defence_wave_counter = 0

    @classmethod
    def set_bg_color(cls):
        Background.bg_color_change(color=(20, 20, 0), speed=3)

    @classmethod
    @timer
    def event_convoy_atack(cls, timer):
        cls.set_bg_color()
        if cls.convoy_attack_set_up:
            Background.bg_move = False
            timer.ticker["c_spawn"] = 380
            cls.c_a_ship = next(cls.convoy_attack_c_length, "stop")
            cls.c_a_y = random.randint(300, 800)
            cls.convoy_attack_set_up = False
        if timer.timer_key_delay(limit=400, key="c_spawn"):
            if cls.c_a_ship != "stop":
                if timer.trigger(60):
                    cls.c_a_ship = next(cls.convoy_attack_c_length, "stop")
                    data.ENEMY_DATA.append(Convoy_ship_enemy(cls.c_a_y))
            else:
                if cls.convoy_attack_wave_counter < cls.convoy_attack_wave_amount:
                    cls.convoy_attack_wave_counter += 1
                    cls.convoy_attack_ship_amount += 1
                    cls.convoy_attack_c_length = (i for i in range(cls.convoy_attack_ship_amount))
                    cls.c_a_ship = next(cls.convoy_attack_c_length, "stop")
                    cls.c_a_y = random.randint(300, 800)
                    timer.timer_key_delay(reset=True, key="c_spawn")
                else:
                    if timer.trigger(240):
                        cls.convoy_attack_reset()
                        Background.bg_move = True

                        return "stop_event"

    @classmethod
    def convoy_attack_reset(cls):
        cls.convoy_attack_set_up = True
        cls.convoy_attack_ship_amount = 6
        cls.convoy_attack_c_length = (i for i in range(cls.convoy_attack_ship_amount))
        cls.convoy_attack_wave_amount = 5
        cls.convoy_attack_wave_counter = 0
        cls.convoy_attack_c_destroyed = 0

    @classmethod
    @timer
    def event_station_hack(cls, timer):
        pass

    @classmethod
    def get_special_events_lst(cls):
        return [
            # (cls.event_comet_storm, 0),
            # (cls.event_mine_field, 0),
            (cls.event_convoy_escort, 0),
            # (cls.event_battleship_defence, 0),
            # (cls.event_convoy_atack, 0),
        ]


data.EVENTS = Events

from init import *

from astraid_funcs import *
import astraid_data as data
from phenomenon import *
from enemys import *
from allies import *
from bosses_def import Elites
from Gfx import Gfx, Background
from items_misc import Item_supply_crate, Item_heal_crate, Item_upgrade_point_crate
from ui import *


class Events():

    special_events_lst = []
    # Intro Event
    intro_set_up = True
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
    hack_set_up = True
    hack_stations_hacked = 0
    # Zone defence
    z_def_set_up = True
    z_def_bc_destroyed = False
    z_def_active_zones = []

    @classmethod
    def intro_event(cls):
        if cls.intro_set_up:
            starting_station = Docile_allied_station(spawn_point=(400, 200))
            data.PLAYER_DATA.append(starting_station)

            Gui.add(Gui_tw_text(text=data.EVENT_TEXT["intro"], anchor=starting_station.hitbox, anchor_x=100))
            Background.bg_move = False
            cls.intro_set_up = False

        if len(data.GUI_DATA) == 0:
            Gui.add(Gui_text(loc=(800, 40), flag="intro_1", text="BEGINN MISSION"))
            Gui.add(Gui_image(loc=(700, 20), flag="intro_1", img_idx=11, animation_interval=60))
            Gui.add(Gui_image(loc=(1060, 20), flag="intro_1", img_idx=11, animation_interval=60))

        if data.PLAYER.hitbox.colliderect(pygame.Rect(0, -10, winwidth, 15)):
            data.PLAYER.hitbox.center = (data.PLAYER.hitbox.center[0], winheight)

            data.PLAYER_DATA.clear()
            data.GUI_DATA.clear()

            Background.y += 1080
            Background.bg_objs.append(Background(y=random.randint(100, 800)))

            # Gui.delete("intro_1")
            Background.bg_move = True

            return "stop_event"

    @classmethod
    def event_wave(cls, enemy=None, spawn=None, amount=None, scaling=None):
        for _ in range(amount + scaling):
            data.ENEMY_DATA.append(enemy(spawn=spawn))

    @classmethod
    @timer
    def event_comet_storm(cls, timer):
        if cls.comet_storm_set_up:
            data.GUI_DATA.append(Gui_text(loc=(600, 100), text=data.EVENT_TEXT["comet_alert"],
                                          text_size=50, decay=400, animation_interval=60))
            cls.comet_storm_set_up = False
        cls.set_bg_color()
        if timer.timer_delay(120):
            if timer.timer_trigger_delay(1100):
                Background.add(loc=(1000, -100), gfx_idx=random.randint(15, 17))

            if not timer.trigger(1400):
                if timer.trigger(17):
                    data.ENEMY_PROJECTILE_DATA.append(Comet())
                if timer.trigger(60):
                    data.ENEMY_PROJECTILE_DATA.append(Comet(special=True))
            else:
                cls.comet_storm_set_up = True
                timer.timer_reset()
                data.ITEMS.drop(
                    (1080, 340), target=Item_supply_crate((100, 100, 100), level=1))

                return "stop_event"

    @classmethod
    @timer
    def event_mine_field(cls, timer):
        cls.set_bg_color()
        if cls.mine_field_set_up:
            data.PLAYER.jumpdrive_disabled = True
            cls.spawn_mine_field()
            Gui.add(Gui_text(loc=(500, 100), text=data.EVENT_TEXT["mine_alert"],
                             text_size=50, decay=360, animation_interval=60))
            cls.mine_field_set_up = False
        if timer.timer_trigger_delay(100):
            Gui.add(Gui_tw_text(text=data.EVENT_TEXT["mine_info_1"], text_size=20, anchor=data.PLAYER.hitbox, anchor_x=80))
        if timer.timer_trigger_delay(400):
            Gui.add(Gui_text(loc=(800, 40), flag="mine_1", text=data.EVENT_TEXT["mine_info_2"],
                             text_size=30, animation_interval=60))
            Gui.add(Gui_text(loc=(970, 980), flag="mine_2", text=data.EVENT_TEXT["mine_info_3"],
                             text_size=25, animation_interval=60))
            Gui.add(Gui_image(loc=(700, 20), flag="mine_1", img_idx=11, animation_interval=60))
            Gui.add(Gui_image(loc=(1320, 20), flag="mine_1", img_idx=11, animation_interval=60))
            Background.bg_move = False

        if not Background.bg_move:
            if data.PLAYER.hitbox.colliderect(pygame.Rect(0, -10, winwidth, 15)):
                data.PLAYER.hitbox.center = (data.PLAYER.hitbox.center[0], winheight)

                # Reset the Scene
                data.ENEMY_PROJECTILE_DATA.clear()
                data.ENEMY_DATA.clear()
                data.PHENOMENON_DATA.clear()
                data.ITEMS.dropped_lst.clear()
                Gfx.gfx_layer_1_lst.clear()
                Background.bg_objs.clear()
                Gui.delete("mine_1")
                Background.y += 1080
                Background.add()
                # Background.bg_objs.append(Background(y=random.randint(100, 800)))

                cls.mine_field_stage += 1
                cls.mine_amount += 1

                if cls.mine_field_stage >= cls.mine_field_max_stages:
                    Background.bg_move = True
                    Background.y += 1080
                    timer.timer_reset()
                    cls.mine_field_reset()
                    data.PLAYER.jumpdrive_disabled = False

                    return "stop_event"
                else:
                    sp = get_random_point()
                    Background.add(loc=(sp[0] - 30, sp[1] - 30), gfx_idx=random.randint(15, 17))
                    random.choice([
                        lambda: data.ITEMS.drop(
                            sp, target=Item_supply_crate((100, 100, 100), level=0)),
                        lambda: data.ITEMS.drop(
                            sp, target=Item_upgrade_point_crate((100, 100, 100), level=0))
                    ])()
                    cls.spawn_mine_field(start=False)

    @classmethod
    def mine_field_reset(cls):
        cls.mine_field_set_up = True
        cls.mine_amount = 8
        cls.mine_field_stage = 0
        Gui.delete("mine_2")

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
            Gui.add(Gui_tw_text(text=data.EVENT_TEXT["convoy_e_intro"], text_size=20, anchor=data.PLAYER.hitbox, anchor_x=80))
            cls.convoy_set_up = False

        if not Background.bg_move:
            # Gui Text
            if timer.timer_trigger_delay(5):
                Gui.add(Gui_tw_text(text=data.EVENT_TEXT["convoy_e_info"],
                                    anchor=data.PLAYER_DATA[0].hitbox, anchor_x=100))
                Gui.add(Gui_text(flag="convoy_count", text=lambda: f"SHIPS {cls.convoy_points}/16", text_size=15,
                                 anchor=data.PLAYER_DATA[0].hitbox, anchor_x=0, anchor_y=-65))

            if timer.trigger(260):
                for a in data.PLAYER_DATA[1:]:
                    if a.health < a.max_health:
                        Gui.add(Gui_tw_text(text=random.choice(data.EVENT_TEXT["convoy_e_shatter"]),
                                            text_size=20, anchor=a.hitbox, anchor_x=15))
            # Event Script
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
                    Elites.spawn(drop=False)

            if cls.convoy_wave >= cls.convoy_wave_amount:
                if len([s for s in data.PLAYER_DATA if isinstance(s, Convoy_ship_allie)]) == 0:
                    Gui.add(Gui_tw_text(text=data.EVENT_TEXT["convoy_e_end"],
                                        anchor=data.PLAYER_DATA[0].hitbox, anchor_x=90))
                    Gui.delete("convoy_count")
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
                data.ENEMY_DATA.append(Event_shooter(get_random_point(), standart_spawn=1))
            timer.ticker.update({"wave_timer": 400})
            Gui.add(Gui_tw_text(text=data.EVENT_TEXT["btl_defence_intro"], text_size=20, anchor=data.PLAYER.hitbox, anchor_x=80))
            cls.battleship_defence_set_up = False

        if not Background.bg_move:
            if timer.timer_trigger_delay(0):
                Gui.add(Gui_tw_text(text=data.EVENT_TEXT["btl_defence_info"],
                                    anchor=data.PLAYER_DATA[0].hitbox, anchor_y=-50, anchor_x=210))
                Gui.add(Gui_text(flag="btl_defence", text=lambda: f"Repair Progress: {int((cls.bs_defence_wave_counter / 5) * 100)}%", text_size=15,
                                 anchor=data.PLAYER_DATA[0].hitbox, anchor_x=15, anchor_y=-100))

            if cls.bs_defence_bs_disabled:
                if timer.timer_key_trigger(cls.bs_defence_wave_trigger, key="wave_timer"):
                    spawn = random.randint(1, 4)
                    for _ in range(cls.bs_defence_wave_strength):
                        data.ENEMY_DATA.append(Event_shooter(get_random_point(), standart_spawn=spawn))
                    cls.bs_defence_wave_trigger -= 65
                    cls.bs_defence_wave_counter += 1
                    cls.bs_defence_wave_strength += 1
                    if cls.bs_defence_wave_counter == 4:
                        Elites.spawn(drop=False)

                if timer.trigger(1000):
                    data.LEVELS.execute_event(5)

                if cls.bs_defence_wave_counter == 5:
                    Gui.delete("btl_defence")
                    Gui.add(Gui_tw_text(text=data.EVENT_TEXT["btl_defence_end"],
                                        anchor=data.PLAYER_DATA[0].hitbox, anchor_y=0, anchor_x=210))
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
    def event_convoy_attack(cls, timer):
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
                    if not isinstance(cls.c_a_ship, str):
                        if cls.c_a_ship % 4 == 0:
                            for i in [150, -150]:
                                data.ENEMY_DATA.append(Event_shooter(
                                    (-200, cls.c_a_y + i), special_spawn=(2000, cls.c_a_y + i), border_check=True))
            else:
                if cls.convoy_attack_wave_counter < cls.convoy_attack_wave_amount:
                    cls.convoy_attack_wave_counter += 1
                    cls.convoy_attack_ship_amount += 1
                    cls.convoy_attack_c_length = (i for i in range(cls.convoy_attack_ship_amount))
                    cls.c_a_ship = next(cls.convoy_attack_c_length, "stop")
                    cls.c_a_y = random.randint(300, 800)
                    timer.timer_key_delay(reset=True, key="c_spawn")
                    if any([cls.convoy_attack_wave_counter == 4,
                            cls.convoy_attack_wave_counter == 5]):
                        Elites.spawn(drop=False)
                else:
                    if timer.trigger(600):
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
        cls.set_bg_color()
        if cls.hack_set_up:
            for i in [-200, -300, -600, -450]:
                spawn = (random.randint(200, 1700), i)
                data.PLAYER_DATA.append(Comrelay(spawn_point=spawn))
                Elites.spawn(special_spawn=spawn)
            cls.hack_set_up = False

        if Background.bg_move:
            if any([a.dest_reached() for a in data.PLAYER_DATA if isinstance(a, Comrelay)]):
                Background.bg_move = False
                for elite in [e for e in data.ENEMY_DATA if isinstance(e, Elites)]:
                    elite.skills_lst.pop(1)
                    elite.special_move = False

        else:
            elite_amount = len([e for e in data.ENEMY_DATA if isinstance(e, Elites)])
            if elite_amount == 2:
                if timer.timer_key_trigger(400, key="wave_trigger"):
                    data.LEVELS.execute_event(random.choice([5, 3]))
            elif elite_amount == 1:
                if timer.timer_key_trigger(260, key="wave_trigger"):
                    data.LEVELS.execute_event(random.choice([5, 3]))
            elif elite_amount == 0:
                if timer.timer_key_trigger(160, key="wave_trigger"):
                    data.LEVELS.execute_event(random.choice([5, 3]))

            if cls.hack_stations_hacked == 4:
                data.ITEMS.drop((1000, 500), amount=1)
                data.ITEMS.drop(
                    ((1000, 500)), target=Item_heal_crate((100, 100, 100), level=2))
                data.ITEMS.drop(
                    ((1000, 500)), target=Item_supply_crate((100, 100, 100), level=1))
                Background.bg_move = True
                cls.hack_reset()

                return "stop_event"

            if timer.timer_key_delay(2700, key="hack_time_limit"):
                # INTERFACE
                if cls.hack_stations_hacked > 0:
                    data.ITEMS.drop(
                        ((1000, 500)), target=Item_heal_crate((100, 100, 100), level=2))
                    data.ITEMS.drop(
                        ((1000, 500)), target=Item_supply_crate((100, 100, 100), level=1))
                if cls.hack_stations_hacked == 3:
                    data.ITEMS.drop(
                        (1000, 500), target=Item_upgrade_point_crate((100, 100, 100), level=3))
                elif cls.hack_stations_hacked == 2:
                    data.ITEMS.drop(
                        (1000, 500), target=Item_upgrade_point_crate((100, 100, 100), level=2))

                Background.bg_move = True
                cls.hack_reset()

                return "stop_event"

    @classmethod
    def hack_reset(cls):
        cls.hack_set_up = True
        cls.hack_stations_hacked = 0

    @classmethod
    @timer
    def event_zone_defence(cls, timer):
        cls.set_bg_color()
        if cls.z_def_set_up:
            data.PLAYER_DATA.append(Battlecruiser_ally(spawn_point=(900, -250), target=(1000, 600)))
            timer.ticker.update({"elite_spawn": 450})
            cls.z_def_set_up = False
        if not Background.bg_move:
            if timer.timer_key_trigger(600, key="elite_spawn"):
                if len(cls.z_def_active_zones) == 0:
                    cls.z_def_active_zones = [z.loc for z in data.PHENOMENON_DATA if not z.captured]
                if len(cls.z_def_active_zones) > 0:
                    Elites.spawn(special_dest=(cls.z_def_active_zones.pop(random.randint(0, len(cls.z_def_active_zones) - 1))))

            if timer.trigger(1400):
                data.LEVELS.execute_event(7)

            if len([z for z in data.PHENOMENON_DATA if not z.captured]) == 0:
                cls.zone_defence_reset_elites()

                if len(data.PLAYER_DATA) == 0:
                    cls.end_zone_defence()

                    return "stop_event"

        if timer.trigger(7200):
            cls.zone_defence_reset_elites()
            cls.end_zone_defence()

            return "stop_event"

    @classmethod
    def zone_defence_reset_elites(cls):
        data.PHENOMENON_DATA.clear()
        for elite in [e for e in data.ENEMY_DATA if isinstance(e, Elites)]:
            if len(elite.checkpoints) == 1:
                elite.angles = angles_360(elite.speed)
                elite.checkpoints = elite.orig_checkpoints
                elite.move_pattern = [random.randint(0, 9) for _ in range(40)]

    @classmethod
    def end_zone_defence(cls):
        if not cls.z_def_bc_destroyed:
            data.ITEMS.drop(
                (1000, 500), target=Item_upgrade_point_crate((100, 100, 100), level=3))
            data.ITEMS.drop(
                (1000, 500), target=Item_supply_crate((100, 100, 100), level=3))
        cls.z_def_set_up = True
        cls.z_def_bc_destroyed = False
        cls.z_def_active_zones = []
        Background.bg_move = True

    @classmethod
    def get_special_events_lst(cls):
        return [
            (cls.event_comet_storm, 0),
            (cls.event_mine_field, 0),
            (cls.event_convoy_escort, 6),
            (cls.event_battleship_defence, 6),
            # (cls.event_convoy_attack, 12),
            # (cls.event_station_hack, 12),
            # (cls.event_zone_defence, 18),
        ]


data.EVENTS = Events

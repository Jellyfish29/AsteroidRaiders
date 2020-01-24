import pygame
import pickle
from pygame.locals import *

from init import *
from interface import *
from astraid_funcs import *
from player import *
from turret import *
from bosses import *
from Gfx import *
from levels import *
from power_ups import *
from blocker import *
from spez_enemy import *
from enemy import *
from items import *
from elites import *
"""
    Main game loop ,Movement Controls event handling, Savegame
"""


def test_mode():
    Player.max_health += 40000
    Player.health += 40000
    Player.damage += 100
    Power_ups.shield_amount += 100
    Power_ups.super_shot_amount += 100
    Power_ups.heal_amount += 100
    Power_ups.star_shot_amount += 100
    Levels.skill_points += 100
    Levels.level += 3
    Turret.pd_ammo += 1000
    Turret.nuke_ammo += 1000
    Turret.missile_ammo += 1000
    Player.jump_charges += 1000
    pygame.mouse.set_visible(True)


def save_game(obj):
    with open(os.path.join(os.getcwd()[:-7], f"save_games\\saves"), "wb") as file:
        pickle.dump(obj, file)


def load_game():
    with open(os.path.join(os.getcwd()[:-7], f"save_games\\saves"), "rb") as file:
        return pickle.load(file)


class Game_state:

    def __init__(self):
        self.max_health = Player.max_health
        self.health = Player.health
        self.shield_amount = Power_ups.shield_amount
        self.super_shot_amount = Power_ups.super_shot_amount
        self.heal_amount = Power_ups.heal_amount
        self.star_shot_amount = Power_ups.star_shot_amount
        self.skill_points = Levels.skill_points
        self.level = Levels.level
        self.pd_ammo = Turret.pd_ammo
        self.nuke_ammo = Turret.nuke_ammo
        self.missile_ammo = Turret.missile_ammo
        self.jump_charges = Player.jump_charges
        self.skill_points = Levels.skill_points
        self.player_damage = Player.damage
        self.fire_rate = Turret.fire_rate
        self.star_shot_tubes = Power_ups.star_shot_tubes
        self.shield_time = Power_ups.shield_time
        self.speed = Player.speed
        self.normal_fire_rate = Turret.normal_fire_rate
        self.pd_reload_speed = Turret.pd_reload_speed
        self.missile_reload_speed = Turret.missile_reload_speed
        self.nuke_reload_speed = Turret.nuke_reload_speed
        self.jump_recharge_rate = Player.jump_recharge_rate
        self.enemy_health = Enemy.health
        self.spez_health = Spez_enemy.health
        self.display_score = Levels.display_score
        self.enemy_amount = Levels.enemy_amount
        self.boss_fight = Levels.boss_fight
        self.level = Levels.level
        self.display_level = Levels.display_level
        self.level_interval = Levels.level_interval
        self.interval = Power_ups.interval
        self.boss_amount = Levels.boss_amount
        self.blocker_amount = Levels.blocker_amount
        self.player_hitbox = Player.hitbox
        self.enemy_lst = Enemy.enemy_lst
        self.spez_lst = Spez_enemy.lst
        self.block_lst = Blocker.block_lst
        self.gfx_y = Gfx.y
        self.power_ups_lst = Power_ups.power_up_lst
        self.drop_table = Items.drop_table
        self.dropped_lst = Items.dropped_lst
        self.active_flag_lst = Items.active_flag_lst
        self.after_boss = Levels.after_boss
        self.ineventory = Items.inventory_dic
        self.wormhole_lst = Wormhole.lst
        self.wormhole_timer = Levels.wormhole_spawn_time

    def load_state(self):
        Player.max_health = self.max_health
        Player.health = self.health
        Power_ups.shield_amount = self.shield_amount
        Power_ups.super_shot_amount = self.super_shot_amount
        Power_ups.heal_amount = self.heal_amount
        Power_ups.star_shot_amount = self.star_shot_amount
        Levels.skill_points = self.skill_points
        Levels.level = self.level
        Turret.pd_ammo = self.pd_ammo
        Turret.nuke_ammo = self.nuke_ammo
        Turret.missile_ammo = self.missile_ammo
        Player.jump_charges = self.jump_charges
        Levels.skill_points = self.skill_points
        Player.damage = self.player_damage
        Turret.fire_rate = self.fire_rate
        Power_ups.star_shot_tubes = self.star_shot_tubes
        Power_ups.shield_time = self.shield_time
        Player.speed = self.speed
        Turret.normal_fire_rate = self.normal_fire_rate
        Turret.pd_reload_speed = self.pd_reload_speed
        Turret.missile_reload_speed = self.missile_reload_speed
        Turret.nuke_reload_speed = self.nuke_reload_speed
        Player.jump_recharge_rate = self.jump_recharge_rate
        Enemy.health = self.enemy_health
        Spez_enemy.health = self.spez_health
        Levels.display_score = self.display_score
        Levels.enemy_amount = self.enemy_amount
        Levels.boss_fight = self.boss_fight
        Levels.level = self.level
        Levels.display_level = self.display_level
        Levels.level_interval = self.level_interval
        Power_ups.interval = self.interval
        Levels.boss_amount = self.boss_amount
        Levels.blocker_amount = self.blocker_amount
        Player.hitbox = self.player_hitbox
        Enemy.enemy_lst = self.enemy_lst
        Spez_enemy.lst = self.spez_lst
        Blocker.block_lst = self.block_lst
        Gfx.y = self.gfx_y
        Power_ups.power_up_lst = self.power_ups_lst
        Items.drop_table = self.drop_table
        Items.dropped_lst = self.dropped_lst
        Items.active_flag_lst = self.active_flag_lst
        Levels.after_boss = self.after_boss
        Items.inventory_dic = self.ineventory
        Wormhole.lst = self.wormhole_lst
        Levels.wormhole_spawn_time = self.wormhole_timer


def main():

    right, left, up, down = [False, False, False, False]

    def move_condition(bool_1, str_1, bool_2, str_2, str_3):
        if bool_1:
            Player.move(str_1)
        elif bool_2:
            Player.move(str_2)
        else:
            Player.move(str_3)

    shooter_event, jumper_event, seeker_event, wave_event = [pygame.USEREVENT + i for i in range(1, 5)]

    event_conditions = [
        (lambda: Levels.spez_event_trigger == 1, pygame.event.Event(shooter_event)),
        (lambda: Levels.spez_event_trigger == 2, pygame.event.Event(jumper_event)),
        (lambda: Levels.spez_event_trigger == 3, pygame.event.Event(seeker_event)),
        (lambda: Levels.spez_event_trigger == 4, pygame.event.Event(wave_event))
    ]

    Gfx.background()
    Interface.create()

    components = [Blocker, Power_ups, Player, Turret, Enemy, Spez_enemy, Bosses, Boss_adds, Elites, Interface, Levels, Gfx, Items]

    # Levels.skill_points += 100
    # Items.drop((winwidth / 2, 400), target=Item_escort_improve((100, 100, 100)))
    Items.drop((winwidth / 2, 400), target=Item_he_rounds((100, 100, 100)))
    # Items.drop((winwidth / 2, 400), amount=1)
    Levels.after_boss = True

    while True:
        Gfx.background()
        # print(Clock.get_fps())wwwww
        # print(Levels.wormhole_spawn_time)

        for component in components:
            component.update()

        for spez_event in map(pygame.event.post, [event for (condition, event) in event_conditions if condition()]):
            spez_event

        for event in pygame.event.get():
            for typ, kind in [
                (shooter_event, "shooter"),
                (jumper_event, "jumper"),
                (seeker_event, "seeker"),
                (wave_event, "wave")
            ]:
                if event.type == typ:
                    Spez_enemy.spez_event(kind)
            if event.type == KEYDOWN:
                if event.key == K_TAB:
                    scrollspeed_temp = Gfx.scroll_speed
                    Gfx.scroll_speed = 0
                    Interface.upgrades_menu(True)
                    Gfx.scroll_speed = scrollspeed_temp
                    right, left, up, down = [False, False, False, False]  # damit palyer nicht moved nach verlassen von menu
                elif event.key == K_d:
                    right = True
                    move_condition(up, "right up", down, "right down", "right")
                elif event.key == K_a:
                    left = True
                    move_condition(up, "left up", down, "left down", "left")
                elif event.key == K_w:
                    up = True
                    move_condition(left, "left up", right, "right up", "up")
                elif event.key == K_s:
                    down = True
                    move_condition(left, "left down", right, "right down", "down")
                elif event.key == K_1:
                    Power_ups.use("heal")
                elif event.key == K_2:
                    Power_ups.use("shield")
                elif event.key == K_3:
                    Power_ups.use("super_shot")
                elif event.key == K_4:
                    Power_ups.use("star_shot")
                elif event.key == K_r:
                    try:
                        Items.inventory_dic[0].toggle()
                        Items.inventory_dic[0].activation_effect()
                    except AttributeError:
                        pass  # Fehlersound
                elif event.key == K_f:
                    try:
                        Items.inventory_dic[1].toggle()
                        Items.inventory_dic[1].activation_effect()
                    except AttributeError:
                        pass

                elif event.key == K_m:
                    test_mode()
                elif event.key == K_SPACE:
                    Turret.missile_fired = True
                elif event.key == K_l:
                    if not Levels.boss_fight:
                        try:
                            load_game().load_state()
                        except FileNotFoundError:
                            pass
                if Turret.nuke_ammo > 0 and not Turret.nuke_fired:
                    if event.key == K_LCTRL:
                        Turret.nuke_fire()
            elif event.type == MOUSEBUTTONDOWN:
                Turret.fire(True)
            elif event.type == KEYUP:
                if event.key == K_w:
                    up = False
                elif event.key == K_s:
                    down = False
                elif event.key == K_d:
                    right = False
                elif event.key == K_a:
                    left = False
                # elif event.key == K_LSHIFT:s
                #     Player.speed_boost(False)
                elif event.key == K_SPACE:
                    Turret.missile_fired = False
                elif event.key == K_r:
                    try:
                        Items.inventory_dic[0].end_activation()
                    except AttributeError:
                        pass
                elif event.key == K_f:
                    try:
                        Items.inventory_dic[1].end_activation()
                    except AttributeError:
                        pass
                    # Player.jumpdrive(True)
                elif event.key == K_ESCAPE:
                    if not Levels.boss_fight and not Levels.elite_fight:
                        save_game(Game_state())
                    pygame.quit()
                    exit()

                if [up, down, left, right].count(True) < 2:
                    for con, cmd in [
                        (up, "up"),
                        (down, "down"),
                        (right, "right"),
                        (left, "left"),
                        (not any([up, down, right, left]), "idle")
                    ]:
                        if con:
                            Player.move(cmd)
            elif event.type == MOUSEBUTTONUP:
                Turret.fire(False)
            elif event.type == QUIT:
                pygame.quit()
                exit()
        Gfx.cursor()
        Clock.tick(fps)
        pygame.display.update()


if __name__ == "__main__":
    main()

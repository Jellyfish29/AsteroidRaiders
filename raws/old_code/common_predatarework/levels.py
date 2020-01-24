import random

from astraid_funcs import *
import enemy as en
import spez_enemy as spez
import Gfx as gfx
import power_ups as pup
import bosses as bo
import elites as el
""" Enemy Class:
        Attributes: Enemy.health
    Spez_enemy Class:
        Attributes: Spez_enemy.health
    Gfx class:
        Attributes: Gfx.scroll_speed
    Power_ups class:
        Attributes: Power_ups.interval
    Bosses class
        methods: Bosses.create()
"""


class Levels:

    interval_score = 0
    display_score = 0
    display_level = 1
    level = 1
    level_interval = 35
    enemy_amount = 4  # at Start
    boss_amount = 1
    blocker_amount = 1
    boss_fight = False
    after_boss = False
    skill_points = 1
    spez_event_trigger = 0
    tc = Time_controler()
    # wormhole/Elites
    wormhole_wait = False
    wormhole_spawn_time = 0
    elite_fight = False
    event_trigger_time = (1400, 3600)

    def boss_trigger():
        if Levels.level % 5 == 0:
            bo.Bosses.create(Levels.level)
            Levels.boss_fight = True
            gfx.Gfx.scroll_speed += 1
            el.Wormhole.lst.clear()
            gfx.Gfx.bg_move = False

    def enemy_scaling():
        en.Enemy.health += 0.3
        spez.Spez_enemy.health += 0.4
        el.Elites.health += el.Elites.health * 0.08
        if Levels.level % 10 == 0:
            spez.Spez_enemy.amount += 1
        elif Levels.level % 4 == 0:
            Levels.enemy_amount += 1
        elif Levels.level % 15 == 0:
            Levels.blocker_amount += 1

    def wormhole_spawn():
        if not Levels.after_boss and not Levels.boss_fight and not Levels.elite_fight:
            if len(el.Wormhole.lst) < 1:
                if not Levels.wormhole_wait:
                    Levels.wormhole_spawn_time = 5400
                    Levels.wormhole_wait = True
                if Levels.wormhole_wait:
                    if Levels.tc.trigger_1(int(Levels.wormhole_spawn_time)):
                        el.Wormhole.trigger = True
                        Levels.wormhole_wait = False

    def update():
        if Levels.tc.trigger_2(random.randint(Levels.event_trigger_time[0], Levels.event_trigger_time[1])):
            Levels.spez_event_trigger = random.randint(1, 4)

        Levels.wormhole_spawn()

        if Levels.interval_score > Levels.level_interval:
            Levels.event_trigger_time = (Levels.event_trigger_time[0] - 50, Levels.event_trigger_time[1] -75)
            Levels.level += 1
            Levels.display_level += 1
            Levels.level_interval += 10
            pup.Power_ups.interval += 5
            Levels.skill_points += 1
            Levels.boss_trigger()
            Levels.enemy_scaling()
            Levels.interval_score = 0

import random

import enemy as en
import spez_enemy as spez
import Gfx as gfx
import power_ups as pup
import bosses as bo
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
    level_interval = 20
    enemy_amount = 4  # at Start
    boss_amount = 1
    blocker_amount = 1
    boss_fight = False
    skill_points = 1
    spez_event_trigger = 0

    def boss_trigger():
        if Levels.level % 5 == 0:
            bo.Bosses.create(Levels.level)
            Levels.boss_fight = True
            gfx.Gfx.scroll_speed += 1

    def enemy_scaling():
        en.Enemy.health += 0.2
        spez.Spez_enemy.health += 0.3
        if Levels.level % 10 == 0:
            spez.Spez_enemy.amount += 1
        elif Levels.level % 3 == 0:
            Levels.enemy_amount += 1
        elif Levels.level % 15 == 0:
            Levels.blocker_amount += 1

    def update():
        if Levels.interval_score > Levels.level_interval:
            # Levels.enemy_amount += Levels.enemys_per_level
            Levels.level += 1
            Levels.display_level += 1
            Levels.level_interval += 10
            pup.Power_ups.interval += 1
            Levels.skill_points += 1
            if not Levels.level % 5 == 1:
                Levels.spez_event_trigger = random.randint(1, 4)
            Levels.boss_trigger()
            Levels.enemy_scaling()
            Levels.interval_score = 0

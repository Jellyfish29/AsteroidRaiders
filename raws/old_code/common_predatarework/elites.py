import pygame
import random

from init import *
from astraid_funcs import *
from Gfx import Gfx
import blocker as bl
import enemy as en
import spez_enemy as spez
import bosses as bo
import player as pl
import turret as tr
import levels as lvl
import items as it


class Elites(bo.Bosses):

    lst = []
    health = 80
    elite_fight = False

    def __init__(self, typ, health, speed, fire_rate, boss_skill, move_pattern, size, gfx_idx, gfx_hook, drop_amount):
        super().__init__(typ, health, speed, fire_rate, boss_skill, move_pattern, size, gfx_idx, gfx_hook, drop_amount)
        self.score_amount = 100
        self.drop_amount = random.randint(1, 2)

    def elite_skills(self):
        pass

    def spawn():
        Elites.elite_fight = True
        Elites.lst.append(random.choice([
            lambda: Elites("elite", Elites.health, 2, 170, ["mines"], [random.randint(0, 9) for _ in range(40)], (80, 180), [0, 1], (50, 120), 0),
            lambda: Elites("elite", Elites.health + Elites.health * 0.2, 4, 120, ["seeker_missiles"], [random.randint(0, 9) for _ in range(40)], (80, 180), [0, 1], (50, 120), 0),
            lambda: Elites("elite", Elites.health - Elites.health * 0.2, 8, 80, ["jumpdrive"], [random.randint(0, 9) for _ in range(40)], (80, 180), [0, 1], (50, 120), 0),
            lambda: Elites("elite", Elites.health + Elites.health, 3, 100, ["salvo"], (0, 7), (80, 180), [0, 1], (50, 120), 0),
            lambda: Elites("elite", Elites.health, 2, 120, ["adds"], (0, 7), (80, 180), [0, 1], (50, 120), 0),
            lambda: Elites("elite", Elites.health + Elites.health * 0.1, 2, 200, ["main_gun"], (8, 9), (80, 180), [0, 1], (50, 120), 0)])())

    def update():

        Wormhole.spawn()

        for wormhole in Wormhole.lst:
            wormhole.move()
            wormhole.gfx_animation()
            wormhole.collison_player()
            if wormhole.border_collison():
                Wormhole.lst.remove(wormhole)

        for elite in Elites.lst:
            elite.move()
            elite.skills()
            elite.boss_skills()
            elite.elite_skills()
            elite.gfx_direction()
            elite.gfx_health_bar()
            elite.gfx_animation()
            tr.Turret.missile_aquisition(elite)
            if elite.player_collide():
                pl.Player.hit(0.05)
            if elite.hit_detection(False):
                Elites.lst.remove(elite)
                bo.Bosses.mine_lst.clear()
                bo.Bosses.missile_lst.clear()
                lvl.Levels.after_boss = True
                lvl.Levels.elite_fight = False
                random.choice([
                    lambda: it.Items.drop(elite.hitbox.center, amount=elite.drop_amount),
                    lambda: it.Items.drop((elite.hitbox.topleft), target=it.Item_supply_crate((100, 100, 100))),
                    lambda: it.Items.drop((elite.hitbox.topleft), amount=2, target=it.Item_supply_crate((100, 100, 100)))
                ])()


class Wormhole:

    lst = []
    trigger = False

    def __init__(self):
        self.hitbox = pygame.Rect(random.randint(200, 800), -300, 100, 100)
        self.speed = 1.5

    def move(self):
        self.hitbox.move_ip(0, self.speed)
        pygame.draw.rect(win, (0, 0, 200), self.hitbox)

    def gfx_animation(self):
        pass

    def collison_player(self):
        if self.hitbox.colliderect(pl.Player.hitbox):
            Elites.spawn()
            Wormhole.wormhole_travel()
            Wormhole.lst.clear()

    def border_collison(self):
        return rect_not_on_sreen(self.hitbox, bot=True, strict=False)

    def wormhole_travel():
        lvl.Levels.elite_fight = True
        en.Enemy.enemy_lst.clear()
        spez.Spez_enemy.lst.clear()
        spez.Spez_enemy.shot_lst.clear()
        tr.Turret.shot_lst.clear()
        bl.Blocker.block_lst.clear()
        Wormhole.lst.clear()

    def spawn():
        if Wormhole.trigger:
            Wormhole.lst.append(Wormhole())
            Wormhole.trigger = False

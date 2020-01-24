import pygame
from pygame.locals import *
import random

from init import *
from astraid_funcs import *
from Gfx import Gfx
import player as pl
import levels as lvl
import spez_enemy as spez
import turret as tr
""" creates an "Blocker" object 

    Gfx class:
        Methods: shot_hit_effect(shot)
    Player class:
        Attributes: Player.hitbox
        Methods: Player.hit()
    Levels class:
        Attributes: Levels.boss_fight
    Spez_enemy class:
        Attributes: Spez_enemy.shot_lst
    Turret class:
        Attributes: Turret.shot_lst
        Methods: Turret.gfx_shot_lst
"""


class Blocker():

    block_lst = []
    gfx_pictures = get_images("blockers")

    def __init__(self):
        self.hitbox = pygame.Rect((random.randint(-50, winwidth - 50), random.randint(-1500, -400), 250, 250))
        self.speed = 1
        self.gfx_idx = random.choice([0, 1])

    def draw(self):
        self.hitbox.move_ip(0, self.speed)
        # pygame.draw.rect(win, (70, 70, 70), self.hitbox)

    def collision(self):
        return rect_not_on_sreen(self.hitbox, bot=True, strict=False)

    def player_collision(self):
        return self.hitbox.colliderect(pl.Player.hitbox)

    def hit_detection(self):
        for shot, _ in spez.Spez_enemy.shot_lst:
            if self.hitbox.colliderect(shot):
                spez.Spez_enemy.shot_lst.remove((shot, _))
        for shot, _ in tr.Turret.shot_lst:
            if self.hitbox.colliderect(shot):
                Gfx.shot_hit_effect(shot)
                tr.Turret.shot_lst.remove((shot, _))

    def create():
        if not lvl.Levels.boss_fight:
            for i in range(lvl.Levels.blocker_amount):
                Blocker.block_lst.append(Blocker())

    def gfx_animation(self):
        win.blit(Blocker.gfx_pictures[self.gfx_idx], (self.hitbox.topleft[0] - 30, self.hitbox.topleft[1] - 40))

    def update():
        # methode for main game loop

        if len(Blocker.block_lst) == 0:
            Blocker.create()
        for blocker in Blocker.block_lst:
            blocker.draw()
            blocker.gfx_animation()
            blocker.hit_detection()
            if blocker.collision():
                Blocker.block_lst.remove(blocker)
            elif blocker.player_collision():
                pl.Player.hit(True)

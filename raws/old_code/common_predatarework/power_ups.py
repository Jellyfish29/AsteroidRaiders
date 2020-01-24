import pygame
import random

from init import *
from astraid_funcs import *
from Gfx import Gfx
import turret as tr
import player as pl
import levels as lvl
""" Turret class:
        Attributes: Turret.super_shot_limiter, Turret.super_star_limiter
    Player class:
        Atttributes: Player.hitbox, Player.health, Player.max_health
"""


class Power_ups:

    power_up_lst = []
    super_shot = False
    star_shot = False
    shield = False
    super_shot_amount = 0
    star_shot_amount = 0
    shield_amount = 0
    heal_amount = 1
    shield_time = 360
    heal_strength = 3
    star_shot_tubes = 6
    score = 0
    interval = 25
    gfx_pictures = get_images("power_ups")
    tc = Time_controler()

    def __init__(self, typ):
        self.hitbox = pygame.Rect(random.randint(100, winwidth - 100), -200, 50, 200)
        self.typ = typ
        self.power_up_tc = Time_controler()
        if typ == "star_shot":
            self.gfx_idx = (0, 1)
        elif typ == "super_shot":
            self.gfx_idx = (2, 3)
        elif typ == "heal":
            self.gfx_idx = (4, 5)
        elif typ == "shield":
            self.gfx_idx = (7, 8)

    def collision(self):
        if self.hitbox.colliderect(pl.Player.hitbox):
            if self.typ == "heal":
                Power_ups.heal_amount += 1
            elif self.typ == "super_shot":
                tr.Turret.super_shot_limiter = 0  # reset bei erneutem einsammeln
                Power_ups.super_shot_amount += 1
            elif self.typ == "star_shot":
                tr.Turret.super_star_limiter = 0
                Power_ups.star_shot_amount += 1
            elif self.typ == "shield":
                Power_ups.shield_amount += 1
            return True
        return rect_not_on_sreen(self.hitbox, True)

    def use(pup_name):
        if pup_name == "super_shot":
            if Power_ups.super_shot_amount > 0 and not Power_ups.star_shot:
                Gfx.create_effect("supers", 20, (pl.Player.hitbox.topleft[0] - 25, pl.Player.hitbox.topleft[1] - 25), hover=True)
                Power_ups.super_shot = True
                Power_ups.super_shot_amount -= 1
                tr.Turret.super_shot_limiter = 0
        elif pup_name == "star_shot":
            if Power_ups.star_shot_amount > 0 and not Power_ups.super_shot:
                Gfx.create_effect("stars", 20, (pl.Player.hitbox.topleft[0] - 25, pl.Player.hitbox.topleft[1] - 25), hover=True)
                Power_ups.star_shot = True
                Power_ups.star_shot_amount -= 1
                tr.Turret.star_shot_limiter = 0
        elif pup_name == "shield":
            if Power_ups.shield_amount > 0:
                Power_ups.shield_amount -= 1
                Power_ups.shield_ticker = 0
                Power_ups.shield = True
        elif pup_name == "heal":
            if Power_ups.heal_amount > 0 and pl.Player.health < pl.Player.max_health:
                Gfx.create_effect("heal", 20, (pl.Player.hitbox.topleft[0] - 25, pl.Player.hitbox.topleft[1] - 25), hover=True)
                Power_ups.heal_amount -= 1
                pl.Player.health += Power_ups.heal_strength
                if pl.Player.health > pl.Player.max_health:
                    pl.Player.health = pl.Player.max_health

    def draw(self):
        self.hitbox.move_ip(0, 1.5)
        # if self.typ == "shield":
        #     pygame.draw.rect(win, (0, 255, 255), self.hitbox)  # green
        # elif self.typ == "super_shot":
        #     pygame.draw.rect(win, (0, 0, 255), self.hitbox)  # blue
        # elif self.typ == "star_shot":
        #     pygame.draw.rect(win, (255, 0, 0), self.hitbox)  # red

    def gfx_animation(self):
        gfx_ticker = self.power_up_tc.animation_ticker(8)
        if gfx_ticker < 4:
            win.blit(Power_ups.gfx_pictures[self.gfx_idx[0]], (self.hitbox.topleft[0], self.hitbox.topleft[1]))
        else:
            win.blit(Power_ups.gfx_pictures[self.gfx_idx[1]], (self.hitbox.topleft[0], self.hitbox.topleft[1]))

    def draw_shield():
        shield_rect = pygame.Rect(pl.Player.hitbox.topleft[0] - 25, pl.Player.hitbox.topleft[1] - 25, 100, 100)
        win.blit(Power_ups.gfx_pictures[6], (shield_rect.topleft[0] - 15, shield_rect.topleft[1] - 40))
        # pygame.draw.rect(win, (0, 240, 220), shield_rect)

    def spawn():
        if not lvl.Levels.after_boss:
            if Power_ups.score > Power_ups.interval:
                Power_ups.score = 0
                return True

    def supply_drop():

        def health():
            if pl.Player.health < pl.Player.max_health:
                pl.Player.health += random.randint(1, 2)

        def supers():
            Power_ups.super_shot_amount += random.randint(1, 2)

        def star():
            Power_ups.star_shot_amount += random.randint(1, 2)

        def shield():
            Power_ups.shield_amount += random.randint(1, 2)

        def heal():
            Power_ups.heal_amount += random.randint(1, 2)

        def skill():
            lvl.Levels.skill_points += 1

        random.choice([health, supers, star, shield, heal, skill])()
        random.choice([health, supers, star, shield, heal, skill])()

    def heal_drop():
        Power_ups.heal_amount += 1
        while pl.Player.health < pl.Player.max_health:
            pl.Player.health += 1

    def update():
        if Power_ups.spawn():
            if pl.Player.health < 3:
                Power_ups.power_up_lst.append(Power_ups("heal"))
            else:
                Power_ups.power_up_lst.append(Power_ups(random.choice(["heal", "super_shot", "star_shot", "shield"])))
        for power_up in Power_ups.power_up_lst:
            power_up.draw()
            power_up.gfx_animation()
            if power_up.collision():
                Power_ups.power_up_lst.remove(power_up)
        if Power_ups.shield:
            Power_ups.draw_shield()
            if Power_ups.tc.trigger_1(Power_ups.shield_time):
                Power_ups.shield = False

import pygame
from pygame.locals import *
import time
import os

from init import *
from astraid_funcs import *
from Gfx import Gfx
import power_ups as pup
import levels as lvl
import blocker as bl
import items as it
import turret as tr
import bosses as bo
import enemy as en
import spez_enemy as spez
import elites as el

""" Power_ups Class:
        Attributes: Power_up.shield
    Levels class:
        Attributes: Levels.display_score
"""


class Player:

    health = 5
    max_health = 5
    hitbox = pygame.Rect(winwidth / 2, winheight / 2, 70, 50)
    speed = 6
    base_damage = 1.0
    damage = base_damage
    direction = "idle"
    directions = directions(speed)
    jump_charges = 1
    jump_draw = False
    jump_recharge_rate = 0.002
    gfx_idx = {
        "up": 0, "down": 2, "right": 4, "left": 6, "right up": 8, "right down": 10, "left up": 12, "left down": 14, "idle": 16}
    gfx_pictures = get_images("player_ship")
    gfx_hit_effect_pictures = get_images("hit_effects")
    gfx_ticker = 0
    tc = Time_controler()
    restart_timer = False

    def move(direction):
        Player.direction = direction

    def hit(damage, sure_death=False):
        if sure_death:
            Player.health = 0
        elif not pup.Power_ups.shield:
            Player.health -= damage
            Player.gfx_hit_effect()
        if "overdrive" in it.Items.active_flag_lst:
            Player.damage -= 0.05 * tr.Turret.overdrive_count
            tr.Turret.fire_rate += 0.7 * tr.Turret.overdrive_count
            tr.Turret.overdrive_count = 0
        if int(Player.health) <= 0:
            with open(os.path.join(os.getcwd()[:-7], "score.txt"), "a")as f:
                f.write(time.strftime("%H:%M:%S") + "   " + time.strftime("%d/%m/%Y") + "\nScore = " + str(lvl.Levels.display_score) + "\n")
                # delete savegame on death
            try:
                os.remove(os.path.join(os.getcwd()[:-7], f"save_games\\saves"))
            except FileNotFoundError:
                pass
            pygame.quit()
            exit()

    def speed_boost(boost):
        if boost:
            Player.directions = directions(Player.speed * 2)
        else:
            Player.directions = directions(Player.speed)

    def jumpdrive():
        if "jump_drive" in it.Items.active_flag_lst:
            Player.jump_charges += Player.jump_recharge_rate
            if it.Item_jump_drive.active:
                if Player.jump_charges > 1:
                    if not it.Item_jump_drive.engage:
                        Player.jump_draw = True
                    if it.Item_jump_drive.engage:
                        Gfx.create_effect("jump", 2, (Player.hitbox.topleft[0] - 40, Player.hitbox.topleft[1] - 40))
                        Player.hitbox.center = pygame.mouse.get_pos()
                        Gfx.create_effect("jumpa", 2, (Player.hitbox.topleft[0] - 60, Player.hitbox.topleft[1] - 60))
                        Player.jump_draw = False
                        Player.jump_charges -= 1
                        it.Item_jump_drive.active = False

    def draw_jump_dest():
        if Player.jump_draw:
            rect = pygame.Rect(1, 1, 1, 1)
            rect.center = pygame.mouse.get_pos()
            win.blit(Player.gfx_pictures[20], (rect.topleft[0] - 41, rect.topleft[1] - 50))

    def gfx_animation(idx):
        if Player.gfx_ticker < 3:
            win.blit(Player.gfx_pictures[Player.gfx_idx[idx]], (Player.hitbox.topleft[0] - 6, Player.hitbox.topleft[1] - 25))
            Player.gfx_ticker += 1
        else:
            win.blit(Player.gfx_pictures[Player.gfx_idx[idx] + 1], (Player.hitbox.topleft[0] - 6, Player.hitbox.topleft[1] - 25))
            Player.gfx_ticker += 1
        if Player.gfx_ticker == 6:
            Player.gfx_ticker = 0

    def gfx_hit_effect():
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect(0, 0, winwidth, winheight))
        win.blit(Player.gfx_hit_effect_pictures[3], (Player.hitbox.topleft[0] - 20, Player.hitbox.topleft[1] - 20))

    def gfx_warning_lights():
        if Player.health < 2:
            ticker = Player.tc.animation_ticker(30)
            if ticker < 20:
                win.blit(Player.gfx_pictures[21], (Player.hitbox.topleft[0] - 6, Player.hitbox.topleft[1] - 25))
            else:
                win.blit(Player.gfx_pictures[22], (Player.hitbox.topleft[0] - 6, Player.hitbox.topleft[1] - 25))

    def update():
        # Methode for main gameloop, everithing that needs to be updated every tick
        for operator, position, con, direction in [
            ("<", Player.hitbox.center[0], 0, (1, 0)),
            (">", Player.hitbox.center[0], winwidth, (-1, 0)),
            ("<", Player.hitbox.center[1], 0, (0, 1)),
            (">", Player.hitbox.center[1], winheight, (0, -1))
        ]:
            if operator == "<":
                if position < con:
                    Player.hitbox.move_ip(direction)
                    break
            if operator == ">":
                if position > con:
                    Player.hitbox.move_ip(direction)
                    break
        else:
            Player.hitbox.move_ip(Player.directions[Player.direction])
        if lvl.Levels.after_boss:
            if Player.hitbox.colliderect(pygame.Rect(0, -10, winwidth, 15)):
                Player.hitbox.center = (Player.hitbox.center[0], winheight)
                for escort in Escort.lst:
                    escort.hitbox.center = (Player.hitbox.center[0] - 100, Player.hitbox.center[1])
                Gfx.y += 1080
                bl.Blocker.block_lst.clear()
                pup.Power_ups.power_up_lst.clear()
                it.Items.dropped_lst.clear()
                Player.restart_timer = True
                Gfx.bg_move = True

        if Player.restart_timer:
            if Player.tc.trigger_1(120):
                lvl.Levels.after_boss = False
                Player.restart_timer = False

        # pygame.draw.rect(win, (255, 0, 0), Player.hitbox)
        Player.jumpdrive()
        Player.gfx_animation(Player.direction)
        Player.draw_jump_dest()
        Player.gfx_warning_lights()

        Escort.spawn()

        for escort in Escort.lst:
            escort.move()
            escort.skills()
            escort.overlap_avoidance()


class Escort:

    lst = []
    spawned = False
    fire_rate = 100

    def __init__(self, typ, color, gfx_idx, second=False):
        self.typ = typ
        self.color = color
        self.gfx_idx = gfx_idx
        self.second = second
        self.tc = Time_controler()
        self.hitbox = pygame.Rect(Player.hitbox.center[0] - 100, Player.hitbox.center[1], 50, 50)

    def move(self):
        self.hitbox.move_ip(Player.directions[Player.direction])
        pygame.draw.circle(win, self.color, self.hitbox.center, 25)

    def overlap_avoidance(self):
        if "2nd_escort" in it.Items.active_flag_lst:
            for escort in Escort.lst:
                if escort != self:
                    if self.hitbox.colliderect(escort.hitbox):
                        self.hitbox.move_ip(200, 0)

    def skills(self):
        if not lvl.Levels.after_boss:
            try:
                target = (spez.Spez_enemy.lst + bo.Bosses.boss_lst + el.Elites.lst)[0]
            except IndexError:
                pass
            if self.typ == "escort_missile":
                if self.tc.trigger_1(Escort.fire_rate * 5):
                    tr.Turret.missile_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1], 10, 10), target))
            elif self.typ == "escort_gun":
                if self.tc.trigger_1(Escort.fire_rate):
                    try:
                        tr.Turret.shot_lst.append((pygame.Rect(
                            self.hitbox.center[0], self.hitbox.center[1], 6, 6), tr.Turret.angles[degrees(target.hitbox.center[0], self.hitbox.center[0], target.hitbox.center[1], self.hitbox.center[1])], Player.damage * 1.15))
                    except UnboundLocalError:
                        pass
            elif self.typ == "escort_gunship":
                if self.tc.trigger_1(Escort.fire_rate * 0.75):
                    for angle in [85, 81, 76]:
                        if self.second:
                            tr.Turret.shot_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1], 6, 6), tr.Turret.angles[angle + 12], Player.damage * 0.75))

                        else:
                            tr.Turret.shot_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1], 6, 6), tr.Turret.angles[angle], Player.damage * 0.75))

    def spawn():
        if not Escort.spawned:
            for typ, c in [
                ("escort_missile", (255, 0, 00)),
                ("escort_gun", (0, 0, 255)),
                ("escort_gunship", (0, 255, 255))
            ]:
                if typ in it.Items.active_flag_lst:
                    if "2nd_escort" in it.Items.active_flag_lst:
                        Escort.lst.append(Escort(typ, c, (0, 1), second=True))
                    Escort.lst.append(Escort(typ, c, (0, 1)))
                    Escort.spawned = True

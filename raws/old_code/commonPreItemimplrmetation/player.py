import pygame
from pygame.locals import *
import time
import os

from init import *
from astraid_funcs import *
from Gfx import Gfx
import power_ups as pup
import levels as lvl
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
    jump_recharge_rate = 0.0005
    gfx_idx = {
        "up": 0, "down": 2, "right": 4, "left": 6, "right up": 8, "right down": 10, "left up": 12, "left down": 14, "idle": 16}
    gfx_pictures = get_images("player_ship")
    gfx_hit_effect_pictures = get_images("hit_effects")
    gfx_ticker = 0
    tc = Time_controler()

    def move(direction):
        Player.direction = direction

    def hit(damage, sure_death=False):
        if sure_death:
            Player.health = 0
        elif not pup.Power_ups.shield:
            Player.health -= damage
            Player.gfx_hit_effect()
        if Player.health <= 0:
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

    def jumpdrive(engage):
        if Player.jump_charges > 1:
            if not engage:
                Player.jump_draw = True
            if engage:
                Gfx.create_effect("jump", 2, (Player.hitbox.topleft[0] - 40, Player.hitbox.topleft[1] - 40))
                Player.hitbox.center = pygame.mouse.get_pos()
                Gfx.create_effect("jumpa", 2, (Player.hitbox.topleft[0] - 60, Player.hitbox.topleft[1] - 60))
                Player.jump_draw = False
                Player.jump_charges -= 1

    def jump_recharge():
        Player.jump_charges += Player.jump_recharge_rate

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
        # pygame.draw.rect(win, (255, 0, 0), Player.hitbox)
        Player.gfx_animation(Player.direction)
        Player.draw_jump_dest()
        Player.jump_recharge()
        Player.gfx_warning_lights()

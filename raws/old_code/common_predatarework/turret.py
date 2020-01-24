import pygame
from pygame.locals import *
# import random

from init import *
from astraid_funcs import *
from Gfx import Gfx
import player as pl
import power_ups as pup
import items as it
""" Player Class:
        Attributes: Player.hitbox, Player.gfx_pictures
    Power_ups Class
        Attributes: Power_ups.super_shot, Power_ups.star_shot, Power_ups.star_shot_tubes
"""


class Turret:

    # normal shot vlaues
    shot_lst = []
    angle = 0
    projectile_size = 6
    projectile_speed = 15
    firing = False
    direction = None
    normal_fire_rate = 35
    fire_rate = normal_fire_rate
    shot_count = 0
    # Overdrive
    overdrive_count = 0
    # ammunition = normal_fire_rate[1]
    fire_limiter = 0
    angles = angles_360(projectile_speed)
    tc = Time_controler()
    # super shot values
    super_shot_fire_rate = 5
    super_shot_ammo = 50
    super_shot_limiter = 0
    # star shot values
    star_shot_limiter = 0
    star_shot_ammo = 30
    # nuke values
    nuke_ammo = 1
    nuke_fired = False
    nuke = pygame.Rect(-1000, -1000, 1, 1)  # Placeholer rect out of sigth
    nuke_angles = angles_360(3)
    nuke_degree = 0
    explosion = True
    nuke_reload_speed = 0.00025
    # pd values
    pd_lst = []
    pd_angles = angles_360(25)
    pd_angle = 90
    pd_ticker = 0
    pd_ammo = 20
    pd_reload_speed = 0.008
    # missile values
    missile_fired = False
    missile_lst = []
    missile_angles = angles_360(10)
    missile_angle = 0
    missile_traget = None
    missile_ammo = 3
    missile_reload_speed = 0.001
    # he values
    he_ammo = 15
    he_reload_speed = 0.004
    he_rounds_lst = []
    # Gfx setup
    gun_draw_angles = angles_360(20)
    gfx_shot_pictures = get_images("projectile")
    gfx_explosion_pictures = get_images("explosions")
    gfx_hit_pictures = get_images("hit_effects")
    gfx_ticker = 0
    gfx_ticker_ex = 0
    gun = pygame.Rect(10, 10, 10, 10)

    def fire(fire):
        Turret.firing = fire

    def nuke_fire():
        if "nuke" in it.Items.active_flag_lst:
            if it.Item_nuke.active:
                if int(Turret.nuke_ammo) > 0 and not Turret.nuke_fired:
                    Turret.nuke_ammo -= 1
                    Turret.nuke = pygame.Rect(pl.Player.hitbox.center[0], pl.Player.hitbox.center[1], 10, 10)
                    Turret.nuke_degree = degrees(pygame.mouse.get_pos()[0], pl.Player.hitbox.center[0], pygame.mouse.get_pos()[1], pl.Player.hitbox.center[1])
                    Turret.nuke_fired = True
                if Turret.nuke_fired:
                    Turret.nuke.move_ip(Turret.nuke_angles[Turret.nuke_degree])
                    # pygame.draw.rect(win, (150, 0, 0), Turret.nuke)
                    if abs(pl.Player.hitbox.center[0] - Turret.nuke.center[0]) > 400 or abs(pl.Player.hitbox.center[1] - Turret.nuke.center[1]) > 400:
                        Turret.explosion = False
                        Turret.nuke.inflate_ip(20, 20)
                        Turret.gfx_nuke_explosion()
                        if abs(Turret.nuke.topleft[0] - Turret.nuke.center[0]) > 400:
                            Turret.nuke = pygame.Rect(-1000, -1000, 1, 1)
                            Turret.nuke_fired = False
                            Turret.gfx_ticker_ex = 0
                            Turret.explosion = True
                            it.Item_nuke.active = False

    def point_defence(rect):
        if "point_defence" in it.Items.active_flag_lst:
            if it.Item_pd.active:
                pd_envelope = pygame.Rect(pl.Player.hitbox.center[0] - 200, pl.Player.hitbox.center[1] - 200, 400, 400)
                # pygame.draw.rect(win, (255, 255, 0), pd_envelope)
                if pd_envelope.colliderect(rect):
                    Turret.pd_ticker += 1
                    Turret.pd_angle = degrees(rect.center[0], pl.Player.hitbox.center[0], rect.center[1], pl.Player.hitbox.center[1] - 35)
                    if int(Turret.pd_ammo) > 0:
                        if Turret.pd_ticker > 6:
                            Turret.pd_lst.append((pygame.Rect(pl.Player.hitbox.center[0], pl.Player.hitbox.center[1] - 35, 6, 6), Turret.pd_angles[Turret.pd_angle], 0))
                            Turret.pd_ammo -= 1
                            Turret.pd_ticker = 0

    def missile_aquisition(enemy):
        if "missile" in it.Items.active_flag_lst:
            if Turret.missile_ammo > 0:
                if it.Item_missile.active:
                    m_pos = pygame.mouse.get_pos()
                    aa_target_area = pygame.Rect(m_pos[0] - 100, m_pos[1] - 100, 200, 200)
                    # pygame.draw.rect(win, (255, 255, 0), aa_target_area)
                    if aa_target_area.colliderect(enemy.hitbox):
                        Gfx.create_effect("missilemuzzle", 3, pl.Player.hitbox, follow=True, x=-18, y=8)
                        Gfx.create_effect("missilemuzzle", 3, pl.Player.hitbox, follow=True, x=60, y=8)
                        Turret.missile_lst.append((pygame.Rect(pl.Player.hitbox.topleft[0], pl.Player.hitbox.topleft[1], 10, 10), enemy))
                        Turret.missile_lst.append((pygame.Rect(pl.Player.hitbox.topright[0], pl.Player.hitbox.topright[1], 10, 10), enemy))
                        Turret.missile_ammo -= 1
                        it.Item_missile.active = False

    def missile_follow():
        if len(Turret.missile_lst) > 0:
            for missile, target in Turret.missile_lst:
                # pygame.draw.rect(win, (255, 0, 0), missile)
                if Turret.tc.delay(True, 20):
                    if not missile.colliderect(target.hitbox):
                        if abs(pl.Player.hitbox.center[0] - target.hitbox.center[0]) > 10 or abs(pl.Player.hitbox.center[1] - target.hitbox.center[1]) > 10:
                            Turret.missile_angle = degrees(target.hitbox.center[0], missile.center[0], target.hitbox.center[1], missile.center[1])
                    elif missile.colliderect(target.hitbox):
                        Turret.missile_lst.remove((missile, target))
                        Turret.tc.delay(False)
                else:
                    Turret.missile_angle = 90
                # Gfx.create_effect("smoke", 3, missile.bottomleft)
                missile.move_ip(Turret.missile_angles[Turret.missile_angle])
                win.blit(gfx_rotate(Turret.gfx_shot_pictures[3], Turret.missile_angle - 90), (missile.topleft[0] - 5, missile.topleft[1] - 5))

    def he_round_hit(location):
        Turret.he_rounds_lst.append((pygame.Rect(location[0], location[1], 1, 1), pl.Player.damage * 0.3))

    def he_round_explosion():
        for explo, dmg in Turret.he_rounds_lst:
            pygame.draw.rect(win, (255, 255, 0), explo)
            explo.inflate_ip(30, 30)
            if abs(explo.topleft[0] - explo.center[0]) > 100:
                Turret.he_rounds_lst.remove((explo, dmg))

    def he_round_ammo_consumption():
        Turret.he_ammo -= 1
        if Turret.he_ammo < 0:
            Turret.he_active = False
            it.Item_he_rounds.active = False
        else:
            Turret.he_active = True

    def fan_shot():
        if "fan_shot" in it.Items.active_flag_lst:
            if Turret.shot_count % 4 == 0:
                for i in range(-5, 6, 10):
                    try:
                        Turret.shot_lst.append(
                            (pygame.Rect(pl.Player.hitbox.center[0], pl.Player.hitbox.center[1], 7, 7),
                             Turret.angles[degrees(pygame.mouse.get_pos()[0], pl.Player.hitbox.center[0], pygame.mouse.get_pos()[1], pl.Player.hitbox.center[1]) + i], pl.Player.damage))
                    except KeyError:
                        if i < 0:
                            Turret.shot_lst.append(
                                (pygame.Rect(pl.Player.hitbox.center[0], pl.Player.hitbox.center[1], 7, 7),
                                 Turret.angles[degrees(pygame.mouse.get_pos()[0], pl.Player.hitbox.center[0], pygame.mouse.get_pos()[1], pl.Player.hitbox.center[1]) + i + 360], pl.Player.damage))
                        else:
                            Turret.shot_lst.append(
                                (pygame.Rect(pl.Player.hitbox.center[0], pl.Player.hitbox.center[1], 7, 7),
                                 Turret.angles[degrees(pygame.mouse.get_pos()[0], pl.Player.hitbox.center[0], pygame.mouse.get_pos()[1], pl.Player.hitbox.center[1]) + i - 360], pl.Player.damage))

    def hammer_shot():
        if "hammer_shot" in it.Items.active_flag_lst:
            if Turret.shot_count % 5 == 0:
                for i in range(5):
                    Turret.shot_lst.append(
                        (pygame.Rect(pl.Player.hitbox.center[0], pl.Player.hitbox.center[1], 7, 7),
                         Turret.angles[degrees(pygame.mouse.get_pos()[0], pl.Player.hitbox.center[0], pygame.mouse.get_pos()[1], pl.Player.hitbox.center[1])], pl.Player.damage))

    def overdrive():
        if "overdrive" in it.Items.active_flag_lst:
            if Turret.overdrive_count < 20:
                Turret.overdrive_count += 1
                pl.Player.damage += 0.05
                Turret.fire_rate -= 0.7

    def super_shot_pup():
        if pup.Power_ups.super_shot:  # and not pup.Power_ups.star_shot:
            Turret.fire_rate = Turret.super_shot_fire_rate
            Turret.super_shot_limiter += 1
            if Turret.super_shot_limiter >= Turret.super_shot_ammo:
                Turret.fire_rate = Turret.normal_fire_rate
                Turret.super_shot_limiter = 0
                pup.Power_ups.super_shot = False
                pup.Power_ups.star_shot = False

    def star_shot_pup():
        if pup.Power_ups.star_shot:  # and not pup.Power_ups.super_shot:
            Turret.star_shot_limiter += 1
            if Turret.star_shot_limiter > Turret.star_shot_ammo:
                Turret.star_shot_limiter = 0
                pup.Power_ups.star_shot = False
                pup.Power_ups.super_shot = False
                Turret.fire_rate = Turret.normal_fire_rate
            for i in range(0, 360, int(360 / pup.Power_ups.star_shot_tubes)):
                Turret.shot_lst.append(
                    (pygame.Rect(pl.Player.hitbox.center[0], pl.Player.hitbox.center[1], Turret.projectile_size, Turret.projectile_size), Turret.angles[0 + i], pl.Player.damage))

    def normal_shot():
        if Turret.firing:
            if Turret.tc.trigger_1(Turret.fire_rate):
                Turret.shot_count += 1
                Turret.star_shot_pup()
                Turret.super_shot_pup()
                Turret.fan_shot()
                Turret.hammer_shot()
                dmg = pl.Player.damage
                # Special Ammo
                if "piercing_shot" in it.Items.active_flag_lst:
                    dmg = pl.Player.damage * 0.25
                if it.Item_he_rounds.active:
                    dmg = pl.Player.damage * 0.45
                    Turret.he_round_ammo_consumption()
                Gfx.create_effect("shot_muzzle", 2, pl.Player.hitbox, follow=True, x=5, y=0)
                Turret.shot_lst.append(
                    (pygame.Rect(pl.Player.hitbox.center[0], pl.Player.hitbox.center[1], Turret.projectile_size, Turret.projectile_size),
                     Turret.angles[degrees(pygame.mouse.get_pos()[0], pl.Player.hitbox.center[0], pygame.mouse.get_pos()[1], pl.Player.hitbox.center[1])],
                     dmg))

    def reloads():
        if "he_rounds" in it.Items.active_flag_lst:
            Turret.he_ammo += Turret.he_reload_speed
            if int(Turret.he_ammo) == 0:
                it.Item_he_rounds.active = False
        if "missile" in it.Items.active_flag_lst:
            Turret.missile_ammo += Turret.missile_reload_speed
            if int(Turret.missile_ammo) == 0:
                it.Item_missile.active = False
        if "nuke" in it.Items.active_flag_lst:
            Turret.nuke_ammo += Turret.nuke_reload_speed
            # if int(Turret.nuke_ammo) == 0:
            #     it.Item_nuke.active = False
        if "point_defence" in it.Items.active_flag_lst:
            Turret.pd_ammo += Turret.pd_reload_speed
            if int(Turret.pd_ammo) == 0:
                it.Item_pd.active = False

    def gfx_nuke(arg):
        if arg:
            if Turret.gfx_ticker < 3:
                win.blit(Turret.gfx_shot_pictures[4], (Turret.nuke.topleft[0] - 18, Turret.nuke.topleft[1] - 25))
                Turret.gfx_ticker += 1
            else:
                win.blit(Turret.gfx_shot_pictures[5], (Turret.nuke.topleft[0] - 18, Turret.nuke.topleft[1] - 25))
                Turret.gfx_ticker += 1
            if Turret.gfx_ticker == 6:
                Turret.gfx_ticker = 0

    def gfx_nuke_explosion():
        if Turret.gfx_ticker_ex < 10:
            win.blit(Turret.gfx_explosion_pictures[0], (Turret.nuke.center[0] - 50, Turret.nuke.center[1] - 50))
            Turret.gfx_ticker_ex += 1
        elif Turret.gfx_ticker_ex < 20:
            win.blit(Turret.gfx_explosion_pictures[1], (Turret.nuke.center[0] - 100, Turret.nuke.center[1] - 100))
            Turret.gfx_ticker_ex += 1
        elif Turret.gfx_ticker_ex < 30:
            win.blit(Turret.gfx_explosion_pictures[2], (Turret.nuke.center[0] - 250, Turret.nuke.center[1] - 250))
            Turret.gfx_ticker_ex += 1
        else:
            win.blit(Turret.gfx_explosion_pictures[3], (Turret.nuke.center[0] - 400, Turret.nuke.center[1] - 400))

    def gfx_shot_animation(shot):
        if pup.Power_ups.super_shot:
            win.blit(Turret.gfx_shot_pictures[1], (shot.topleft[0] - 10, shot.topleft[1] - 10))
        elif pup.Power_ups.star_shot:
            win.blit(Turret.gfx_shot_pictures[2], (shot.topleft[0] - 10, shot.topleft[1] - 10))
        else:
            win.blit(Turret.gfx_shot_pictures[0], (shot.topleft[0] - 10, shot.topleft[1] - 10))

    def gfx_gun_draw():
        Turret.gun.center = pl.Player.hitbox.center
        win.blit(rot_center(
            pl.Player.gfx_pictures[18], degrees(pygame.mouse.get_pos()[1], Turret.gun.center[1], pygame.mouse.get_pos()[0], Turret.gun.center[0])),
            (Turret.gun.center[0] - 17, Turret.gun.topleft[1] - 6))
        win.blit(rot_center(
            pl.Player.gfx_pictures[19], Turret.pd_angle - 90), (Turret.gun.center[0] - 6, Turret.gun.center[1] - 35))

    def update():
        Turret.gfx_gun_draw()
        Turret.missile_follow()
        Turret.nuke_fire()
        Turret.gfx_nuke(Turret.explosion)
        Turret.normal_shot()
        Turret.he_round_explosion()
        Turret.reloads()

        for shot, direction, _ in Turret.shot_lst:
            shot.move_ip(direction)
            # pygame.draw.rect(win, (255, 255, 0), shot)
            Turret.gfx_shot_animation(shot)
            if rect_not_on_sreen(shot):
                Turret.shot_lst.remove((shot, direction, _))
        for shot, direction, dmg in Turret.pd_lst:
            # pygame.draw.rect(win, (0, 255, 255), shot)
            win.blit(Turret.gfx_shot_pictures[10], (shot.topleft[0] - 5, shot.topleft[1] - 5))
            shot.move_ip(direction)
            if rect_not_on_sreen(shot):
                Turret.pd_lst.remove((shot, direction, dmg))

        if "point_defence" in it.Items.active_flag_lst:
            if it.Item_pd.active:
                win.blit(Turret.gfx_shot_pictures[14], (pl.Player.hitbox.topleft[0] - 190, pl.Player.hitbox.topleft[1] - 220))

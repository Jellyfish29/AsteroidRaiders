import pygame
from pygame.locals import *
import random
import time
from astraid_funcs import *


# Title: "Asteroid Raider"
# Author: Clemens Lütge
# CC-BY-NC-SA 4.0

pygame.init()
Clock = pygame.time.Clock()
winwidth = 1920
winheight = 1080
white = (255, 255, 255)
black = (0, 0, 0)
fps = 62
win = pygame.display.set_mode((winwidth, winheight), pygame.FULLSCREEN | pygame.DOUBLEBUF)
# win = pygame.display.set_mode((winwidth, winheight))
pygame.mouse.set_visible(False)


def test_mode():
    Player.max_health += 40000
    Player.health += 40000
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


class Gfx:

    gfx_cursor = get_images("cursor")
    bg = get_images("background")
    y = 0
    scroll_speed = 0.5

    def cursor():
        rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0, 0)
        win.blit(Gfx.gfx_cursor[2], (rect.topleft[0] - 9, rect.topleft[1] - 10))

    def background():
        Gfx.y += Gfx.scroll_speed
        win.blit(Gfx.bg[0], (0, Gfx.y - winheight * 6))
        win.blit(Gfx.bg[3], (0, Gfx.y - winheight * 5))
        win.blit(Gfx.bg[0], (0, Gfx.y - winheight * 4))
        win.blit(Gfx.bg[2], (0, Gfx.y - winheight * 3))
        win.blit(Gfx.bg[0], (0, Gfx.y - winheight * 2))
        win.blit(Gfx.bg[1], (0, Gfx.y - winheight))
        win.blit(Gfx.bg[0], (0, Gfx.y))
        if Gfx.y >= 6480:
            Gfx.y = 0


class Interface:

    gfx_pictures = get_images("icons")
    inter_lst = []
    tc = Time_controler()

    def __init__(self, color, location, icon_idx, font_size):
        self.font = pygame.font.SysFont("arial", font_size, 20)
        self.text = ""
        self.color = color
        self.text_render = self.font.render(self.text, True, color)
        self.location = location
        self.icon_idx = icon_idx
        self.rect = pygame.Rect(self.location[0], self.location[1], 1, 1)

    def draw(self):
        self.text_render = self.font.render(self.text, True, self.color)
        win.blit(self.text_render, self.rect)
        win.blit(Interface.gfx_pictures[self.icon_idx], (self.rect.topleft[0] - 50, self.rect.topleft[1] - 8))

    def create():
        for color, location, icon_idx, font_size in[
                ((255, 255, 255), (130, 20), 5, 30),  # Score
                ((255, 255, 255), (130, 55), 5, 30),  # Level
                ((255, 255, 255), (65, 1000), 3, 30),  # health
                ((255, 255, 255), (65, 920), 7, 25),   # repair
                ((255, 255, 255), (65, 860), 8, 25),  # shield
                ((255, 255, 255), (65, 800), 1, 25),  # super_shot
                ((255, 255, 255), (65, 740), 2, 25),  # star_shot
                ((255, 255, 255), (65, 150), 4, 20),  # Turret.nuke
                ((255, 255, 255), (65, 200), 9, 20),  # Turret.pd
                ((255, 255, 255), (65, 250), 10, 20),  # missile ammo
                ((255, 255, 255), (65, 300), 11, 20),  # jump charges
                ((255, 255, 255), (1885, 1045), 5, 25)  # FPS
        ]:
            Interface.inter_lst.append(Interface(color, location, icon_idx, font_size))

    def update():
        win.blit(Interface.gfx_pictures[13], (0, 0))
        for inter, text in zip(Interface.inter_lst, [
                f"Score = {Levels.display_score}",
                f"Level  = {Levels.display_level}",
                f"{Player.health}/{Player.max_health}",
                f"{Power_ups.heal_amount}",
                f"{Power_ups.shield_amount}",
                f"{Power_ups.super_shot_amount}",
                f"{Power_ups.star_shot_amount}",
                f"{int(Turret.nuke_ammo)}",
                f"{int(Turret.pd_ammo)}",
                f"{int(Turret.missile_ammo)}",
                f"{int(Player.jump_charges)}",
                f"{int(Clock.get_fps())}"
        ]):
            setattr(inter, "text", text)
            inter.draw()
        # Red Alert
        if Levels.boss_fight:
            win.blit(Interface.gfx_pictures[6], (420, 10))
        # Skill_up
        if Levels.skill_points > 0:
            ani_ticker = Interface.tc.animation_ticker(40)
            if ani_ticker < 30:
                win.blit(Interface.gfx_pictures[12], (49, 42))
            else:
                pass

    def upgrades(upgrades_pressed):
        pygame.mouse.set_visible(True)
        font = pygame.font.SysFont("fixed", 20)
        texts = [
            f"Skill Points = {Levels.skill_points}",
            f"{int(Player.speed)}      ++    Speed",  # len 57
            f"{Player.max_health}      ++    Max Health",
            f"{round(Player.damage, 2)}    ++    Damage",
            f"{round(1/ (Turret.fire_rate / 60), 2)}   ++    Fire Rate",
            f"{Turret.super_shot_ammo}     ++    Rapid Fire Ammo",
            f"{Turret.star_shot_ammo}     ++    Star Shot Ammo",
            f"{Power_ups.star_shot_tubes}      ++    Star Shot Tubes",
            f"{Power_ups.shield_time / 60}s   ++    Shield Duration",
            f"CIWIS Reload Rate        + 50%",
            f"AMRAAM Reload Rate       + 50%",
            f"MK II Nuke Reload Rate   + 50%",
            f"Jumpdrive Recharge Rate  + 50%"
        ]
        rects = [pygame.Rect(winwidth / 2 - 350 / 2, (winheight - 300) / 2 + i, 350, 30) for i in range(0, len(texts) * 30 + 1, 30)]
        render_lst = [(idx, font.render(text, False, (255, 255, 255)), rect) for idx, rect, text in zip([i for i in range(len(rects))], rects, texts)]
        while True:
            win.blit(Interface.gfx_pictures[14], (700, 250))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == KEYDOWN:
                    if event.key == K_TAB:
                        pygame.mouse.set_visible(False)
                        return
            mouse_pos = pygame.mouse.get_pos()
            # print(mouse_pos)
            # for rect in rects:
            #     pygame.draw.rect(win, (30, 30, 30), rect)
            for idx, text, rect in render_lst:
                win.blit(Interface.gfx_pictures[14], (winwidth / 2, winheight))
                win.blit(text, rect)
                if Levels.skill_points > 0:
                    if pygame.mouse.get_pressed()[0] == 1:
                        if rect.collidepoint(mouse_pos):
                            if idx == 1:
                                Player.speed += 0.5
                                Player.directions = directions(Player.speed)
                            elif idx == 2:
                                Player.max_health += 1
                                Player.health += 1
                            elif idx == 3:
                                Player.damage += Player.base_damage * 0.1
                            elif idx == 4:
                                if Turret.fire_rate >= 10:
                                    Turret.fire_rate -= 1.5
                                    Turret.normal_fire_rate[0] -= 1.5
                            elif idx == 5:
                                Turret.super_shot_ammo += 20
                            elif idx == 6:
                                Turret.star_shot_ammo += 10
                            elif idx == 7:
                                if Power_ups.star_shot_tubes < 14:
                                    Power_ups.star_shot_tubes += 2
                            elif idx == 8:
                                Power_ups.shield_time += 180
                            elif idx == 9:
                                Turret.pd_reload_speed += 0.002 * 0.5
                            elif idx == 10:
                                Turret.missile_reload_speed += 0.0005 * 0.5
                            elif idx == 11:
                                Turret.nuke_reload_speed += 0.0001 * 0.5
                            elif idx == 12:
                                Player.jump_recharge_rate += 0.0005 * 0.5
                            Levels.skill_points -= 1
                            pygame.mouse.set_visible(False)
                            return
            # win.blit(Interface.gfx_pictures[14], (winwidth / 2, winheight))
            Clock.tick(fps)
            pygame.display.update()


class Player:

    health = 4
    max_health = 4
    hitbox = pygame.Rect(winwidth / 2, winheight / 2, 70, 50)
    speed = 3
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
        elif not Power_ups.shield:
            Player.health -= damage
            Player.gfx_hit_effect()
        if Player.health <= 0:
            with open("score.txt", "a")as f:
                f.write(time.strftime("%H:%M:%S") + "   " + time.strftime("%d/%m/%Y") + "\nScore = " + str(Levels.display_score) + "\n")
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
                Player.hitbox.center = pygame.mouse.get_pos()
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


class Turret:

    # normal shot vlaues
    shot_lst = []
    angle = 0
    projectile_size = 6
    projectile_speed = 15
    firing = False
    direction = None
    normal_fire_rate = [30, 10]
    fire_rate = normal_fire_rate[0]
    ammunition = normal_fire_rate[1]
    fire_limiter = 0
    angles = angles_360(projectile_speed)
    tc = Time_controler()
    # super shot values
    super_shot_fire_rate = [5, 50]
    super_shot_ammo = super_shot_fire_rate[1]
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
    nuke_reload_speed = 0.0001
    # pd values
    pd_lst = []
    pd_angles = angles_360(25)
    pd_angle = 90
    pd_ticker = 0
    pd_ammo = 10
    pd_on = False
    pd_reload_speed = 0.002
    # missile values
    missile_fired = False
    missile_lst = []
    missile_angles = angles_360(10)
    missile_angle = 0
    missile_traget = None
    missile_ammo = 3
    missile_reload_speed = 0.0005
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
        Turret.nuke_fired = True
        if int(Turret.nuke_ammo) > 0:
            Turret.nuke_ammo -= 1
            Turret.nuke = pygame.Rect(Player.hitbox.center[0], Player.hitbox.center[1], 10, 10)
            Turret.nuke_degree = degrees(pygame.mouse.get_pos()[0], Player.hitbox.center[0], pygame.mouse.get_pos()[1], Player.hitbox.center[1])

    def point_defence(rect):  # degrees(Player.hitbox.center[0], self.hitbox.center[0], Player.hitbox.center[1], self.hitbox.center[1])
        if Turret.pd_on:
            pd_envelope = pygame.Rect(Player.hitbox.center[0] - 200, Player.hitbox.center[1] - 200, 400, 400)
            # pygame.draw.rect(win, (255, 255, 0), pd_envelope)
            if pd_envelope.colliderect(rect):
                Turret.pd_ticker += 1
                Turret.pd_angle = degrees(rect.center[0], Player.hitbox.center[0], rect.center[1], Player.hitbox.center[1] - 35)
                if int(Turret.pd_ammo) > 0:
                    if Turret.pd_ticker > 6:
                        Turret.pd_lst.append((pygame.Rect(Player.hitbox.center[0], Player.hitbox.center[1] - 35, 6, 6), Turret.pd_angles[Turret.pd_angle]))
                        Turret.pd_ammo -= 1
                        Turret.pd_ticker = 0

    def missile_aquisition(enemy):
        if Turret.missile_ammo > 0:
            if Turret.missile_fired:
                m_pos = pygame.mouse.get_pos()
                aa_target_area = pygame.Rect(m_pos[0] - 100, m_pos[1] - 100, 200, 200)
                # pygame.draw.rect(win, (255, 255, 0), aa_target_area)
                if aa_target_area.colliderect(enemy.hitbox):
                    Turret.missile_lst.append(pygame.Rect(Player.hitbox.topleft[0], Player.hitbox.topleft[1], 10, 10))
                    Turret.missile_lst.append(pygame.Rect(Player.hitbox.topright[0], Player.hitbox.topright[1], 10, 10))
                    Turret.missile_target = enemy
                    Turret.missile_ammo -= 1
                    Turret.missile_fired = False

    def missile_follow():
        if len(Turret.missile_lst) > 0:
            for missile in Turret.missile_lst:
                # pygame.draw.rect(win, (255, 0, 0), missile)
                if Turret.tc.delay(True, 20):
                    if not missile.colliderect(Turret.missile_target.hitbox):
                        if abs(Player.hitbox.center[0] - Turret.missile_target.hitbox.center[0]) > 10 or abs(Player.hitbox.center[1] - Turret.missile_target.hitbox.center[1]) > 10:
                            Turret.missile_angle = degrees(Turret.missile_target.hitbox.center[0], missile.center[0], Turret.missile_target.hitbox.center[1], missile.center[1])
                    elif missile.colliderect(Turret.missile_target.hitbox):
                        Turret.missile_lst.remove(missile)
                        Turret.tc.delay(False)
                else:
                    Turret.missile_angle = 90
                missile.move_ip(Turret.missile_angles[Turret.missile_angle])
                win.blit(gfx_rotate(Turret.gfx_shot_pictures[3], Turret.missile_angle - 90), (missile.topleft[0] - 5, missile.topleft[1] - 5))

    def pd_ammo_reload():
        Turret.pd_ammo += Turret.pd_reload_speed

    def nuke_reload(boss_kill):
        if boss_kill:
            Turret.nuke_ammo += 1
        else:
            Turret.nuke_ammo += Turret.nuke_reload_speed

    def missile_reload():
        Turret.missile_ammo += Turret.missile_reload_speed

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
        if Power_ups.super_shot:
            win.blit(Turret.gfx_shot_pictures[1], (shot.topleft[0] - 10, shot.topleft[1] - 10))
        elif Power_ups.star_shot:
            win.blit(Turret.gfx_shot_pictures[2], (shot.topleft[0] - 10, shot.topleft[1] - 10))
        else:
            win.blit(Turret.gfx_shot_pictures[0], (shot.topleft[0] - 10, shot.topleft[1] - 10))

    def gfx_hit_effect(shot):
        win.blit(Turret.gfx_hit_pictures[random.choice([0, 1, 2])], (shot.topleft[0] - 10, shot.topleft[1] - 10))

    def gun_draw():
        Turret.gun.center = Player.hitbox.center
        win.blit(rot_center(
            Player.gfx_pictures[18], degrees(pygame.mouse.get_pos()[0], Turret.gun.center[0], pygame.mouse.get_pos()[1], Turret.gun.center[1]) - 90),
            (Turret.gun.center[0] - 17, Turret.gun.topleft[1] - 6))
        win.blit(rot_center(
            Player.gfx_pictures[19], Turret.pd_angle - 90), (Turret.gun.center[0] - 6, Turret.gun.center[1] - 35))

    def update():
        # Method for main gameloop, everything that needs to be updated every tick

        # Gun indicator
        Turret.gun_draw()
        Turret.pd_ammo_reload()
        Turret.nuke_reload(False)
        Turret.missile_reload()
        Turret.missile_follow()
        # Shot creation
        if Turret.firing:
            if Turret.tc.trigger_1(Turret.fire_rate):
                # star_shot
                if Power_ups.star_shot:
                    Turret.angle = 0
                    Turret.star_shot_limiter += 1
                    Turret.ammunition = 1000
                    if Turret.star_shot_limiter > Turret.star_shot_ammo:
                        Turret.ammunition = Turret.normal_fire_rate[1]
                        Turret.star_shot_limiter = 0
                        Power_ups.star_shot = False
                    for i in range(0, 360, int(360 / Power_ups.star_shot_tubes)):
                        Turret.shot_lst.append(
                            (pygame.Rect(Player.hitbox.center[0], Player.hitbox.center[1], Turret.projectile_size, Turret.projectile_size), Turret.angles[Turret.angle + i]))
                # super_shot
                elif Power_ups.super_shot:
                    Turret.fire_rate, Turret.ammunition = Turret.super_shot_fire_rate
                    Turret.super_shot_limiter += 1
                    if Turret.super_shot_limiter >= Turret.super_shot_ammo:
                        Turret.fire_rate, Turret.ammunition = Turret.normal_fire_rate
                        Turret.super_shot_limiter = 0
                        Power_ups.super_shot = False
                # normal shot
                Turret.shot_lst.append(
                    (pygame.Rect(
                        Player.hitbox.center[0], Player.hitbox.center[1], Turret.projectile_size, Turret.projectile_size),
                        Turret.angles[degrees(pygame.mouse.get_pos()[0], Player.hitbox.center[0], pygame.mouse.get_pos()[1], Player.hitbox.center[1])]))
        if len(Turret.shot_lst) > Turret.ammunition:
            del(Turret.shot_lst)[Turret.ammunition]
        # Shot draw and border collision
        for shot, direction in Turret.shot_lst:
            shot.move_ip(direction)
            # pygame.draw.rect(win, (255, 255, 0), shot)
            Turret.gfx_shot_animation(shot)
            if rect_not_on_sreen(shot):
                Turret.shot_lst.remove((shot, direction))
        for shot, direction in Turret.pd_lst:
            # pygame.draw.rect(win, (0, 255, 255), shot)
            win.blit(Turret.gfx_shot_pictures[10], (shot.topleft[0] - 5, shot.topleft[1] - 5))
            shot.move_ip(direction)
            if rect_not_on_sreen(shot):
                Turret.pd_lst.remove((shot, direction))
        # nuke
        Turret.gfx_nuke(Turret.explosion)
        if Turret.nuke_fired:
            Turret.nuke.move_ip(Turret.nuke_angles[Turret.nuke_degree])
            # pygame.draw.rect(win, (150, 0, 0), Turret.nuke)
            if abs(Player.hitbox.center[0] - Turret.nuke.center[0]) > 400 or abs(Player.hitbox.center[1] - Turret.nuke.center[1]) > 400:
                Turret.explosion = False
                Turret.nuke.inflate_ip(20, 20)
                Turret.gfx_nuke_explosion()
                if abs(Turret.nuke.topleft[0] - Turret.nuke.center[0]) > 400:
                    Turret.nuke = pygame.Rect(-1000, -1000, 1, 1)
                    Turret.nuke_fired = False
                    Turret.gfx_ticker_ex = 0
                    Turret.explosion = True


class Enemy:

    enemy_lst = []
    speed = [2, 7]
    health = 2.6
    direction = (0, 79)
    size = (lambda speed=speed[1]: {speed + 1 - i: i * 15 for i in range(1, speed + 1)})()  # oof
    spawn_point = (1, 4)
    gfx_pictures_ast = get_images("asteroids")
    spez_gfx = get_images("spez")
    boss_gfx = get_images("boss_ship")

    def __init__(self, direction, speed, spawn_point, health):
        self.spawn_points = {
            1: [random.randint(100, winwidth - 50), random.randint(-150, -50)],  # Top
            2: [random.randint(100, winwidth - 50), random.randint(winheight + 50, winheight + 100)],  # Bot
            3: [random.randint(-150, -100), random.randint(0, winheight)],  # random.randint(0, winheight)),  # Left
            4: [random.randint(winwidth, winwidth + 50), random.randint(0, winheight)]  # Right
        }
        self.spawn_point = spawn_point
        self.direction = direction
        self.angles = angles_80(speed)
        self.hitbox = pygame.Rect(
            self.spawn_points[spawn_point][0], self.spawn_points[spawn_point][1], 70, 70)
        self.health = health
        self.max_health = self.health
        self.healthbar_len = 70
        self.healthbar_height = 1
        self.healthbar_max_len = self.healthbar_len
        self.score_amount = speed + 1
        self.speed = speed
        self.gfx_idx = 0
        self.animation_speed = Enemy.size[speed]
        self.typ = "normal"
        self.skill = "normal"
        self.enemy_tc = Time_controler()

    def draw(self):
        self.hitbox.move_ip(self.angles[int(self.direction)])
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)

    def gfx_health_bar(self):
        if self.health < self.max_health:
            pygame.draw.rect(win, (200, 0, 0), (pygame.Rect(self.hitbox.topleft[0], self.hitbox.topleft[1] - 30, self.healthbar_max_len, self.healthbar_height)))
            pygame.draw.rect(win, (0, 200, 0), (pygame.Rect(self.hitbox.topleft[0], self.hitbox.topleft[1] - 30, self.healthbar_len, self.healthbar_height)))

    def border_collide(self):
        return rect_not_on_sreen(self.hitbox, bot=False, strict=False)

    def player_collide(self):
        return self.hitbox.colliderect(Player.hitbox)

    def hit_detection(self, missile_hit):
        for missile in Turret.missile_lst:
            if self.hitbox.colliderect(missile):
                self.health -= Player.damage * 4
                self.healthbar_len -= (self.healthbar_max_len / (self.max_health / (Player.damage * 4)))
                Turret.missile_lst.remove(missile)
        if self.hitbox.colliderect(Turret.nuke):
            self.health -= 1.5
            self.healthbar_len -= (self.healthbar_max_len / (self.max_health / 2))
        for shot, _ in Turret.shot_lst:
            if self.hitbox.colliderect(shot):
                Turret.gfx_hit_effect(shot)
                Turret.shot_lst.remove((shot, _))
                self.health -= Player.damage
                self.healthbar_len -= (self.healthbar_max_len / (self.max_health / Player.damage))
        if self.skill == "seeker" or self.skill == "jumper":
            for shot, _ in Turret.pd_lst:
                if shot.colliderect(self.hitbox):
                    self.health -= 1
                    self.healthbar_len -= (self.healthbar_max_len / (self.max_health / 1))
                    Turret.pd_lst.remove((shot, _))
        if self.health <= 0:
            Levels.display_score += self.score_amount
            Levels.interval_score += self.score_amount
            Power_ups.score += self.score_amount
            return True

    def gfx_animation(self):
        if self.typ == "normal":
            animation_ticker = self.enemy_tc.animation_ticker(self.animation_speed * len(Enemy.gfx_pictures_ast))
            if animation_ticker == (self.animation_speed * len(Enemy.gfx_pictures_ast)):  # 480
                self.gfx_idx = 0
            if animation_ticker % self.animation_speed == 0:
                self.gfx_idx += 1
                if self.gfx_idx == len(Enemy.gfx_pictures_ast):
                    self.gfx_idx = 0
            win.blit(Enemy.gfx_pictures_ast[self.gfx_idx], (self.hitbox.topleft[0] - 8, self.hitbox.topleft[1] - 15))
        elif self.typ == "seeker" or self.typ == "shooter" or self.typ == "add":
            animation_ticker = self.enemy_tc.animation_ticker(6)
            if animation_ticker < 3:
                win.blit(Enemy.spez_gfx[self.gfx_idx[0]], (self.hitbox.center[0] - self.gfx_hook[0], self.hitbox.center[1] - self.gfx_hook[1]))
            else:
                win.blit(Enemy.spez_gfx[self.gfx_idx[1]], (self.hitbox.center[0] - self.gfx_hook[0], self.hitbox.center[1] - self.gfx_hook[1]))
        elif self.typ != "normal" or self.typ != "seeker" or self.typ != "shooter":
            animation_ticker = self.enemy_tc.animation_ticker(10)
            if animation_ticker < 5:
                win.blit(Enemy.boss_gfx[self.gfx_idx[0]], (self.hitbox.center[0] - self.gfx_hook[0], self.hitbox.center[1] - self.gfx_hook[1]))
            else:
                win.blit(Enemy.boss_gfx[self.gfx_idx[1]], (self.hitbox.center[0] - self.gfx_hook[0], self.hitbox.center[1] - self.gfx_hook[1]))

    def update():
        # Method for main gameloop

        # Enemy instance creation
        if not Levels.boss_fight:
            while len(Enemy.enemy_lst) < Levels.enemy_amount:
                Enemy.enemy_lst.append(Enemy(
                    random.randint(Enemy.direction[0], Enemy.direction[1]),
                    random.randint(Enemy.speed[0], Enemy.speed[1]),
                    random.randint(Enemy.spawn_point[0], Enemy.spawn_point[1]),
                    Enemy.health
                ))
        # Enemy draw and collision detection Border/Player/Shot
        for enemy in Enemy.enemy_lst:
            enemy.draw()
            enemy.gfx_animation()
            enemy.gfx_health_bar()
            Turret.missile_aquisition(enemy)
            if enemy.border_collide() or enemy.hit_detection(False):
                Enemy.enemy_lst.remove(enemy)
            elif enemy.player_collide():
                if Power_ups.shield:
                    enemy.health = 0
                else:
                    Player.hit(1)
                    Enemy.enemy_lst.remove(enemy)


class Spez_enemy(Enemy):

    lst = []
    shot_lst = []
    amount = 1
    health = 2
    shot_gfx = get_images("projectile")

    def __init__(self, typ, spawn):
        self.typ = typ
        self.score_amount = 10
        self.spez_tc = Time_controler()
        self.gfx_hook = (40, 50)
        if self.typ == "seeker":
            super().__init__(1, 4, spawn, Spez_enemy.health + 1)  # direction, speed, spawnpoint, health
            self.angles = angles_360(self.speed)
            self.gfx_idx = (8, 9)
            self.skill, self.typ = typ, typ
            self.score_amount += 2
        elif self.typ == "jumper":
            super().__init__(random.randint(1, 79), 7, spawn, Spez_enemy.health)
            self.dir_change_interval = random.randint(5, 40)
            self.skill, self.typ = typ, "normal"
            self.score_amount += 4
        elif self.typ == "shooter":
            super(). __init__(1, random.randint(4, 6), spawn, Spez_enemy.health + 2)
            for sp, direction, gfx_idx in [(1, 40, (2, 3)), (2, 79, (6, 7)), (3, 20, (0, 1)), (4, 60, (4, 5))]:
                if self.spawn_point == sp:
                    self.direction = direction
                    self.gfx_idx = gfx_idx
            self.shot_angle = 0
            self.shot_angles = angles_360(7)
            self.fire_rate = random.randint(60, 100)
            self.skill, self.typ = typ, typ
            self.score_amount += 3

    def skills(self):
        # Seeker
        if self.skill == "seeker":
            self.direction = degrees(Player.hitbox.center[0], self.spawn_points[self.spawn_point][0], Player.hitbox.center[1], self.spawn_points[self.spawn_point][1])
            if abs(Player.hitbox.center[0] - self.hitbox.center[0]) > 20 or abs(Player.hitbox.center[1] - self.hitbox.center[1]) > 20:
                self.spawn_points[self.spawn_point][0] = self.hitbox.center[0]
                self.spawn_points[self.spawn_point][1] = self.hitbox.center[1]
        # jumper
        elif self.skill == "jumper":
            if self.spez_tc.trigger_1(self.dir_change_interval):
                self.direction = random.randint(0, 79)
        # shooter
        elif self.skill == "shooter":
            self.shot_angle = degrees(Player.hitbox.center[0], self.hitbox.center[0], Player.hitbox.center[1], self.hitbox.center[1])
            if self.spez_tc.trigger_2(self.fire_rate):
                Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1], 7, 7), self.shot_angles[int(self.shot_angle)]))

    def gfx_shot(rect):
        win.blit(Spez_enemy.shot_gfx[6], (rect))

    def spez_event(kind):
        if not Levels.boss_fight:
            Levels.spez_event_trigger = 0
            spawn = random.randint(1, 4)
            if kind == "wave":
                for i in range(15):
                    Enemy.enemy_lst.append(Enemy(40, 5, 1, Enemy.health))
            elif kind == "jumper":
                for i in range(10 + Levels.level):
                    Spez_enemy.lst.append(Spez_enemy(kind, spawn))
            elif kind == "shooter":
                for i in range(3 + int(Levels.level / 6)):
                    Spez_enemy.lst.append(Spez_enemy(kind, spawn))
            elif kind == "seeker":
                for i in range(2 + int(Levels.level / 10)):
                    Spez_enemy.lst.append(Spez_enemy(kind, spawn))

    def update():
        # create instances
        if not Levels.boss_fight:
            while len(Spez_enemy.lst) < Spez_enemy.amount:
                Spez_enemy.lst.append(Spez_enemy(random.choice(["shooter", "seeker", "jumper"]), random.randint(1, 4)))  # "seeker", random.randint(1, 4)))
        # draw, update, skills, ...
        for spez in Spez_enemy.lst:
            spez.draw()
            spez.gfx_animation()
            spez.skills()
            spez.gfx_health_bar()
            if spez.skill == "seeker" or spez.skill == "jumper":
                Turret.point_defence(spez.hitbox)
            Turret.missile_aquisition(spez)
            if spez.border_collide() or spez.hit_detection(False):
                Spez_enemy.lst.remove(spez)
            elif spez.player_collide():
                Spez_enemy.lst.remove(spez)
                Player.hit(1)
        # Shot draw / hitdetection
        for shot, angle in Spez_enemy.shot_lst:
            shot.move_ip(angle)
            Spez_enemy.gfx_shot(shot)
            # pygame.draw.rect(win, (255, 0, 0), shot)
            if shot.colliderect(Player.hitbox):
                Player.hit(1)
                Spez_enemy.shot_lst.remove((shot, angle))
            if rect_not_on_sreen(shot, bot=False, strict=False):
                Spez_enemy.shot_lst.remove((shot, angle))


class Bosses(Spez_enemy):

    shot_lst = []
    mine_lst = []
    missile_lst = []
    main_gun_lst = []
    boss_lst = []

    def __init__(self, typ, health, speed, fire_rate, boss_skill, move_pattern, size, gfx_idx, gfx_hook):
        self.checkpoints = {
            0: (winwidth / 2, 300),             # topmid
            1: (300, 300),                      # topleft
            2: (winwidth - 300, 300),           # topright
            3: (300, winheight / 2),             # midleft
            4: (winwidth - 300, winheight / 2),   # midright
            5: (300, winheight - 300),             # leftbot
            6: (winwidth - 300, winheight - 300),  # rightbot
            7: (winwidth / 2, winheight - 100),   # midbot
            8: (winwidth / 2, 600),
            9: (winwidth / 2, 610)
        }
        self.orig_gfx_idx = gfx_idx
        self.gfx_idx = gfx_idx
        self.gfx_hook = gfx_hook
        self.enemy_tc = Time_controler()
        self.cp_ticker = 0
        self.direction = 0
        self.healthbar_len = 100
        self.healthbar_height = 5
        self.healthbar_max_len = self.healthbar_len
        self.shot_angle = 0
        self.shot_angles = angles_360(7)  # projectilespeed
        self.spez_tc = Time_controler()
        self.score_amount = 400
        self.health = health
        self.max_health = self.health
        self.speed = speed
        self.fire_rate = fire_rate
        self.boss_skill = boss_skill
        self.skill = "shooter"
        self.move_pattern = move_pattern
        self.typ = typ
        self.size = size
        self.directions = angles_360(self.speed)
        self.hitbox = pygame.Rect(winwidth / 2, -250, size[0], size[1])
        self.enrage_trigger = self.health * 0.15
        if "mines" in self.boss_skill:
            self.mine_tc = Time_controler()
            self.mine_trigger = 220
            self.mine_angles = angles_360(10)
        if "seeker_missiles" in self.boss_skill:
            self.missile_tc = Time_controler()
            self.missile_duration = 480
            self.missile_angles = angles_360(6)
            self.missile_retarget_trigger = 90
            self.missile_direction = 270
        if "salvo" in self.boss_skill:
            self.salvo_tc = Time_controler()
        if "volley" in self.boss_skill:
            self.volley_tc = Time_controler()
        if "main_gun" in self.boss_skill:
            self.mg_angle = 0
            self.main_gun_tc = Time_controler()
            self.main_gun_angles = angles_360(35)
        if "jumpdrive" in self.boss_skill:
            self.jumpdrive_tc = Time_controler()
            self.jump_charge = False
            self.jump_point = 0
            self.jump_chance = 1100
        if self.typ == "CA":
            self.add_respawn_time = 720
        if self.typ == "BB":
            self.add_respawn_time = 600

    def gfx_direction(self):
        if self.direction > 45 and self.direction < 135:  # up
            self.gfx_idx = self.orig_gfx_idx
        elif self.direction > 135 and self.direction < 225:  # left
            self.gfx_idx = [i + 2 for i in self.orig_gfx_idx]
        elif self.direction > 225 and self.direction < 315:  # down
            self.gfx_idx = [i + 4 for i in self.orig_gfx_idx]
        elif self.direction < 45 or self.direction > 315:  # right
            self.gfx_idx = [i + 6 for i in self.orig_gfx_idx]

    def move(self):
        rel_x, rel_y = self.checkpoints[self.move_pattern[self.cp_ticker]][0] - self.hitbox.center[0], self.checkpoints[self.move_pattern[self.cp_ticker]][1] - self.hitbox.center[1]
        self.direction = -math.atan2(rel_y, rel_x)
        self.direction = math.degrees(self.direction)
        if self.direction < 0:
            self.direction += 360
        self.hitbox.move_ip(self.directions[int(self.direction)])
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        if self.hitbox.collidepoint(self.checkpoints[self.move_pattern[self.cp_ticker]]):
            self.cp_ticker += 1
            if self.cp_ticker > len(self.move_pattern) - 1:
                self.cp_ticker = 0

    def enrage(self):
        if self.health < self.enrage_trigger:
            self.fire_rate -= self.fire_rate * 0.5
            self.speed += 2
            self.directions = angles_360(self.speed)
            if "mines" in self.boss_skill:
                self.mine_trigger -= 100
            if "seeker_missiles" in self.boss_skill:
                self.missile_retarget_trigger -= 45
            if "jumpdrive" in self.boss_skill:
                self.jump_chance -= 250
            if "adds" in self.boss_skill:
                self.add_respawn_time -= 120
            self.enrage_trigger = -10

    def boss_skills(self):
        # mines
        if "mines" in self.boss_skill:
            if self.mine_tc.trigger_1(self.mine_trigger):
                Bosses.mine_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1], 20, 20), pygame.Rect(self.hitbox.center[0] - 175, self.hitbox.center[1] - 175, 350, 350)))
                if len(Bosses.mine_lst) > 15:
                    del Bosses.mine_lst[15]
            for mine, envelope in Bosses.mine_lst:
                Turret.point_defence(mine)
                # pygame.draw.rect(win, (100, 100, 0), envelope)
                # pygame.draw.rect(win, (100, 0, 0), mine)
                win.blit(Spez_enemy.shot_gfx[12], (mine.topleft[0] - 5, mine.topleft[1] - 5))
                win.blit(Spez_enemy.shot_gfx[13], (envelope.topleft[0] - 27, envelope.topleft[1] - 27))
                if envelope.colliderect(Player.hitbox):
                    mine_direction = degrees(Player.hitbox.center[0], mine.center[0], Player.hitbox.center[1], mine.center[1])
                    mine.move_ip(self.mine_angles[int(mine_direction)])
                    envelope.move_ip(self.mine_angles[int(mine_direction)])
                    if mine.colliderect(Player.hitbox):
                        Player.hit(1)
                        Bosses.mine_lst.remove((mine, envelope))
                for shot, _ in Turret.shot_lst + Turret.pd_lst:
                    if mine.colliderect(shot):
                        try:
                            Bosses.mine_lst.remove((mine, envelope))
                            Turret.shot_lst.remove((shot, _))
                        except ValueError:
                            pass
                if mine.colliderect(Turret.nuke):
                    Bosses.mine_lst.remove((mine, envelope))
        # seeker missile
        if "seeker_missiles" in self.boss_skill:
            if self.missile_tc.trigger_1(self.missile_duration) or len(Bosses.missile_lst) == 0:
                Bosses.missile_lst.clear()
                self.missile_direction = 270
                Bosses.missile_lst.append(pygame.Rect(self.hitbox.center[0], self.hitbox.center[1], 20, 20))
            for missile in Bosses.missile_lst:
                Turret.point_defence(missile)
                # pygame.draw.rect(win, (230, 40, 0), missile)
                if self.missile_tc.trigger_2(self.missile_retarget_trigger):
                    if abs(Player.hitbox.center[0] - missile.center[0]) > 1 or abs(Player.hitbox.center[1] - missile.center[1]) > 1:
                        self.missile_direction = degrees(Player.hitbox.center[0], missile.center[0], Player.hitbox.center[1], missile.center[1])
                win.blit(gfx_rotate(Spez_enemy.shot_gfx[11], self.missile_direction - 90), (missile.topleft[0] - 10, missile.topleft[1] - 10))
                missile.move_ip(self.missile_angles[self.missile_direction])
                if missile.colliderect(Player.hitbox):
                    Player.hit(1)
                    Bosses.missile_lst.remove(missile)
                elif rect_not_on_sreen(missile, strict=True):
                    Bosses.missile_lst.remove(missile)
                for shot, _ in Turret.pd_lst:
                    if shot.colliderect(missile):
                        try:
                            Bosses.missile_lst.remove(missile)
                            Turret.pd_lst.remove((shot, _))
                        except ValueError:
                            pass
            if len(Bosses.missile_lst) > 1:
                del Bosses.missile_lst[1]
        # salvo fire
        if "salvo" in self.boss_skill:
            if self.salvo_tc.trigger_1(self.fire_rate * 5):
                for i in range(135, 225, 15):
                    Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0] - self.size[0] / 2, self.hitbox.center[1], 7, 7), self.shot_angles[i]))
                for i in range(0, 45, 15):
                    Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0] + self.size[0] / 2, self.hitbox.center[1], 7, 7), self.shot_angles[i]))
                for i in range(315, 360, 15):
                    Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0] + self.size[0] / 2, self.hitbox.center[1], 7, 7), self.shot_angles[i]))
        # volley fire
        if "volley" in self.boss_skill:
            if self.volley_tc.trigger_1(self.fire_rate * 3):
                for i in range(-20, 20, 20):
                    try:
                        Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0] - self.size[0] / 2, self.hitbox.center[1], 7, 7), self.shot_angles[self.shot_angle + i]))
                    except KeyError:
                        if i < 0:
                            Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0] - self.size[0] / 2, self.hitbox.center[1], 7, 7), self.shot_angles[self.shot_angle + i + 360]))
                        else:
                            Spez_enemy.shot_lst.append((pygame.Rect(self.hitbox.center[0] - self.size[0] / 2, self.hitbox.center[1], 7, 7), self.shot_angles[self.shot_angle + i - 360]))
        # main Gun
        if "main_gun" in self.boss_skill:
            if self.main_gun_tc.delay(True, self.fire_rate * 6):
                Bosses.main_gun_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1] + self.size[1] / 2, 4, 4), False, 7))
                if "main_gun_2"in self. boss_skill:
                    Bosses.main_gun_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1] - self.size[1] / 2, 4, 4), False, 7))
                if self.main_gun_tc.trigger_2(100):
                    Bosses.main_gun_lst.clear()
                    Bosses.main_gun_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1] + self.size[1] / 2, 30, 30), True, 8))
                    if "main_gun_2"in self. boss_skill:
                        Bosses.main_gun_lst.append((pygame.Rect(self.hitbox.center[0], self.hitbox.center[1] - self.size[1] / 2, 30, 30), True, 8))
                    self.main_gun_tc.delay(False)
            for idx, (main_gun, fire, gfx_idx) in enumerate(Bosses.main_gun_lst):
                # if not fire:
                if "main_gun_2" in self.boss_skill:
                    if idx % 2 == 0:
                        self.mg_angle = degrees(Player.hitbox.center[0], self.hitbox.center[0], Player.hitbox.center[1], (self.hitbox.center[1] + self.size[1] / 2))
                    else:
                        self.mg_angle = degrees(Player.hitbox.center[0], self.hitbox.center[0], Player.hitbox.center[1], (self.hitbox.center[1] - self.size[1] / 2))
                else:
                    self.mg_angle = degrees(Player.hitbox.center[0], self.hitbox.center[0], Player.hitbox.center[1], (self.hitbox.center[1] + self.size[1] / 2))
                if fire:
                    if main_gun.colliderect(Player.hitbox):
                        Player.hit(1)
                if rect_not_on_sreen(main_gun):
                    Bosses.main_gun_lst.remove((main_gun, fire, gfx_idx))
                main_gun.move_ip(self.main_gun_angles[self.mg_angle])
                win.blit(Spez_enemy.shot_gfx[gfx_idx], (main_gun.topleft[0], main_gun.topleft[1] - 8))
                # pygame.draw.rect(win, (255, 0, 0), main_gun)
        if "jumpdrive" in self.boss_skill:
            if not self.jump_charge:
                jumpdrive_trigger = random.randint(1, self.jump_chance)
                if jumpdrive_trigger == 1:
                    self.jump_point = self.checkpoints[random.choice([1, 2, 3, 4])]
                    jumpdrive_trigger = 0
                    self.jump_charge = True
            if self.jump_charge:
                # pygame.draw.rect(win, (0, 0, 100), pygame.Rect(self.jump_point, self.size))
                if self.typ == "CA":
                    win.blit(Enemy.boss_gfx[40], self.jump_point)
                elif self.typ == "BB":
                    win.blit(Enemy.boss_gfx[41], self.jump_point)
                if self.jumpdrive_tc.trigger_1(60):
                    self.hitbox.topleft = self.jump_point
                    self.jump_charge = False
        if "adds" in self.boss_skill:
            if self.typ == "CA":
                Boss_adds.create(1, self.add_respawn_time, [])
            elif self.typ == "BB":
                Boss_adds.create(2, self.add_respawn_time, ["volley"])

    def create(lvl):
        # typ, health, speed, fire_rate, boss_skill, move_pattern, size(), gfx_idx(), gfx_hook() // Skills: "mines", "seeker_missiles", "salvo", "volley", "main_gun", "main_gun_2"
        if lvl == 5:  # The Corvette
            Bosses.boss_lst.append(Bosses("corv", 250, 5, 90, ["mines", "volley"], (0, 1, 2, 3, 4, 5, 6), (80, 180), [0, 1], (50, 120)))
        elif lvl == 10:  # The Frigate
            Bosses.boss_lst.append(Bosses("FF", 350, 3, 60, ["seeker_missiles", "salvo", "volley"], (0, 1, 2, 3), (100, 220), (8, 9), (65, 120)))
        elif lvl == 15:  # The Destroyerd
            Bosses.boss_lst.append(Bosses("DD", 600, 2, 60, ["seeker_missiles", "mines", "salvo", "volley"], (0, 7), (120, 260), (16, 17), (70, 140)))
        elif lvl == 20:  # The Cruiser
            Bosses.boss_lst.append(Bosses("CA", 1000, 1, 50, ["seeker_missiles", "salvo", "main_gun", "jumpdrive", "adds"], (8, 9), (130, 240), (24, 25), (80, 180)))
        elif lvl == 25:  # The Batleship
            Bosses.boss_lst.append(Bosses("BB", 1600, 1, 70, ["salvo", "volley", "main_gun", "main_gun_2", "jumpdrive", "seeker_missiles", "adds"], (8, 9), (140, 360), (32, 33), (80, 220)))

    def update():
        if Levels.boss_fight:
            for boss in Bosses.boss_lst:
                boss.move()
                boss.skills()
                boss.boss_skills()
                boss.gfx_direction()
                boss.gfx_animation()
                boss.gfx_health_bar()
                boss.enrage()
                Turret.missile_aquisition(boss)
                if boss.player_collide():
                    Player.hit(1)
                if boss.hit_detection(False):
                    Bosses.boss_lst.remove(boss)
                    Bosses.mine_lst.clear()
                    Bosses.missile_lst.clear()
                    Turret.nuke_reload(True)
                    Levels.skill_points += 2
                    Levels.boss_fight = False


class Boss_adds(Bosses):

    add_lst = []
    tc = Time_controler()

    def __init__(self, move_pattern, skills):
        Bosses.__init__(self, "add", 2, 5, 120, skills, move_pattern, (20, 50), 0, 0)
        self.checkpoints = {
            0: (400, 750),
            1: (700, 750),
            2: (700, 850),
            3: (400, 850),
            4: (winwidth - 400, 750),
            5: (winwidth - 700, 750),
            6: (winwidth - 700, 850),
            7: (winwidth - 400, 850)
        }
        self.score_amount = 10
        self.gfx_idx = (10, 11)
        self.gfx_hook = (17, 30)
        self.healthbar_len = 50
        self.healthbar_max_len = 50
        self.healthbar_height = 1

    def create(amount, respawn_speed, skills):
        if Boss_adds.tc.trigger_1(respawn_speed) and len(Boss_adds.add_lst) < amount:
            Boss_adds.add_lst.append(Boss_adds((0, 1, 2, 3, 4, 5, 6, 7), skills))
            if amount == 2 and len(Boss_adds.add_lst) < amount:
                Boss_adds.add_lst.append(Boss_adds((7, 6, 5, 4, 3, 2, 1, 0), skills))

    def update():
        for add in Boss_adds.add_lst:
            add.move()
            add.skills()
            add.boss_skills()
            add.gfx_health_bar()
            add.gfx_animation()
            Turret.missile_aquisition(add)
            if add.player_collide():
                Player.hit(1)
            if add.hit_detection(False):
                Boss_adds.add_lst.remove(add)


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
        return self.hitbox.colliderect(Player.hitbox)

    def hit_detection(self):
        for shot, _ in Spez_enemy.shot_lst:
            if self.hitbox.colliderect(shot):
                Spez_enemy.shot_lst.remove((shot, _))
        for shot, _ in Turret.shot_lst:
            if self.hitbox.colliderect(shot):
                Turret.gfx_hit_effect(shot)
                Turret.shot_lst.remove((shot, _))

    def create():
        if not Levels.boss_fight:
            for i in range(Levels.blocker_amount):
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
                Player.hit(True)


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

    def level_up():
        if Levels.interval_score > Levels.level_interval:
            # Levels.enemy_amount += Levels.enemys_per_level
            Levels.level += 1
            Levels.display_level += 1
            Levels.level_interval += 10
            Power_ups.interval += 1
            Levels.skill_points += 1
            if not Levels.level % 5 == 1:
                Levels.spez_event_trigger = random.randint(1, 4)
            Levels.boss_trigger()
            Levels.enemy_scaling()
            Levels.interval_score = 0

    def boss_trigger():
        if Levels.level % 5 == 0:
            Bosses.create(Levels.level)
            Levels.boss_fight = True
            Gfx.scroll_speed += 1

    def enemy_scaling():
        Enemy.health += 0.2
        Spez_enemy.health += 0.3
        if Levels.level % 10 == 0:
            Spez_enemy.amount += 1
        elif Levels.level % 3 == 0:
            Levels.enemy_amount += 1
        elif Levels.level % 15 == 0:
            Levels.blocker_amount += 1


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
        if self.hitbox.colliderect(Player.hitbox):
            if self.typ == "heal":
                Power_ups.heal_amount += 1
            elif self.typ == "super_shot":
                Turret.super_shot_limiter = 0  # reset bei erneutem einsammeln
                Power_ups.super_shot_amount += 1
            elif self.typ == "star_shot":
                Turret.super_star_limiter = 0
                Power_ups.star_shot_amount += 1
            elif self.typ == "shield":
                Power_ups.shield_amount += 1
            return True
        return rect_not_on_sreen(self.hitbox, True)

    def use(pup_name):
        if pup_name == "super_shot":
            if Power_ups.super_shot_amount > 0:
                Power_ups.super_shot = True
                Power_ups.super_shot_amount -= 1
        elif pup_name == "star_shot":
            if Power_ups.star_shot_amount > 0:
                Power_ups.star_shot = True
                Power_ups.star_shot_amount -= 1
        elif pup_name == "shield":
            if Power_ups.shield_amount > 0:
                Power_ups.shield_amount -= 1
                Power_ups.shield_ticker = 0
                Power_ups.shield = True
        elif pup_name == "heal":
            if Power_ups.heal_amount > 0:
                Power_ups.heal_amount -= 1
                Player.health += Power_ups.heal_strength
                if Player.health > Player.max_health:
                    Player.health = Player.max_health

    def draw(self):
        self.hitbox.move_ip(0, 1)
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
        shield_rect = pygame.Rect(Player.hitbox.topleft[0] - 25, Player.hitbox.topleft[1] - 25, 100, 100)
        win.blit(Power_ups.gfx_pictures[6], (shield_rect.topleft[0] - 15, shield_rect.topleft[1] - 40))
        # pygame.draw.rect(win, (0, 240, 220), shield_rect)

    def spawn():
        if Power_ups.score > Power_ups.interval:
            Power_ups.score = 0
            return True

    def update():
        if Power_ups.spawn():
            if Player.health == 1:
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
    Interface.upgrades(True)

    while True:
        # print(Clock.get_fps())
        # win.fill(black)
        # print(len(Spez_enemy.shot_lst))
        Gfx.background()
        Blocker.update()
        Power_ups.update()
        Player.update()
        Turret.update()
        Enemy.update()
        Spez_enemy.update()
        Bosses.update()
        Boss_adds.update()
        Interface.update()
        Levels.level_up()
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
                    Interface.upgrades(True)
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
                elif event.key == K_LSHIFT:
                    Player.speed_boost(True)
                elif event.key == K_f:
                    Player.jumpdrive(False)
                elif event.key == K_l:
                    test_mode()
                elif event.key == K_r:
                    if not Turret.pd_on:
                        Turret.pd_on = True
                    else:
                        Turret.pd_on = False
                elif event.key == K_SPACE:
                    Turret.missile_fired = True
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
                elif event.key == K_LSHIFT:
                    Player.speed_boost(False)
                elif event.key == K_SPACE:
                    Turret.missile_fired = False
                elif event.key == K_f:
                    Player.jumpdrive(True)
                elif event.key == K_ESCAPE:
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

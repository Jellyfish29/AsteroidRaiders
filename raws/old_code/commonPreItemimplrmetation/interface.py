from pygame.locals import *
import pygame

from init import *
from astraid_funcs import *
import player as pl
import levels as lvl
import turret as tr
import power_ups as pup
""" Player class:
        Attributes: Player.health, Player.max_health, Player.speed, Player.damage, Player.base_damage, Player.jump_charges, Player.jump_charge_rate
    Levels class: 
        Attributes: Levels.display_score, Levels.display_level, Levels.skill_points, Levels.boss_fight
    Turret class:
        Attributes: Turret.nuke_ammo, Turret.pd_ammo, Turret.missile_ammo, Turret.super_shot_ammon, Turret.star_shot_ammo, Turret.fire_rate
                    Turret.pd_reload_speed, Turret.missile_reload_speed, Turret.nuke_reload_speed, Turret.normal_fire_rate
    Power_ups:
        Attributes: Power_ups.shield_amount, Power_ups.star_shot_amount, Power_ups.super_shot_amount, Power_ups.heal_amount, Power_ups.star_shot_tubes
                    Power_ups.shield_time
"""


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
                ((255, 255, 255), (65, 920), 2, 25),   # repair
                ((255, 255, 255), (65, 860), 1, 25),  # shield
                ((255, 255, 255), (65, 800), 8, 25),  # super_shot
                ((255, 255, 255), (65, 740), 7, 25),  # star_shot
                ((255, 255, 255), (65, 1000), 3, 30),  # health
                ((255, 255, 255), (65, 150), 4, 20),  # tr.Turret.nuke
                ((255, 255, 255), (65, 200), 9, 20),  # tr.Turret.pd
                ((255, 255, 255), (65, 250), 10, 20),  # missile ammo
                ((255, 255, 255), (65, 300), 11, 20),  # jump charges
                ((255, 255, 255), (1885, 1045), 5, 25)  # FPS
        ]:
            Interface.inter_lst.append(Interface(color, location, icon_idx, font_size))

    def update():
        win.blit(Interface.gfx_pictures[13], (0, 0))
        for inter, text in zip(Interface.inter_lst, [
                f"Score = {lvl.Levels.display_score}",
                f"Level  = {lvl.Levels.display_level}",
                f"{pup.Power_ups.star_shot_amount}",
                f"{pup.Power_ups.super_shot_amount}",
                f"{pup.Power_ups.shield_amount}",
                f"{pup.Power_ups.heal_amount}",
                f"{pl.Player.health}/{pl.Player.max_health}",
                f"{int(tr.Turret.nuke_ammo)}",
                f"{int(tr.Turret.pd_ammo)}",
                f"{int(tr.Turret.missile_ammo)}",
                f"{int(pl.Player.jump_charges)}",
                f"{int(Clock.get_fps())}"
        ]):
            setattr(inter, "text", text)
            inter.draw()
        # Red Alert
        if lvl.Levels.boss_fight:
            win.blit(Interface.gfx_pictures[6], (420, 10))
        # Skill_up
        if lvl.Levels.skill_points > 0:
            ani_ticker = Interface.tc.animation_ticker(40)
            if ani_ticker < 30:
                win.blit(Interface.gfx_pictures[12], (49, 42))
            else:
                pass

    def upgrades(upgrades_pressed):
        pygame.mouse.set_visible(True)
        font = pygame.font.SysFont("fixed", 22)
        texts = [
            f"Skill Points = {lvl.Levels.skill_points}",
            f"{int(pl.Player.speed)}      ++    Speed",  # len 57
            f"{pl.Player.max_health}      ++    Max Health",
            f"{round(pl.Player.damage, 2)}    ++    Damage",
            f"{round(1/ (tr.Turret.fire_rate / 60), 2)}   ++    Fire Rate",
            f"{tr.Turret.super_shot_ammo}     ++    Rapid Fire Ammo",
            f"{tr.Turret.star_shot_ammo}     ++    Star Shot Ammo",
            f"{pup.Power_ups.star_shot_tubes}      ++    Star Shot Tubes",
            f"{pup.Power_ups.shield_time / 60}s   ++    Shield Duration",
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
                if lvl.Levels.skill_points > 0:
                    if pygame.mouse.get_pressed()[0] == 1:
                        if rect.collidepoint(mouse_pos):
                            if idx == 1:
                                pl.Player.speed += 1
                                pl.Player.directions = directions(pl.Player.speed)
                            elif idx == 2:
                                pl.Player.max_health += 1
                                pl.Player.health += 1
                            elif idx == 3:
                                pl.Player.damage += pl.Player.base_damage * 0.1
                            elif idx == 4:
                                if tr.Turret.fire_rate >= 10:
                                    tr.Turret.fire_rate -= 1.5
                                    tr.Turret.normal_fire_rate[0] -= 1.5
                            elif idx == 5:
                                tr.Turret.super_shot_ammo += 20
                            elif idx == 6:
                                tr.Turret.star_shot_ammo += 10
                            elif idx == 7:
                                if pup.Power_ups.star_shot_tubes < 14:
                                    pup.Power_ups.star_shot_tubes += 2
                            elif idx == 8:
                                pup.Power_ups.shield_time += 180
                            elif idx == 9:
                                tr.Turret.pd_reload_speed += 0.002 * 0.5
                            elif idx == 10:
                                tr.Turret.missile_reload_speed += 0.0005 * 0.5
                            elif idx == 11:
                                tr.Turret.nuke_reload_speed += 0.0001 * 0.5
                            elif idx == 12:
                                pl.Player.jump_recharge_rate += 0.0005 * 0.5
                            lvl.Levels.skill_points -= 1
                            pygame.mouse.set_visible(False)
                            return
            # win.blit(Interface.gfx_pictures[14], (winwidth / 2, winheight))
            Clock.tick(fps)
            pygame.display.update()

from pygame.locals import *
import pygame

from init import *
from astraid_funcs import *
import player as pl
import levels as lvl
import turret as tr
import power_ups as pup
from items import *
from Gfx import Gfx
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
    inventory_grid_lst = [
        pygame.Rect(300, 300, 100, 100),
        pygame.Rect(450, 300, 100, 100),
        pygame.Rect(200, 500, 100, 100),
        pygame.Rect(350, 500, 100, 100),
        pygame.Rect(500, 500, 100, 100)

    ]
    tc = Time_controler()
    clickable = True

    def __init__(self, color, location, icon_idx, font_size, text=""):
        self.font = pygame.font.SysFont("arial", font_size, 20)
        self.text = text
        self.color = color
        self.text_render = self.font.render(self.text, True, color)
        self.location = location
        self.icon_idx = icon_idx
        self.rect = pygame.Rect(self.location[0], self.location[1], 1, 1)

    def draw(self):
        self.text_render = self.font.render(self.text, True, self.color)
        win.blit(self.text_render, self.rect)
        win.blit(Interface.gfx_pictures[self.icon_idx], (self.rect.topleft[0] - 50, self.rect.topleft[1] - 8))

    def update_inter_item():
        if Items.inventory_dic[0] is not None:
            Interface((255, 255, 255), (65, 150), 4, 20, Items.inventory_dic[0].text).draw()
        if Items.inventory_dic[1] is not None:
            Interface((255, 255, 255), (65, 200), 4, 20, Items.inventory_dic[1].text).draw()
        if Items.inventory_dic[2] is not None:
            Interface((255, 255, 255), (65, 250), 4, 20).draw()
        if Items.inventory_dic[3] is not None:
            Interface((255, 255, 255), (65, 300), 4, 20).draw()
        if Items.inventory_dic[4] is not None:
            Interface((255, 255, 255), (65, 350), 4, 20).draw()

    def update_inter():
        for inter, text in zip(Interface.inter_lst, [
            f"Score = {lvl.Levels.display_score}",
            f"Level  = {lvl.Levels.display_level}",
            f"{pup.Power_ups.star_shot_amount}",
            f"{pup.Power_ups.super_shot_amount}",
            f"{pup.Power_ups.shield_amount}",
            f"{pup.Power_ups.heal_amount}",
            f"{int(pl.Player.health)}/{pl.Player.max_health}",
        ]):
            setattr(inter, "text", text)
            inter.draw()

    def create():
        for color, location, icon_idx, font_size in[
                ((255, 255, 255), (130, 20), 5, 30),  # Score
                ((255, 255, 255), (130, 55), 5, 30),  # Level
                ((255, 255, 255), (65, 920), 2, 25),   # repair
                ((255, 255, 255), (65, 860), 1, 25),  # shield
                ((255, 255, 255), (65, 800), 8, 25),  # super_shot
                ((255, 255, 255), (65, 740), 7, 25),  # star_shot
                ((255, 255, 255), (65, 1000), 3, 30),  # health
        ]:
            Interface.inter_lst.append(Interface(color, location, icon_idx, font_size))

    def update():
        win.blit(Interface.gfx_pictures[13], (0, 0))

        Interface.update_inter()
        Interface.update_inter_item()

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

    def upgrades_menu(upgrades_pressed):
        pygame.mouse.set_visible(True)
        font = pygame.font.SysFont("fixed", 22)

        while upgrades_pressed:

            Gfx.background()
            texts = [
                f"Skill Points = {lvl.Levels.skill_points}",
                f"{int(pl.Player.speed)}      ++    Speed",  # len 57
                f"{pl.Player.max_health}      ++    Max Health",
                f"{round(pl.Player.damage, 2)}    ++    Damage",
                f"{round(1/ (tr.Turret.fire_rate / 60), 2)}   ++    Fire Rate",
                f"{tr.Turret.super_shot_ammo}     ++    Rapid Fire Ammo",
                f"{tr.Turret.star_shot_ammo}     ++    Star Shot Ammo",
                f"{pup.Power_ups.star_shot_tubes}      ++    Star Shot Tubes",
                f"{pup.Power_ups.shield_time / 60}s   ++    Shield Duration"

            ]
            rects = [pygame.Rect(winwidth / 2 - 350 / 2, (winheight - 300) / 2 + i, 350, 30) for i in range(0, len(texts) * 30 + 1, 30)]
            render_lst = [(idx, font.render(text, False, (255, 255, 255)), rect) for idx, rect, text in zip([i for i in range(len(rects))], rects, texts)]

            win.blit(Interface.gfx_pictures[14], (700, 250))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == KEYDOWN:
                    if event.key == K_TAB:
                        pygame.mouse.set_visible(False)

                        upgrades_pressed = False
                        # return
            mouse_pos = pygame.mouse.get_pos()

            # Skill up
            for idx, text, rect in render_lst:
                win.blit(Interface.gfx_pictures[14], (winwidth / 2, winheight))
                win.blit(text, rect)
                if lvl.Levels.skill_points > 0:
                    if Interface.clickable:
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
                                        tr.Turret.fire_rate -= 1
                                        tr.Turret.normal_fire_rate -= 1
                                elif idx == 5:
                                    tr.Turret.super_shot_ammo += 20
                                elif idx == 6:
                                    tr.Turret.star_shot_ammo += 10
                                elif idx == 7:
                                    if pup.Power_ups.star_shot_tubes < 12:
                                        pup.Power_ups.star_shot_tubes += 1
                                elif idx == 8:
                                    pup.Power_ups.shield_time += 120
                                lvl.Levels.skill_points -= 1
                                Interface.clickable = False

            if pygame.mouse.get_pressed()[0] == 0:
                Interface.clickable = True

            # Items
            for slot in Interface.inventory_grid_lst:
                pygame.draw.rect(win, (40, 40, 40), slot)

            for key in Items.inventory_dic:
                try:
                    Items.inventory_dic[key].draw()
                    # Items.inventory_dic[key].gfx_draw()
                    Items.inventory_dic[key].drag_drop(mouse_pos, Interface.inventory_grid_lst, key=key)
                    Items.inventory_dic[key].tool_tip()
                except AttributeError:
                    pass
            # print(Items.inventory_dic)

            # win.blit(Interface.gfx_pictures[14], (winwidth / 2, winheight))
            Clock.tick(fps)
            pygame.display.update()

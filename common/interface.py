from pygame.locals import *
import pygame

from init import *
from astraid_funcs import *
import astraid_data as data
from items import Items, Active_Items
from Gfx import Gfx, Background


class Interface:

    icon_sprites = get_images("icons")
    item_sprites = get_images("items")
    item_lvl_sprites = get_images("item_lvl")
    inter_lst = []
    inventory_grid_lst = [
        pygame.Rect(200, 300, 100, 100),
        pygame.Rect(350, 300, 100, 100),
        pygame.Rect(500, 300, 100, 100),
        pygame.Rect(200, 500, 100, 100),
        pygame.Rect(350, 500, 100, 100),
        pygame.Rect(500, 500, 100, 100)

    ]

    clickable = True

    def __init__(self, color, location, icon_idx, font_size, text="", button_size=(1, 1)):
        self.font = pygame.font.SysFont("arial", font_size, 20)
        self.text = text
        self.color = color
        self.text_render = self.font.render(self.text, True, color)
        self.location = location
        self.icon_idx = icon_idx
        self.rect = pygame.Rect(self.location[0], self.location[1], button_size[0], button_size[1])
        self.item_lvl_gfx_idx = [4, 5, 6, 7]

    def draw(self, item=False, key=0):
        if item:
            win.blit(
                Interface.item_sprites[self.icon_idx],
                (self.rect.topleft[0] - 50,
                 self.rect.topleft[1] - 8)
            )
            win.blit(
                Interface.item_lvl_sprites[self.item_lvl_gfx_idx[Items.inventory_dic[key].lvl]],
                (self.rect.topleft[0] - 53,
                 self.rect.topleft[1] - 16)
            )
        else:
            win.blit(
                Interface.icon_sprites[self.icon_idx],
                (self.rect.topleft[0] - 50,
                 self.rect.topleft[1] - 8)
            )
        self.text_render = self.font.render(self.text, True, self.color)
        win.blit(self.text_render, self.rect)

    @classmethod
    def update_inter_item(cls):
        if Items.inventory_dic[0] is not None:
            Interface((255, 255, 255), (65, 150), Items.inventory_dic[0].gfx_idx[0],
                      20, Items.inventory_dic[0].text).draw(item=True, key=0)
        if Items.inventory_dic[1] is not None:
            Interface((255, 255, 255), (65, 200), Items.inventory_dic[1].gfx_idx[0],
                      20, Items.inventory_dic[1].text).draw(item=True, key=1)
        if Items.inventory_dic[2] is not None:
            Interface((255, 255, 255), (65, 250), Items.inventory_dic[2].gfx_idx[0],
                      20, Items.inventory_dic[2].text).draw(item=True, key=2)
        if Items.inventory_dic[3] is not None:
            Interface((255, 255, 255), (65, 300), Items.inventory_dic[3].gfx_idx[0],
                      20, Items.inventory_dic[3].text).draw(item=True, key=3)
        if Items.inventory_dic[4] is not None:
            Interface((255, 255, 255), (65, 350), Items.inventory_dic[4].gfx_idx[0],
                      20, Items.inventory_dic[4].text).draw(item=True, key=4)
        if Items.inventory_dic[5] is not None:
            Interface((255, 255, 255), (65, 400), Items.inventory_dic[5].gfx_idx[0],
                      20, Items.inventory_dic[5].text).draw(item=True, key=5)

    @classmethod
    def update_inter(cls):
        for inter, text in zip(Interface.inter_lst, [
            f"Score = {data.LEVELS.display_score}",
            f"Level  = {data.LEVELS.display_level}",
            # f"{pup.Power_ups.star_shot_amount}",
            f"{data.PLAYER.jumpdrive.text}",
            f"{data.PLAYER.shield.text}",
            f"{data.PLAYER.heal_amount}",
            f"{int(data.PLAYER.health)}/{data.PLAYER.max_health}",
            f"{Clock.get_fps()}",
        ]):
            setattr(inter, "text", text)
            inter.draw()

    @classmethod
    def create(cls):
        for color, location, icon_idx, font_size in[
                ((255, 255, 255), (130, 20), 5, 30),  # Score
                ((255, 255, 255), (130, 55), 5, 30),  # Level
                # ((255, 255, 255), (65, 920), 2, 25),   # repair
                ((255, 255, 255), (65, 800), 11, 25),  # jumpdrive
                ((255, 255, 255), (65, 860), 8, 25),  # shield
                ((255, 255, 255), (65, 920), 7, 25),  # repair
                ((255, 255, 255), (65, 1000), 3, 30),  # health
                ((255, 255, 255), (1800, 900), 11, 25)
        ]:
            Interface.inter_lst.append(Interface(color, location, icon_idx, font_size))

    @classmethod
    @timer
    def update(cls, timer):
        win.blit(Interface.icon_sprites[13], (0, 0))

        Interface.update_inter()
        Interface.update_inter_item()

        # Red Alert
        if data.LEVELS.boss_fight:
            win.blit(Interface.icon_sprites[6], (420, 10))
        # Skill_up
        if data.LEVELS.skill_points > 0:
            ani_ticker = timer.timer_animation_ticker(40)
            if ani_ticker < 30:
                win.blit(Interface.icon_sprites[12], (49, 42))
            else:
                pass

    @classmethod
    def upgrades_menu(cls, upgrades_pressed):
        pygame.mouse.set_visible(True)
        font = pygame.font.SysFont("arial", 25)

        while upgrades_pressed:

            win.fill(Background.bg_color)

            Background.update()
            texts = [
                f"Skill Points = {data.LEVELS.skill_points}",
                f"{int(data.PLAYER.speed)}      ++    Speed",  # len 57
                f"{data.PLAYER.max_health}      ++    Max Health",
                f"{int(data.PLAYER.damage * 10)}    ++    Damage",
                f"{100 - data.PLAYER.crit_chance} %   ++    Crit Chance",
                f"{round(data.TURRET.fire_rate, 2)}/s   ++    Fire Rate",
                f"{int(Active_Items.cd_reduction * 100)} %  ++ Cooldown reduction"

            ]
            rects = [
                pygame.Rect(winwidth / 2 - 350 / 2, (winheight - 300) / 2 + i, 350, 30) for i in range(0, len(texts) * 30 + 1, 30)
            ]
            render_lst = [
                (idx, font.render(text, False, (255, 255, 255)), rect) for idx, rect, text in zip([i for i in range(len(rects))], rects, texts)
            ]

            win.blit(Interface.icon_sprites[14], (700, 250))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == KEYDOWN:
                    if event.key == K_TAB:
                        pygame.mouse.set_visible(False)

                        upgrades_pressed = False
                        # return

            for standart_item, loc in [
                (data.PLAYER.shield, (65, 900)),
                (data.PLAYER.jumpdrive, (65, 800)),
                (data.PLAYER.afterburner, (65, 700))
            ]:
                standart_item.hitbox.center = loc
                standart_item.draw()
                standart_item.gfx_draw()
                standart_item.tool_tip()
                if Interface.clickable:
                    if pygame.mouse.get_pressed()[2] == 1:
                        if standart_item.hitbox.collidepoint(pygame.mouse.get_pos()):
                            standart_item.upgrade()
                            Interface.clickable = False

            mouse_pos = pygame.mouse.get_pos()

            # Skill up
            for idx, text, rect in render_lst:
                win.blit(Interface.icon_sprites[14], (winwidth / 2, winheight))
                win.blit(text, rect)
                if data.LEVELS.skill_points > 0:
                    if Interface.clickable:
                        if pygame.mouse.get_pressed()[0] == 1:
                            if rect.collidepoint(mouse_pos):
                                if idx == 1:
                                    data.PLAYER.set_player_speed(1)
                                    if data.PLAYER.speed == data.PLAYER.speed_limit:
                                        data.LEVELS.skill_points += 1
                                elif idx == 2:
                                    data.PLAYER.set_player_health(1)
                                    data.PLAYER.health += 1
                                    if data.PLAYER.max_health == data.PLAYER.health_limit:
                                        data.LEVELS.skill_points += 1
                                        data.PLAYER.health -= 1
                                elif idx == 3:
                                    data.PLAYER.damage += 0.11  # data.PLAYER.base_damage * 0.1
                                elif idx == 4:
                                    data.PLAYER.set_player_crit_chance(1)
                                    if data.PLAYER.crit_chance == data.PLAYER.crit_limit:
                                        data.LEVELS.skill_points += 1
                                elif idx == 5:
                                    data.TURRET.set_fire_rate(data.TURRET.base_fire_rate * 0.05)
                                    if data.TURRET.fire_rate == data.TURRET.fire_rate_limit:
                                        data.LEVELS.skill_points += 1
                                elif idx == 6:
                                    Active_Items.set_cd_reduction(0.04)
                                    if Active_Items.cd_reduction == Active_Items.cd_limit:
                                        data.LEVELS.skill_points += 1
                                data.LEVELS.skill_points -= 1
                                Interface.clickable = False

            # Items

            win.blit(font.render(
                f"Upgrade Points: {Items.upgrade_points}", False, (255, 255, 255)), (250, 250)
            )

            for slot in Interface.inventory_grid_lst:
                pygame.draw.rect(win, (40, 40, 40), slot)

            for key in Items.inventory_dic:
                if Items.inventory_dic[key] is not None:
                    Items.inventory_dic[key].draw()
                    Items.inventory_dic[key].gfx_draw()
                    Items.inventory_dic[key].tool_tip()
                    Items.inventory_dic[key].drag_drop(mouse_pos, Interface.inventory_grid_lst, key=key)

                    if Interface.clickable:
                        if pygame.mouse.get_pressed()[2] == 1:
                            if Items.inventory_dic[key].hitbox.collidepoint(pygame.mouse.get_pos()):
                                Items.inventory_dic[key].upgrade()
                                Interface.clickable = False

            if pygame.mouse.get_pressed() == (0, 0, 0):
                Interface.clickable = True

            # win.blit(Interface.icon_sprites[14], (winwidth / 2, winheight))
            Clock.tick(fps)
            pygame.display.update()

    @classmethod
    def pause_menu(cls, pause_pressed):

        while pause_pressed:

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    pause_pressed = False
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            Clock.tick(fps)
            pygame.display.update()

    @classmethod
    def main_menu(cls, menu_pressed):

        pygame.mouse.set_visible(True)
        # Interface(color, location, icon_idx, font_size)
        menu_buttons = [
            Interface((255, 255, 255), (800, 300), 15, 70,
                      text="Start Game", button_size=(400, 80)),
            Interface((255, 255, 255), (800, 500), 15, 70,
                      text="Highscore(WIP)", button_size=(400, 80)),
            Interface((255, 255, 255), (800, 700), 15, 70,
                      text="Options(WIP)", button_size=(400, 80))
        ]

        while menu_pressed:

            for btn in menu_buttons:
                pygame.draw.rect(win, (100, 100, 100), btn.rect)
                btn.draw()

            if pygame.mouse.get_pressed()[0] == 1:
                if menu_buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
                    menu_pressed = False
                    pygame.mouse.set_visible(False)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        exit()

            Clock.tick(fps)
            pygame.display.update()


data.INTERFACE = Interface

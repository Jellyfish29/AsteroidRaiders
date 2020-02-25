
from init import *
from ui import *
import astraid_data as data
from Gfx import Gfx, Background


class Upgrade_menu(Timer):

    def __init__(self):
        Timer.__init__(self)
        self.menu_active = False
        self.clickable = False
        self.bg_state = True
        self.menu = []
        self.item_cost_indicators = []
        self.inventory_grid = [pygame.Rect(420, y, 50, 50) for y in range(145, 678, 76)]
        self.standart_items = [data.PLAYER.shield, data.PLAYER.jumpdrive]
        self.dropped_item_pos = []
        self.orig_dropped_len = 0

        # Background
        self.menu.append(Gui_image(loc=(0, 0), img_idx=10))
        # Upgrade Points
        self.menu.append(Gui_text(loc=(1423, 98), text=lambda: f"{data.LEVELS.skill_points}"))
        self.menu.append(Gui_text(loc=(585, 96), text=lambda: f"{data.ITEMS.upgrade_points}"))
        # Skill number
        self.menu.append(Gui_text(loc=(1420, 190), text=lambda: f"{data.PLAYER.speed}", text_size=20))
        self.menu.append(Gui_text(loc=(1420, 250), text=lambda: f"{data.PLAYER.max_health}", text_size=20))
        self.menu.append(Gui_text(loc=(1420, 314), text=lambda: f"{int(data.PLAYER.damage * 10)}", text_size=20))
        self.menu.append(Gui_text(loc=(1420, 374), text=lambda: f"{100 - data.PLAYER.crit_chance}", text_size=20))
        self.menu.append(Gui_text(loc=(1415, 434), text=lambda: f"{round(data.TURRET.fire_rate, 1)}", text_size=20))
        self.menu.append(Gui_text(loc=(1420, 494), text=lambda: f"{int(data.ACTIVE_ITEMS.cd_reduction * 100)}", text_size=20))
        # Skill Buttons
        self.menu.append(Gui_button(loc=(1458, 185), btn_idx=(1, 2),
                                    btn_effect=lambda: self.speed_upgrade_btn_effect(), btn_text="2", text_x=3))
        self.menu.append(Gui_button(loc=(1456, 245), btn_idx=(1, 2),
                                    btn_effect=lambda: self.health_upgrade_btn_effect(), btn_text="2", text_x=3))
        self.menu.append(Gui_button(loc=(1456, 305), btn_idx=(1, 2),
                                    btn_effect=lambda: self.damage_upgrade_btn_effect(), btn_text="1", text_x=3))
        self.menu.append(Gui_button(loc=(1456, 368), btn_idx=(1, 2),
                                    btn_effect=lambda: self.crit_chance_upgrade_btn_effect(), btn_text="1", text_x=3))
        self.menu.append(Gui_button(loc=(1456, 428), btn_idx=(1, 2),
                                    btn_effect=lambda: self.fire_rate_upgrade_btn_effect(), btn_text="1", text_x=3))
        self.menu.append(Gui_button(loc=(1456, 490), btn_idx=(1, 2),
                                    btn_effect=lambda: self.cd_reduction_upgrade_btn_effect(), btn_text="1", text_x=3))

        for standart_item, loc in zip(self.standart_items, ((420, 753), (420, 829))):
            standart_item.hitbox.topleft = loc

    def tick(self):

        self.place_proximity_items()

        while self.menu_active:
            Background.bg_color_change(color=[0, 30, 0], instant=True)
            if self.timer_delay(10):
                self.clickable = True

            win.fill(Background.bg_color)
            Background.update()

            self.ui_update()

            self.item_interaction()

            self.proximity_items_interaction()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_TAB:
                        Background.bg_color_change(color=Background.standart_color, instant=True)
                        self.reset_item_bar()
                        self.reset_dropped_items()
                        Background.bg_move = self.bg_state
                        self.menu_active = False

                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        exit()

            if pygame.mouse.get_pressed() == (0, 0, 0):
                self.clickable = True

            Clock.tick(fps)
            pygame.display.flip()

    def ui_update(self):
        data.INTERFACE.cursor_update()
        data.INTERFACE.standart_ui_update()
        data.INTERFACE.health_bar_update()

        for element in self.menu:
            element.tick()

    def item_interaction(self):
        for key, item in data.ITEMS.inventory_dic.items():
            if item is not None:
                item.cost_indicator_update()
                item.gfx_draw()
                item.tool_tip()
                item.drag_drop(pygame.mouse.get_pos(), self.inventory_grid, key=key)

                if self.clickable:
                    if pygame.mouse.get_pressed()[2] == 1:
                        if item.hitbox.collidepoint(pygame.mouse.get_pos()):
                            item.upgrade()
                            self.clickable = False

        for item in self.standart_items:
            item.cost_indicator_update()
            item.gfx_draw()
            item.tool_tip()

            if self.clickable:
                if pygame.mouse.get_pressed()[2] == 1:
                    if item.hitbox.collidepoint(pygame.mouse.get_pos()):
                        item.upgrade()
                        self.clickable = False

    def reset_item_bar(self):
        for i in range(8):
            data.INTERFACE.inventory[i] = []
        for idx, slot in data.ITEMS.inventory_dic.items():
            if slot is not None:
                slot.set_cd_img = True
                slot.add_ui_elements(idx)

    def place_proximity_items(self):
        dropped_items = [i for i in data.ITEMS.dropped_lst if not any([isinstance(i, c) for c in data.ITEMS.consumables])]
        self.orig_dropped_len = len(dropped_items)
        for i, item in enumerate(dropped_items):
            self.dropped_item_pos.append(item.hitbox.center)
            item.hitbox.center = (740, 400 + i * 80)

    def proximity_items_interaction(self):
        dropped_items = [i for i in data.ITEMS.dropped_lst if not any([isinstance(i, c) for c in data.ITEMS.consumables])]
        for item in dropped_items:
            item.gfx_draw()
            item.tool_tip()
            item.drag_drop(pygame.mouse.get_pos(), self.inventory_grid, key="proximity")

        if len(dropped_items) != self.orig_dropped_len:
            self.place_proximity_items()

    def reset_dropped_items(self):
        for idx, item in enumerate([i for i in data.ITEMS.dropped_lst if not any([isinstance(i, c) for c in data.ITEMS.consumables])]):
            item.hitbox.center = self.dropped_item_pos[idx]
        self.dropped_item_pos.clear()

    def speed_upgrade_btn_effect(self):
        if data.LEVELS.skill_points > 1:
            data.LEVELS.skill_points -= 2
            data.PLAYER.set_player_speed(1)
            if data.PLAYER.speed == data.PLAYER.speed_limit:
                data.LEVELS.skill_points += 2

    def health_upgrade_btn_effect(self):
        if data.LEVELS.skill_points > 1:
            data.LEVELS.skill_points -= 2
            data.PLAYER.set_player_health(1)
            data.PLAYER.health += 1
            if data.PLAYER.max_health == data.PLAYER.health_limit:
                data.LEVELS.skill_points += 2
                data.PLAYER.health -= 1

    def damage_upgrade_btn_effect(self):
        if data.LEVELS.skill_points > 0:
            data.LEVELS.skill_points -= 1
            data.PLAYER.damage += 0.101

    def crit_chance_upgrade_btn_effect(self):
        if data.LEVELS.skill_points > 0:
            data.LEVELS.skill_points -= 1
            data.PLAYER.set_player_crit_chance(2)
            if data.PLAYER.crit_chance == data.PLAYER.crit_limit:
                data.LEVELS.skill_points += 1

    def fire_rate_upgrade_btn_effect(self):
        if data.LEVELS.skill_points > 0:
            data.LEVELS.skill_points -= 1
            data.TURRET.set_fire_rate(data.TURRET.base_fire_rate * 0.055)
            if data.TURRET.fire_rate == data.TURRET.fire_rate_limit:
                data.LEVELS.skill_points += 1

    def cd_reduction_upgrade_btn_effect(self):
        if data.LEVELS.skill_points > 0:
            data.LEVELS.skill_points -= 1
            data.ACTIVE_ITEMS.set_cd_reduction(0.03)
            if data.ACTIVE_ITEMS.cd_reduction == data.ACTIVE_ITEMS.cd_limit:
                data.LEVELS.skill_points += 1

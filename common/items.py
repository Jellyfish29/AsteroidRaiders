import pygame
from pygame.locals import *
import random

from init import *
from ui import *
from astraid_funcs import *
import astraid_data as data
from Gfx import Gfx


class Items(Timer):

    dropped_lst = []
    # inventory_dic = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None}
    inventory_dic = {i: None for i in range(8)}
    inv_grid_cords = [(420, y) for y in range(145, 678, 76)]
    active_flag_lst = []
    drop_table = []
    icon_sprites = get_images("gui_items_icon_large")
    lvl_sprites = get_images("item_lvl")
    tt_delay = 15
    font_20 = pygame.font.SysFont("arial", 20, 10)
    font_15 = pygame.font.SysFont("arial", 15, 10)
    upgrade_points = 0
    drop_table_absolute = []
    consumables = []

    def __init__(self, item_name, discription, gfx_idx, start=False):
        Timer.__init__(self)
        self.hitbox = pygame.Rect(-1000, -1000, 50, 50)
        if start:
            self.hitbox = pygame.Rect(Items.inv_grid_cords[0][0] + 25, Items.inv_grid_cords[0][1] + 25, 50, 50)
        self.item_name = item_name
        self.discription = discription
        self.gfx_idx = gfx_idx
        self.drag = False
        self.clicked = False
        self.color = (0, 0, 160)
        self.text = " "
        self.lvl = 0
        self.upgrade_cost_base = (2, 4, 7, "/")
        self.upgrade_cost = self.upgrade_cost_base[self.lvl]
        self.cd_len = None

    def draw(self):
        pass
        # pygame.draw.rect(win, self.color, self.hitbox)

    def activ(self):
        self.effect()

    def add_to_inventory(self, dropped=False):
        """BIGGO OOF"""
        if self.hitbox.colliderect(data.PLAYER.hitbox) or dropped:
            try:
                Items.dropped_lst.remove(self)
            except ValueError:
                pass
            for idx, slot in Items.inventory_dic.items():
                if idx < 4 and issubclass(self.__class__, Active_Items):
                    if slot is None:
                        self.hitbox.topleft = (Items.inv_grid_cords[idx][0] + 0, Items.inv_grid_cords[idx][1] + 0)
                        Items.inventory_dic[idx] = self
                        self.add_ui_elements(idx)

                        break
                elif idx >= 4 and not issubclass(self.__class__, Active_Items):
                    if slot is None:
                        self.hitbox.topleft = (Items.inv_grid_cords[idx][0] + 0, Items.inv_grid_cords[idx][1] + 0)
                        Items.inventory_dic[idx] = self
                        self.add_ui_elements(idx)

                        break

            else:
                if any([isinstance(self, item) for item in Items.consumables]):
                    self.effect()
                else:
                    Items.dropped_lst.append(self)

    def add_ui_elements(self, idx):
        data.INTERFACE.inventory[idx].append(Gui_image(
            loc=data.INTERFACE.item_slots[idx], flag=self.flag,
            img_idx=self.gfx_idx[1], sprites=Gui.item_small_sprites))

        data.INTERFACE.inventory[idx].append(Gui_text(
            loc=(data.INTERFACE.item_slots[idx][0] + 15, data.INTERFACE.item_slots[idx][1] + 12),
            text=lambda: Items.inventory_dic[idx].text if Items.inventory_dic[idx] is not None else f" "))

    def remove_from_inventory(self, key):
        self.hitbox.center = (data.PLAYER.hitbox.center[0], data.PLAYER.hitbox.center[1] + 100)
        self.end_effect()
        Items.dropped_lst.append(self)
        Items.inventory_dic[key] = None

    def drag_drop(self, mouse_pos, inventory, key=None):
        # Viel Glück beim verstehen
        if pygame.mouse.get_pressed()[0] == 1:
            self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        if self.clicked:
            if self.hitbox.collidepoint(mouse_pos):
                self.drag = True
        if self.drag:
            self.hitbox.center = mouse_pos
        if not self.clicked and self.drag:
            Items.inventory_dic[key] = None
            for idx, slot in enumerate(inventory):
                if self.hitbox.colliderect(slot):
                    if idx < 4 and issubclass(self.__class__, Active_Items):
                        if Items.inventory_dic[idx] is not None:
                            Items.inventory_dic[idx].add_to_inventory(dropped=True)
                            Items.inventory_dic[idx] = None
                        Items.inventory_dic[idx] = self
                        self.hitbox.topleft = (slot.topleft[0] + 0, slot.topleft[1] + 0)
                        break
                    elif idx >= 4 and issubclass(self.__class__, Active_Items):
                        Items.inventory_dic[key] = self
                        Items.inventory_dic[key].hitbox.topleft = (Items.inv_grid_cords[key][0] + 0, Items.inv_grid_cords[key][1] + 0)
                        break

                    elif idx >= 4 and not issubclass(self.__class__, Active_Items):
                        if Items.inventory_dic[idx] is not None:
                            Items.inventory_dic[idx].add_to_inventory(dropped=True)
                            Items.inventory_dic[idx] = None
                        Items.inventory_dic[idx] = self
                        self.hitbox.topleft = (slot.topleft[0] + 0, slot.topleft[1] + 0)
                        break

                    elif idx < 4 and not issubclass(self.__class__, Active_Items):
                        Items.inventory_dic[key] = self
                        Items.inventory_dic[key].hitbox.topleft = (Items.inv_grid_cords[key][0] + 0, Items.inv_grid_cords[key][1] + 0)
                        break

            else:
                self.remove_from_inventory(key)
            self.drag = False

    def despawn_avoidance(self):
        for item in Items.dropped_lst:
            if self != item:
                if self.hitbox.colliderect(item.hitbox):
                    self.hitbox.move_ip(random.choice([100, -100]), 0)
            for phenom in data.PHENOMENON_DATA:
                if self.hitbox.colliderect(phenom.hitbox):
                    self.hitbox.move_ip(random.choice([100, -100]), 0)
            if item.hitbox[0] < 0:
                item.hitbox.center = (100, item.hitbox.center[1])
            elif item.hitbox[0] > winwidth:
                item.hitbox.center = (winwidth - 100, item.hitbox.center[1])
            elif item.hitbox[1] < 0:
                item.hitbox.center = (item.hitbox.center[1], 100)
            # elif item.hitbox[1] > winheight:
            #     item.hitbox.center = (item.hitbox.center[1], winheight - 100)

    def decay(self):
        if not any([data.LEVELS.after_boss,
                    data.LEVELS.special_events]):
            self.hitbox.move_ip(0, 1)
            if rect_not_on_sreen(self.hitbox):
                Items.dropped_lst.remove(self)

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)

    def get_upgrade_desc(self):
        return ""

    def tool_tip(self):

        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if self.timer_key_delay(limit=Items.tt_delay, key=self.flag + "tt"):
                # Name
                win.blit(Gui.fonts[20].render(self.item_name, True, (255, 255, 255)), (pygame.mouse.get_pos()[0] + 30, pygame.mouse.get_pos()[1]))
                # Desc
                win.blit(Gui.fonts[15].render(self.discription, True, (255, 255, 255)), (pygame.mouse.get_pos()[0] + 30, pygame.mouse.get_pos()[1] + 30))
                # level
                win.blit(Gui.fonts[15].render(f"Item Level: {self.lvl + 1}/4  Cost: {self.upgrade_cost_base[self.lvl]}", True, (255, 255, 255)), (pygame.mouse.get_pos()[0] + 30, pygame.mouse.get_pos()[1] + 55))
                # lvl_effect
                win.blit(Gui.fonts[15].render(self.get_upgrade_desc(), True, (255, 255, 255)), (pygame.mouse.get_pos()[0] + 30, pygame.mouse.get_pos()[1] + 75))
        else:
            self.timer_key_delay(key=self.flag + "tt", reset=True)

    def gfx_draw(self):
        if self.lvl is not None:
            if any([self.flag == "supply_con", self.flag == "upgrade_con", self.flag == "heal_con"]):
                win.blit(Items.lvl_sprites[self.lvl + 5], (self.hitbox.topleft[0] - 20, self.hitbox.topleft[1] - 20))
            else:
                win.blit(Items.lvl_sprites[self.lvl + 1], (self.hitbox.topleft[0] - 10, self.hitbox.topleft[1] - 10))
        win.blit(Items.icon_sprites[self.gfx_idx[0]], (self.hitbox.topleft[0] - 10, self.hitbox.topleft[1] - 10))

    def get_lvl_effects(self, reverse=False):
        effects = [self.base_effect * (i / 100) for i in (100, 80, 65, 45)]
        if reverse:
            effects.reverse()
            return effects
        else:
            return effects

    def upgrade(self):
        if self.lvl < 3:
            if Items.upgrade_points >= self.upgrade_cost:
                Items.upgrade_points -= self.upgrade_cost
                self.end_effect()
                self.lvl += 1
                self.effect()
                self.upgrade_cost = self.upgrade_cost_base[self.lvl]
                self.set_effect_strength()

    def upgradeable(self):
        try:
            return Items.upgrade_points >= self.upgrade_cost_base[self.lvl]
        except TypeError:
            pass

    def set_effect_strength(self):
        pass

    def toggle(self):
        pass

    def activation_effect(self):
        pass

    def end_activation(self):
        pass

    def set_text_update(self):
        pass

    @classmethod
    def set_drop_table(cls, table):
        cls.drop_table_absolute += table

    @classmethod
    def start_item_generator(cls):
        table = cls.drop_table_absolute[:12]
        return table[random.randint(0, len(table) - 1)][0]

    @classmethod
    def item_generator(cls):
        if len(cls.drop_table) < 3:
            cls.drop_table = cls.drop_table_absolute.copy()
        item, color = cls.drop_table.pop(random.randint(0, len(cls.drop_table) - 1))
        return item(color)

    @classmethod
    def drop(cls, location, amount=0, target=None):
        if target is not None:
            cls.dropped_lst.append(target)
            if amount == 2:
                cls.dropped_lst.append(target)
        else:
            while len(cls.dropped_lst) < amount:
                random_item = cls.item_generator()
                for key in cls.inventory_dic:
                    if type(random_item) == type(cls.inventory_dic[key]):
                        break
                else:
                    cls.dropped_lst.append(random_item)
        for i, item in enumerate(cls.dropped_lst):
            if item.hitbox[0] < 0:
                item.hitbox.center = location
        # for i, item in enumerate(cls.dropped_lst):
        #     item.hitbox.center = (location[0] + i * 100, location[1])

    @classmethod
    def get_all_inventory_items(cls):
        items = [cls.inventory_dic[key] for key in cls.inventory_dic if cls.inventory_dic[key] is not None]
        return items

    @classmethod
    def get_item(cls, flag=""):
        item = [cls.inventory_dic[i] for i in range(len(cls.inventory_dic)) if cls.inventory_dic[i] is not None and cls.inventory_dic[i].flag == flag]
        if len(item) == 0:
            return Item_mock_test((0, 0, 0))
        else:
            return item[0]

    @classmethod
    def spawm_items_test(cls):
        cls.dropped_lst.clear()
        cls.drop((winwidth / 2, 400), amount=4)

    @classmethod
    @timer
    def spawm_all_items_test(cls, timer):
        if timer.trigger(30):
            cls.dropped_lst.clear()
            cls.drop((winwidth / 2, 400), amount=4)

    @classmethod
    def update(cls):

        # cls.spawm_all_items_test()

        for item in cls.dropped_lst:
            item.draw()
            item.gfx_draw()
            item.decay()
            item.add_to_inventory()
            item.despawn_avoidance()
            item.tool_tip()

        for item in cls.get_all_inventory_items():
            item.effect()
            item.set_text_update()


data.ITEMS = Items


class Active_Items(Items):

    cd_reduction = 0
    raw_cd_reduction = 0
    cd_limit = 0.4

    def __init__(self, color, name, desc, gfx_idx):
        super().__init__(name, desc, gfx_idx)
        self.color = color
        self.flag = "none"
        self.active = False
        self.cooldown = False
        self.cd_len = 0
        self.text = " "
        self.active_time = None
        self.effect_name = None
        self.engage = False
        self.set_cd_img = False
        self.ticker.update({"cd": 0, "active_time": 0})

    def effect(self):
        if self.get_inventory_key() < 4:
            if self.flag not in Items.active_flag_lst:
                Items.active_flag_lst.append(self.flag)

            if self.active:
                if self.active_time is not None:
                    if self.timer_key_trigger(self.active_time, key="active_time"):
                        self.end_active()

                self.text = self.get_active_str()

            elif self.cooldown:
                if self.timer_key_trigger(self.get_cd_len(), key="cd"):
                    self.cooldown = False

                self.text = self.get_cd_str()

            else:
                pass
                self.text = " "  # self.get_key_str()
        else:
            self.end_effect()
            self.text = " "

        self.timer_tick()

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
        self.end_active()

    def end_active(self):
        if self.active:
            self.cooldown = True
            self.set_cd_img = True
        if self.engage:
            self.engage = False
        self.active = False

    def toggle(self):
        if not self.active and not self.cooldown:
            self.active = True
            self.set_cd_img = True

    def activation_effect(self):
        if self.effect_name is not None:
            if self.active:
                Gfx.create_effect(self.effect_name, 25, data.PLAYER.hitbox.topleft, hover=True)

    def end_activation(self):
        if not self.cooldown:
            self.engage = True

    def get_cd_str(self):
        return str(int((self.get_cd_len() - self.ticker["cd"]) / 60) + 1)

    def get_active_str(self):
        if self.active_time is not None:
            return f">{int((self.active_time - self.ticker['active_time']) / 60 + 1)}"

    def get_cd_len(self):
        return self.cd_len - self.cd_len * Active_Items.cd_reduction

    def get_key_str(self):
        if self.get_inventory_key() == 0:
            return "R"
        elif self.get_inventory_key() == 1:
            return "F"
        else:
            return "E"

    def get_inventory_key(self):
        key = [key for (key, item) in Items.inventory_dic.items() if item == self]
        return key[0]

    @classmethod
    def set_cd_reduction(cls, cd):
        cls.raw_cd_reduction += cd
        cls.cd_reduction = cls.raw_cd_reduction
        if cls.cd_reduction > cls.cd_limit:
            cls.cd_reduction = cls.cd_limit


class Item_mock_test(Active_Items):

    def __init__(self, color):
        super().__init__(color, "Item_mock_test name", "Item_mock_test discription", (40, 40))
        self.color = color
        self.flag = "Item_mock_test"
        self.active = True
        self.get_cd_len = 60
        self.active_time = 60
        self.lvl = 0
        self.engage = True
        self.effect_strength = 1

    def end_active(self):
        self.engage = True

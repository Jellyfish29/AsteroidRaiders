import pygame
from pygame.locals import *
import random

from init import *
from astraid_funcs import *
import astraid_data as data
from Gfx import Gfx


class Items(Timer):

    dropped_lst = []
    inventory_dic = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None}
    inv_grid_cords = [(200, 300), (350, 300), (500, 300), (200, 500), (350, 500), (500, 500)]
    active_flag_lst = []
    drop_table = []
    icon_sprites = get_images("items")
    lvl_sprites = get_images("item_lvl")
    tt_delay = 15
    font_20 = pygame.font.SysFont("arial", 20, 10)
    font_15 = pygame.font.SysFont("arial", 15, 10)
    upgrade_points = 0

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
        if self.hitbox.colliderect(data.PLAYER.hitbox) or dropped:
            try:
                Items.dropped_lst.remove(self)
            except ValueError:
                pass
            for idx, slot in Items.inventory_dic.items():
                if slot is None:
                    self.hitbox.topleft = (Items.inv_grid_cords[idx][0] + 25, Items.inv_grid_cords[idx][1] + 25)
                    Items.inventory_dic[idx] = self
                    break
            else:
                if isinstance(self, Item_supply_crate) or isinstance(self, Item_heal_crate):
                    self.effect()
                else:
                    Items.dropped_lst.append(self)

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
                    if Items.inventory_dic[idx] is not None:
                        Items.inventory_dic[idx].add_to_inventory(dropped=True)
                        Items.inventory_dic[idx] = None
                    Items.inventory_dic[idx] = self
                    self.hitbox.topleft = (slot.topleft[0] + 25, slot.topleft[1] + 25)
                    break
            else:
                self.remove_from_inventory(key)
            self.drag = False

    def collision_avoidance(self):
        for item in Items.dropped_lst:
            if self != item:
                if self.hitbox.colliderect(item.hitbox):
                    self.hitbox.move_ip(random.choice([50, -50]), 0)

    def decay(self):
        if not data.LEVELS.after_boss:
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

    # def get_upgrade_desc(self, effects, v):
        # if v == "cd" or v == "s":
        #     effects = [int(j / 60) for j in effects]
        # else:
        #     effects = [int(j) for j in effects]

        # upgrade_desc = [i for i in zip(["1", "2", "3", "4"], effects)]
        # desc_str = ""
        # for d in upgrade_desc:
        #     desc_str += f"{d[0]}. = {d[1]}{v}  "
        # return desc_str

    @timer
    def tool_tip(self, timer):

        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if timer.timer_delay(limit=Items.tt_delay):
                # Name
                win.blit(Items.font_20.render(self.item_name, True, (255, 255, 255)), (pygame.mouse.get_pos()[0] + 30, pygame.mouse.get_pos()[1]))
                # Desc
                win.blit(Items.font_15.render(self.discription, True, (255, 255, 255)), (pygame.mouse.get_pos()[0] + 30, pygame.mouse.get_pos()[1] + 30))
                # level
                win.blit(Items.font_15.render(f"Item Level: {self.lvl + 1}/4  Cost: {self.upgrade_cost_base[self.lvl]}", True, (255, 255, 255)), (pygame.mouse.get_pos()[0] + 30, pygame.mouse.get_pos()[1] + 55))
                # lvl_effect
                win.blit(Items.font_15.render(self.get_upgrade_desc(), True, (255, 255, 255)), (pygame.mouse.get_pos()[0] + 30, pygame.mouse.get_pos()[1] + 75))
        else:
            timer.timer_delay(reset=True)

    def gfx_draw(self):
        if self.lvl is not None:
            win.blit(Items.lvl_sprites[self.lvl], (self.hitbox.topleft[0] - 26, self.hitbox.topleft[1] - 25))
        win.blit(Items.icon_sprites[self.gfx_idx[1]], (self.hitbox.topleft[0] - 10, self.hitbox.topleft[1] - 10))

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
    def get_drop_table_absolute(cls):
        drop_table_absolute = [
            # Active Items
            # (Item_jump_drive, (0, 100, 0)),
            (Item_pd, (100, 0, 0)),
            (Item_nuke, (0, 0, 100)),
            (Item_missile, (100, 100, 0)),
            (Item_he_rounds, (200, 19, 123)),
            (Item_star_fire, (44, 81, 255)),
            (Item_rapid_fire, (255, 45, 12)),
            (Item_piercing_shot, (120, 15, 0)),
            # (Item_gravity_bomb, (120, 15, 0)),
            (Item_black_hole_bomb, (120, 15, 0)),
            # Passiv Items
            (Item_auto_repair, (255, 0, 0)),
            (Item_targeting_scanner, (0, 0, 0)),
            (Item_damage_core, (100, 250, 20)),
            (Item_ablativ_armor, (200, 40, 170)),
            (Item_engine_core, (10, 100, 200)),
            (Item_ammo_racks, (255, 0, 70)),
            (Item_improved_feeding, (0, 20, 40)),
            (Item_hyper_shields, (99, 99, 230)),
            # (Item_expert_damage_control, (20, 10, 251)),
            (Item_fan_shot, (12, 64, 1)),
            (Item_hammer_shot, (99, 140, 3)),
            (Item_hyper_velocity_rounds, (1, 169, 201)),
            (Item_overdrive, (89, 1, 37)),
            # (Item_2nd_escort, (0, 23, 63)),
            # (Item_escort_improve, (10, 20, 30)),
            # (Item_escort_gunship, (90, 12, 54)),
            # (Item_escort_gun, (39, 178, 210)),
            # (Item_escort_missile, (32, 99, 99))
        ]
        return drop_table_absolute

    @classmethod
    def start_item_generator(cls):
        table = cls.get_drop_table_absolute()[:8]
        return table[random.randint(0, len(table) - 1)][0]

    @classmethod
    def item_generator(cls):
        if len(cls.drop_table) < 3:
            cls.drop_table = cls.get_drop_table_absolute().copy()
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
            item.hitbox.center = (location[0] + i * 100, location[1])

    @classmethod
    def get_all_inventory_items(cls):
        items = [cls.inventory_dic[key] for key in cls.inventory_dic if cls.inventory_dic[key] is not None]
        return items

    @classmethod
    def get_item(cls, flag=""):
        item = [cls.inventory_dic[i] for i in range(6) if cls.inventory_dic[i] is not None and cls.inventory_dic[i].flag == flag]
        if len(item) == 0:
            return Placeholder((0, 0, 0))
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

        for item in cls.dropped_lst:
            item.draw()
            item.gfx_draw()
            item.decay()
            item.add_to_inventory()
            item.collision_avoidance()
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
        self.text = "/"
        self.active_time = None
        self.effect_name = None

    def effect(self):
        print(self.ticker)
        if self.get_inventory_key() < 3:
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

                self.text = self.get_cd_str() + "s"

            else:
                self.text = self.get_key_str()
        else:
            self.end_effect()
            self.text = "/"

        self.timer_tick()

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
        self.end_active()

    def end_active(self):
        self.active = False
        self.cooldown = True

    def toggle(self):
        if not self.active and not self.cooldown:
            self.active = True

    def activation_effect(self):
        if self.effect_name is not None:
            if self.active:
                Gfx.create_effect(self.effect_name, 25, data.PLAYER.hitbox.topleft, hover=True)

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


class Placeholder(Active_Items):

    def __init__(self, color):
        super().__init__("placeholder name", "placeholder discription", (40, 40))
        self.color = color
        self.flag = "placeholder"


### Activ Items ###


class Item_pd(Active_Items):

    def __init__(self, color, start=False):
        super().__init__(color, "Pointdefence (active)", "shoots down incoming enemy weapons", (4, 5))
        self.color = color
        self.flag = "point_defence"
        self.cd_len = 2000
        self.base_effect = 1000  # active time
        self.active_time = self.get_lvl_effects(reverse=True)[self.lvl]
        self.effect_name = "pd_on"
        self.upgrade_desc = (f"Cooldown", self.get_lvl_effects(reverse=True)[self.lvl], "s")

    def get_upgrade_desc(self):
        return f"Active Time: {int(self.active_time / 60 + 1)}s <> Cooldown: {int(self.get_cd_len() / 60) + 1}s"

    def set_effect_strength(self):
        self.active_time = self.get_lvl_effects(reverse=True)[self.lvl]


class Item_missile(Active_Items):

    def __init__(self, color):
        super().__init__(color, "Heat seeking Missiles (acive)", "Fires two heat seeking Missile at the Target", (6, 7))
        self.color = color
        self.flag = "missile"
        self.base_effect = 1000  # cooldown time
        self.cd_len = self.get_lvl_effects()[self.lvl]
        self.active_time = 1
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(), "cd")

    def get_upgrade_desc(self):
        return f"Cooldown: {int(self.cd_len / 60) + 1}s"

    def set_effect_strength(self):
        self.cd_len = self.get_lvl_effects()[self.lvl]


class Item_nuke(Active_Items):

    def __init__(self, color):
        super().__init__(color, "Nuclear Warhead (active)", "Fires a 45 Megaton nuclear Warhead", (2, 3))
        self.color = color
        self.flag = "nuke"
        self.base_effect = 5400  # cooldown time
        self.cd_len = self.get_lvl_effects()[self.lvl]
        self.active_time = None
        self.engage = False
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(), "cd")

    def get_upgrade_desc(self):
        return f"Cooldown: {int(self.get_cd_len() / 60) + 1}s"

    def set_effect_strength(self):
        self.cd_len = self.get_lvl_effects()[self.lvl]

    def end_activation(self):
        self.engage = True


class Item_jump_drive(Active_Items):

    def __init__(self, color):
        super().__init__(color, "Jump Drive (active)", "Jumps the ship to the marked location", (0, 1))
        self.color = color
        self.flag = "jump_drive"
        self.base_effect = 900  # cooldown time
        self.cd_len = self.get_lvl_effects()[self.lvl]
        self.active_time = None
        self.engage = False
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(), "cd")

    def get_upgrade_desc(self):
        return f"Cooldown: {int(self.get_cd_len() / 60) + 1}s"

    def set_effect_strength(self):
        self.cd_len = self.get_lvl_effects()[self.lvl]

    def get_active_str(self):
        return "Charging"

    def end_activation(self):
        self.engage = True

    def get_inventory_key(self):
        return 0

    def get_key_str(self):
        return ""


class Item_he_rounds(Active_Items):

    def __init__(self, color, start=False):
        super().__init__(color, "HE Rounds (active)", "On Activation fires Powerful HE Rounds that explode on impact", (8, 9))
        self.color = color
        self.flag = "he_rounds"
        self.cd_len = 1800
        self.base_effect = 900  # active time
        self.active_time = self.get_lvl_effects(reverse=True)[self.lvl]
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "s")

    def get_upgrade_desc(self):
        return f"Active Time: {int(self.active_time / 60 + 1)}s <> Cooldown: {int(self.get_cd_len() / 60) + 1}s"

    def set_effect_strength(self):
        self.active_time = self.get_lvl_effects(reverse=True)[self.lvl]


class Item_piercing_shot(Active_Items):

    def __init__(self, color):
        super().__init__(color, "Hyper Penetrator rounds (active)", "Rounds pierce the target and deal damge depending on traveltime", (32, 33))
        self.color = color
        self.flag = "piercing_shot"
        self.base_effect = 0.8
        self.effect_strength = self.get_lvl_effects(reverse=True)[self.lvl]
        self.cd_len = 1200
        self.active_time = 600

    def get_upgrade_desc(self):
        return f"Piercing Damage: {int(self.get_lvl_effects(reverse=True)[self.lvl] * 10)} <> Cooldown: {int(self.get_cd_len() / 60) + 1}s"

    def set_effect_strength(self):
        self.effect_strength = self.get_lvl_effects(reverse=True)[self.lvl]


class Item_rapid_fire(Active_Items):

    def __init__(self, color):
        super().__init__(color, "Rapid Fire (active)", "On Activation massivly increases Fire Rate", (41, 42))
        self.color = color
        self.flag = "rapid_fire"
        self.base_effect = 3600  # cooldown time
        self.cd_len = self.get_lvl_effects()[self.lvl]
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(), "cd")

    def get_upgrade_desc(self):
        return f"Cooldown: {int(self.get_cd_len() / 60) + 1}s"

    def set_effect_strength(self):
        self.cd_len = self.get_lvl_effects()[self.lvl]

    def get_active_str(self):
        return str((data.TURRET.super_shot_ammo - data.TURRET.super_shot_limiter))


class Item_star_fire(Active_Items):

    def __init__(self, color, start=False):
        super().__init__(color, "Star Fire (active)", "On Activation the ship fire from additional fixed tubes", (43, 44))
        self.color = color
        self.flag = "star_fire"
        self.base_effect = 3600  # cooldwon time
        self.cd_len = self.get_lvl_effects()[self.lvl]
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(), "cd")

    def get_upgrade_desc(self):
        return f"Cooldown: {int(self.get_cd_len() / 60) + 1}s"

    def set_effect_strength(self):
        self.cd_len = self.get_lvl_effects()[self.lvl]

    def get_active_str(self):
        return str((data.TURRET.star_shot_ammo - data.TURRET.star_shot_limiter))


class Item_gravity_bomb(Active_Items):

    def __init__(self, color, start=False):
        super().__init__(color, "Gravity Bomb (active)", "Fires a Missile that upon Impact slows all Object in its Radius", (40, 40))
        self.color = color
        self.flag = "gravity_bomb"
        self.base_effect = 3600  # cooldwon time
        self.cd_len = self.get_lvl_effects()[self.lvl]
        self.active_time = 1000
        self.engage = False
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(), "cd")

    def get_upgrade_desc(self):
        return f"Cooldown: {int(self.get_cd_len() / 60) + 1}s"

    def set_effect_strength(self):
        self.cd_len = self.get_lvl_effects()[self.lvl]

    def end_activation(self):
        self.engage = True


class Item_black_hole_bomb(Active_Items):

    def __init__(self, color, start=False):
        super().__init__(color, "Balck Hole Bomb (active)", "Fires a Missile that upon Impact creates a micro singularity", (40, 40))
        self.color = color
        self.flag = "black_hole_bomb"
        self.base_effect = 2200  # cooldwon time
        self.cd_len = self.get_lvl_effects()[self.lvl]
        self.active_time = 300
        self.engage = False
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(), "cd")

    def get_upgrade_desc(self):
        return f"Cooldown: {int(self.get_cd_len() / 60) + 1}s"

    def set_effect_strength(self):
        self.cd_len = self.get_lvl_effects()[self.lvl]

    def end_activation(self):
        self.engage = True


class Item_shield(Active_Items):

    def __init__(self, color, start=False):
        super().__init__(color, "Shield", f"Shields the ship from hits", (40, 40))
        self.color = color
        self.flag = "shield"
        self.lvl = 0
        self.base_effect = 5400  # cooldown time
        self.cd_len = self.get_lvl_effects()[self.lvl]
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(), "cd")

    def get_upgrade_desc(self):
        return f"Cooldown: {int(self.get_cd_len() / 60) + 1}s"

    def set_effect_strength(self):
        self.cd_len = self.get_lvl_effects()[self.lvl]

    def get_active_str(self):
        return str(data.PLAYER.shield_strength)

    def get_inventory_key(self):
        return 0

    def get_key_str(self):
        return ""


class Item_afterburner(Active_Items):

    def __init__(self, color, start=False):
        super().__init__(color, "Afterburner", f"A short speedboost in the current direction", (40, 40))
        self.color = color
        self.flag = "afterburner"
        self.lvl = 3
        self.base_effect = 100  # cooldown time
        self.cd_len = self.get_lvl_effects()[self.lvl]
        self.active_time = 4
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(), "cd")

    def get_upgrade_desc(self):
        return f"Cooldown: {int(self.get_cd_len() / 60) + 1}s"

    def set_effect_strength(self):
        self.cd_len = self.get_lvl_effects()[self.lvl]

    def get_inventory_key(self):
        return 0

    def get_key_str(self):
        return ""


### Passiv Items ###


class Item_auto_repair(Items):

    def __init__(self, color):
        super().__init__("Repair Drones (passiv)", "Drones passively repair the Ship over time", (10, 11))
        self.color = color
        self.flag = "auto_repair"
        self.tc = Time_controler()
        self.base_effect = 3000
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(), "cd")

    def get_upgrade_desc(self):
        return f"Repair Time: {int(self.get_lvl_effects()[self.lvl] / 60) + 1}s"

    @timer
    def effect(self, timer):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
        if timer.trigger(self.get_lvl_effects()[self.lvl]):
            if data.PLAYER.health < data.PLAYER.max_health:
                data.PLAYER.health += 1


class Item_damage_core(Items):

    def __init__(self, color):
        super().__init__("Damage Core (passiv)", "Massivily increases Weapon Damage", (12, 13))
        self.color = color
        self.flag = "damage_core"
        self.base_effect = 1.4
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "DMG")

    def get_upgrade_desc(self):
        return f"Bonus Damage: {int(self.get_lvl_effects(reverse=True)[self.lvl] * 10)}"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            data.PLAYER.damage += self.get_lvl_effects(reverse=True)[self.lvl]

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.PLAYER.damage -= self.get_lvl_effects(reverse=True)[self.lvl]


class Item_ablativ_armor(Items):

    def __init__(self, color):
        super().__init__("Ablativ Armor (passiv)", "Massivily increases Ship Strength", (14, 15))
        self.color = color
        self.flag = "ablativ_armor"
        self.base_effect = 10
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "HP")

    def get_upgrade_desc(self):
        return f"Bonus Health: {int(self.get_lvl_effects(reverse=True)[self.lvl])}"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            data.PLAYER.set_player_health(int(self.get_lvl_effects(reverse=True)[self.lvl]))

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.PLAYER.set_player_health(-int(self.get_lvl_effects(reverse=True)[self.lvl]))


class Item_engine_core(Items):

    def __init__(self, color):
        super().__init__("Engine Core (passiv)", "Massivily increases Ship Speed", (16, 17))
        self.color = color
        self.flag = "engine_core"
        self.base_effect = 5
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "km/s")

    def get_upgrade_desc(self):
        return f"Bonus Speed: {int(self.get_lvl_effects(reverse=True)[self.lvl])}"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            data.PLAYER.set_player_speed(int(self.get_lvl_effects(reverse=True)[self.lvl]))

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.PLAYER.set_player_speed(-int(self.get_lvl_effects(reverse=True)[self.lvl]))


class Item_ammo_racks(Items):

    def __init__(self, color):
        super().__init__("Ammo Racks (passiv)", "Reduces all Cooldowns by 30 %", (18, 19))
        self.color = color
        self.flag = "ammo_racks"
        self.base_effect = 0.3
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "cd red")

    def get_upgrade_desc(self):
        return f"Cooldown Reduction: {int(self.get_lvl_effects(reverse=True)[self.lvl] * 100)}%"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            Active_Items.set_cd_reduction(self.get_lvl_effects(reverse=True)[self.lvl])

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            Active_Items.set_cd_reduction(-self.get_lvl_effects(reverse=True)[self.lvl])


class Item_improved_feeding(Items):

    def __init__(self, color):
        super().__init__("Improved Ammo Feeding System (passiv)", "Increases Fire Rate", (20, 21))
        self.color = color
        self.flag = "improved_feeding"
        self.base_effect = 12
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "Shots/s")

    def get_upgrade_desc(self):
        return f"Bonus Fire Rate: {round(1 / (int(self.get_lvl_effects(reverse=True)[self.lvl]) / 60), 2)}/s"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            data.TURRET.set_fire_rate(-int(self.get_lvl_effects(reverse=True)[self.lvl]))

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.TURRET.set_fire_rate(int(self.get_lvl_effects(reverse=True)[self.lvl]))


class Item_targeting_scanner(Items):

    def __init__(self, color):
        super().__init__("Improved Targeting Scanner (passiv)", "Increases Crit Chance", (40, 40))
        self.color = color
        self.flag = "targeting_scanner"
        self.base_effect = 25
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "Shots/s")

    def get_upgrade_desc(self):
        return f"Bonus Crit Chance: {int(self.get_lvl_effects(reverse=True)[self.lvl])}%"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            data.PLAYER.set_player_crit_chance(int(self.get_lvl_effects(reverse=True)[self.lvl]))

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.PLAYER.set_player_crit_chance(-int(self.get_lvl_effects(reverse=True)[self.lvl]))


class Item_hyper_shields(Items):

    def __init__(self, color):
        super().__init__("Hyper Shields (passiv)", "Massivliy Increases Shield Duration", (22, 23))
        self.color = color
        self.flag = "hyper_shields"
        self.base_effect = 4
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "Shield HP")

    def get_upgrade_desc(self):
        return f"Bonus Shield HP: {int(self.get_lvl_effects(reverse=True)[self.lvl])}"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            data.PLAYER.shield_strength += int(self.get_lvl_effects(reverse=True)[self.lvl])
            data.PLAYER.max_shield_strength += int(self.get_lvl_effects(reverse=True)[self.lvl])

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.PLAYER.shield_strength -= int(self.get_lvl_effects(reverse=True)[self.lvl])
            data.PLAYER.max_shield_strength -= int(self.get_lvl_effects(reverse=True)[self.lvl])


class Item_expert_damage_control(Items):

    def __init__(self, color):
        super().__init__("Expert Damage Controll (passiv)", "Increases Damage Control Power Up Efficiency", (24, 25))
        self.color = color
        self.flag = "ex_damage_control"
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "Shield HP")

    def get_upgrade_desc(self):
        return f"Bonus Damage: {self.get_lvl_effects(reverse=True)[self.lvl]}"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)


class Item_fan_shot(Items):

    def __init__(self, color):
        super().__init__("MULTI Cannon (shot mod)", "Fires 2 extra shots every 4 shots", (28, 29))
        self.color = color
        self.flag = "fan_shot"
        self.base_effect = 6
        self.effect_strength = int(self.get_lvl_effects()[self.lvl])
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "Interval")

    def get_upgrade_desc(self):
        return f"Attack Interval: {int(self.get_lvl_effects()[self.lvl])}"

    def set_effect_strength(self):
        self.effect_strength = int(self.get_lvl_effects()[self.lvl])


class Item_hammer_shot(Items):

    def __init__(self, color):
        super().__init__("HAMMER Cannon (shot mod)", "Every 5th shot deals increased Damage", (30, 31))
        self.color = color
        self.flag = "hammer_shot"
        self.base_effect = 15
        self.effect_strength = int(self.get_lvl_effects(reverse=True)[self.lvl])
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "DMG")

    def get_upgrade_desc(self):
        return f"Bonus Damage: {int(self.get_lvl_effects(reverse=True)[self.lvl]) * 10} <> Attack Interval: 5"

    def set_effect_strength(self):
        self.effect_strength = int(self.get_lvl_effects(reverse=True)[self.lvl])


class Item_hyper_velocity_rounds(Items):

    def __init__(self, color):
        super().__init__("Hyper Velocity Rounds (shot mod)", "Increases Projectile Speed and Damage", (34, 35))
        self.color = color
        self.flag = "hyper_vel_rounds"
        self.base_effect = 1
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "+%Speed/DMG")

    def get_upgrade_desc(self):
        return f"Projectile Speed: {int(25 * self.get_lvl_effects(reverse=True)[self.lvl])} <> Bonus Damage: {int(1 * self.get_lvl_effects(reverse=True)[self.lvl] * 10)}"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            data.TURRET.projectile_speed += int(25 * self.get_lvl_effects(reverse=True)[self.lvl])
            data.PLAYER.damage += 1 * self.get_lvl_effects(reverse=True)[self.lvl]

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.TURRET.projectile_speed -= int(25 * self.get_lvl_effects(reverse=True)[self.lvl])
            data.PLAYER.damage -= 1 * self.get_lvl_effects(reverse=True)[self.lvl]


class Item_overdrive(Items):

    def __init__(self, color):
        super().__init__("Weapons system Overdrive (passive)", "Every Kill increases Damage and Fire Rate until taking Damage", (36, 37))
        self.color = color
        self.flag = "overdrive"
        self.base_effect = 30
        self.effect_strength = self.get_lvl_effects(reverse=True)[self.lvl]
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "Stacks")

    def get_upgrade_desc(self):
        return f"Max Stacks: {int(self.get_lvl_effects(reverse=True)[self.lvl])}"

    def set_effect_strength(self):
        self.effect_strength = int(self.get_lvl_effects(reverse=True)[self.lvl])

    def set_text_update(self):
        self.text = f"{data.TURRET.overdrive_count}/{int(self.effect_strength)}"

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.PLAYER.damage -= 0.05 * data.TURRET.overdrive_count
            data.TURRET.fire_rate += 0.7 * data.TURRET.overdrive_count
            data.TURRET.overdrive_count = 0


## Escorts ##


class Item_2nd_escort(Items):

    def __init__(self, color):
        super().__init__("Improved Hangar", "The Hangar is now able to support two Escort Craft", (40, 40))
        self.color = color
        self.flag = "2nd_escort"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            if pl.Escort.spawned:
                data.PLAYER_DATA.remove([obj for obj in data.PLAYER_DATA if obj.__class__.__name__ == "Escort"][0])
                pl.Escort.spawned = False

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.PLAYER_DATA.remove([obj for obj in data.PLAYER_DATA if obj.__class__.__name__ == "Escort"][0])


class Item_escort_improve(Items):

    def __init__(self, color):
        super().__init__("Trained Fighter Crews", "Increases Fire Rate of Escort Ships", (40, 40))
        self.color = color
        self.flag = "trained_escorts"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            pl.Escort.fire_rate -= 40

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            pl.Escort.fire_rate += 40


class Item_escort_gun(Items):

    def __init__(self, color):
        super().__init__("MK I Fighter (Escort)", "An Escort Fighter that fires its gun at hostile ships", (40, 40))
        self.color = color
        self.flag = "escort_gun"

    def effect(self):
        if Items.inventory_dic[5] == self:
            if self.flag not in Items.active_flag_lst:
                Items.active_flag_lst.append(self.flag)
        elif Items.inventory_dic[5] != self:
            if self.flag in Items.active_flag_lst:
                Items.active_flag_lst.remove(self.flag)
                pl.Escort.spawned = False
                data.PLAYER_DATA.remove([obj for obj in data.PLAYER_DATA if obj.__class__.__name__ == "Escort"][0])
                if "2nd_escort" in Items.active_flag_lst:
                    data.PLAYER_DATA.remove([obj for obj in data.PLAYER_DATA if obj.__class__.__name__ == "Escort"][0])

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            pl.Escort.spawned = False
            data.PLAYER_DATA.remove([obj for obj in data.PLAYER_DATA if obj.__class__.__name__ == "Escort"][0])
            if "2nd_escort" in Items.active_flag_lst:
                data.PLAYER_DATA.remove([obj for obj in data.PLAYER_DATA if obj.__class__.__name__ == "Escort"][0])


class Item_escort_missile(Items):

    def __init__(self, color):
        super().__init__("MK II Interceptor (Escort)", "An Escort Fighter that fires Missiles at hostile ships", (40, 40))
        self.color = color
        self.flag = "escort_missile"

    def effect(self):
        if Items.inventory_dic[5] == self:
            if self.flag not in Items.active_flag_lst:
                Items.active_flag_lst.append(self.flag)
        elif Items.inventory_dic[5] != self:
            if self.flag in Items.active_flag_lst:
                Items.active_flag_lst.remove(self.flag)
                pl.Escort.spawned = False
                data.PLAYER_DATA.remove([obj for obj in data.PLAYER_DATA if obj.__class__.__name__ == "Escort"][0])
                if "2nd_escort" in Items.active_flag_lst:
                    data.PLAYER_DATA.remove([obj for obj in data.PLAYER_DATA if obj.__class__.__name__ == "Escort"][0])

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            pl.Escort.spawned = False
            print([obj for obj in data.PLAYER_DATA if obj.__class__.__name__ == "Escort"][0])
            data.PLAYER_DATA.remove([obj for obj in data.PLAYER_DATA if obj.__class__.__name__ == "Escort"][0])
            if "2nd_escort" in Items.active_flag_lst:
                data.PLAYER_DATA.remove([obj for obj in data.PLAYER_DATA if obj.__class__.__name__ == "Escort"][0])


class Item_escort_gunship(Items):

    def __init__(self, color):
        super().__init__("MK III Gun Ship (Escort)", "An Escort Gun Ship that fires a continious Stream of Rounds", (40, 40))
        self.color = color
        self.flag = "escort_gunship"

    def effect(self):
        if Items.inventory_dic[5] == self:
            if self.flag not in Items.active_flag_lst:
                Items.active_flag_lst.append(self.flag)
        elif Items.inventory_dic[5] != self:
            if self.flag in Items.active_flag_lst:
                Items.active_flag_lst.remove(self.flag)
                pl.Escort.spawned = False
                data.PLAYER_DATA.remove([obj for obj in data.PLAYER_DATA if obj.__class__.__name__ == "Escort"][0])
                if "2nd_escort" in Items.active_flag_lst:
                    data.PLAYER_DATA.remove([obj for obj in data.PLAYER_DATA if obj.__class__.__name__ == "Escort"][0])

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            pl.Escort.spawned = False
            data.PLAYER_DATA.remove([obj for obj in data.PLAYER_DATA if obj.__class__.__name__ == "Escort"][0])
            if "2nd_escort" in Items.active_flag_lst:
                data.PLAYER_DATA.remove([obj for obj in data.PLAYER_DATA if obj.__class__.__name__ == "Escort"][0])


## Supply Crate ##


class Item_supply_crate(Items):

    def __init__(self, color, start=False):
        super().__init__("Supply Container", "Provides New Supplies", (38, 38))
        self.color = color
        self.flag = "supply_con"
        self.lvl = 0

    def get_upgrade_desc(self):
        return f"Skill Points: + 1"

    def effect(self):
        if "supply_con" not in Items.active_flag_lst:

            data.LEVELS.skill_points += 1

            # Gfx.create_effect("con_collected", 25, data.PLAYER.hitbox.topleft, hover=True)
            for key, item in Items.inventory_dic.items():
                if item == self:
                    Items.inventory_dic[key] = None


class Item_upgrade_point_crate(Items):

    def __init__(self, color, start=False):
        super().__init__("Scrap", "Used to updgrade Items", (38, 38))
        self.color = color
        self.flag = "upgrade_con"
        self.base_effect = 4
        self.lvl = random.randint(0, 3)

    def get_upgrade_desc(self):
        return f"Upgrade Points: + {int(self.get_lvl_effects(reverse=True)[self.lvl])}"

    def effect(self):
        if "upgrade_con" not in Items.active_flag_lst:

            Items.upgrade_points += int(self.get_lvl_effects(reverse=True)[self.lvl])

            # Gfx.create_effect("con_collected", 25, data.PLAYER.hitbox.topleft, hover=True)
            for key, item in Items.inventory_dic.items():
                if item == self:
                    Items.inventory_dic[key] = None


class Item_heal_crate(Items):

    def __init__(self, color, start=False):
        super().__init__("Spare Part Container", "Spare Parts to restore the Ship to full Strength", (39, 39))
        self.color = color
        self.flag = "heal_con"
        self.base_effect = 4
        self.lvl = random.randint(0, 3)

    def get_upgrade_desc(self):
        return f"Health: + {int(self.get_lvl_effects(reverse=True)[self.lvl])} <> Damage Control: + 1"

    def effect(self):
        if "supply_con" not in Items.active_flag_lst:

            if data.PLAYER.health < data.PLAYER.max_health:
                data.PLAYER.health += int(self.get_lvl_effects(reverse=True)[self.lvl])
                if data.PLAYER.health > data.PLAYER.max_health:
                    data.PLAYER.health = data.PLAYER.max_health
            data.PLAYER.heal_amount += 1

            # Gfx.create_effect("con_collected", 25, data.PLAYER.hitbox.topleft, hover=True)
            for key, item in Items.inventory_dic.items():
                if item == self:
                    Items.inventory_dic[key] = None

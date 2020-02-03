from items import Items
from Gfx import Gfx
import astraid_data as data
from astraid_funcs import *
from init import *


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
        self.base_effect = 4
        self.lvl = random.choices([0, 1, 2, 3], weights=[50, 30, 20, 10], k=1)[0]

    def get_upgrade_desc(self):
        return f"Upgrade Points: + {int(self.get_lvl_effects(reverse=True)[self.lvl])}"

    def effect(self):
        if "supply_con" not in Items.active_flag_lst:

            data.LEVELS.skill_points += int(self.get_lvl_effects(reverse=True)[self.lvl])

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
        self.lvl = random.choices([0, 1, 2, 3], weights=[50, 30, 20, 10], k=1)[0]

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
        self.lvl = random.choices([0, 1, 2, 3], weights=[50, 30, 20, 10], k=1)[0]

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

### Event Items ###


class Event_item_boss_snare(Items):

    def __init__(self, color, start=False):
        super().__init__("Snare", "", (38, 38))
        self.color = color
        self.flag = "boss_snare"
        self.base_effect = 4
        self.lvl = 0

    def get_upgrade_desc(self):
        return f" "

    def effect(self):
        if "boss_snare" not in Items.active_flag_lst:

            data.TURRET.snare_charge += 1

            for key, item in Items.inventory_dic.items():
                if item == self:
                    Items.inventory_dic[key] = None

    def decay(self):
        self.hitbox.move_ip(0, 8)
        if rect_not_on_sreen(self.hitbox):
            Items.dropped_lst.remove(self)
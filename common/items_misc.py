from items import Items
from Gfx import Gfx
import astraid_data as data
from astraid_funcs import *
from init import *


class Item_supply_crate(Items):

    def __init__(self, color, level=None):
        super().__init__("Supply Container", "Provides New Supplies", (24, 0))
        self.color = color
        self.flag = "supply_con"
        self.base_effect = 6
        if level is None:
            self.lvl = random.choices([0, 1, 2, 3], weights=[50, 30, 20, 10], k=1)[0]
        else:
            self.lvl = level

    def get_upgrade_desc(self):
        return f"Upgrade Points: + {int(self.get_lvl_effects(reverse=True)[self.lvl])}"

    def effect(self):
        if "supply_con" not in Items.active_flag_lst:

            data.LEVELS.skill_points += int(self.get_lvl_effects(reverse=True)[self.lvl])

            data.INTERFACE.notification_read = False

            # Gfx.create_effect("con_collected", 25, data.PLAYER.hitbox.topleft, hover=True)
            for key, item in Items.inventory_dic.items():
                if item == self:
                    Items.inventory_dic[key] = None


class Item_upgrade_point_crate(Items):

    def __init__(self, color, level=None):
        super().__init__("Scrap", "Used to updgrade Items", (22, 0))
        self.color = color
        self.flag = "upgrade_con"
        self.base_effect = 4
        if level is None:
            self.lvl = random.choices([0, 1, 2, 3], weights=[50, 30, 20, 10], k=1)[0]
        else:
            self.lvl = level

    def get_upgrade_desc(self):
        return f"Upgrade Points: + {int(self.get_lvl_effects(reverse=True)[self.lvl])}"

    def effect(self):
        if "upgrade_con" not in Items.active_flag_lst:

            Items.upgrade_points += int(self.get_lvl_effects(reverse=True)[self.lvl])

            data.INTERFACE.notification_read = False

            # Gfx.create_effect("con_collected", 25, data.PLAYER.hitbox.topleft, hover=True)
            for key, item in Items.inventory_dic.items():
                if item == self:
                    Items.inventory_dic[key] = None


class Item_heal_crate(Items):

    def __init__(self, color, level=None):
        super().__init__("Spare Part Container", "Spare Parts to restore the Ship to full Strength", (23, 0))
        self.color = color
        self.flag = "heal_con"
        self.base_effect = 4
        if level is None:
            self.lvl = random.choices([0, 1, 2, 3], weights=[50, 30, 20, 10], k=1)[0]
        else:
            self.lvl = level

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


class Event_item_battleship_heal(Items):

    def __init__(self, color, start=False):
        super().__init__("Repair Parts", "", (38, 38))
        self.color = color
        self.flag = "bs_heal"
        self.base_effect = 4
        self.lvl = 0

    def get_upgrade_desc(self):
        return f" "

    def effect(self):
        if "bs_heal" not in Items.active_flag_lst:

            data.EVENTS.bs_heals += 1

            for key, item in Items.inventory_dic.items():
                if item == self:
                    Items.inventory_dic[key] = None

    def decay(self):
        pass


Items.consumables = [
    Event_item_boss_snare,
    Item_supply_crate,
    Item_upgrade_point_crate,
    Item_heal_crate
]

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

    def get_lvl_effects(self, reverse=False):
        return [1, 2, 3, 5]


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

### Prog Items ###


class Item_cd_reduction_prog(Items):

    def __init__(self, color):
        super().__init__("Heatsinks", "Reduces Weapons Cooldown", (34, 1))
        self.color = color
        self.flag = "cd_prog"
        self.base_effect = 4
        self.lvl = None

    def get_upgrade_desc(self):
        return f"CD Reduction: 5s"

    def effect(self):
        if self.flag not in Items.active_flag_lst:

            for key, item in Items.inventory_dic.items():
                if key < 4:
                    if item is not None:
                        if item.cooldown:
                            item.ticker["cd"] += 300
                if item == self:
                    Items.inventory_dic[key] = None

            data.UP_MENU.reset_item_bar()


class Item_damage_prog(Items):

    def __init__(self, color):
        super().__init__("Instable Matter", "Supercharges 1 Standart Projectile, dealing extra Damage", (35, 1))
        self.color = color
        self.flag = "dmg_prog"
        self.base_effect = 4
        self.lvl = None

    def get_upgrade_desc(self):
        return f"Damage: {data.PLAYER.damage + data.PLAYER.damage * 3 * 10}"

    def effect(self):
        if self.flag not in Items.active_flag_lst:

            data.TURRET.special_damage += data.PLAYER.damage * 3

            for key, item in Items.inventory_dic.items():
                if item == self:
                    Items.inventory_dic[key] = None


class Item_shield_prog(Items):

    def __init__(self, color):
        super().__init__("Energy Crystal", "Supercharges the Shield, increasing Strength", (36, 1))
        self.color = color
        self.flag = "shield_prog"
        self.base_effect = 4
        self.lvl = None

    def get_upgrade_desc(self):
        return f"Bonus Shield Strength: 1"

    def effect(self):
        if self.flag not in Items.active_flag_lst:

            data.PLAYER.shield_strength += 1

            for key, item in Items.inventory_dic.items():
                if item == self:
                    Items.inventory_dic[key] = None


### Event Items ###


class Event_item_boss_snare(Items):

    def __init__(self, color, start=False):
        super().__init__("Snare", "", (1, 0))
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


Items.consumables = [
    Event_item_boss_snare,
    Item_supply_crate,
    Item_upgrade_point_crate,
    Item_heal_crate,
    Item_cd_reduction_prog,
    Item_shield_prog,
    Item_damage_prog
]

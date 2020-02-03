from items import Active_Items, Items
from Gfx import Gfx
import astraid_data as data
from astraid_funcs import *
from init import *


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
        self.base_effect = 5400   # cooldown time
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
        self.base_effect = 2700  # cooldwon time
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


class Item_jump_drive(Active_Items):

    def __init__(self, color):
        super().__init__(color, "Jump Drive (active)", "Jumps the ship to the marked location", (0, 1))
        self.color = color
        self.flag = "jump_drive"
        self.base_effect = 600  # cooldown time
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


class Item_shield(Active_Items):

    def __init__(self, color, start=False):
        super().__init__(color, "Shield", f"Shields the ship from hits", (40, 40))
        self.color = color
        self.flag = "shield"
        self.lvl = 0
        self.base_effect = 5400  # cooldown time
        self.cd_len = self.get_lvl_effects()[self.lvl]
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(), "cd")

    def activation_effect(self):
        if not self.cooldown:
            Gfx.create_effect("shield", 2, pl_shield=True)

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


Items.set_drop_table([
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
    (Item_black_hole_bomb, (120, 15, 0))
])
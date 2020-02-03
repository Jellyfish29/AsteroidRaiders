from items import Items
from Gfx import Gfx
import astraid_data as data
from astraid_funcs import *
from init import *


class Item_auto_repair(Items):

    def __init__(self, color):
        super().__init__("Repair Drones (passiv)", "Drones passively repair the Ship over time", (10, 11))
        self.color = color
        self.flag = "auto_repair"
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
        self.base_effect = 0.8
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "Shots/s")

    def get_upgrade_desc(self):
        return f"Bonus Fire Rate: {int(self.get_lvl_effects(reverse=True)[self.lvl] * 100)}%"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            data.TURRET.set_fire_rate(data.TURRET.base_fire_rate * self.get_lvl_effects(reverse=True)[self.lvl])

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.TURRET.set_fire_rate(-(data.TURRET.base_fire_rate * self.get_lvl_effects(reverse=True)[self.lvl]))


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
            data.PLAYER.reset_overdrive()
            Items.active_flag_lst.remove(self.flag)


Items.set_drop_table([
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
])

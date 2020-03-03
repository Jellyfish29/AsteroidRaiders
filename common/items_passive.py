from items import Items
from Gfx import Gfx
import astraid_data as data
from astraid_funcs import *
from init import *
from ui import *


class Item_auto_repair(Items):

    def __init__(self, color):
        super().__init__("Repair Drones (passiv)", "Drones passively repair the Ship over time", (6, 8))
        self.color = color
        self.flag = "auto_repair"
        self.base_effect = 2100
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
        super().__init__("Damage Core (passiv)", "Massivily increases Weapon Damage", (7, 9))
        self.color = color
        self.flag = "damage_core"
        self.base_effect = 1.6
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
        super().__init__("Ablativ Armor (passiv)", "Massivily increases Ship Strength", (8, 10))
        self.color = color
        self.flag = "ablativ_armor"
        self.base_effect = 10
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "HP")

    def get_upgrade_desc(self):
        return f"Bonus Health: {int(self.get_lvl_effects(reverse=True)[self.lvl])}"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            data.PLAYER.health_limit += 5
            data.PLAYER.set_player_health(int(self.get_lvl_effects(reverse=True)[self.lvl]))

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.PLAYER.health_limit -= 5
            data.PLAYER.set_player_health(-int(self.get_lvl_effects(reverse=True)[self.lvl]))


class Item_engine_core(Items):

    def __init__(self, color):
        super().__init__("Engine Core (passiv)", "Massivily increases Ship Speed", (9, 11))
        self.color = color
        self.flag = "engine_core"
        self.base_effect = 5
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "km/s")

    def get_upgrade_desc(self):
        return f"Bonus Speed: {int(self.get_lvl_effects(reverse=True)[self.lvl])}"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            data.PLAYER.speed_limit += 2
            data.PLAYER.set_player_speed(int(self.get_lvl_effects(reverse=True)[self.lvl]))

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.PLAYER.speed_limit -= 2
            data.PLAYER.set_player_speed(-int(self.get_lvl_effects(reverse=True)[self.lvl]))


class Item_ammo_racks(Items):

    def __init__(self, color):
        super().__init__("Ammo Racks (passiv)", "Reduces all Cooldowns by 30 %", (10, 12))
        self.color = color
        self.flag = "ammo_racks"
        self.base_effect = 0.3
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "cd red")

    def get_upgrade_desc(self):
        return f"Cooldown Reduction: {int(self.get_lvl_effects(reverse=True)[self.lvl] * 100)}%"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            data.ACTIVE_ITEMS.cd_limit += 0.2
            data.ACTIVE_ITEMS.set_cd_reduction(self.get_lvl_effects(reverse=True)[self.lvl])

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.ACTIVE_ITEMS.cd_limit -= 0.2
            data.ACTIVE_ITEMS.set_cd_reduction(-self.get_lvl_effects(reverse=True)[self.lvl])


class Item_improved_feeding(Items):

    def __init__(self, color):
        super().__init__("Improved Ammo Feeding System (passiv)", "Increases Fire Rate", (11, 13))
        self.color = color
        self.flag = "improved_feeding"
        self.base_effect = 0.5
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


class Item_hyper_shields(Items):

    def __init__(self, color):
        super().__init__("Hyper Shields (passiv)", "Massivliy Increases Shield Duration", (12, 14))
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


class Item_fan_shot(Items):

    def __init__(self, color):
        super().__init__("MULTI Cannon (shot mod)", "Fires 2 extra shots every 4 shots", (15, 17))
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
        super().__init__("HAMMER Cannon (shot mod)", "Every 5th shot deals increased Damage", (16, 18))
        self.color = color
        self.flag = "hammer_shot"
        self.base_effect = 12
        self.effect_strength = int(self.get_lvl_effects(reverse=True)[self.lvl])
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "DMG")

    def get_upgrade_desc(self):
        return f"Bonus Damage: {int(self.get_lvl_effects(reverse=True)[self.lvl]) * 10} <> Attack Interval: 5"

    def set_effect_strength(self):
        self.effect_strength = int(self.get_lvl_effects(reverse=True)[self.lvl])


class Item_hyper_velocity_rounds(Items):

    def __init__(self, color):
        super().__init__("Hyper Velocity Rounds (shot mod)", "Increases Projectile Speed and Damage", (18, 20))
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
        super().__init__("Weapons system Overdrive (passive)", "Every Kill increases Damage and Fire Rate until taking Damage", (19, 21))
        self.color = color
        self.flag = "overdrive"
        self.base_effect = 28
        self.effect_strength = int(self.get_lvl_effects(reverse=True)[self.lvl])
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "Stacks")

    def get_upgrade_desc(self):
        return f"Max Stacks: {int(self.get_lvl_effects(reverse=True)[self.lvl])}"

    def set_effect_strength(self):
        self.effect_strength = int(self.get_lvl_effects(reverse=True)[self.lvl])

    # def set_text_update(self):
    #     self.text = f"{data.TURRET.overdrive_count}/{int(self.effect_strength)}"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            for _ in range(data.TURRET.overdrive_count):
                data.PLAYER.damage += 0.05
                data.TURRET.set_fire_rate(0.07)
            if data.PLAYER.indicator_slots[0] is None:  # left
                data.PLAYER.indicator_slots[0] = Gui_text(
                    anchor=data.PLAYER.hitbox,
                    anchor_x=data.PLAYER.indicator_pos[0][0],
                    anchor_y=data.PLAYER.indicator_pos[0][1],
                    text=lambda: f"{int(data.TURRET.overdrive_count)}/{self.effect_strength}",
                    text_size=15,
                    flag="overdrive_counter")
                data.PLAYER.indicator_slots[2] = Gui_image(
                    anchor=data.PLAYER.hitbox,
                    anchor_x=data.PLAYER.indicator_pos[0][0] - 30,
                    anchor_y=data.PLAYER.indicator_pos[0][1] - 5,
                    img_idx=14,
                    flag="overdrive_counter")
            else:  # Right
                if data.PLAYER.indicator_slots[1] is None:
                    data.PLAYER.indicator_slots[1] = Gui_text(
                        anchor=data.PLAYER.hitbox,
                        anchor_x=data.PLAYER.indicator_pos[1][0],
                        anchor_y=data.PLAYER.indicator_pos[1][1],
                        text=lambda: f"{int(data.TURRET.overdrive_count)}/{int(self.effect_strength)}",
                        text_size=15,
                        flag="overdrive_counter")
                    data.PLAYER.indicator_slots[3] = Gui_image(
                        anchor=data.PLAYER.hitbox,
                        anchor_x=data.PLAYER.indicator_pos[1][0] + 30,
                        anchor_y=data.PLAYER.indicator_pos[1][1] - 5,
                        img_idx=14,
                        flag="overdrive_counter")

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            for _ in range(data.TURRET.overdrive_count):
                data.PLAYER.damage -= 0.05
                data.TURRET.set_fire_rate(-0.07)

            Items.active_flag_lst.remove(self.flag)
            for key in data.PLAYER.indicator_slots:
                if data.PLAYER.indicator_slots[key] is not None:
                    if data.PLAYER.indicator_slots[key].flag == "overdrive_counter":
                        data.PLAYER.indicator_slots[key] = None


class Item_targeting_scanner(Items):

    def __init__(self, color):
        super().__init__("Improved Targeting Scanner (passiv)", "Increases Crit Chance", (32, 30))
        self.color = color
        self.flag = "targeting_scanner"
        self.base_effect = 25
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "Shots/s")

    def get_upgrade_desc(self):
        return f"Bonus Crit Chance: {int(self.get_lvl_effects(reverse=True)[self.lvl])}%"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            data.PLAYER.crit_limit -= 10
            data.PLAYER.set_player_crit_chance(int(self.get_lvl_effects(reverse=True)[self.lvl]))

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.PLAYER.crit_limit += 10
            data.PLAYER.set_player_crit_chance(-int(self.get_lvl_effects(reverse=True)[self.lvl]))


class Item_expert_damage_control(Items):

    def __init__(self, color):
        super().__init__("Expert Damage Controll (passiv)", "Increases Damage Control Power Up Efficiency", (13, 15))
        self.color = color
        self.flag = "ex_damage_control"
        self.base_effect = 8

    def get_upgrade_desc(self):
        return f"Bonus Heal: {int(self.get_lvl_effects(reverse=True)[self.lvl])}"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            data.PLAYER.heal_strenght += int(self.get_lvl_effects(reverse=True)[self.lvl])

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.PLAYER.heal_strenght -= int(self.get_lvl_effects(reverse=True)[self.lvl])


class Item_bi_weave_shields(Items):

    def __init__(self, color):
        super().__init__("Bi-Weave Shields (passiv)", "Reduces Shield Strength for faster Shield Recharge Rate", (1, 1))
        self.color = color
        self.flag = "bi_weave_shields"
        self.base_effect = 0.35
        self.player_shield_orig_base = 5400
        # self.upgrade_desc = self.get_upgrade_desc(self.get_lvl_effects(reverse=True), "Shield HP")

    def get_upgrade_desc(self):
        return f"CD Reduction: {int((1 - self.get_lvl_effects()[self.lvl]) * 100)}s"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            data.PLAYER.max_shield_strength = int(data.PLAYER.max_shield_strength / 2)
            if data.PLAYER.shield_strength > data.PLAYER.max_shield_strength:
                data.PLAYER.shield_strength = data.PLAYER.max_shield_strength
            data.PLAYER.shield.base_effect *= self.get_lvl_effects()[self.lvl]
            data.PLAYER.shield.set_effect_strength()

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.PLAYER.max_shield_strength = int(data.PLAYER.max_shield_strength * 2)
            data.PLAYER.shield.base_effect = self.player_shield_orig_base
            data.PLAYER.shield.set_effect_strength()


class Item_debris_scanner(Items):

    def __init__(self, color):
        super().__init__("Debris Scanner (passiv)", "Passivily Scans the Debris of destroyed Enemys for useful Items", (1, 1))
        self.color = color
        self.flag = "debris_scanner"
        self.base_effect = 12
        self.effect_strength = self.get_lvl_effects(reverse=True)[self.lvl]

    def get_upgrade_desc(self):
        return f"Discovery Chance: {int(self.get_lvl_effects(reverse=True)[self.lvl])} %"

    def set_effect_strength(self):
        self.effect_strength = self.get_lvl_effects(reverse=True)[self.lvl]

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)


class Item_reflex_shield(Items):

    def __init__(self, color):
        super().__init__("Reflex Shields (passiv)", "Incomming damage to the Shield gets relfected, amplified and dispersed around the ship", (1, 1))
        self.color = color
        self.flag = "reflex_shield"
        self.base_effect = 4
        self.effect_strength = self.get_lvl_effects(reverse=True)[self.lvl]

    def get_upgrade_desc(self):
        return f"Reflex Damage: {data.PLAYER.damage * 4 * 10 * int(self.get_lvl_effects(reverse=True)[self.lvl])} / Shield strength + 1"

    def set_effect_strength(self):
        self.effect_strength = self.get_lvl_effects(reverse=True)[self.lvl]

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            data.PLAYER.shield_strength += 1
            data.PLAYER.max_shield_strength += 1

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            data.PLAYER.shield_strength -= 1
            data.PLAYER.max_shield_strength -= 1


Items.set_drop_table([
    (Item_auto_repair, (255, 0, 0)),
    (Item_targeting_scanner, (0, 0, 0)),
    (Item_damage_core, (100, 250, 20)),
    (Item_ablativ_armor, (200, 40, 170)),
    (Item_engine_core, (10, 100, 200)),
    (Item_ammo_racks, (255, 0, 70)),
    (Item_improved_feeding, (0, 20, 40)),
    (Item_hyper_shields, (99, 99, 230)),
    (Item_fan_shot, (12, 64, 1)),
    (Item_hammer_shot, (99, 140, 3)),
    (Item_hyper_velocity_rounds, (1, 169, 201)),
    (Item_expert_damage_control, (0, 0, 0)),
    (Item_overdrive, (89, 1, 37)),
    (Item_bi_weave_shields, (0, 0, 0)),
    (Item_debris_scanner, (0, 0, 0)),
    (Item_reflex_shield, (0, 0, 0))
])

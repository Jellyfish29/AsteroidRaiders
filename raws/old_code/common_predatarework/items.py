import pygame
from pygame.locals import *
import random

from init import *
from astraid_funcs import *
# import turret as tr
import player as pl
import turret as tr
import levels as lvl
import power_ups as pup
from Gfx import Gfx


class Items:

    dropped_lst = []
    inventory_dic = {0: None, 1: None, 2: None, 3: None, 4: None}
    inventory_size = 5
    gfx_img = None
    inv_grid_cords = [(300, 300), (450, 300), (200, 500), (350, 500), (500, 500)]
    active_items = 2
    active_flag_lst = []
    drop_table = []
    drop_amount = 2
    front = pygame.font.SysFont("fixed", 20, 10)
    gfx_img = get_images("icons")
    tt_delay = 15

    def __init__(self, item_name, discription, gfx_idx, start=False):
        self.hitbox = pygame.Rect(-1000, -1000, 50, 50)
        if start:
            self.hitbox = pygame.Rect(Items.inv_grid_cords[0][0] + 25, Items.inv_grid_cords[0][1] + 25, 50, 50)
        self.item_name = item_name
        self.discription = discription
        self.gfx_idx = gfx_idx
        self.tc = Time_controler()
        self.drag = False
        self.clicked = False
        self.color = (0, 0, 160)
        self.text = " "

    def draw(self):
        pygame.draw.rect(win, self.color, self.hitbox)

    def activ(self):
        self.effect()

    def pick_up(self, dropped=False):
        if self.hitbox.colliderect(pl.Player.hitbox) or dropped:
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
                if isinstance(self, Item_supply_crate):
                    self.effect()
                else:
                    Items.dropped_lst.append(self)

    def collision_avoidance(self):
        for item in Items.dropped_lst:
            if self != item:
                if self.hitbox.colliderect(item.hitbox):
                    self.hitbox.move_ip(random.choice([50, -50]), 0)

    def drop_from_inv(self, key):
        self.hitbox.center = (pl.Player.hitbox.center[0], pl.Player.hitbox.center[1] + 100)
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
                        Items.inventory_dic[idx].pick_up(dropped=True)
                        Items.inventory_dic[idx] = None
                    Items.inventory_dic[idx] = self
                    self.hitbox.topleft = (slot.topleft[0] + 25, slot.topleft[1] + 25)
                    break
            else:
                self.drop_from_inv(key)
            self.drag = False

    def decay(self):
        if not lvl.Levels.after_boss:
            self.hitbox.move_ip(0, 2)
            if rect_not_on_sreen(self.hitbox):
                Items.dropped_lst.remove(self)

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
        self.__class__.active = False

    def tool_tip(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if self.tc.delay(True, limit=Items.tt_delay):
                win.blit(pygame.font.SysFont("fixed", 20, 10).render(self.item_name, True, (255, 255, 255)), (pygame.mouse.get_pos()[0] + 30, pygame.mouse.get_pos()[1]))
                win.blit(pygame.font.SysFont("fixed", 15, 10).render(self.discription, True, (255, 255, 255)), (pygame.mouse.get_pos()[0] + 30, pygame.mouse.get_pos()[1] + 30))
        else:
            self.tc.delay(False)

    def gfx_draw(self):
        win.blit(Items.gfx_img[self.gfx_idx], self.hitbox)

    def toggle(self):
        pass

    def activation_effect(self):
        pass

    def end_activation(self):
        pass

    def item_generator():
        global drop_table_absolute
        if len(Items.drop_table) < 3:
            Items.drop_table = drop_table_absolute.copy()
        item, color = Items.drop_table.pop(random.randint(0, len(Items.drop_table) - 1))
        return item(color)

    def drop(location, amount=0, target=None):
        if target is not None:
            Items.dropped_lst.append(target)
            if amount == 2:
                Items.dropped_lst.append(target)
        else:
            while len(Items.dropped_lst) < amount:
                random_item = Items.item_generator()
                for key in Items.inventory_dic:
                    if type(random_item) == type(Items.inventory_dic[key]):
                        break
                else:
                    Items.dropped_lst.append(random_item)
        for i, item in enumerate(Items.dropped_lst):
            item.hitbox.center = (location[0] + i * 100, location[1])

    def update():
        # print(Items.active_flag_lst)
        for item in Items.dropped_lst:
            item.draw()
            # item.gfx_draw()
            item.decay()
            item.pick_up()
            item.collision_avoidance()
            item.tool_tip()

        for i in range(5):
            try:
                Items.inventory_dic[i].effect()
            except AttributeError:
                pass


class Placeholder(Items):

    active = False

    def __init__(self, color):
        super().__init__("placeholder name", "placeholder discription", 1)
        self.color = color
        self.flag = "placeholder"

### Activ Items ###


class Item_pd(Items):

    active = False

    def __init__(self, color, start=False):
        super().__init__("Pointdefence (active)", "shoots down incoming enemy weapons", 1, start=start)
        self.color = color
        self.flag = "point_defence"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
        self.text = str(int(tr.Turret.pd_ammo))

    def toggle(self):
        if not Item_pd.active:
            Item_pd.active = True
        else:
            Item_pd.active = False

    def activation_effect(self):
        if Item_pd.active:
            Gfx.create_effect("pd_on", 25, pl.Player.hitbox.topleft, hover=True)


class Item_missile(Items):

    active = False

    def __init__(self, color):
        super().__init__("Heat seeking Missiles (acive)", "Fires two heat seeking Missile at the Target", 2)
        self.color = color
        self.flag = "missile"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
        self.text = str(int(tr.Turret.missile_ammo))

    def toggle(self):
        Item_missile.active = True


class Item_nuke(Items):

    active = False

    def __init__(self, color):
        super().__init__("Nuclear Warhead (active)", "Fires a 45 Megaton nuclear Warhead", 3)
        self.color = color
        self.flag = "nuke"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
        self.text = str(int(tr.Turret.nuke_ammo))

    def toggle(self):
        Item_nuke.active = True


class Item_jump_drive(Items):

    active = False
    engage = False

    def __init__(self, color):
        super().__init__("Jump Drive (active)", "Jumps the ship to the marked location", 4)
        self.color = color
        self.flag = "jump_drive"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
        self.text = str(int(pl.Player.jump_charges))

    def toggle(self):
        Item_jump_drive.active = True

    def end_activation(self):
        Item_jump_drive.engage = True


class Item_he_rounds(Items):

    active = False

    def __init__(self, color, start=False):
        super().__init__("HE Rounds (active)", "On Activation fires Powerful HE Rounds that explode on impact", 1, 19)
        self.color = color
        self.flag = "he_rounds"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
        self.text = str(int(tr.Turret.he_ammo))

    def toggle(self):
        if not Item_he_rounds.active:
            Item_he_rounds.active = True
        else:
            Item_he_rounds.active = False

    def activation_effect(self):
        if Item_he_rounds.active:
            Gfx.create_effect("pd_on", 25, pl.Player.hitbox.topleft, hover=True)


### Passiv Items ###


class Item_auto_repair(Items):

    active = False

    def __init__(self, color):
        super().__init__("Repair Drones (passiv)", "Drones passively repair the Ship over time", 5)
        self.color = color
        self.flag = "auto_repair"
        self.tc = Time_controler()

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
        if self.tc.trigger_1(1500):
            if pl.Player.health < pl.Player.max_health:
                pl.Player.health += 1


class Item_damage_core(Items):

    active = False

    def __init__(self, color):
        super().__init__("Damage Core (passiv)", "Massivily increases Weapon Damage", 6)
        self.color = color
        self.flag = "damage_core"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            pl.Player.damage += 1

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            pl.Player.damage -= 1
        self.__class__.active = False


class Item_ablativ_armor(Items):

    active = False

    def __init__(self, color):
        super().__init__("Ablativ Armor (passiv)", "Massivily increases Ship Strength", 7)
        self.color = color
        self.flag = "ablativ_armor"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            pl.Player.max_health += 6

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            pl.Player.max_health -= 6
        self.__class__.active = False


class Item_engine_core(Items):

    active = False

    def __init__(self, color):
        super().__init__("Engine Core (passiv)", "Massivily increases Ship Speed", 8)
        self.color = color
        self.flag = "engine_core"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            pl.Player.speed += 2.5
            pl.Player.directions = directions(pl.Player.speed)

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            pl.Player.speed -= 2.5
            pl.Player.directions = directions(pl.Player.speed)
        self.__class__.active = False


class Item_ammo_racks(Items):

    active = False

    def __init__(self, color):
        super().__init__("Ammo Racks (passiv)", "Increases Special Munitions Stowage", 9)
        self.color = color
        self.flag = "ammo_racks"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            tr.Turret.super_shot_ammo += 70
            tr.Turret.star_shot_ammo += 50

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            tr.Turret.super_shot_ammo -= 70
            tr.Turret.star_shot_ammo -= 50
        self.__class__.active = False


class Item_improved_feeding(Items):

    active = False

    def __init__(self, color):
        super().__init__("Improved Ammo Feeding System (passiv)", "Increases Fire Rate", 10)
        self.color = color
        self.flag = "improved_feeding"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            tr.Turret.fire_rate -= 10
            tr.Turret.normal_fire_rate -= 10

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            tr.Turret.fire_rate += 10
            tr.Turret.normal_fire_rate += 10
        self.__class__.active = False


class Item_hyper_shields(Items):

    active = False

    def __init__(self, color):
        super().__init__("Hyper Shields (passiv)", "Massivliy Increases Shield Duration", 11)
        self.color = color
        self.flag = "hyper_shields"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            pup.Power_ups.shield_time += 600

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            pup.Power_ups.shield_time -= 600
        self.__class__.active = False


class Item_expert_damage_control(Items):

    active = False

    def __init__(self, color):
        super().__init__("Expert Damage Controll (passiv)", "Increases Damage Control Power Up Efficiency", 12)
        self.color = color
        self.flag = "ex_damage_control"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            pup.Power_ups.heal_strength += 2

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            pup.Power_ups.heal_strength -= 2
        self.__class__.active = False


class Item_super_star(Items):

    active = False

    def __init__(self, color):
        super().__init__("ARC Cannon (passiv)", "Effects of STAR and SUPER shot combined", 13)
        self.color = color
        self.flag = "super_star"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            tr.Turret.star_shot_ammo += 20
        if pup.Power_ups.super_shot:
            pup.Power_ups.star_shot = True
        if pup.Power_ups.star_shot:
            pup.Power_ups.super_shot = True

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            tr.Turret.star_shot_ammo -= 20
        self.__class__.active = False


class Item_fan_shot(Items):

    active = False

    def __init__(self, color):
        super().__init__("MULTI Cannon (shot mod)", "Fires 2 extra shots every 4 shots", 14)
        self.color = color
        self.flag = "fan_shot"


class Item_hammer_shot(Items):

    active = False

    def __init__(self, color):
        super().__init__("HAMMER Cannon (shot mod)", "Every 5th shot deals increased Damage", 15)
        self.color = color
        self.flag = "hammer_shot"


class Item_piercing_shot(Items):

    active = False

    def __init__(self, color):
        super().__init__("Hyper Penetrator rounds (shot mod)", "Rounds pierce the target and deal damge depending on traveltime", 16)
        self.color = color
        self.flag = "piercing_shot"


class Item_hyper_velocity_rounds(Items):

    active = False

    def __init__(self, color):
        super().__init__("Hyper Velocity Rounds (shot mod)", "Increases Projectile Speed and Damage", 17)
        self.color = color
        self.flag = "hyper_vel_rounds"

    def effect(self):
        if self.flag not in Items.active_flag_lst:
            Items.active_flag_lst.append(self.flag)
            tr.Turret.angles = angles_360(30)
            pl.Player.damage += 0.4

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            tr.Turret.angles = angles_360(tr.Turret.projectile_speed)
            pl.Player.damage -= 0.4
        self.__class__.active = False


class Item_overdrive(Items):

    active = False

    def __init__(self, color):
        super().__init__("Weapons system Overdrive (passive)", "Every Kill increases Damage and Fire Rate until taking Damage", 18)
        self.color = color
        self.flag = "overdrive"

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            pl.Player.damage -= 0.05 * tr.Turret.overdrive_count
            tr.Turret.fire_rate += 0.7 * tr.Turret.overdrive_count
            tr.Turret.overdrive_count = 0
        self.__class__.active = False


## Escorts ##


class Item_2nd_escort(Items):

    active = False

    def __init__(self, color):
        super().__init__("Improved Hangar", "The Hangar is now able to support two Escort Craft", 16)
        self.color = color
        self.flag = "2nd_escort"


class Item_escort_improve(Items):

    active = False

    def __init__(self, color):
        super().__init__("Trained Fighter Crews", "Increases Fire Rate of Escort Ships", 17)
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
        self.__class__.active = False


class Item_escort_gun(Items):

    active = False

    def __init__(self, color):
        super().__init__("MK I Fighter (Escort)", "An Escort Fighter that fires its gun at hostile ships", 18)
        self.color = color
        self.flag = "escort_gun"

    def effect(self):
        if Items.inventory_dic[4] == self:
            if self.flag not in Items.active_flag_lst:
                Items.active_flag_lst.append(self.flag)
        elif Items.inventory_dic[4] != self:
            if self.flag in Items.active_flag_lst:
                Items.active_flag_lst.remove(self.flag)
                pl.Escort.spawned = False
                pl.Escort.lst.clear()

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            pl.Escort.spawned = False
            pl.Escort.lst.clear()
        self.__class__.active = False


class Item_escort_missile(Items):

    active = False

    def __init__(self, color):
        super().__init__("MK II Interceptor (Escort)", "An Escort Fighter that fires Missiles at hostile ships", 18)
        self.color = color
        self.flag = "escort_missile"

    def effect(self):
        if Items.inventory_dic[4] == self:
            if self.flag not in Items.active_flag_lst:
                Items.active_flag_lst.append(self.flag)
        elif Items.inventory_dic[4] != self:
            if self.flag in Items.active_flag_lst:
                Items.active_flag_lst.remove(self.flag)
                pl.Escort.spawned = False
                pl.Escort.lst.clear()

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            pl.Escort.spawned = False
            pl.Escort.lst.clear()
        self.__class__.active = False


class Item_escort_gunship(Items):

    active = False

    def __init__(self, color):
        super().__init__("MK III Gun Ship (Escort)", "An Escort Gun Ship that fires a continious Stream of Rounds", 18)
        self.color = color
        self.flag = "escort_gunship"

    def effect(self):
        if Items.inventory_dic[4] == self:
            if self.flag not in Items.active_flag_lst:
                Items.active_flag_lst.append(self.flag)
        elif Items.inventory_dic[4] != self:
            if self.flag in Items.active_flag_lst:
                Items.active_flag_lst.remove(self.flag)
                pl.Escort.spawned = False
                pl.Escort.lst.clear()

    def end_effect(self):
        if self.flag in Items.active_flag_lst:
            Items.active_flag_lst.remove(self.flag)
            pl.Escort.spawned = False
            pl.Escort.lst.clear()
        self.__class__.active = False


## Supply Crate ##


class Item_supply_crate(Items):

    active = False

    def __init__(self, color, start=False):
        super().__init__("Supply Container", "Provides New Supplies", 1, 20)
        self.color = color
        self.flag = "supply_con"

    def effect(self):
        if "supply_con" not in Items.active_flag_lst:
            pup.Power_ups.supply_drop()
            # Gfx.create_effect("con_collected", 25, pl.Player.hitbox.topleft, hover=True)
            for key, item in Items.inventory_dic.items():
                if item == self:
                    Items.inventory_dic[key] = None


class Item_heal_crate(Items):

    active = False

    def __init__(self, color, start=False):
        super().__init__("Spare Part Container", "Spare Parts to restore the Ship to full Strength", 1, 20)
        self.color = color
        self.flag = "heal_con"

    def effect(self):
        if "supply_con" not in Items.active_flag_lst:
            pup.Power_ups.heal_drop()
            # Gfx.create_effect("con_collected", 25, pl.Player.hitbox.topleft, hover=True)
            for key, item in Items.inventory_dic.items():
                if item == self:
                    Items.inventory_dic[key] = None


drop_table_absolute = [
    (Item_pd, (100, 0, 0)),
    (Item_jump_drive, (0, 100, 0)),
    (Item_nuke, (0, 0, 100)),
    (Item_missile, (100, 100, 0)),
    (Item_auto_repair, (255, 0, 0)),
    (Item_damage_core, (100, 250, 20)),
    (Item_ablativ_armor, (200, 40, 170)),
    (Item_engine_core, (10, 100, 200)),
    (Item_ammo_racks, (255, 0, 70)),
    (Item_improved_feeding, (0, 20, 40)),
    (Item_hyper_shields, (99, 99, 230)),
    (Item_expert_damage_control, (20, 10, 251)),
    (Item_super_star, (64, 21, 190)),
    (Item_fan_shot, (12, 64, 1)),
    (Item_hammer_shot, (99, 140, 3)),
    (Item_piercing_shot, (120, 15, 0)),
    (Item_hyper_velocity_rounds, (1, 169, 201)),
    (Item_overdrive, (89, 1, 37)),
    (Item_he_rounds, (200, 19, 123)),
    (Item_2nd_escort, (0, 23, 63)),
    (Item_escort_improve, (10, 20, 30)),
    (Item_escort_gunship, (90, 12, 54)),
    (Item_escort_gun, (39, 178, 210)),
    (Item_escort_missile, (32, 99, 99))
]

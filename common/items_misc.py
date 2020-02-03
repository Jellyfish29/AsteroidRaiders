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

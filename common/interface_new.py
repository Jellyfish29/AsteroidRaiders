from init import *
from ui import *
import astraid_data as data
from Gfx import Gfx, Background


class Interface_new(Timer):

    item_slots = {
        0: (772, 1016),
        1: (829, 1016),
        2: (885, 1016),
        3: (941, 1016),
        4: (997, 1016),
        5: (1054, 1016),
        6: (1109, 1016),
        7: (1165, 1016),
        8: (1222, 1016),
        9: (1276, 1016),

    }

    @classmethod
    def set_up_standart_ui(cls):
        # Item bar
        Gui.add(Gui_image(loc=(750, 995), img_idx=1))

        # Score board
        Gui.add(Gui_image(loc=(0, 0), img_idx=2))
        Gui.add(Gui_text(loc=(65, 4), text=lambda: f"{data.LEVELS.display_score}"))
        Gui.add(Gui_text(loc=(65, 34), text=lambda: f"{data.LEVELS.level}"))

        # Health bar
        Gui.add(Gui_image(loc=(0, 1000), img_idx=3))
        Gui.add(Gui_text(loc=(65, 1010), text=lambda: f"{data.PLAYER.heal_amount}"))
        Gui.add(Gui_text(loc=(100, 1010), text=lambda: f"(+{data.PLAYER.heal_strenght})"))
        Gui.add(Gui_text(loc=(65, 1040), text=lambda: f"{data.PLAYER.health}"))
        Gui.add(Gui_text(loc=(100, 1040), text=lambda: f"/{data.PLAYER.max_health}"))

        # Gui.add(Gui_image(loc=cls.item_slots[0], img_idx=1, sprites=Gui.item_small_sprites))
        # Gui.add(Gui_image(loc=cls.item_slots[1], img_idx=2, sprites=Gui.item_small_sprites))

    @classmethod
    def set_up_items_ui(cls):
        for i in range(5):
            Gui.add(Gui_text(loc=(cls.item_slots[i][0], cls.item_slots[i][1] + 12),
                             text=lambda: data.ITEMS.inventory_dic[i].text if data.ITEMS.inventory_dic[i] is not None else f" ",
                             text_size=25))

    @classmethod
    def create(cls):
        cls.set_up_standart_ui()

    @classmethod
    def update(cls):
        pass


data.INTERFACE = Interface_new

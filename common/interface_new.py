from init import *
from ui import *
import astraid_data as data
from Gfx import Gfx, Background


class Interface_new(Timer):

    # Standart Ui
    standat_ui = []
    # Health bar
    health_bar = []
    health_bar_x_pos = 55
    max_health_indicator = pygame.Rect(0, 0, 0, 0)
    # Shield indicator
    shield_bar = []
    shield_x_pos = 0
    # Inventory
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
    inventory = {i: [] for i in range(11)}
    item_bar = None
    # Indicators
    indicators = {}
    show_skill_upgrade = True
    show_item_upgrade = True

    @classmethod
    def set_up_standart_ui(cls):
        # Item bar
        cls.item_bar = Gui_image(loc=(750, 995), img_idx=1)

        # Score board
        cls.standat_ui.append(Gui_image(loc=(0, 0), img_idx=2))
        cls.standat_ui.append(Gui_text(loc=(65, 4), text=lambda: f"{data.LEVELS.display_score}"))
        cls.standat_ui.append(Gui_text(loc=(65, 34), text=lambda: f"{data.LEVELS.level}"))

        # Health bar
        cls.standat_ui.append(Gui_image(loc=(0, 1000), img_idx=3))
        cls.standat_ui.append(Gui_text(loc=(65, 1010), text=lambda: f"{data.PLAYER.heal_amount}"))
        cls.standat_ui.append(Gui_text(loc=(100, 1010), text=lambda: f"(+{data.PLAYER.heal_strenght})"))
        cls.standat_ui.append(Gui_image(anchor=cls.max_health_indicator, img_idx=5))

        # standart Items
        cls.inventory[8].append(Gui_image(
            loc=cls.item_slots[8], flag="shield",
            img_idx=1, sprites=Gui.item_small_sprites))

        cls.inventory[8].append(Gui_text(
            loc=(cls.item_slots[8][0] + 15, cls.item_slots[8][1] + 12),
            text=lambda: data.PLAYER.shield.text))

        cls.inventory[9].append(Gui_image(
            loc=cls.item_slots[9], flag="jump_drive",
            img_idx=3, sprites=Gui.item_small_sprites))

        cls.inventory[9].append(Gui_text(
            loc=(cls.item_slots[9][0] + 15, cls.item_slots[9][1] + 12),
            text=lambda: data.PLAYER.jumpdrive.text))

        # Upgrade Indicators
        cls.indicators.update({"skill_up": Gui_image(loc=(0, 100), img_idx=9, animation_interval=80)})
        cls.indicators.update({"item_up": Gui_image(loc=(0, 150), img_idx=8, animation_interval=80)})
        cls.indicators.update({"shield": Gui_image(loc=(1222, 1016), img_idx=2, sprites=Gui.item_small_sprites)})
        cls.indicators.update({"jumpdrive": Gui_image(loc=(1276, 1016), img_idx=2, sprites=Gui.item_small_sprites)})

    @classmethod
    def standart_ui_update(cls):
        for element in cls.standat_ui:
            element.tick()

    @classmethod
    def health_bar_update(cls):
        while len(cls.health_bar) < data.PLAYER.health:
            if len(cls.health_bar) == 1:
                cls.health_bar.pop()
                cls.health_bar.append(Gui_image(loc=(cls.health_bar_x_pos - 20, 1040), img_idx=4))

            cls.health_bar.append(Gui_image(loc=(cls.health_bar_x_pos, 1040), img_idx=4))
            cls.health_bar_x_pos += 20

        while len(cls.health_bar) > data.PLAYER.health:
            cls.health_bar.pop()
            cls.health_bar_x_pos -= 20

            if len(cls.health_bar) == 1:
                cls.health_bar.pop()
                cls.health_bar.append(Gui_image(loc=(cls.health_bar_x_pos - 20, 1040), img_idx=(4, 0), animation_interval=16))

        for element in cls.health_bar:
            element.tick()

        cls.max_health_indicator.topleft = (70 + (20 * data.PLAYER.max_health), 1035)

    @classmethod
    def player_shield_update(cls):
        if data.PLAYER.shield.active:
            while len(cls.shield_bar) < data.PLAYER.shield_strength:
                cls.shield_bar.append(Gui_image(img_idx=7, anchor=data.PLAYER.hitbox,
                                                anchor_x=80 + cls.shield_x_pos, anchor_y=15))
                cls.shield_x_pos += 15
            while len(cls.shield_bar) > data.PLAYER.shield_strength:
                cls.shield_bar.pop()
                cls.shield_x_pos -= 15
        else:
            cls.shield_bar.clear()

        for element in cls.shield_bar:
            element.tick()

    @classmethod
    def update_item_ui(cls):
        for key, item in data.ITEMS.inventory_dic.items():
            if item is not None:
                if issubclass(item.__class__, data.ACTIVE_ITEMS):
                    if item.set_cd_img:
                        if item.active:
                            if item.active_time is not None:
                                cls.inventory[key].insert(1, (Gui_image(
                                    loc=data.INTERFACE.item_slots[key], img_idx=2,
                                    sprites=Gui.item_small_sprites, decay=item.active_time)
                                ))
                                item.set_cd_img = False
                        elif item.cooldown:
                            cls.inventory[key].insert(1, (Gui_image(
                                loc=data.INTERFACE.item_slots[key], img_idx=2,
                                sprites=Gui.item_small_sprites, decay=item.cd_len)
                            ))
                            item.set_cd_img = False
            else:
                if cls.inventory[key] is not None:
                    cls.inventory[key] = []

        for key in cls.inventory:
            for element in cls.inventory[key]:
                if element.kill:
                    cls.inventory[key].remove(element)
                else:
                    element.tick()

        cls.item_bar.tick()

    @classmethod
    def update_standart_item_ui(cls):
        if data.PLAYER.shield.cooldown:
            if data.PLAYER.shield.set_cd_img:
                cls.inventory[8].insert(1, (Gui_image(
                    loc=data.INTERFACE.item_slots[8], img_idx=2,
                    sprites=Gui.item_small_sprites, decay=data.PLAYER.shield.cd_len)
                ))
                data.PLAYER.shield.set_cd_img = False

        if data.PLAYER.jumpdrive.cooldown:
            if data.PLAYER.jumpdrive.set_cd_img:
                cls.inventory[9].insert(1, (Gui_image(
                    loc=data.INTERFACE.item_slots[9], img_idx=2,
                    sprites=Gui.item_small_sprites, decay=data.PLAYER.jumpdrive.cd_len)
                ))
                data.PLAYER.jumpdrive.set_cd_img = False

    @classmethod
    def indicator_update(cls):
        if data.LEVELS.skill_points > 0:
            cls.indicators["skill_up"].tick()
        if any([data.ITEMS.inventory_dic[k].upgradeable() for k in data.ITEMS.inventory_dic if data.ITEMS.inventory_dic[k] is not None]):
            cls.indicators["item_up"].tick()
            if data.LEVELS.skill_points > 0:
                cls.indicators["skill_up"].ticker = cls.indicators["item_up"].ticker
        if data.PLAYER.shield.active:
            cls.indicators["shield"].tick()
        if data.PLAYER.jumpdrive_disabled:
            cls.indicators["jumpdrive"].tick()

    @classmethod
    def cursor_update(cls):
        mouse_pos = pygame.mouse.get_pos()
        win.blit(Gui.image_sprites[6], (mouse_pos[0] - 16, mouse_pos[1] - 15))

    @classmethod
    def create(cls):
        cls.set_up_standart_ui()

    @classmethod
    def update(cls):
        cls.standart_ui_update()
        cls.health_bar_update()
        cls.player_shield_update()
        cls.update_item_ui()
        cls.indicator_update()
        cls.update_standart_item_ui()
        cls.cursor_update()


data.INTERFACE = Interface_new

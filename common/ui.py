from pygame.locals import *
import pygame

from init import *
from astraid_funcs import *
import astraid_data as data
from Gfx import Gfx, Background

"""
- Buttons
-
"""


class Gui(Timer):

    image_sprites = get_images("gui_elements")
    button_sprites = get_images("gui_buttons")
    item_small_sprites = get_images("gui_items_icons_small")
    fonts = {
        5: pygame.font.SysFont("Consolas", 5),
        10: pygame.font.SysFont("Consolas", 10),
        15: pygame.font.SysFont("Consolas", 15),
        20: pygame.font.SysFont("Consolas", 20),
        25: pygame.font.SysFont("Consolas", 25),
        30: pygame.font.SysFont("Consolas", 30),
        35: pygame.font.SysFont("Consolas", 35),
        40: pygame.font.SysFont("Consolas", 40),
        50: pygame.font.SysFont("Consolas", 50),
        60: pygame.font.SysFont("Consolas", 60),
    }

    def __init__(self, loc=(0, 0), anchor=None, anchor_x=0, anchor_y=0,
                 flag="standart_gui", decay=None):
        self.loc = loc
        self.x_loc = loc[0]
        self.y_loc = loc[1]
        self.anchor = anchor
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.flag = flag
        self.decay = decay
        self.kill = False
        Timer.__init__(self)

    def draw(self):
        pass

    def button(self):
        pass

    def rm(self):
        self.kill = True

    def tick(self):
        if self.decay is not None:
            if self.timer_trigger(self.decay):
                self.kill = True
        self.timer_tick()
        self.draw()
        self.button()

    @classmethod
    def add(cls, element):
        data.GUI_DATA.append(element)

    @classmethod
    def delete(cls, flag):
        [e.rm() for e in data.GUI_DATA if e.flag == flag]


class Gui_text(Gui):

    def __init__(
        self,
        loc=(0, 0),
        flag="standart_gui",
        text=" ",
        text_size=25,
        text_color=(189, 233, 193),  # bde9c1
        anchor=None,
        anchor_x=0,
        anchor_y=0,
        decay=None,
        animation_interval=None
    ):
        super().__init__(loc, anchor, anchor_x, anchor_y, flag, decay)
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.animation_interval = animation_interval
        if not callable(self.text):
            self.render_text = Gui.fonts[self.text_size].render(self.text, True, self.text_color)

    def _get_text(self):
        return self.text()

    def draw(self):
        if self.anchor is not None:
            self.loc = self.anchor.topleft

        if callable(self.text):
            self.render_text = Gui.fonts[self.text_size].render(
                self._get_text(), True, self.text_color)

        if self.animation_interval is None:
            win.blit(self.render_text, (self.loc[0] + self.anchor_x, self.loc[1] + self.anchor_y))
        else:
            animation_ticker = self.timer_animation_ticker(self.animation_interval)

            if animation_ticker < self.animation_interval * 0.5:
                win.blit(self.render_text, (self.loc[0] + self.anchor_x, self.loc[1] + self.anchor_y))
            else:
                pass


class Gui_image(Gui):

    def __init__(
        self,
        loc=(0, 0),
        flag="standart_gui",
        img_idx=0,
        sprites=Gui.image_sprites,
        anchor=None,
        anchor_x=0,
        anchor_y=0,
        animation_interval=None,
        decay=None
    ):
        super().__init__(loc, anchor, anchor_x, anchor_y, flag, decay)
        self.img_idx = img_idx
        self.sprites = sprites
        self.animation_interval = animation_interval
        if all([animation_interval is not None, isinstance(img_idx, int)]):
            self.img_idx = (self.img_idx, 0)

    def draw(self):
        if self.anchor is not None:
            self.loc = self.anchor.topleft

        if self.animation_interval is None:
            win.blit(self.sprites[self.img_idx],
                     (self.loc[0] + self.anchor_x, self.loc[1] + self.anchor_y))
        else:
            animation_ticker = self.timer_animation_ticker(self.animation_interval)

            if animation_ticker < self.animation_interval * 0.5:
                win.blit(self.sprites[self.img_idx[0]],
                         (self.loc[0] + self.anchor_x, self.loc[1] + self.anchor_y))
            else:
                win.blit(self.sprites[self.img_idx[1]],
                         (self.loc[0] + self.anchor_x, self.loc[1] + self.anchor_y))


class Gui_button(Gui):

    def __init__(
        self,
        loc=(0, 0),
        flag="standart_gui",
        btn_idx=(0, 0),
        btn_text="",
        btn_text_size=25,
        btn_text_color=(255, 255, 255),
        btn_effect=None,
        text_x=30,
        text_y=8
    ):
        super().__init__(loc, flag)
        self.btn_idx = btn_idx
        self.btn_text = btn_text
        self.btn_text_size = btn_text_size
        self.btn_text_color = btn_text_color
        self.btn_effect = btn_effect
        self.text_x = text_x
        self.text_y = text_y
        self.sprite_default = Gui.button_sprites[self.btn_idx[0]]
        self.sprite_clicked = Gui.button_sprites[self.btn_idx[1]]
        self.hitbox = self.sprite_default.get_rect()
        self.hitbox.topleft = loc
        self.render_text = Gui.fonts[btn_text_size].render(btn_text, True, btn_text_color)
        self.clicked = False

    def draw(self):
        if not self.clicked:
            win.blit(self.sprite_default, self.loc)
        else:
            win.blit(self.sprite_clicked, self.loc)

        win.blit(self.render_text, (self.loc[0] + self.text_x, self.loc[1] + self.text_y))

    def button(self):
        if pygame.mouse.get_pressed()[0] == 1:
            if self.hitbox.collidepoint(pygame.mouse.get_pos()):
                self.clicked = True

        if self.clicked:
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
                if self.hitbox.collidepoint(pygame.mouse.get_pos()):
                    self.btn_effect()

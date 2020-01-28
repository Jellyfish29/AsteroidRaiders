import pygame

from init import *
from astraid_funcs import *
import astraid_data as data


class Gfx(Timer):

    gfx_lst = []
    effect_sprites = get_images("effects")
    cursor_sprites = get_images("cursor")
    explosion_sprites = get_images("explosions")
    bg = get_images("background")
    y = 0
    scroll_speed = 1
    bg_move = True
    font = pygame.font.SysFont("arial", 20)

    def __init__(self, typ, interval, anchor, hover, follow, x, y, dmg_text, text_color, explo, pl_shield, rot):
        Timer.__init__(self)
        if explo:
            self.sprites = Gfx.explosion_sprites
        else:
            self.sprites = Gfx.effect_sprites
        self.pl_shield = pl_shield
        self.typ = typ
        self.interval = interval
        self.anchor = anchor
        self.hover = hover
        self.hover_rect = pygame.Rect(anchor[0], anchor[1], 1, 1)
        self.x = x
        self.y = y
        self.follow = follow
        self.dmg_text = dmg_text
        self.text_color = text_color
        self.rot = rot
        self.effect_types = {
            "shield": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
            "shot_hit": (12, 13, 14),
            "jump": (15, 16, 17, 18, 19, 20),
            "jumpa": (21, 22),
            "heal": (23, 23),
            "pd_on": (24, 24),
            "shot_muzzle": (25, 26, 27),
            "explosion_1": (0, 1, 2, 3, 4, 5, 6, 7, 8),
            "explosion_2": (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23),
            "explosion_3": (24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37),
            "nuke": (39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51),
            "lightning": (28, 29, 30, 31, 32, 33, 34, 35),
            "radar": (36, 37, 38, 39, 40, 41, 42),
            "engine": (43, 44, 45, 46, 47, 48, 49),
            "engine2": (50, 51, 52, 53)
        }
        print(Gfx.effect_sprites)

    def draw(self):
        if self.hover:
            self.hover_rect.move_ip(0, -2)
            if self.dmg_text is not None:
                try:
                    text = Gfx.font.render(self.get_dmg_str(), True, self.text_color, self.hover_rect)
                except SystemError:
                    return True
                win.blit(text, self.hover_rect)

                if self.timer_trigger(30):
                    return True
            else:
                try:
                    win.blit(self.sprites[self.effect_types[self.typ][self.timer_animation_range(self.interval, len(self.effect_types[self.typ]))]], self.hover_rect)
                except TypeError:
                    return True
        elif self.follow:
            try:
                win.blit(self.sprites[
                    self.effect_types[self.typ][self.timer_animation_range(self.interval, len(self.effect_types[self.typ]))]], (self.anchor.topleft[0] + self.x, self.anchor.topleft[1] + self.y))
            except TypeError:
                return True

        elif self.pl_shield:
            try:
                win.blit(self.sprites[
                    self.effect_types[self.typ][self.timer_animation_range(self.interval, len(self.effect_types[self.typ]))]], (data.PLAYER.hitbox.topleft[0] - 65, data.PLAYER.hitbox.topleft[1] - 70))
            except TypeError:
                if not data.PLAYER.shield.active:
                    return True
        elif self.rot is not None:
            try:
                win.blit(rot_center(self.sprites[
                    self.effect_types[self.typ][self.timer_animation_range(self.interval, len(self.effect_types[self.typ]))]], self.rot), (self.anchor.center[0] + self.x, self.anchor.center[1] + self.y))
            except TypeError:
                return True

        # elif not self.hover and not self.follow:
        else:

            try:
                win.blit(self.sprites[
                    self.effect_types[self.typ][self.timer_animation_range(self.interval, len(self.effect_types[self.typ]))]], self.anchor)
            except TypeError:
                return True

    def get_dmg_str(self):
        return str(int(self.dmg_text * 10))

    @classmethod
    def shot_hit_effect(cls, shot, effect="shot_hit"):
        Gfx.create_effect(effect, 4, (shot.topleft[0] - 10, shot.topleft[1] - 10))

    @classmethod
    def create_effect(cls, typ, interval, anchor=(0, 0), hover=False, follow=False, x=0, y=0, dmg_text=None, text_color=(0, 0, 0), explo=False, pl_shield=False, rot=None):
        Gfx.gfx_lst.append(Gfx(typ, interval, anchor, hover, follow, x, y, dmg_text, text_color, explo, pl_shield, rot))

    @classmethod
    def cursor(cls):
        rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0, 0)
        win.blit(Gfx.cursor_sprites[2], (rect.topleft[0] - 9, rect.topleft[1] - 10))

    @classmethod
    def background(cls):
        if Gfx.bg_move:
            Gfx.y += Gfx.scroll_speed
        win.blit(Gfx.bg[0], (0, Gfx.y - winheight * 6))
        win.blit(Gfx.bg[3], (0, Gfx.y - winheight * 5))
        win.blit(Gfx.bg[0], (0, Gfx.y - winheight * 4))
        win.blit(Gfx.bg[2], (0, Gfx.y - winheight * 3))
        win.blit(Gfx.bg[0], (0, Gfx.y - winheight * 2))
        win.blit(Gfx.bg[1], (0, Gfx.y - winheight))
        win.blit(Gfx.bg[0], (0, Gfx.y))
        if Gfx.y >= 6480:
            Gfx.y = 0

    @classmethod
    def update(cls):
        for effect in Gfx.gfx_lst:
            if effect.draw():  # if animation over
                Gfx.gfx_lst.remove(effect)
            effect.timer_tick()

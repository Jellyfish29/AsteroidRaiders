import pygame

from init import *
from astraid_funcs import *
import astraid_data as data


class Gfx(Timer):

    gfx_layer_1_lst = []
    gfx_layer_2_lst = []
    gfx_layer_3_lst = []
    effect_sprites = get_images("effects")
    cursor_sprites = get_images("cursor")
    explosion_sprites = get_images("explosions")
    gun_sprites = get_images("guns")
    font = pygame.font.SysFont("arial", 20)

    def __init__(
        self, typ, interval,
        anchor, hover, follow,
        x, y, dmg_text,
        text_color, explo, pl_shield, rot
    ):
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
            "explosion_4": (38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50),
            "nuke": (39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51),
            "lightning": (28, 29, 30, 31, 32, 33, 34, 35),
            "radar": (36, 37, 38, 39, 40, 41, 42),
            "engine": (43, 44, 45, 46, 47, 48, 49),
            "engine2": (50, 51, 52, 53),
            "circle": (54, 55, 56, 57, 58, 59, 60, 61),
            "shield2": (62, 63, 64, 65, 66, 67, 68, 69, 70, 71)
        }

    def draw(self):
        if self.hover:
            self.hover_rect.move_ip(0, -2)
            if self.dmg_text is not None:
                try:
                    text = Gfx.font.render(
                        self.get_dmg_str(), True, self.text_color, self.hover_rect
                    )
                except SystemError:
                    return True
                win.blit(text, self.hover_rect)

                if self.timer_trigger(30):
                    return True
            else:
                try:
                    win.blit(self.sprites[
                        self.effect_types[self.typ][
                            self.timer_animation_range(self.interval, len(self.effect_types[self.typ]))
                        ]
                    ], self.hover_rect)
                except TypeError:
                    return True
        elif self.follow:
            try:
                win.blit(self.sprites[
                    self.effect_types[self.typ][
                        self.timer_animation_range(self.interval, len(self.effect_types[self.typ]))
                    ]
                ], (self.anchor.topleft[0] + self.x, self.anchor.topleft[1] + self.y))
            except TypeError:
                return True

        elif self.pl_shield:
            try:
                win.blit(self.sprites[
                    self.effect_types[self.typ][
                        self.timer_animation_range(self.interval, len(self.effect_types[self.typ]))
                    ]
                ], (data.PLAYER.hitbox.topleft[0] - 65, data.PLAYER.hitbox.topleft[1] - 70))
            except TypeError:
                if not data.PLAYER.shield.active:
                    return True
        elif self.rot is not None:
            try:
                win.blit(rot_center(self.sprites[
                    self.effect_types[self.typ][
                        self.timer_animation_range(self.interval, len(self.effect_types[self.typ]))
                    ]
                ], self.rot), (self.anchor.center[0] + self.x, self.anchor.center[1] + self.y))
            except TypeError:
                return True

        # elif not self.hover and not self.follow:
        else:

            try:
                win.blit(self.sprites[
                    self.effect_types[self.typ][
                        self.timer_animation_range(self.interval, len(self.effect_types[self.typ]))
                    ]
                ], self.anchor)
            except TypeError:
                return True

    def get_dmg_str(self):
        return str(int(self.dmg_text * 10))

    @classmethod
    def create_effect(
            cls,
            typ,
            interval,
            anchor=(0, 0),
            hover=False,
            follow=False,
            x=0, y=0,
            dmg_text=None,
            text_color=(0, 0, 0),
            explo=False,
            pl_shield=False,
            rot=None,
            layer=1
    ):
        if layer == 3:
            Gfx.gfx_layer_3_lst.append(
                Gfx(typ, interval, anchor, hover, follow, x, y, dmg_text, text_color, explo, pl_shield, rot)
            )
        elif layer == 2:
            Gfx.gfx_layer_2_lst.append(
                Gfx(typ, interval, anchor, hover, follow, x, y, dmg_text, text_color, explo, pl_shield, rot)
            )
        else:
            Gfx.gfx_layer_1_lst.append(
                Gfx(typ, interval, anchor, hover, follow, x, y, dmg_text, text_color, explo, pl_shield, rot)
            )

    @classmethod
    def cursor(cls):
        rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0, 0)
        win.blit(Gfx.cursor_sprites[2], (rect.topleft[0] - 9, rect.topleft[1] - 10))

    @classmethod
    def update(cls):
        if Gfx.bg_move:
            Gfx.y += Gfx.scroll_speed
        win.blit(Gfx.bg[8], (0, Gfx.y - 4040))
        win.blit(Gfx.bg[8], (0, Gfx.y - 1480))
        if Gfx.y >= 4040:
            Gfx.y = 0

    @classmethod
    def layer_1_update(cls):
        for effect in Gfx.gfx_layer_1_lst:
            if effect.draw():  # if animation over
                Gfx.gfx_layer_1_lst.remove(effect)
            effect.timer_tick()

    @classmethod
    def layer_2_update(cls):
        for effect in Gfx.gfx_layer_2_lst:
            if effect.draw():  # if animation over
                Gfx.gfx_layer_2_lst.remove(effect)
            effect.timer_tick()

    @classmethod
    def layer_3_update(cls):
        for effect in Gfx.gfx_layer_3_lst:
            if effect.draw():  # if animation over
                Gfx.gfx_layer_3_lst.remove(effect)
            effect.timer_tick()


class Background(Timer):

    bg_sprites = get_images("background")
    y = 0
    scroll_speed = 1
    bg_move = True
    bg_color = [0, 0, 30]
    bg_objs = []
    bg_obj_spawn_rate = 1200

    def __init__(self, y=-1000):
        self.gfx_idx = random.randint(2, 9)
        self.x = random.randint(100, 1800)
        self.y = y
        self.kill = False

    def gfx_animation(self):
        win.blit(Background.bg_sprites[self.gfx_idx], (self.x, self.y))

        if Background.bg_move:
            self.y += Background.scroll_speed
            if self.y > 1600:
                self.kill = True

    @classmethod
    @timer
    def bg_color_change(cls, timer, color=None, speed=None, sub=False):
        if color is None:
            color = (0, 0, 30)
        if speed is None:
            speed = 5
        if timer.trigger(speed):
            if not all([cls.bg_color[i] == color[i] for i in range(3)]):
                for i in range(3):
                    if not cls.bg_color[i] == color[i]:
                        if cls.bg_color[i] < color[i]:
                            cls.bg_color[i] += 1
                        else:
                            cls.bg_color[i] -= 1
                # return True

    @classmethod
    @timer
    def update(cls, timer):
        if not data.LEVELS.boss_fight:
            if timer.trigger(cls.bg_obj_spawn_rate):
                cls.bg_objs.append(Background())

        for bg_obj in cls.bg_objs:
            bg_obj.gfx_animation()
            if bg_obj.kill:
                cls.bg_objs.remove(bg_obj)

        if any([data.LEVELS.after_boss,
                not data.LEVELS.special_events and not data.LEVELS.boss_fight
                ]):
            cls.bg_color_change(color=(0, 0, 30))

        if cls.bg_move:
            cls.y += cls.scroll_speed
        win.blit(cls.bg_sprites[1], (0, cls.y - 1080))  # 4040
        win.blit(cls.bg_sprites[1], (0, cls.y - 0))  # 1480
        if cls.y >= 1080:
            cls.y = 0

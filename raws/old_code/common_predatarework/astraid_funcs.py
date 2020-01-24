import pygame
import numpy as np
import os
import math


winwidth = 1920
winheight = 1080
""" Provides functionaly used by almost all classes:
    handles: angle calculation, image loading, image roattion, pagame.rect on screen detection, time control
"""


def angles_80(speed):
    return {idx: i for idx, i in enumerate(
        [(speed * (i / 100), -speed) for i in range(0, 100, 10)] +
        [(speed, -speed * (-i / 100)) for i in range(-100, 0, 10)] +
        [(speed, speed * (i / 100)) for i in range(0, 100, 10)] +
        [(speed * (-i / 100), speed) for i in range(-100, 0, 10)] +
        [(-speed * (i / 100), speed) for i in range(0, 100, 10)] +
        [(-speed, speed * (-i / 100)) for i in range(-100, 0, 10)] +
        [(-speed, -speed * (i / 100)) for i in range(0, 100, 10)] +
        [(-speed * (-i / 100), -speed) for i in range(-100, 0, 10)]
    )}


# def angles_360(speed):
#     return {idx: i for idx, i in enumerate(
#         [(speed, speed * (-i / 100)) for i in np.arange(0, 100, 2.23)] +
#         [(speed * (-i / 100), -speed) for i in np.arange(-100, 0, 2.23)] +
#         [(-speed * (i / 100), - speed) for i in np.arange(0, 100, 2.23)] +
#         [(-speed, -speed * (-i / 100)) for i in np.arange(-100, 0, 2.23)] +
#         [(-speed, speed * (i / 100)) for i in np.arange(0, 100, 2.23)] +
#         [(-speed * (-i / 100), speed) for i in np.arange(-100, 0, 2.23)] +
#         [(speed * (i / 100), speed) for i in np.arange(0, 100, 2.23)] +
#         [(speed, speed * (-i / 100)) for i in np.arange(-100, 0, 2.23)]
#     )}

def angles_360(speed, n=360):
    return {idx: i for idx, i in enumerate([(math.cos(2 * math.pi / n * x) * speed, math.sin(2 * math.pi / n * x) * speed) for x in range(0, n + 1)])}


def degrees(x0, y0, x1, y1):
    rel_x, rel_y = x0 - y0, x1 - y1  # rel_x, rel_y = x0 - y0, x1 - y1
    angle = math.atan2(rel_y, rel_x)
    angle = math.degrees(angle)
    if angle < 0:
        angle += 360
    return int(angle)


def directions(speed):
    return {
        "up": (0, -speed),
        "down": (0, speed),
        "right": (speed, 0),
        "left": (-speed, 0),
        "right up": (speed * 0.8, -speed * 0.8),
        "right down": (speed * 0.8, speed * 0.8),
        "left up": (-speed * 0.8, -speed * 0.8),
        "left down": (-speed * 0.8, speed * 0.8),
        "idle": (0, 0)
    }


def get_images(kind):
    pathes = [os.path.join(os.getcwd()[:-7], f"Gfx\\{kind}\\" + file) for file in os.listdir(os.path.join(os.getcwd()[:-7], f"Gfx\\{kind}"))]
    return {idx: pygame.image.load(img).convert_alpha() for idx, img in enumerate(sorted(pathes))}


def rect_not_on_sreen(rect, bot=False, strict=False):
    if strict:
        if rect.center[0] > winwidth or rect.center[0] < 0:
            return True
        if rect.center[1] > winheight or rect.center[1] < 0:
            return True

    if rect.center[0] > winwidth + 120 or rect.center[0] < - 100:
        return True
    if bot:
        if rect.center[1] > winheight + 250:
            return True

    if not bot:
        if rect.center[1] > winheight + 150 or rect.center[1] < - 150:
            return True
    else:
        return False


def gfx_rotate(surf, angle):
    return pygame.transform.rotate(surf, angle)


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    try:
        rot_image = rot_image.subsurface(rot_rect).copy()
    except ValueError:
        pass
    return rot_image


class Time_controler:

    def __init__(self):
        self.ticker_1 = 0
        self.ticker_2 = 0
        self.ticker_3 = 0
        self.delay_ticker = 0
        self.ani_ticker = 0
        self.animation_range_ticker = 0
        self.i = 0

    def trigger_1(self, limit):
        self.ticker_1 += 1
        if self.ticker_1 >= limit:
            self.ticker_1 = 0
            return True
        else:
            return False

    def trigger_2(self, limit):
        self.ticker_2 += 1
        if self.ticker_2 >= limit:
            self.ticker_2 = 0
            return True
        else:
            return False

    def trigger_3(self, limit):
        self.ticker_3 += 1
        if self.ticker_3 >= limit:
            self.ticker_3 = 0
            return True
        else:
            return False

    def delay(self, run, limit=0):
        if run:
            self.delay_ticker += 1
            if self.delay_ticker > limit:
                return True
            else:
                return False
        else:
            self.delay_ticker = 0

    def animation_ticker(self, limit):
        if self.ani_ticker >= limit:
            self.ani_ticker = 0
        self.ani_ticker += 1
        return self.ani_ticker

    def animation_range(self, interval, limit):
        if self.animation_range_ticker >= interval:
            self.i += 1
            self.animation_range_ticker = 0
        if self.i >= limit:
            self.i = 0
            return None
        self.animation_range_ticker += 1
        return self.i

# def change():
#     for i, name in enumerate(os.listdir(os.path.join(os.getcwd()[:-7], "Gfx\\effects"))):
#         Gfx.gfx_img[name] = Gfx.gfx_img.pop(i)
#     print(Gfx.gfx_img)


# timer decorator


# class timer():

#     def __init__(self, arg):
#         self.arg = arg
#         # self.counter = 0

#     def __call__(self, orig):

#         self.counter = 0

#         def wrapper(*args):
#             self.limiter = getattr(args[0], self.arg)  # holt sich das Attribut der Instanz mit dem namen des Atrributes der als string bei dem Decorator übergeben wird (z.B "fire_rate")
#             self.counter += 1
#             if self.counter >= self.limiter:
#                 self.counter = 0
#                 return orig(args[0], True)
#             else:
#                 return orig(args[0], False)
#         return wrapper

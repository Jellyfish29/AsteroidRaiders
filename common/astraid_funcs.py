import pygame
import os
import math
import random


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


def angles_360(speed, n=360):
    return {idx: i for idx, i in enumerate([(math.cos(2 * math.pi / n * x) * speed, math.sin(2 * math.pi / n * x) * speed) for x in range(0, n + 1)])}


def angle_switcher(a):
    if a > 359:
        a -= 359
    elif a < 0:
        a += 359
    return a


def get_sin(i, a):
    d = math.degrees(math.sin(i))
    if d + a > 359:
        d -= 359
    elif d + a < 0:
        d += 359
    return int(d + a)


def get_cos(i, a):
    d = math.degrees(math.cos(i))
    if d + a > 359:
        d -= 359
    elif d + a < 0:
        d += 359
    return int(d + a)


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


def get_random_point():
    return (random.randint(0, winwidth), random.randint(0, winheight))


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


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


# Positional Arguments müssen vor das timer arguments geschrieben werden Keyword dahinter
# @timer
# foo(pos_arg_1, pos_arg_2, timer, kw_arg=0)
def timer(f):
    timer = Timer()

    def wrapper(*args, timer=timer, **kwargs):
        timer.timer_tick()
        return f(*args, timer, **kwargs)
    return wrapper


class Timer:

    def __init__(self):
        self.ticker = {}
        self.timer_calls_per_tick = 0
        self.animation_range_ticker_1 = 0
        self.animation_range_ticker_2 = 0

    def timer_trigger(self, limit):
        self.timer_calls_per_tick += 1
        if self.timer_calls_per_tick not in self.ticker:
            self.ticker.update({self.timer_calls_per_tick: 0})
        self.ticker[self.timer_calls_per_tick] += 1

        if self.ticker[self.timer_calls_per_tick] >= limit:
            self.ticker[self.timer_calls_per_tick] = 0
            return True

    def timer_key_trigger(self, limit, key=0):
        if key not in self.ticker:
            self.ticker.update({key: 0})
        self.ticker[key] += 1
        if self.ticker[key] >= limit:
            self.ticker[key] = 0
            return True

    def trigger(self, limit):
        self.timer_calls_per_tick += 1
        if self.timer_calls_per_tick not in self.ticker:
            self.ticker.update({self.timer_calls_per_tick: 0})
        self.ticker[self.timer_calls_per_tick] += 1
        if self.ticker[self.timer_calls_per_tick] >= limit:
            self.ticker[self.timer_calls_per_tick] = 0
            return True

    def timer_delay(self, limit=0, reset=False):
        if reset:
            self.ticker[self.timer_calls_per_tick] = 0
        self.timer_calls_per_tick += 1
        if self.timer_calls_per_tick not in self.ticker:
            self.ticker.update({self.timer_calls_per_tick: 0})
        if self.ticker[self.timer_calls_per_tick] < limit:
            self.ticker[self.timer_calls_per_tick] += 1
        else:
            return True

    def timer_key_delay(self, limit=0, reset=False, key=""):
        if key not in self.ticker:
            self.ticker.update({key: 0})
        if reset:
            self.ticker[key] = 0
        if self.ticker[key] < limit:
            self.ticker[key] += 1
        else:
            return True

    def timer_animation_ticker(self, limit):
        self.timer_calls_per_tick += 1
        if self.timer_calls_per_tick not in self.ticker:
            self.ticker.update({self.timer_calls_per_tick: 0})
        self.ticker[self.timer_calls_per_tick] += 1
        if self.ticker[self.timer_calls_per_tick] >= limit:
            self.ticker[self.timer_calls_per_tick] = 0
        return self.ticker[self.timer_calls_per_tick]

    def timer_animation_range(self, interval, limit):
        if self.animation_range_ticker_1 >= interval:
            self.animation_range_ticker_2 += 1
            self.animation_range_ticker_1 = 0
        if self.animation_range_ticker_2 >= limit:
            self.animation_range_ticker_2 = 0
            return None
        self.animation_range_ticker_1 += 1
        return self.animation_range_ticker_2

    def timer_reset(self):
        self.ticker = {}
        self.timer_calls_per_tick = 0
        self.animation_range_ticker_1 = 0
        self.animation_range_ticker_2 = 0

    def timer_tick(self):
        self.timer_calls_per_tick = 0


class Run_limiter:

    game_tick = 0
    previous_tick = 0

    def __init__(self):
        self.code_block_ran = False
        self.run_counter = 0
        self.ticker = {}

    def run_block_once(self):
        if not self.code_block_ran:
            self.code_block_ran = True
            return True
        else:
            return False

    def run_block_for(self, amount):
        self.run_counter += 1
        if self.run_counter <= amount:
            return True
        else:
            return False

    def run_limiter_reset(self, key="one"):
        self.code_block_ran = False


def run_limiter(f):
    rl = Run_limiter()

    def wrapper(*args, limiter=rl, **kwargs):
        return f(*args, limiter, **kwargs)
    return wrapper

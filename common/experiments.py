import astraid_data as data
from astraid_funcs import *
import time
import random


# class Testo(Timer):

#     def __init__(self):
#         Timer.__init__(self)
#         self.num = random.random()

#     def one(self):
#         if self.timer_trigger(10):
#             # pass
#             print("one")

#     def two(self):
#         if self.timer_trigger(11):
#             # pass
#             print("two")

#     def three(self):
#         if self.timer_trigger(12):
#             # pass
#             print("three")

#     def tick(self):
#         self.one()
#         self.two()
#         self.three()
#         # print(self.calls_per_tick)
#         self.timer_tick()


# @timer
# def foo(timer):
#     if timer.timer_trigger(10):
#         print("one")
#     if timer.timer_trigger(11):
#         print("two")
#     if timer.timer_trigger(12):
#         print("three")


# lst = [Testo() for i in range(1)]


# j = 0
# while j < 100:
#     j += 1
#     time.sleep(0.1)
#     for t in lst:
#         t.tick()
#         print(id(t))
# print(t.ticker)
# foo()
# pri
# T = Testo
# if type(T) == "<class 'type'>":
#     print("oof")
# x = iter([i for i in range(0, 200, int(200 / 10))])

# print([8 * i for i in range(4)])


# r1 = pygame.Rect(100, 100, 50, 50)
# x = abs(Player.hitbox.center[0] - r.center[0])
# y = abs(Player.hitbox.center[1] - r.center[1])
# r2 = pygame.Rect(x, y, 50, 50)
# pygame.draw.rect(win, (255, 255, 255), r1)
# pygame.draw.rect(win, (255, 255, 255), r2)

# pygame.draw.rect(win, (255, 255, 255), r1)
# x = (Player.hitbox.center[0] + r1.center[0]) / 2
# y = (Player.hitbox.center[1] + r1.center[1]) / 2
# r2 = pygame.Rect(x, y, 5, 5)
# lst.append(r2)

# x = (r2.center[0] + r1.center[0]) / 2
# y = (r2.center[1] + r1.center[1]) / 2
# r3 = pygame.Rect(x, y, 5, 5)
# lst.append(r3)

# x = (r2.center[0] + Player.hitbox.center[0]) / 2
# y = (r2.center[1] + Player.hitbox.center[1]) / 2
# r4 = pygame.Rect(x, y, 5, 5)
# lst.append(r4)

# for r in lst:
#     pygame.draw.rect(win, (255, 255, 255), r)
#     gfx_angle = degrees(
#         Player.hitbox.center[1],
#         r.center[1],
#         Player.hitbox.center[0],
#         r.center[0]
#     )
#     win.blit(rot_center(
#         Phenomenon.phenom_sprites[16], gfx_angle), (r[0] - 200, r[1] - 200))
#     lst.remove(r)

def foo():
    pass


x = foo

print(x.__name__)

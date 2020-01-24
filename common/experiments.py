import astraid_data as data
from astraid_funcs import *
import time


class Testo(Timer):

    def __init__(self):
        Timer.__init__(self)

    def one(self):
        if self.timer_trigger(10):
            print("one")

    def two(self):
        if self.timer_trigger(10):
            print("two")

    def three(self):
        if self.timer_trigger(10):
            print("three")

    def tick(self):
        self.one()
        self.two()
        self.three()
        # print(self.calls_per_tick)
        self.calls_per_tick = 0

# class Testo():

#     def __init__(self):
#         self.tc = Time_controler()

#     def one(self):
#         if self.tc.trigger_1(10):
#             print("one")

#     def two(self):
#         if self.tc.trigger_2(10):
#             print("two")

#     def three(self):
#         if self.tc.trigger_3(10):
#             print("three")

#     def tick(self):
#         self.one()
#         self.two()
#         self.three()


lst = [Testo() for i in range(1)]


j = 0
while j < 20:
    j += 1
    time.sleep(0.1)
    for t in lst:
        t.tick()
        print(t.ticker)

    # print(j)

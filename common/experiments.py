import astraid_data as data
from astraid_funcs import *
import time


class Testo(Timer):

    def __init__(self):
        Timer.__init__(self)

    def one(self):
        if self.timer_trigger(10):
            # pass
            print("one")

    def two(self):
        if self.timer_trigger(11):
            # pass
            print("two")

    def three(self):
        if self.timer_trigger(12):
            # pass
            print("three")

    def tick(self):
        self.one()
        self.two()
        self.three()
        # print(self.calls_per_tick)
        self.timer_tick()


@timer_t
def foo(timer):
    if timer.timer_trigger(10):
        print("one")
    if timer.timer_trigger(11):
        print("two")
    if timer.timer_trigger(12):
        print("three")


lst = [Testo() for i in range(1)]


j = 0
while j < 100:
    j += 1
    time.sleep(0.1)
    # for t in lst:
    #     t.tick()
    #     # print(t.ticker)
    foo()
    print(j)

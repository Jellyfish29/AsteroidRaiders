import astraid_data as data
from astraid_funcs import *
import time
import random


i = 0


class off:

    def __init__(self, e):
        self.e = e

    def foo(self):
        return self.e()


x = off(lambda: f"{i} ist cool")

if callable(x.e):
    print("foo")

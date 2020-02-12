import astraid_data as data
from astraid_funcs import *
import time
import random


x = [1, 2, 3, 4, 5, 6]
y = ["a", "b", "c"]

v = [[e] + y for e in x if e % 2 == 0]


print(v)

# import astraid_data as data
# from astraid_funcs import *
# import time
# import random


# x = {1: 1, 2: 2, 3: 3}


# print(abs(-20))

swerte = iter([233, 233, 233, 233, 555, 555, 555, 5634, 322, 322])

tz = 0
az = 0
sw = next(swerte)
sv = sw

while sw != -1:
    if sw == sv:
        tz += 1
    else:
        print(f"Sensorwert: {sw} Anzahl: {tz}")
        tz = 1
        sw = sv
        az += 1
    sv = next(swerte, -1)

print(f"Anzahl der Artikel: {az}")

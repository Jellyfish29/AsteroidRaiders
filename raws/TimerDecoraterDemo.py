import time


class timer(object):

    def __init__(self, limit):
        self.limit = limit
        self.counter = 0

    def __call__(self, orig):
        def wrapper(*args):
            self.counter += 1
            if self.counter >= self.limit:
                self.counter = 0
                return orig()
            else:
                return orig
        return wrapper


@timer(2)
def oof():
    print("oof")


@timer(5)
def kat():
    print("kat")


c = 0
while c < 10:
    time.sleep(0.1)
    c += 1
    kat()
    oof()

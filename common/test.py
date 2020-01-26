from init import *
from astraid_funcs import *
import astraid_data as data
from interface import *
from player import *
from turret import *
from enemys import *
from bosses import *
from Gfx import *
from levels import *
from items import *
from phenomenon import *


Boss_test_lst = [Boss_mine_boat(), Boss_frigatte(), Boss_corvette(), Boss_destroyer(), Boss_cruiser()]  # Boss_battleship(), Boss_carrier()]

fps = 10000


def boss_tick_test():
    j = 0
    data.PLAYER.health = 1000000
    while j < 10000:
        j += 1
        print(j)
        for boss in Boss_test_lst:
            if j == 2000:
                boss.phase_1()
            elif j == 5000:
                boss.phase_2()
            elif j == 7000:
                boss.phase_3()
            boss.tick()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        Clock.tick(fps)
        pygame.display.update()


if __name__ == "__main__":
    boss_tick_test()

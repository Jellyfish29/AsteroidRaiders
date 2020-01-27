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

win = pygame.display.set_mode((winwidth, winheight))

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
    print("Boss Test Complete")


def item_test():
    for item in Items.get_drop_table_absolute():
        it = item[0]((item[1]))
        Items.inventory_dic[0] = it
        it.effect()
        Items.update()
        assert it.flag in Items.active_flag_lst
        it.lvl += 3
        assert it.get_lvl_effects() == self.base_effect
        it.remove_from_inventory(0)
        assert len(Items.active_flag_lst) == 0
        assert it in Items.dropped_lst
        assert Items.inventory_dic[0] == None
    print("Item Test complete")

if __name__ == "__main__":
    # boss_tick_+test()
    item_test()

from init import *
from astraid_funcs import *
import astraid_data as data
from interface import *
from player import *
from turret import *
from enemys import *
from bosses import *
from bosses_def import *
from Gfx import *
from levels import *
from items import *
from items_active import *
from items_passive import *
from items_misc import *
from phenomenon import *

win = pygame.display.set_mode((winwidth, winheight))

Boss_test_lst = [Boss_mine_boat(), Boss_frigatte(), Boss_corvette(), Boss_destroyer(), Boss_cruiser(), Boss_battleship(), Boss_scout()]  # Boss_battleship(), Boss_carrier()]

fps = 10000


class Mock_enemy():

    def __init__(self):

        self.hitbox = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 10, 10)


def boss_tick_test():
    j = 0
    data.PLAYER.health = 1000000
    while j < 10000:
        j += 1
        # print(j)
        for boss in Boss_test_lst:
            if j == 2000:
                boss.phase_1()
            elif j == 5000:
                boss.phase_2()
            elif j == 7000:
                boss.phase_3()
            elif j > 9990:
                boss.health = 0
                assert boss.destroy() is True
            boss.tick()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        Clock.tick(fps)
        pygame.display.update()
    print("Boss Test Complete")


def item_test():
    for item in Items.drop_table_absolute:
        it = item[0]((item[1]))
        Items.inventory_dic[0] = it
        it.effect()
        Items.update()
        assert it.flag in Items.active_flag_lst
        it.lvl = 3
        it.remove_from_inventory(0)
        assert len(Items.active_flag_lst) == 0
        assert it in Items.dropped_lst
        assert Items.inventory_dic[0] is None
    print("Item Test complete")


def turret_test():
    i = 0
    for item in Items.drop_table_absolute:
        it = item[0]((item[1]))
        Items.inventory_dic[0] = it
        it.effect()
        it.active = True

    while i < 1000:
        i += 1
        Turret.normal_fire()
        Turret.star_fire()
        Turret.rapid_fire()
        Turret.nuke_fire()
        Turret.gravity_bomb()
        Turret.black_hole_bomb()
        Turret.missile_aquisition(Mock_enemy())
        Turret.point_defence(pygame.Rect(Player.hitbox.center[0], Player.hitbox.center[1], 10, 10))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        Clock.tick(fps)
        pygame.display.update()
    print("Turret Test complete")


if __name__ == "__main__":
    boss_tick_test()
    item_test()
    turret_test()

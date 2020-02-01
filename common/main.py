
from pygame.locals import *

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


def test_mode():
    Levels.display_level += 1
    Levels.level += 1
    Levels.scaling()
    # Player.max_health +d= 0 40000
    Player.health += 40000
    Player.damage += 10
    Items.upgrade_points += 400
    Levels.skill_points += 100
    # pygame.mouse.set_visible(True)AAAAAAAAAA
    # Elites.spawn()
    # data.ENEMY.set_spawn_table(Shooter)
    # data.ENEMY_DATA.append(random.choice(Enemy.spez_spawn_table)())


def main():

    right, left, up, down = [False, False, False, False]

    def move_condition(bool_1, str_1, bool_2, str_2, str_3):
        if bool_1:
            Player.move(str_1)
        elif bool_2:
            Player.move(str_2)
        else:
            Player.move(str_3)

    shooter_event, jumper_event, seeker_event, wave_event = [pygame.USEREVENT + i for i in range(1, 5)]

    event_conditions = [
        (lambda: Levels.spez_event_trigger == 1, pygame.event.Event(shooter_event)),
        (lambda: Levels.spez_event_trigger == 2, pygame.event.Event(jumper_event)),
        (lambda: Levels.spez_event_trigger == 3, pygame.event.Event(seeker_event)),
        (lambda: Levels.spez_event_trigger == 4, pygame.event.Event(wave_event))
    ]

    Gfx.background()
    Interface.create()

    components = [Player, Turret, Enemy, Phenomenon, Interface, Levels, Items]

    # # # # Levels.skill_points += 100
    # Items.drop((winwidth / 2, 400), target=Item_nuke((100, 100, 100)))
    # Items.drop((winwidth / 2, 400), target=Item_he_rounds((100, 100, 150)))
    # Items.drop((winwidth / 2, 400), target=Item_improved_feeding((100, 100, 200)))
    Items.drop((winwidth / 2, 400), target=Items.start_item_generator()((100, 100, 200)))
    # Items.drop((winwidth / 2, 400), amount=1)
    Levels.after_boss = True
    Interface.main_menu(True)
    Levels.spez_add()

    # print(Player.shield.__class__.__bases__[0].__name__)

    while True:
        # print(data.PLAYER, data.TURRET, data.ITEMS, data.BOSS, data.ELITES, data.PHENOM, data.LEVELS, data.ENEMY)
        Gfx.background()
        # print(type(pl.Player))
        # Items.spawm_all_items_test()
        # print(Clock.get_fps())wwwwwsss
        # print(Items.upgrade_points)
        # print(len(data.ENEMY_DATA))ddwww

        Gfx.layer_3_update()

        data.GAME_UPDATE()

        Gfx.layer_2_update()

        for component in components:
            component.update()

        Gfx.layer_1_update()

        for spez_event in map(pygame.event.post, [event for (condition, event) in event_conditions if condition()]):
            spez_event

        for event in pygame.event.get():
            for typ, kind in [
                (shooter_event, "shooter"),
                (jumper_event, "jumper"),
                (seeker_event, "seeker"),
                (wave_event, "wave")
            ]:
                if event.type == typ:
                    Levels.spez_event(kind)
            if event.type == KEYDOWN:
                if event.key == K_TAB:
                    scrollspeed_temp = Gfx.scroll_speed
                    # Gfx.scroll_speed = 0
                    Interface.upgrades_menu(True)
                    Gfx.scroll_speed = scrollspeed_temp
                    right, left, up, down = [False, False, False, False]  # damit palyer nicht moved nach verlassen von menu
                elif event.key == K_d:
                    right = True
                    move_condition(up, "right up", down, "right down", "right")
                elif event.key == K_a:
                    left = True
                    move_condition(up, "left up", down, "left down", "left")
                elif event.key == K_w:
                    up = True
                    move_condition(left, "left up", right, "right up", "up")
                elif event.key == K_s:
                    down = True
                    move_condition(left, "left down", right, "right down", "down")
                elif event.key == K_1:
                    Player.use_heal()
                elif event.key == K_2:
                    Player.shield.toggle()
                    Player.shield.activation_effect()
                elif event.key == K_r:
                    try:
                        Items.inventory_dic[0].toggle()
                        Items.inventory_dic[0].activation_effect()
                    except AttributeError:
                        pass  # Fehlersound
                elif event.key == K_f:
                    try:
                        Items.inventory_dic[1].toggle()
                        Items.inventory_dic[1].activation_effect()
                    except AttributeError:
                        pass
                elif event.key == K_e:
                    try:
                        Items.inventory_dic[2].toggle()
                        Items.inventory_dic[2].activation_effect()
                    except AttributeError:
                        pass

                elif event.key == K_p:
                    Interface.pause_menu(True)

                elif event.key == K_i:
                    Items.spawm_items_test()

                elif event.key == K_m:
                    test_mode()
                elif event.key == K_SPACE:
                    Player.jumpdrive.toggle()
                    Player.jumpdrive.activation_effect()
                elif event.key == K_LSHIFT:
                    Player.afterburner.toggle()
                    Player.afterburner.activation_effect()

                elif event.key == K_l:
                    if not Levels.boss_fight:
                        try:
                            data.LEVELS.load_game().load_save()
                        except FileNotFoundError:
                            pass
            elif event.type == MOUSEBUTTONDOWN:
                Turret.fire(True)
            elif event.type == KEYUP:
                if event.key == K_w:
                    up = False
                elif event.key == K_s:
                    down = False
                elif event.key == K_d:
                    right = False
                elif event.key == K_a:
                    left = False
                elif event.key == K_r:
                    try:
                        Items.inventory_dic[0].end_activation()
                    except AttributeError:
                        pass
                elif event.key == K_f:
                    try:
                        Items.inventory_dic[1].end_activation()
                    except AttributeError:
                        pass
                elif event.key == K_e:
                    try:
                        Items.inventory_dic[2].end_activation()
                    except AttributeError:
                        pass
                elif event.key == K_SPACE:
                    Player.jumpdrive.end_activation()
                elif event.key == K_LSHIFT:
                    Player.afterburner.end_activation()

                elif event.key == K_ESCAPE:
                    pygame.quit()
                    exit()

                if [up, down, left, right].count(True) < 2:
                    for con, cmd in [
                        (up, "up"),
                        (down, "down"),
                        (right, "right"),
                        (left, "left"),
                        (not any([up, down, right, left]), "idle")
                    ]:
                        if con:
                            Player.move(cmd)
            elif event.type == MOUSEBUTTONUP:
                Turret.fire(False)
            elif event.type == QUIT:
                pygame.quit()
                exit()
        Gfx.cursor()
        Clock.tick(fps)
        pygame.display.update()


if __name__ == "__main__":
    main()

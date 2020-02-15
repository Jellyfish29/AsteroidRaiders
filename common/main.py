
from pygame.locals import *

from init import *
from astraid_funcs import *
import astraid_data as data
from interface import *
from interface_new import *
from player import *
from turret import *
from enemys import *
from allies import *
from bosses import *
from Gfx import *
from levels import *
from events import *
from items import *
from items_active import *
from items_passive import *
from items_misc import *
from phenomenon import *
from bosses_def import *
from ui import *

from profilehooks import profile


def test_mode():
    Levels.display_level += 1
    Levels.level += 1
    Levels.events_disabled = True
    Levels.scaling()
    Levels.display_score += 400
    Player.health += 40000
    Player.damage += 102
    Items.upgrade_points += 400
    Levels.skill_points += 100
    Levels.execute_special_event()
    Player.health = 20
    Player.max_health = 20
    # Elites.spawn()
    # data.ENEMY.set_spawn_table(Shooter)
    # data.ENEMY_DATA.append(random.choice(Enemy.spez_spawn_table)())


@profile
def main():

    right, left, up, down = [False, False, False, False]

    def move_condition(bool_1, str_1, bool_2, str_2, str_3):
        if bool_1:
            Player.move(str_1)
        elif bool_2:
            Player.move(str_2)
        else:
            Player.move(str_3)

    components = [Player, Turret, Enemy, Phenomenon, Levels, Items]  # Interface,

    # @profile
    def components_update():
        for component in components:
            component.update()

    # Background Setup
    Background.update()
    Background.bg_objs += [Background(y=0), Background(y=1000), Background(y=-1000)]

    # Item Setup
    # Items.drop((winwidth / 2, 400), target=Item_pd((100, 100, 200)))
    Items.drop((winwidth / 2, 400), target=start_item_generator()((100, 100, 200)))
    Levels.after_boss = True

    # Interface Setup
    # Interface.create()
    Interface_new.create()
    # Interface.main_menu(True)

    # Enemy Setup
    Levels.spez_add()

    while True:

        win.fill(Background.bg_color)
        Background.update()

        Gfx.layer_3_update()

        data.GAME_UPDATE()

        Gfx.layer_2_update()

        components_update()

        Gfx.layer_1_update()

        data.GUI_UPDATE()

        Interface_new.update()

        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_TAB:
                    scrollspeed_temp = Background.scroll_speed
                    # Background.scroll_speed = 0
                    Interface.upgrades_menu(True)
                    Background.scroll_speed = scrollspeed_temp
                    right, left, up, down = [False, False, False, False]
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

                elif event.key == K_q:
                    try:
                        Items.inventory_dic[0].toggle()
                        Items.inventory_dic[0].activation_effect()
                    except AttributeError:
                        pass  # Fehlersound
                elif event.key == K_e:
                    try:
                        Items.inventory_dic[1].toggle()
                        Items.inventory_dic[1].activation_effect()
                    except AttributeError:
                        pass
                elif event.key == K_r:
                    try:
                        Items.inventory_dic[2].toggle()
                        Items.inventory_dic[2].activation_effect()
                    except AttributeError:
                        pass  # Fehlersound

                elif event.key == K_f:
                    try:
                        Items.inventory_dic[3].toggle()
                        Items.inventory_dic[3].activation_effect()
                    except AttributeError:
                        pass

                elif event.key == K_SPACE:
                    if not Player.jumpdrive_disabled:
                        Player.jumpdrive.toggle()
                        Player.jumpdrive.activation_effect()

                elif event.key == K_LSHIFT:
                    Player.afterburner.toggle()
                    Player.afterburner.activation_effect()

                elif event.key == K_LALT:
                    Player.interaction_button(True)

                elif event.key == K_p:
                    Interface.pause_menu(True)

                elif event.key == K_l:
                    if not Levels.boss_fight:
                        try:
                            data.LEVELS.load_game().load_save()
                        except FileNotFoundError:
                            pass
                elif event.key == K_i:
                    Items.spawm_items_test()

                elif event.key == K_m:
                    test_mode()

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

                elif event.key == K_q:
                    try:
                        Items.inventory_dic[0].end_activation()
                    except AttributeError:
                        pass

                elif event.key == K_e:
                    try:
                        Items.inventory_dic[1].end_activation()
                    except AttributeError:
                        pass

                elif event.key == K_r:
                    try:
                        Items.inventory_dic[2].end_activation()
                    except AttributeError:
                        pass

                elif event.key == K_f:
                    try:
                        Items.inventory_dic[3].end_activation()
                    except AttributeError:
                        pass

                elif event.key == K_SPACE:
                    if not Player.jumpdrive_disabled:
                        Player.jumpdrive.end_activation()

                elif event.key == K_LSHIFT:
                    Player.afterburner.end_activation()

                elif event.key == K_LALT:
                    Player.interaction_button(False)

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

        Clock.tick(fps)
        pygame.display.update()
        # pygame.display.flip()


if __name__ == "__main__":
    main()

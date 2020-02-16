
from init import *
from ui import *
import astraid_data as data
from Gfx import Gfx, Background


class Upgrade_menu(Timer):

    def __init__(self):
        self.menu_active = False
        self.menu = []

        self.menu.append(Gui_image(loc=(0, 0), img_idx=10))

    def tick(self):
        while self.menu_active:

            win.fill(Background.bg_color)
            Background.update()
            data.INTERFACE.cursor_update()
            data.INTERFACE.standart_ui_update()
            data.INTERFACE.health_bar_update()

            for element in self.menu:
                element.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_TAB:
                        Background.bg_move = True
                        self.menu_active = False

            Clock.tick(fps)
            pygame.display.flip()

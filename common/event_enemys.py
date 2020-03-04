import pygame
import random

from init import *
from astraid_funcs import *
import astraid_data as data
from Gfx import Gfx
from projectiles import Projectile, Mine, Explosion
from items_misc import Item_upgrade_point_crate, Item_supply_crate
from enemys import Enemy, Shooter


class Comet(Enemy):
    def __init__(self, special=False):

        super().__init__(
            0,
            20,
            1,
            Enemy.health,
            (60, 60),
            (13, 13),
            (-50, -50),
            Enemy.spez_sprites
        )
        if special:
            self.hitbox.center = random.choice([(60, -100), (1860, -100)])
            self.target = (self.hitbox.center[0], 2000)
            self.direction = 90
        self.hitable = False
        self.score_amount = 8
        self.fire_rate = 180
        self.ttk_bonus = 50


class Event_shooter(Shooter):

    def __init__(self, dest, standart_spawn=None,
                 special_spawn=None, border_check=False, gfx_rot=True):
        if standart_spawn is None:
            standart_spawn = random.randint(1, 4)
        super().__init__(spawn=standart_spawn)
        if special_spawn is not None:
            self.hitbox.center = special_spawn
        self.dest = dest
        self.border_check = border_check
        self.gfx_hook = (-50, -50)
        self.health = Enemy.health + 6
        self.max_health = self.health
        self.fire_rate = random.randint(40, 120)
        self.gfx_rot = gfx_rot
        self.idle_gfx_idx = (15, 15)
        self.animation_speed = 8

    def move(self):
        self.direction = degrees(
            self.dest[0], self.hitbox.center[0],
            self.dest[1], self.hitbox.center[1]
        )

        self.hitbox.move_ip(self.angles[self.direction])

        if self.hitbox.collidepoint(self.dest):
            self.angles = angles_360(0)
            self.gfx_idx = self.idle_gfx_idx

    def gfx_animation(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        animation_ticker = self.timer_animation_ticker(self.animation_speed)

        if self.gfx_rot:

            if len(data.PLAYER_DATA) > 0:
                target = data.PLAYER_DATA[0].hitbox.center
            else:
                target = self.dest

            gfx_angle = degrees(
                target[1],
                self.hitbox.center[1],
                target[0],
                self.hitbox.center[0]
            )

            if animation_ticker < self.animation_speed / 2:
                win.blit(rot_center(
                    self.sprites[self.gfx_idx[0]], gfx_angle),
                    (self.hitbox.topleft[0] + self.gfx_hook[0],
                     self.hitbox.topleft[1] + self.gfx_hook[1])
                )
            else:
                win.blit(rot_center(
                    self.sprites[self.gfx_idx[1]], gfx_angle),
                    (self.hitbox.topleft[0] + self.gfx_hook[0],
                     self.hitbox.topleft[1] + self.gfx_hook[1])
                )

        else:

            if animation_ticker < self.animation_speed / 2:
                win.blit(self.sprites[self.gfx_idx[0]],
                         (self.hitbox.topleft[0] + self.gfx_hook[0], self.hitbox.topleft[1] + self.gfx_hook[1]))
            else:
                win.blit(self.sprites[self.gfx_idx[1]],
                         (self.hitbox.topleft[0] + self.gfx_hook[0], self.hitbox.topleft[1] + self.gfx_hook[1]))

    def reset(self):
        self.dest = (-1000, -500)
        self.angles = angles_360(4)
        self.border_check = True
        self.gfx_idx = (7, 8)


class Convoy_ship_enemy(Shooter):

    def __init__(self, y):
        super().__init__()
        self.x = random.randint(1950, 2050)
        self.y = random.randint(-50, 50)
        self.gfx_idx = (11, 12)
        self.spawn_points = [(self.x, y + self.y)]
        self.spawn_point = 0
        self.hitbox.center = (self.x, y + self.y)
        self.direction = degrees(-100, self.x, y + self.y, y + self.y)
        self.orig_direction = self.direction
        self.target = (-100, y + self.y)
        self.angles = angles_360(4)
        self.health = Enemy.health + 10
        self.max_health = self.health

    # def move(self):
    #     self.hitbox.move_ip(self.speed, 0)

    def skill(self):
        pass

    def death(self):
        data.TURRET.overdrive()
        self.gfx_hit()
        data.EVENTS.convoy_attack_c_destroyed += 1
        if data.EVENTS.convoy_attack_c_destroyed == 4:
            data.EVENTS.convoy_attack_c_destroyed = 0
            random.choice([
                lambda: data.ITEMS.drop(
                    self.hitbox.topleft, target=Item_upgrade_point_crate((100, 100, 200), level=0)),
                lambda: data.ITEMS.drop(
                    (self.hitbox.topleft), target=Item_supply_crate((100, 100, 100), level=0))
            ])()
        self.kill = True


class Ground_infantry(Event_shooter):

    def __init__(self, dest):
        super().__init__(dest, standart_spawn=random.choice([1, 3, 4]))
        self.gfx_idx = (23, 24)
        self.gfx_hook = (-30, -30)
        self.idle_gfx_idx = (22, 22)
        self.angles = angles_360(2)
        self.health = 1
        self.animation_speed = 60
        self.hitbox = pygame.Rect(self.hitbox.topleft[0], self.hitbox.topleft[1], 35, 35)

    def skill(self):
        pass

import pygame
import random

from init import *
from astraid_funcs import *
import astraid_data as data
from Gfx import Gfx, Background
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
        self.zero_angles = angles_360(0)
        self.target_player = False

    def move(self):
        self.direction = degrees(
            self.dest[0], self.hitbox.center[0],
            self.dest[1], self.hitbox.center[1]
        )

        self.hitbox.move_ip(self.angles[self.direction])

        if self.hitbox.collidepoint(self.dest):
            self.angles = self.zero_angles
            self.gfx_idx = self.idle_gfx_idx

    def gfx_animation(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        animation_ticker = self.timer_animation_ticker(self.animation_speed)

        if self.gfx_rot:

            if self.target_player:
                target = data.PLAYER.hitbox.center
            elif len(data.PLAYER_DATA) > 0:
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

    def __init__(self, dest, speed=2):
        super().__init__(dest, standart_spawn=1)
        self.gfx_idx = (23, 24)
        self.gfx_hook = (-10, -10)
        self.idle_gfx_idx = (22, 22)
        self.angles = angles_360(speed)
        self.speed = speed
        self.health = 1
        self.max_health = 1
        self.animation_speed = 60
        self.hitbox = pygame.Rect(self.hitbox.topleft[0], self.hitbox.topleft[1], 35, 35)
        self.charge = False
        self.score_amount = 0.1

    def gfx_hit(self):
        Background.bg_objs.append(Infantry_corps(self.hitbox.topleft))
        Gfx.create_effect(
            "blood", 2,
            (self.hitbox.topleft[0] - 50, self.hitbox.topleft[1] - 50)
        )

    def skill(self):
        if self.charge:
            self.dest = (1000, 900)
            self.angles = angles_360(self.speed)
            self.charge = False

        try:
            if self.hitbox.colliderect(data.PLAYER_DATA[0].hitbox):
                if not data.EVENTS.ground_sup_cap_limiter:
                    data.EVENTS.ground_sup_cap_progress += 0.1
                    data.EVENTS.ground_sup_cap_limiter = True
        except IndexError:
            pass


class Infantry_corps(Timer):

    def __init__(self, loc):
        self.loc = loc
        super().__init__()
        self.kill = False
        self.gfx_idx = random.choice([27, 28, 29])

    def gfx_animation(self):
        win.blit(Enemy.spez_sprites[self.gfx_idx], (self.loc[0], self.loc[1]))
        if self.timer_trigger(240):
            self.kill = True
        self.timer_tick()


class Ground_aa_tank(Event_shooter):

    def __init__(self, dest, spawn):
        super().__init__(dest, standart_spawn=1)
        self.hitbox.center = spawn
        self.gfx_idx = (25, 25)
        self.idle_gfx_idx = (25, 25)
        self.health = Enemy.health * 6
        self.max_health = self.health
        self.target_player = True
        self.delta_salvo_limit = (i for i in range(6))
        self.fire_rate = random.randint(100, 160)
        self.animation_speed = 10
        self.gun_idx = 15
        self.angles = angles_360(1)
        self.gfx_rot = False

    def skill(self):
        if len(data.PLAYER_DATA) > 0:
            if self.timer_key_delay(limit=self.fire_rate, key="salvo_d"):
                if self.timer_trigger(5):
                    self.fire_rate -= 1
                    self.gun_idx = 15
                    data.ENEMY_PROJECTILE_DATA.append(Projectile(
                        15, (6, 6),
                        (self.hitbox.center[0], self.hitbox.center[1]),
                        1, "enemy", 12,
                        target=data.PLAYER.hitbox)
                    )
                    limit = next(self.delta_salvo_limit, "stop")
                    if limit == "stop":
                        self.timer_key_delay(reset=True, key="salvo_d")
                        self.delta_salvo_limit = (i for i in range(6))
                else:
                    self.gun_idx = 16

        self.gfx_gun()

    def gfx_gun(self):
        gfx_angle = degrees(
            data.PLAYER.hitbox.center[1],
            self.hitbox.center[1],
            data.PLAYER.hitbox.center[0],
            self.hitbox.center[0]
        )

        win.blit(rot_center(
            Gfx.gun_sprites[self.gun_idx], gfx_angle),
            (self.hitbox.topleft[0] - 26, self.hitbox.topleft[1] - 30)
        )

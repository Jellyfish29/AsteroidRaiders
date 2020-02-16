import pygame
import random

from init import *
from astraid_funcs import *
import astraid_data as data
from Gfx import Gfx, Background
from projectiles import Projectile
from phenomenon import Defence_zone
from items_misc import Item_upgrade_point_crate, Item_heal_crate, Item_supply_crate


class Allied_entity(Timer):

    allied_sprites = get_images("allies")

    def __init__(self, speed=0, health=0, spawn_point=0, target=None,
                 size=(0, 0), gfx_idx=(0, 0), gfx_hook=(0, 0)):
        self.speed = speed
        self.health = health
        self.spawn_point = spawn_point
        self.target = target
        self.size = size
        self.gfx_idx = gfx_idx
        self.gfx_hook = gfx_hook
        self.angles = angles_360(self.speed)
        self.hitbox = pygame.Rect(self.spawn_point[0], self.spawn_point[1],
                                  self.size[0], self.size[1])
        self.max_health = self.health
        self.healthbar_len = self.size[0]
        self.healthbar_height = 1
        self.healthbar_max_len = self.healthbar_len
        self.direction = 0
        self.rot_sprite = True
        self.kill = False
        self.hitable = True
        self.super_hitable = True
        self.hide_healthbar = False
        self.border_check = True
        self.flag = "allie"
        Timer.__init__(self)

    def move(self):
        self.direction = degrees(
            self.target[0], self.hitbox.center[0],
            self.target[1], self.hitbox.center[1]
        )

        self.hitbox.move_ip(self.angles[self.direction])
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)

    def skill(self):
        pass

    def script(self):
        pass

    def border_collide(self):
        if rect_not_on_sreen(self.hitbox, bot=False, strict=False):
            self.kill = True

    def hit(self, enemy):
        if self.hitbox.colliderect(enemy.hitbox):
            return True

    def take_damage(self, dmg, staggered=False):
        color = (255, 10, 10)

        if staggered:
            if self.timer_trigger(30):
                self.set_health(dmg, color)
        else:
            self.set_health(dmg, color)

    def set_health(self, hp, color):
        self.health -= hp
        self.healthbar_len -= (self.healthbar_max_len / (self.max_health / hp))
        Gfx.create_effect(
            "dmg_text", 4,
            (self.hitbox.center[0] + random.randint(-10, 10),
             self.hitbox.center[1] + random.randint(-10, 10)),
            hover=True, follow=True, text=hp, text_color=color
        )

        if self.health > self.max_health:
            self.health = self.max_health

    def gfx_health_bar(self):
        if self.health < self.max_health:
            pygame.draw.rect(win, (200, 0, 0),
                             (pygame.Rect(self.hitbox.topleft[0],
                                          self.hitbox.topleft[1] - 60,
                                          self.healthbar_max_len,
                                          self.healthbar_height
                                          )))
            if not self.healthbar_len < 0:
                pygame.draw.rect(win, (0, 200, 0),
                                 (pygame.Rect(self.hitbox.topleft[0],
                                              self.hitbox.topleft[1] - 60,
                                              self.healthbar_len,
                                              self.healthbar_height
                                              )))

    def gfx_animation(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        animation_ticker = self.timer_animation_ticker(16)
        if not self.rot_sprite:
            gfx_angle = 0
        else:
            gfx_angle = degrees(
                self.target[1], self.hitbox.center[1],
                self.target[0], self.hitbox.center[0]
            )
        if animation_ticker < 8:
            win.blit(rot_center(
                Allied_entity.allied_sprites[self.gfx_idx[0]], gfx_angle),
                (self.hitbox.topleft[0] + self.gfx_hook[0] - 50,
                 self.hitbox.topleft[1] + self.gfx_hook[1] - 50)
            )
        else:
            win.blit(rot_center(
                Allied_entity.allied_sprites[self.gfx_idx[1]], gfx_angle),
                (self.hitbox.topleft[0] + self.gfx_hook[0] - 50,
                 self.hitbox.topleft[1] + self.gfx_hook[1] - 50)
            )

    def gfx_hit(self):
        Gfx.create_effect(
            "explosion_2", 2,
            (self.hitbox.topleft[0] - 120, self.hitbox.topleft[1] - 130),
            explo=True
        )

    def get_name(self):
        return self.__class__.__name__

    def destroy(self):
        return self.kill

    def death(self):
        self.gfx_hit()
        self.kill = True

    def tick(self):
        self.gfx_animation()
        if not self.hide_healthbar:
            self.gfx_health_bar()
        self.move()
        self.skill()
        self.script()
        if self.border_check:
            self.border_collide()
        if self.health <= 0:
            self.death()
        self.timer_tick()


class Space_station_allie(Allied_entity):

    def __init__(self, spawn_point=0, target=None):
        super().__init__(speed=Background.scroll_speed, health=100, spawn_point=spawn_point,
                         target=target, size=(200, 200), gfx_idx=(0, 0), gfx_hook=(-50, 0))
        self.hitable = False
        self.rot_sprite = False
        self.run_limiter = Run_limiter()
        self.border_check = False

    def move(self):
        self.hitbox.move_ip(0, self.speed)

    def script(self):
        if self.hitbox.center[1] >= self.target[1]:
            self.speed = 0
            Background.bg_move = False

        if not data.LEVELS.special_events:
            self.border_check = True
            Background.bg_move = True
            self.speed = Background.scroll_speed

            if self.run_limiter.run_block_once():

                data.ITEMS.drop(
                    (self.hitbox.topleft), target=Item_heal_crate((100, 100, 100), level=2))

                if data.EVENTS.convoy_points >= 12:
                    data.ITEMS.drop((self.hitbox.topright), amount=1)
                elif data.EVENTS.convoy_points >= 8:
                    data.ITEMS.drop(
                        (self.hitbox.topright), target=Item_upgrade_point_crate((100, 100, 100), level=3))
                elif data.EVENTS.convoy_points >= 6:
                    data.ITEMS.drop(
                        (self.hitbox.topright), target=Item_upgrade_point_crate((100, 100, 100), level=2))
                elif data.EVENTS.convoy_points >= 4:
                    data.ITEMS.drop(
                        (self.hitbox.topright), target=Item_upgrade_point_crate((100, 100, 100), level=1))

                data.LEVELS.convoy_points = 0


class Convoy_ship_allie(Allied_entity):

    def __init__(self, spawn_point=0, target=(0, 0),):
        super().__init__(speed=2, health=3, spawn_point=spawn_point, target=target,
                         size=(80, 80), gfx_idx=(1, 2), gfx_hook=(0, 0))
        self.run_limiter = Run_limiter()
        self.border_check = False

    def script(self):
        if self.hitbox.collidepoint(self.target):
            self.angles = angles_360(0)
            if self.run_limiter.run_block_once():
                data.EVENTS.convoy_points += 1
                Gfx.create_effect(
                    "text", 4,
                    (self.hitbox.center[0] + random.randint(-10, 10),
                     self.hitbox.center[1] + random.randint(-10, 10)),
                    hover=True, follow=True, text="Saved Ships + 1", text_color=(0, 0, 100)
                )
                self.gfx_idx = (3, 3)
                self.hitable = False
            if self.timer_trigger(120):
                self.kill = True


class Battleship_allie(Allied_entity):

    def __init__(self, spawn_point=0, target=None):
        super().__init__(speed=Background.scroll_speed, health=150, spawn_point=spawn_point,
                         target=target, size=(200, 200), gfx_idx=(4, 4), gfx_hook=(0, 0))
        self.hitable = True
        self.rot_sprite = False
        self.border_check = False
        self.healthbar_height = 5
        self.fire_rate = 150
        self.run_limiter = Run_limiter()
        self.direction = 90
        self.orig_directions = self.direction

    def move(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        self.hitbox.move_ip(self.angles[self.direction])

    def script(self):
        if self.hitbox.center[1] >= self.target[1]:
            self.angles = angles_360(0)
            Background.bg_move = False

        if not data.EVENTS.bs_defence_bs_disabled:
            if not self.timer_delay(120):
                self._draw_damage_effect()

            # self.hitable = False
            # self.hide_healthbar = True
            self.angles = angles_360(1)
            self.gfx_idx = (5, 6)
            self.fire_rate = 10
            if self.hitbox.center[1] > 1200:
                Background.bg_move = True
                self.kill = True

                data.ITEMS.drop(
                    (1000, 400), target=Item_heal_crate((100, 100, 100), level=2))

                if self.health >= self.max_health * 0.85:
                    data.ITEMS.drop((self.hitbox.topright), amount=1)
                elif self.health >= self.max_health * 0.7:
                    data.ITEMS.drop(
                        (1000, 400), target=Item_supply_crate((100, 100, 100), level=3))
                elif self.health >= self.max_health * 0.4:
                    data.ITEMS.drop(
                        (1000, 400), target=Item_supply_crate((100, 100, 100), level=2))
                elif self.health >= self.max_health * 0.2:
                    data.ITEMS.drop(
                        (1000, 400), target=Item_supply_crate((100, 100, 100), level=1))
                elif self.health > 0:
                    data.ITEMS.drop(
                        (1000, 400), target=Item_supply_crate((100, 100, 100), level=0))
        else:
            self._draw_damage_effect()

    def _draw_damage_effect(self):
        for x, y, i in [self._get_smoke_loc() + [i] for i in range(20, 41, 10)]:
            if self.timer_trigger(i):
                Gfx.create_effect(
                    "smoke1", 4, anchor=self.hitbox, follow=True, x=x, y=y
                )

    def _get_smoke_loc(self):
        return [random.randint(-100, 80), random.randint(-100, 80)]

    def skill(self):
        if len(data.ENEMY_DATA) > 0:
            target = data.ENEMY_DATA[random.randint(0, len(data.ENEMY_DATA) - 1)].hitbox.center
            if self.timer_trigger(self.fire_rate):
                # self.muzzle_effect_timer = (i for i in range(8))
                data.PLAYER_PROJECTILE_DATA.append(Projectile(
                    speed=20,
                    size=(6, 6),
                    start_point=self.hitbox.center,
                    damage=1,
                    flag="ally",
                    gfx_idx=15,
                    target=target
                ))

    def death(self):
        Background.bg_move = True
        self.kill = True


class Comrelay(Allied_entity):

    def __init__(self, spawn_point=0, target=None):
        super().__init__(speed=Background.scroll_speed, health=100, spawn_point=spawn_point,
                         target=target, size=(70, 200), gfx_idx=(7, 8), gfx_hook=(35, 50))
        self.hitable = False
        self.super_hitable = False
        self.rot_sprite = False
        self.run_limiter = Run_limiter()
        self.border_check = False
        self.interaction_hitbox = pygame.Rect(self.hitbox.center[0], self.hitbox.center[1], 300, 300)
        self.hack_progress = 0
        self.healthbar_height = 8
        self.healthbar_max_len = 100

    def move(self):
        self.hitbox.move_ip(0, self.speed)
        self.interaction_hitbox.center = self.hitbox.center

    def gfx_health_bar(self):
        pygame.draw.rect(win, (200, 200, 200),
                         (pygame.Rect(self.hitbox.topleft[0],
                                      self.hitbox.topleft[1] - 80,
                                      self.healthbar_max_len,
                                      self.healthbar_height
                                      )))

        pygame.draw.rect(win, (0, 0, 200),
                         (pygame.Rect(self.hitbox.topleft[0],
                                      self.hitbox.topleft[1] - 80,
                                      self.hack_progress,
                                      self.healthbar_height
                                      )))

    def script(self):
        if not Background.bg_move:
            self.speed = 0
        else:
            self.speed = Background.scroll_speed

        # if data.PLAYER.interaction_button_pressed:
        if self.interaction_hitbox.colliderect(data.PLAYER.hitbox):
            if self.hack_progress < 100:
                if self.timer_trigger(5):
                    self.hack_progress += 1

        if self.hack_progress >= 100:
            if self.run_limiter.run_block_once():
                data.EVENTS.hack_stations_hacked += 1
                self.gfx_idx = (7, 9)
                self.border_check = True
                self.hide_healthbar = True
        if len(data.LEVELS.special_event_queue) == 0:
            self.border_check = True
            self.hide_healthbar = True

    def dest_reached(self):
        if self.hitbox.center[1] > 700:
            return True


class Battlecruiser_ally(Battleship_allie):

    def __init__(self, spawn_point=None, target=None):
        super().__init__(spawn_point=spawn_point, target=target)
        self.gfx_idx = (10, 11)
        self.hitable = False
        self.hide_healthbar = True
        self.health = 15
        self.max_health = self.health
        self.angles = angles_360(3)

    def script(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        if Background.bg_move:
            if len(data.LEVELS.special_event_queue) == 0:
                self.angles = angles_360(4)
            else:
                if not self.hitable:
                    if self.hitbox.bottom >= self.target[1]:
                        self.gfx_idx = (12, 12)
                        self.angles = angles_360(0)
                        for loc in [
                            (700, 200), (1000, 200), (1300, 200),
                            (700, 500), (1300, 500),
                            (700, 800), (1000, 800), (1300, 800)
                        ]:
                            data.PHENOMENON_DATA.append(Defence_zone(loc))
                        Background.bg_move = False
        else:
            if len([z for z in data.PHENOMENON_DATA if not z.captured]) == 0:
                self.hitable = True
                self.hide_healthbar = False
                self.angles = angles_360(1)

    def death(self):
        data.EVENTS.z_def_bc_destroyed = True
        self.gfx_hit()
        self.kill = True


data.ALLIE = Allied_entity

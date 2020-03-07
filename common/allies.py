import pygame
import random

from init import *
from astraid_funcs import *
import astraid_data as data
from Gfx import Gfx, Background
from projectiles import Projectile, Missile, Impactor, Explosion
from phenomenon import Defence_zone
from items_misc import Item_upgrade_point_crate, Item_heal_crate, Item_supply_crate
from ui import *


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
        self.zero_angles = angles_360(0)
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
        self.scripts = {None: self.script}
        self.script_name = None
        self.animation_speed = 16
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
        animation_ticker = self.timer_animation_ticker(self.animation_speed)
        if not self.rot_sprite:
            gfx_angle = 0
        else:
            gfx_angle = degrees(
                self.target[1], self.hitbox.center[1],
                self.target[0], self.hitbox.center[0]
            )
        if animation_ticker < self.animation_speed / 2:
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
        self.scripts[self.script_name]()
        if self.border_check:
            self.border_collide()
        if self.health <= 0:
            self.death()
        self.timer_tick()


class Space_station_ally(Allied_entity):

    def __init__(self, spawn_point=0, target=None, script_name=None):
        super().__init__(speed=Background.scroll_speed, health=100, spawn_point=spawn_point,
                         target=target, size=(200, 200), gfx_idx=(0, 0), gfx_hook=(-50, 0))
        self.hitable = False
        self.rot_sprite = False
        self.run_limiter = Run_limiter()
        self.border_check = False
        self.script_name = script_name
        self.scripts.update({"convoy_defence": self.convoy_defence_script,
                             "intro": self.intro_script})

    def move(self):
        self.hitbox.move_ip(0, self.speed)

    def convoy_defence_script(self):
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
                data.ITEMS.drop(
                    (self.hitbox.topright), target=Item_supply_crate((100, 100, 100), level=1))

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

    def intro_script(self):
        self.speed = 0


class Transport_ship_ally(Allied_entity):

    def __init__(self, spawn_point=0, target=(0, 0), script_name=None, speed=2):
        super().__init__(speed=speed, health=3, spawn_point=spawn_point, target=target,
                         size=(80, 80), gfx_idx=(1, 2), gfx_hook=(0, 0))
        self.run_limiter = Run_limiter()
        self.script_name = script_name
        self.border_check = False
        self.scripts.update({"convoy_defence": self.convoy_defence_script,
                             "planet_evac": self.planet_evac_script,
                             "planet_invasion": self.planet_invasion_script})

    def convoy_defence_script(self):
        if self.hitbox.collidepoint(self.target):
            self.angles = angles_360(0)
            if self.run_limiter.run_block_once():
                data.EVENTS.convoy_points += 1
                self.gfx_idx = (3, 3)
                self.hitable = False
            if self.timer_trigger(120):
                self.kill = True

    def planet_evac_script(self):
        self.border_check = True

    def planet_invasion_script(self):
        self.border_check = False
        if self.hitbox.collidepoint(self.target):
            self.angles = angles_360(0)
            if self.run_limiter.run_block_once():
                self.gfx_idx = (3, 3)
                self.hitable = False
                self.speed = 0

                data.ITEMS.drop(
                    self.hitbox.center, target=Item_heal_crate((100, 100, 100), level=2))
                data.ITEMS.drop(
                    self.hitbox.center, target=Item_supply_crate((100, 100, 100), level=2))
                data.ITEMS.drop(
                    self.hitbox.center, target=Item_upgrade_point_crate((100, 100, 100), level=2))

        if Background.bg_move:
            self.hitbox.move_ip(0, Background.scroll_speed)
            self.border_check = True


class Battleship_allie(Allied_entity):

    def __init__(self, spawn_point=0, target=None, script_name=None):
        super().__init__(speed=Background.scroll_speed, health=150, spawn_point=spawn_point,
                         target=target, size=(200, 200), gfx_idx=(4, 4), gfx_hook=(20, 0))
        self.hitable = True
        self.rot_sprite = False
        self.border_check = False
        self.healthbar_height = 5
        self.fire_rate = 150
        self.run_limiter = Run_limiter()
        self.direction = 90
        self.orig_directions = self.direction
        self.script_name = script_name
        self.scripts.update({"btl_defence": self.btl_defence_script})

    def move(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        self.hitbox.move_ip(self.angles[self.direction])

    def btl_defence_script(self):
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

                data.ITEMS.drop(
                    (1000, 400), target=Item_heal_crate((100, 100, 100), level=2))

                if self.health > 0:
                    data.ITEMS.drop(
                        (1000, 400), target=Item_supply_crate((100, 100, 100), level=3))
                self.kill = True
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

    def __init__(self, spawn_point=0, target=None, script_name=None):
        super().__init__(speed=Background.scroll_speed, health=100, spawn_point=spawn_point,
                         target=target, size=(70, 70), gfx_idx=(7, 8), gfx_hook=(35, 0))
        self.hitable = False
        self.super_hitable = False
        self.rot_sprite = False
        self.run_limiter = Run_limiter()
        self.border_check = False
        self.hack_progress = 0
        self.healthbar_height = 8
        self.healthbar_max_len = 100
        self.script_name = script_name
        self.scripts.update({"hack": self.hack_script})

    def move(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        self.hitbox.move_ip(0, self.speed)

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

    def hack_script(self):
        if not Background.bg_move:
            self.speed = 0
        else:
            self.speed = Background.scroll_speed

        # if data.PLAYER.interaction_button_pressed:
        if self.hitbox.colliderect(data.PLAYER.hitbox):
            if self.hack_progress < 100:
                if self.timer_trigger(2):
                    self.hack_progress += 1

        if self.hack_progress >= 100:
            if self.run_limiter.run_block_once():
                data.EVENTS.hack_stations_hacked += 1
                self.gfx_idx = (7, 9)
                self.border_check = True
                self.hide_healthbar = True
                Gui.delete(str(id(self)))
        if len(data.LEVELS.special_event_queue) == 0:
            self.border_check = True
            self.hide_healthbar = True

    def dest_reached(self):
        if self.hitbox.center[1] > 700:
            return True


class Battlecruiser_ally(Battleship_allie):

    def __init__(self, spawn_point=None, target=None, script_name=None):
        super().__init__(spawn_point=spawn_point, target=target)
        self.gfx_idx = (10, 11)
        self.hitable = False
        self.hide_healthbar = True
        self.health = 15
        self.max_health = self.health
        self.angles = angles_360(3)
        self.script_name = script_name
        self.scripts.update({"zone_def": self.zone_defence_script})
        self.run_limiter = Run_limiter()

    def zone_defence_script(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        if Background.bg_move:
            if len(data.LEVELS.special_event_queue) == 0:
                self.angles = angles_360(4)
            else:
                if self.hitbox.bottom >= self.target[1]:
                    self.gfx_idx = (12, 12)
                    self.angles = angles_360(0)
                    if self.run_limiter.run_block_once():
                        Background.bg_move = False
                        for loc in [
                            (700, 200), (1000, 200), (1300, 200),
                            (700, 500), (1300, 500),
                            (700, 800), (1000, 800), (1300, 800)
                        ]:
                            data.PHENOMENON_DATA.append(Defence_zone(loc))
        else:
            if len([
                    z for z in data.PHENOMENON_DATA if not z.captured and z.get_name() == "Defence_zone"]) == 0:
                self.hitable = True
                self.hide_healthbar = False
                self.border_check = True
                self.angles = angles_360(1)

    def death(self):
        data.EVENTS.z_def_bc_destroyed = True
        self.gfx_hit()
        self.kill = True


class Destroyer_ally(Allied_entity):

    def __init__(self, spawn_point=None, target=None, script_name=None):
        Allied_entity.__init__(self, speed=2, health=60, spawn_point=spawn_point,
                               target=target, size=(100, 100), gfx_idx=(13, 14), gfx_hook=(-25, -25))
        self.script_name = script_name
        self.scripts.update({"planet_invasion": self.planet_invasion_script,
                             "ground_support": self.ground_support_script})
        self.max_health = self.health
        self.border_check = False
        self.fire_rate = 50

    def planet_invasion_script(self):
        if self.hitbox.collidepoint(self.target):
            self.gfx_idx = (15, 15)
            self.angles = angles_360(0)

        if Background.bg_move:
            self.hitbox.move_ip(0, Background.scroll_speed)
            self.border_check = True

    def ground_support_script(self):
        self.angles = self.zero_angles
        self.gfx_idx = (15, 15)

        if Background.bg_move:
            self.hitbox.move_ip(0, Background.scroll_speed)
            if self.hitbox.top >= 1200:
                self.border_check = True

    def skill(self):
        if len(data.ENEMY_DATA) > 0:
            target = data.ENEMY_DATA[random.randint(0, len(data.ENEMY_DATA) - 1)].hitbox.center
            if self.timer_trigger(self.fire_rate):
                # self.muzzle_effect_timer = (i for i in range(8))
                data.PLAYER_PROJECTILE_DATA.append(Projectile(
                    speed=20,
                    size=(6, 6),
                    start_point=self.hitbox.center,
                    damage=data.PLAYER.damage,
                    flag="ally",
                    gfx_idx=15,
                    target=target
                ))


class Fighter_ally(Allied_entity):

    def __init__(self, spawn_point=None, target=None, script_name=None):
        Allied_entity.__init__(self, speed=8, health=3, spawn_point=spawn_point,
                               target=target, size=(60, 60), gfx_idx=(16, 17), gfx_hook=(0, 0))
        self.fire_rate = 120

        # self.border_check = False

    def skill(self):
        if len(data.ENEMY_DATA) > 0:
            target = data.ENEMY_DATA[random.randint(0, len(data.ENEMY_DATA) - 1)].hitbox
            if self.timer_trigger_delay(self.fire_rate):
                # self.muzzle_effect_timer = (i for i in range(8))
                for _ in range(3):
                    data.PLAYER_PROJECTILE_DATA.append(Missile(
                        speed=25,
                        size=(5, 5),
                        start_point=self.hitbox.center,
                        target=target,
                        damage=data.PLAYER.damage * 1.5,
                        flag="missile",
                        gfx_idx=24
                    ))


class Mech_ally(Allied_entity):

    def __init__(self):
        Allied_entity.__init__(self, speed=0, health=50, spawn_point=(1000, 850),
                               size=(60, 60), gfx_idx=(18, 18), gfx_hook=(0, 0))
        self.rot_sprite = False
        self.fire_rate = 100
        self.muzzle_effect_timer = (i for i in range(1))
        self.hitable = False
        self.healthbar_height = 8
        self.healthbar_max_len = 100

    def move(self):
        pass

    def skill(self):
        if len(data.ENEMY_DATA) > 0:
            target = data.ENEMY_DATA[random.randint(0, len(data.ENEMY_DATA) - 1)].hitbox.center
            if self.timer_trigger(self.fire_rate):
                self.muzzle_effect_timer = (i for i in range(10))
                # self.muzzle_effect_timer = (i for i in range(8))
                for start_point in [self.hitbox.topleft, self.hitbox.topright]:
                    data.PLAYER_PROJECTILE_DATA.append(Impactor(
                        speed=15,
                        size=(4, 4),
                        start_point=start_point,
                        damage=0,
                        gfx_idx=15,
                        target=target,
                        impact_effect=lambda loc=target: data.PLAYER_PROJECTILE_DATA.append(Explosion(
                            location=loc,
                            explo_size=100,
                            damage=1,
                            explosion_effect=lambda loc: Gfx.create_effect(
                                "explosion_2", 2, (loc[0] - 120, loc[1] - 120), explo=True),
                            explo_speed=(60, 60)
                        ))
                    ))
        if next(self.muzzle_effect_timer, "stop") == "stop":
            self.gfx_idx = (18, 18)
        else:
            self.gfx_idx = (19, 19)

        if data.EVENTS.ground_sup_cap_progress >= 100:
            self.kill = True

        if self.timer_trigger(self.fire_rate * 2):
            Gui.add(Gui_tw_text(text=random.choice(data.EVENT_TEXT["ground_sup_mech"]),
                                text_size=20, anchor=self.hitbox, anchor_x=140, anchor_y=40))

    def gfx_health_bar(self):
        pygame.draw.rect(win, (200, 200, 200),
                         (pygame.Rect(self.hitbox.bottomleft[0],
                                      self.hitbox.bottomleft[1] + 10,
                                      self.healthbar_max_len,
                                      self.healthbar_height
                                      )))

        pygame.draw.rect(win, (0, 0, 200),
                         (pygame.Rect(self.hitbox.bottomleft[0],
                                      self.hitbox.bottomleft[1] + 10,
                                      data.EVENTS.ground_sup_cap_progress,
                                      self.healthbar_height
                                      )))


data.ALLIE = Allied_entity

import pygame
import random

from astraid_funcs import *
from init import *
from Gfx import Gfx, Background
from projectiles import Projectile, Explosion
from enemys import Shooter
import astraid_data as data


class Phenomenon(Timer):

    phenom_sprites = get_images("phenomenon")
    phenomenon_spawn_table = []
    spawn_time = 100  # 3600
    amount = 1

    def __init__(self, speed, size, gfx_idx, gfx_hook, flag="neutral", decay=None):
        Timer.__init__(self)
        self.speed = speed
        self.size = size
        self.hitbox = pygame.Rect(random.randint(200, winwidth - 200), -650, size[0], size[0])
        self.kill = False
        self.gfx_idx = gfx_idx
        self.gfx_hook = gfx_hook
        self.flag = flag
        self.decay = decay
        self.scripts = {None: self.script}
        self.script_name = None
        self.captured = False

    def move(self):
        if Background.bg_move:
            self.hitbox.move_ip(0, self.speed)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)

    def decay_update(self):
        if self.decay is not None:
            if self.timer_trigger(self.decay):
                self.kill = True

    def border_collision(self):
        if rect_not_on_sreen(self.hitbox, bot=True, strict=False):
            self.kill = True

    def player_collision(self):
        pass

    def hit(self, enemy):
        pass

    def script(self):
        pass

    def gfx_draw(self):
        animation_ticker = self.timer_animation_ticker(10)
        if animation_ticker < 5:
            win.blit(
                Phenomenon.phenom_sprites[self.gfx_idx[0]],
                (self.hitbox.center[0] + self.gfx_hook[0],
                 self.hitbox.center[1] + self.gfx_hook[1])
            )
        else:
            win.blit(
                Phenomenon.phenom_sprites[self.gfx_idx[1]],
                (self.hitbox.center[0] + self.gfx_hook[0],
                 self.hitbox.center[1] + self.gfx_hook[1])
            )

    def destroy(self):
        return self.kill

    def get_name(self):
        return self.__class__.__name__

    def tick(self):
        if Background.bg_move:
            self.move()
        self.scripts[self.script_name]()
        self.decay_update()
        self.gfx_draw()
        self.border_collision()
        self.player_collision()
        self.timer_tick()

    @classmethod
    def get_spawn_table(cls):
        return cls.phenomenon_spawn_table

    @classmethod
    def set_spawn_table(cls, p):
        cls.phenomenon_spawn_table.append(p)

    @classmethod
    @timer
    def update(cls, timer):
        pass

        # if not any((data.LEVELS.boss_fight, data.LEVELS.after_boss, data.LEVELS.special_events)):
        #     if data.LEVELS.level not in [i - 1 for i in range(6, 49, 6)]:
        #         if timer.trigger(Phenomenon.spawn_time):
        #             if len(data.PHENOMENON_DATA) < Phenomenon.amount:
        #                 data.PHENOMENON_DATA.append(random.choice(cls.phenomenon_spawn_table)())


data.PHENOM = Phenomenon


class Gravity_well(Phenomenon):

    def __init__(
            self,
            speed=1,
            size=(500, 500),
            gfx_idx=(1, 1),
            gfx_hook=(-300, -300),
            decay=None,
            location=None,
            flag="phenom"
    ):
        super().__init__(speed, size, gfx_idx, gfx_hook, flag=flag, decay=decay)
        self.new_d = directions(2)
        self.new_a = angles_360(2)
        self.objs = {}

        if location is not None:
            self.hitbox.center = location

    def hit(self, obj):
        if self.hitbox.colliderect(obj.hitbox):
            if not any([issubclass(obj.__class__, Phenomenon),
                        obj.get_name() == "Boss_laser_battery",
                        obj.get_name() == "Boss_main_gun_battery"]):
                if obj not in self.objs:
                    self.objs.update({obj: obj.angles})
                    # if "Enemy" in obj.get_bases_names():
                    obj.angles = angles_360(int(obj.speed * 0.25))
                    # elif "Projectile" in obj.get_bases_names():
                    #     obj.angles = angles_360(obj.speed / 2)
                if isinstance(obj, type):
                    obj.angles = self.new_d
        if obj in self.objs:
            if not self.hitbox.colliderect(obj.hitbox):
                obj.angles = self.objs[obj]
                del self.objs[obj]

    def destroy(self):
        if self.kill:
            for obj, speed in list(self.objs.items()):
                obj.angles = speed
                del self.objs[obj]
            return True


class Black_hole(Phenomenon):

    def __init__(
            self,
            speed=0,
            size=(400, 400),
            gfx_idx=(0, 0),
            gfx_hook=(-150, -150),
            decay=300,
            location=None,
            flag="phenom",
            damage=1
    ):
        super().__init__(speed, size, gfx_idx, gfx_hook, flag=flag, decay=decay)
        # self.new_d = directions(2)
        self.new_a = angles_360(6)
        self.zero_a = angles_360(0)
        self.new_d = directions(12)
        self.zero_d = directions(0)
        self.damage = damage
        self.objs = {}
        if location is not None:
            self.hitbox.center = location

    def hit(self, obj):
        if self.hitbox.colliderect(obj.hitbox):
            if not any([issubclass(obj.__class__, Phenomenon),
                        obj.get_name() == "Boss_laser_battery",
                        obj.get_name() == "Boss_main_gun_battery"]):
                if obj not in self.objs:
                    self.objs.update({obj: obj.angles})
                    if isinstance(obj, type):  # Player check
                        pass
                    else:
                        obj.angles = self.new_a
                        obj.direction = degrees(
                            self.hitbox.center[0],
                            obj.hitbox.center[0],
                            self.hitbox.center[1],
                            obj.hitbox.center[1]
                        )
                if any([abs(obj.hitbox.center[0] - self.hitbox.center[0]) < 5,
                        abs(obj.hitbox.center[1] - self.hitbox.center[1]) < 5]):
                    try:
                        obj.take_damage(self.damage, staggered=True)
                    except AttributeError:
                        obj.kill = True
                    obj.angles = self.zero_a

        if obj in self.objs:
            if not self.hitbox.colliderect(obj.hitbox):
                obj.angles = self.objs[obj]
                del self.objs[obj]

    def destroy(self):
        if self.kill:
            for obj, speed in list(self.objs.items()):
                obj.angles = speed
                del self.objs[obj]
            return True


class Implosion(Phenomenon):
    def __init__(
            self,
            speed=0,
            size=(400, 400),
            gfx_idx=(18, 18),
            gfx_hook=(-150, -150),
            decay=15,
            location=None,
            flag="phenom",
            damage=1
    ):
        super().__init__(speed, (700, 700), gfx_idx, gfx_hook, flag=flag, decay=decay)
        # self.new_d = directions(2)
        self.new_a = angles_360(20)
        self.zero_a = angles_360(0)
        self.objs = {}
        if location is not None:
            self.hitbox.center = location

        Gfx.create_effect(
            "implosion", 2, (self.hitbox.center[0] - 400, self.hitbox.center[1] - 400), explo=True)

    def hit(self, obj):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        if self.hitbox.colliderect(obj.hitbox):
            if not any([issubclass(obj.__class__, Phenomenon),
                        obj.get_name() == "Boss_laser_battery",
                        obj.get_name() == "Boss_main_gun_battery"]):
                if obj not in self.objs:
                    self.objs.update({obj: obj.angles})
                    if isinstance(obj, type):  # Player check
                        pass
                    else:
                        obj.angles = self.new_a
                        obj.direction = degrees(
                            self.hitbox.center[0],
                            obj.hitbox.center[0],
                            self.hitbox.center[1],
                            obj.hitbox.center[1]
                        )
                if any([abs(obj.hitbox.center[0] - self.hitbox.center[0]) < 5,
                        abs(obj.hitbox.center[1] - self.hitbox.center[1]) < 5]):

                    obj.angles = self.zero_a

        if obj in self.objs:
            if not self.hitbox.colliderect(obj.hitbox):
                obj.angles = self.objs[obj]
                del self.objs[obj]

    def decay_update(self):
        if self.decay is not None:
            if self.timer_trigger(self.decay):
                data.PLAYER_PROJECTILE_DATA.append(Explosion(
                    location=self.hitbox.center,
                    explo_size=200,
                    damage=data.PLAYER.damage * 0.8,
                    explosion_effect=None
                ))
                self.kill = True

    def destroy(self):
        if self.kill:
            for obj, speed in list(self.objs.items()):
                obj.angles = speed
                del self.objs[obj]
            return True


class Repair_station(Phenomenon):

    def __init__(self):
        super().__init__(Background.scroll_speed, (200, 200), (3, 4), (-125, -125))

    def player_collision(self):
        if self.hitbox.colliderect(data.PLAYER.hitbox):
            if data.PLAYER.health < data.PLAYER.max_health:
                if self.timer_trigger(90):
                    data.PLAYER.health += 1
                    pygame.draw.rect(win, (0, 255, 0), pygame.Rect(0, 0, winwidth, winheight))


class Planet(Phenomenon):

    def __init__(self, loc=None, script_name=None):
        super().__init__(Background.scroll_speed, (250, 250), (2, 2), (-160, -160))
        if loc is not None:
            self.hitbox.center = loc
        self.script_name = script_name
        self.scripts.update({"evac": self.evac_script})

    def hit(self, obj):
        if self.hitbox.colliderect(obj.hitbox):
            if any([obj.get_name() == "Player",
                    issubclass(obj.__class__, Projectile)]):
                pass
            else:
                try:
                    obj.gfx_hit()
                except AttributeError:
                    pass
                obj.kill = True
                if self.script_name == "evac":
                    data.EVENTS.planet_evac_hit_count += 1

    def evac_script(self):
        if data.EVENTS.planet_evac_hit_count >= 30:
            self.kill = True
            Gfx.create_effect("explosion_3", 6,
                              (self.hitbox.topleft[0] - 300, self.hitbox.topleft[1] - 300),
                              explo=True)
            Gfx.create_effect("explosion_3", 6,
                              (self.hitbox.topleft[0] - 350, self.hitbox.topleft[1] - 350),
                              explo=True)


class Force_field(Timer):

    def __init__(self, location=None):
        Timer.__init__(self)
        self.hitbox = pygame.Rect(location[0], location[1], 400, 10)
        self.kill = False
        self.speed = Background.scroll_speed  # random.randint(8, 16)
        self.flag = "shield"
        self.sprite_lst = iter([8, 9, 10, 11, 12, 13, 14])
        self.gfx_idx = 8

    def hit(self, player):
        if self.hitbox.colliderect(player.hitbox):
            self.kill = True
            data.PLAYER.take_damage(3)

    def destroy(self):
        return self.kill

    def gfx_animation(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        if self.timer_trigger(2):
            self.gfx_idx = next(self.sprite_lst, 15)
            if self.gfx_idx == 15:
                self.sprite_lst = iter([8, 9, 10, 11, 12, 13, 14])
        win.blit(Phenomenon.phenom_sprites[self.gfx_idx], (self.hitbox.center[0] - 220, self.hitbox.center[1] - 220))

    def tick(self):
        self.gfx_animation()
        self.hitbox.move_ip(0, self.speed)
        if self.hitbox.center[1] > 1200:
            self.kill = True
        self.timer_tick()


class Defence_zone(Timer):

    def __init__(self, loc):
        Timer.__init__(self)
        self.loc = loc
        self.hitbox = pygame.Rect(0, 0, 300, 300)
        self.hitbox.center = loc
        self.loc = loc
        self.kill = False
        self.flag = "player"
        self.gfx_idx = 16
        self.capture_counter = 0
        self.captured = False
        self.reset = True
        self.zone_reset = True

    def hit(self, obj):
        if obj.get_name() == "Elites":
            if obj.hitbox.colliderect(self.hitbox):
                if self.timer_key_trigger(8, key="capture"):
                    self.capture_counter += 1
                if self.captured:
                    if self.zone_reset:
                        self.zone_reset = False
                        for obj in [e for e in data.ENEMY_DATA if e.get_name() == "Elites"]:
                            if obj.checkpoints[0] == self.loc:
                                obj.angles = angles_360(obj.speed)
                                if len(data.EVENTS.z_def_active_zones) == 0:
                                    data.EVENTS.z_def_active_zones = [
                                        z.loc for z in data.PHENOMENON_DATA if not z.captured and z.__class__ == self.__class__
                                    ]
                                try:
                                    obj.checkpoints = {
                                        0: data.EVENTS.z_def_active_zones.pop(
                                            random.randint(0, len(data.EVENTS.z_def_active_zones) - 1))
                                    }
                                    obj.skills_lst.append(obj.skill_zone_capture)
                                except (IndexError, ValueError):
                                    pass

    def script(self):
        if self.capture_counter >= 100:
            self.gfx_idx = 17
            self.captured = True

    def destroy(self):
        return self.kill

    def get_name(self):
        return self.__class__.__name__

    def tick(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        self.script()
        win.blit(Phenomenon.phenom_sprites[self.gfx_idx], self.hitbox.topleft)

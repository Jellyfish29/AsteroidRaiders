import pygame
import random

from astraid_funcs import *
from init import *
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

    def move(self):
        self.hitbox.move_ip(0, self.speed)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
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

    def gfx_draw(self):
        animation_ticker = self.timer_animation_ticker(10)
        if animation_ticker < 5:
            win.blit(Phenomenon.phenom_sprites[self.gfx_idx[0]], (self.hitbox.center[0] + self.gfx_hook[0], self.hitbox.center[1] + self.gfx_hook[1]))
        else:
            win.blit(Phenomenon.phenom_sprites[self.gfx_idx[1]], (self.hitbox.center[0] + self.gfx_hook[0], self.hitbox.center[1] + self.gfx_hook[1]))

    def destroy(self):
        return self.kill

    def tick(self):
        self.move()
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

        if not any((data.LEVELS.boss_fight, data.LEVELS.after_boss)):
            if data.LEVELS.level not in [i - 1 for i in range(5, 41, 5)]:
                if timer.trigger(Phenomenon.spawn_time):
                    if len(data.PHENOMENON_DATA) < Phenomenon.amount:
                        data.PHENOMENON_DATA.append(random.choice(cls.phenomenon_spawn_table)())
# Anti_gravity_well(),Planet(), Gravity_well(), Nebulae_fire_rate_plus(), Repair_station(), Nabulae_aoe_damage()


data.PHENOM = Phenomenon


class Wormhole(Phenomenon):

    trigger = False

    def __init__(self):
        super().__init__(1.5, (200, 200), (0, 0), (-150, -150))

    def player_collision(self):
        if self.hitbox.colliderect(data.PLAYER.hitbox):
            data.ENEMY_DATA.clear()
            data.PHENOMENON_DATA.clear()
            data.ENEMY_PROJECTILE_DATA.clear()
            data.PLAYER_PROJECTILE_DATA.clear()
            data.LEVELS.elite_fight = True
            self.kill = True
            data.PLAYER.hitbox.center = (winwidth / 2, 900)

    def hit(self, obj):
        if self.hitbox.colliderect(obj.hitbox):
            obj.kill = True

    @classmethod
    def spawn(cls):
        if not any((data.LEVELS.boss_fight, data.LEVELS.after_boss)):
            if Wormhole.trigger:
                data.PHENOMENON_DATA.append(Wormhole())
                Wormhole.trigger = False


class Gravity_well(Phenomenon):

    def __init__(self, speed=1, size=(500, 500), gfx_idx=(1, 1), gfx_hook=(-300, -300), decay=None, location=None, flag="phenom"):
        super().__init__(speed, size, gfx_idx, gfx_hook, flag=flag, decay=decay)
        self.new_d = directions(2)
        self.new_a = angles_360(2)
        self.objs = {}

        if location is not None:
            self.hitbox.center = location

    def hit(self, obj):
        if not issubclass(obj.__class__, Phenomenon):
            if self.hitbox.colliderect(obj.hitbox):
                if obj not in self.objs:
                    self.objs.update({obj: obj.angles})
                if isinstance(obj, type):
                    obj.angles = self.new_d
                else:
                    obj.angles = self.new_a
        for obj, speed in list(self.objs.items()):
            if not self.hitbox.colliderect(obj.hitbox):
                obj.angles = speed
                del self.objs[obj]


class Black_hole(Phenomenon):

    def __init__(self, speed=0, size=(300, 300), gfx_idx=(0, 0), gfx_hook=(-150, -150), decay=300, location=None, flag="phenom", damage=1):
        super().__init__(speed, size, gfx_idx, gfx_hook, flag=flag, decay=decay)
        # self.new_d = directions(2)
        self.new_a = angles_360(6)
        self.zero_a = angles_360(0)
        self.damage = damage
        self.objs = {}
        if location is not None:
            self.hitbox.center = location

    def hit(self, obj):
        if not issubclass(obj.__class__, Phenomenon):
            if self.hitbox.colliderect(obj.hitbox):
                if obj not in self.objs:
                    self.objs.update({obj: obj.angles})
                if isinstance(obj, type):
                    pass
                else:
                    obj.angles = self.new_a
                    obj.direction = degrees(self.hitbox.center[0], obj.hitbox.center[0], self.hitbox.center[1], obj.hitbox.center[1])
                if abs(obj.hitbox.center[0] - self.hitbox.center[0]) < 5 or abs(obj.hitbox.center[1] - self.hitbox.center[1]) < 5:
                    try:
                        obj.take_damage(self.damage, staggered=True)
                    except AttributeError:
                        obj.kill = True
                    obj.angles = self.zero_a

        for obj, speed in list(self.objs.items()):
            if not self.hitbox.colliderect(obj.hitbox):
                obj.angles = speed
                del self.objs[obj]

    def destroy(self):
        if self.kill:
            for obj, speed in list(self.objs.items()):
                obj.angles = speed
                del self.objs[obj]
            return True


class Repair_station(Phenomenon):

    def __init__(self):
        super().__init__(1, (200, 200), (3, 4), (-125, -125))

    def player_collision(self):
        if self.hitbox.colliderect(data.PLAYER.hitbox):
            if data.PLAYER.health < data.PLAYER.max_health:
                if self.timer_trigger(180):
                    data.PLAYER.health += 1
                    pygame.draw.rect(win, (0, 255, 0), pygame.Rect(0, 0, winwidth, winheight))


class Nebulae_fire_rate_plus(Phenomenon):

    def __init__(self):
        super().__init__(1, (300, 300), (5, 5), (-180, -180))
        self.move_trigger = False

    def move(self):
        self.hitbox.move_ip(0, self.speed)
        if not self.move_trigger:
            if self.hitbox.center[1] > winheight / 2:
                self.speed = 0
                if self.timer_trigger(1200):
                    self.move_trigger = True
                    self.speed = 1

    def player_collision(self):
        if self.hitbox.colliderect(data.PLAYER.hitbox):
            data.TURRET.fire_rate = data.TURRET.normal_fire_rate - 15
        else:
            data.TURRET.fire_rate = data.TURRET.normal_fire_rate


class Planet(Phenomenon):

    def __init__(self):
        super().__init__(1, (250, 250), (2, 2), (-160, -160))

    def player_collision(self):
        if self.hitbox.colliderect(data.PLAYER.hitbox):
            data.PLAYER.take_damage(0.1)

    def hit(self, obj):
        if self.hitbox.colliderect(obj.hitbox):
            if obj.flag == "boss" or obj.flag == "elite":
                if self.hitbox.center[0] < winwidth / 2:
                    new_cp = (self.hitbox.center[0] + 300, winheight / 2)
                else:
                    new_cp = (self.hitbox.center[0] - 300, winheight / 2)
                if new_cp not in obj.checkpoints:
                    obj.move_pattern.append(len(obj.checkpoints) + 1)
                    obj.checkpoints.update({len(obj.checkpoints) + 1: new_cp})
                obj.cp_ticker = len(obj.checkpoints)

            else:
                try:
                    obj.gfx_hit()
                except AttributeError:
                    pass
                obj.kill = True


class Nabulae_aoe_damage(Phenomenon):

    def __init__(self):
        super().__init__(1, (300, 300), (6, 6), (-180, -180))

    def player_collision(self):
        if self.hitbox.colliderect(data.PLAYER.hitbox):
            if self.timer_trigger_1(60):
                data.PLAYER.health -= 1
                pygame.draw.rect(win, (0, 0, 255), pygame.Rect(0, 0, winwidth, winheight))

    def hit(self, obj):
        if self.hitbox.colliderect(obj.hitbox):
            try:
                obj.take_damage(0.015)
            except AttributeError:
                obj.kill = True


class Anti_gravity_well(Phenomenon):

    def __init__(self):
        super().__init__(1, (500, 500), (7, 7), (-300, -300))
        self.new_d = directions(40)
        self.new_a = angles_360(60)
        self.objs = {}

    def hit(self, obj):
        if not issubclass(obj.__class__, Phenomenon):
            if self.hitbox.colliderect(obj.hitbox):
                if obj not in self.objs:
                    self.objs.update({obj: obj.angles})
                if isinstance(obj, type):
                    obj.angles = self.new_d
                else:
                    obj.angles = self.new_a
        for obj, speed in list(self.objs.items()):
            if not self.hitbox.colliderect(obj.hitbox):
                obj.angles = speed
                del self.objs[obj]

import pygame

from init import *
from astraid_funcs import *
import astraid_data as data
from Gfx import Gfx


class Projectile:

    projectile_sprites = get_images("projectile")

    def __init__(self, speed=0, size=(0, 0), start_point=(0, 0), damage=0, flag="player", gfx_idx=0, angle=0, angle_variation=0, target=None, piercing=False, gfx_hit_effect="shot_hit", hit_effect=None, homing=False):
        self.speed = speed
        self.size = size
        self.start_point = start_point
        self.target = target
        self.flag = flag
        self.damage = damage
        self.gfx_idx = gfx_idx
        self.piercing = piercing
        self.angle_variation = angle_variation
        self.gfx_hit_effect = gfx_hit_effect
        self.hit_effect = hit_effect
        self.kill = False
        self.hitbox = pygame.Rect(start_point[0], start_point[1], size[0], size[1])
        self.angles = angles_360(speed)
        self.orig_angles = self.angles
        self.tc = Time_controler()
        self.target = target
        self.start_point = start_point
        self.homing = homing

        if target is None:
            self.angle = angle
        else:
            self.angle = degrees(target[0], start_point[0], target[1], start_point[1])
        self.has_been_called = False

    def move(self):
        self.hitbox.move_ip(self.angles[self.get_angle()])

    def get_angle(self):
        angle = self.angle + self.angle_variation
        if angle > 359:
            angle -= 359
        elif angle < 0:
            angle += 359
        if self.homing:
            self.angle = degrees(self.target[0], self.hitbox.center[0], self.target[1], self.hitbox.center[1])
        return angle

    def hit(self, obj):
        if self.hitbox.colliderect(obj.hitbox):
            if self.damage > 0:
                self.gfx_hit()  # Gfx.shot_hit_effect(self.hitbox, effect=self.gfx_hit_effect)
                if self.hit_effect is not None:
                    self.hit_effect.set_location(self.hitbox.center)
                    data.PLAYER_PROJECTILE_DATA.append(self.hit_effect)
                return True

    def gfx_draw(self):
        # pygame.draw.rect(win, (0, 255, 255), self.hitbox)
        win.blit(Projectile.projectile_sprites[self.gfx_idx], (self.hitbox.topleft[0] - 8, self.hitbox.topleft[1] - 8))

    def gfx_hit(self):
        Gfx.shot_hit_effect(self.hitbox, effect=self.gfx_hit_effect)

    def out_of_bounds(self):
        return rect_not_on_sreen(self.hitbox)

    def hit_effect(self):
        Gfx.shot_hit_effect(self.hitbox, effect=self.gfx_hit_effect)

    def apply_damage(self):
        return self.damage

    def destroy(self):
        return self.kill

    def tick(self):
        self.move()
        self.gfx_draw()
        if self.out_of_bounds():
            self.kill = True


class Impactor(Projectile):

    def __init__(self, speed=0, size=(0, 0), start_point=(0, 0), damage=0, flag="", gfx_idx=3, target=None, impact_effect=None, trigger_dist=10):
        super().__init__(speed=speed, size=size, start_point=start_point, damage=damage, flag=flag, gfx_idx=gfx_idx, target=target, homing=True)
        self.trigger_dist = trigger_dist
        self.impact_effect = impact_effect

    def move(self):
        self.hitbox.move_ip(self.angles[self.get_angle()])
        if self.get_distance():
            self.impact_effect()
            self.kill = True

    def gfx_draw(self):
        win.blit(gfx_rotate(Projectile.projectile_sprites[self.gfx_idx], degrees(self.target[1], self.hitbox.center[1], self.target[0], self.hitbox.center[0])), (self.hitbox.topleft[0] - 5, self.hitbox.topleft[1] - 5))

    def get_distance(self):
        if abs(self.target[0] - self.hitbox.topleft[0]) < self.trigger_dist or abs(self.target[1] - self.hitbox.topleft[1]) < self.trigger_dist:
            return True
        else:
            return False


class Missile(Projectile):

    def __init__(self, speed=0, size=(0, 0), start_point=(0, 0), target=None, damage=0, flag="", gfx_idx=3, aquisition_delay=0, enemy_missile=False):
        super().__init__(speed=speed, size=size, start_point=start_point, damage=damage, flag=flag, gfx_idx=gfx_idx, target=target)
        self.aquisition_delay = aquisition_delay
        self.movement_checker = 0  # check if target is stanionary --> means target is already destroyed
        self.enemy_missile = enemy_missile

    def move(self):
        if not self.enemy_missile:
            if self.movement_checker == self.target.center:
                try:
                    self.target = data.ENEMY_DATA[0].hitbox
                except IndexError:
                    self.kill = True
        self.movement_checker = self.target.center
        if self.tc.trigger_1(self.aquisition_delay):
            if abs(self.hitbox.center[0] - self.target.center[0]) > 10 or abs(self.hitbox.center[1] - self.target.center[1]) > 10:
                self.angle = degrees(self.target.center[0], self.hitbox.center[0], self.target.center[1], self.hitbox.center[1])
        self.hitbox.move_ip(self.angles[self.angle])
        if self.tc.delay(True, limit=480):
            Gfx.shot_hit_effect(self.hitbox, effect=self.gfx_hit_effect)
            self.kill = True

    def gfx_draw(self):
        win.blit(gfx_rotate(Projectile.projectile_sprites[self.gfx_idx], degrees(self.target.center[1], self.hitbox.center[1], self.target.center[0], self.hitbox.center[0])), (self.hitbox.topleft[0] - 5, self.hitbox.topleft[1] - 5))

    def tick(self):
        self.move()
        self.gfx_draw()
        data.TURRET.point_defence(self.hitbox)
        if self.out_of_bounds():
            self.kill = True


class Mine(Projectile):

    def __init__(self, speed=0, start_point=(0, 0), damage=0, flag="", decay=False):
        super().__init__(speed=speed, size=(20, 20), start_point=start_point, damage=damage, flag=flag)
        self.envelope = pygame.Rect(self.hitbox.center[0] - 175, self.hitbox.center[1] - 175, 350, 350)
        self.decay = decay

    def move(self):
        pass

    def hit(self, obj):
        if self.decay:
            if self.tc.trigger_1(600):
                self.kill = True
        if self.tc.delay(True, 240):  # Fuse Delay
            if self.envelope.colliderect(obj.hitbox):
                self.angle = degrees(obj.hitbox.center[0], self.hitbox.center[0], obj.hitbox.center[1], self.hitbox.center[1])
                self.hitbox.move_ip(self.angles[self.angle])
                self.envelope.move_ip(self.angles[self.angle])
            if self.hitbox.colliderect(obj.hitbox):
                Gfx.shot_hit_effect(self.hitbox, effect=self.gfx_hit_effect)
                return True

    def gfx_draw(self):
        win.blit(Projectile.projectile_sprites[12], (self.hitbox.topleft[0] - 5, self.hitbox.topleft[1] - 5))
        win.blit(Projectile.projectile_sprites[13], (self.envelope.topleft[0] - 27, self.envelope.topleft[1] - 27))

    def tick(self):
        self.move()
        self.gfx_draw()
        data.TURRET.point_defence(self.hitbox)
        if self.out_of_bounds():
            self.kill = True


class Explosion(Projectile):
    def __init__(self, location=(0, 0), explo_size=0, damage=0, explo_delay=0):
        super().__init__(damage=damage, flag="explo", piercing=True)
        self.hitbox = pygame.Rect(location[0], location[1], 1, 1)
        self.explo_size = explo_size
        self.explo_delay = explo_delay
        self.piercing = True

    def set_location(self, l):
        self.hitbox.center = l

    def move(self):
        if self.tc.delay(True, self.explo_delay):
            self.hitbox.inflate_ip(30, 30)
            if abs(self.hitbox.topleft[0] - self.hitbox.center[0]) > self.explo_size:
                self.kill = True

    def gfx_draw(self):
        pygame.draw.rect(win, (255, 0, 0), self.hitbox)


class Wave(Projectile):

    def __init__(self, speed=0, size=(0, 0), start_point=(0, 0), damage=0, flag="player", gfx_idx=0, target=None, curve_size=0.1, fixed_angle=None, variation=True):
        super().__init__(speed, size, start_point, damage, flag, gfx_idx, target=target)
        self.curv_ticker = 0
        self.angle_variation = 0
        self.curve_size = curve_size
        self.fixed_angle = fixed_angle
        self.variation = variation

    def move(self):
        self.curv_ticker += self.get_curve_size()
        if self.fixed_angle is not None:
            self.hitbox.move_ip(self.angles[get_sin(self.curv_ticker, self.fixed_angle)])
        else:
            self.hitbox.move_ip(self.angles[get_sin(self.curv_ticker, self.get_angle())])

    def get_curve_size(self):
        if self.variation:
            self.curve_size -= 0.01
        return self.curve_size

    # def gfx_draw(self):
    #     win.blit(gfx_rotate(Projectile.projectile_sprites[self.gfx_idx], degrees(self.target[1], self.hitbox.center[1], self.target[0], self.hitbox.center[0])), (self.hitbox.center[0] - 5, self.hitbox.center[1] - 5))

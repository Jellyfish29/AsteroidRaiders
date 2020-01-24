import pygame

from astraid_funcs import *
from astraid_data import *

from Gfx import Gfx


class Projectile:

    def __init__(self, speed, size, start_point, target, damage, typ):
        self.speed = speed
        self.size = size
        self.start_point = start_point
        self.target = target
        self.typ = typ
        self.damage = damage
        self.hitbox = pygame.Rect(start_point[0], start_point[1], size[0], size[1])
        self.angle = degrees(target[0], start_point[0], target[1], start_point[1])
        self.angles = angles_360(speed)
        self.tc = Time_controler()
        self.hit_effect = "shot_hit"

    def move(self):
        self.hitbox.move_ip(self.angles[self.angle])

    def hit(self, obj):
        if self.hitbox.colliderect(obj):
            Gfx.shot_hit_effect(self.hitbox, effect=self.hit_effect)
            return True

    def apply_damage(self):
        return self.damage


class Missile(Projectile):

    def __init__(self, speed, size, start_point, target, damage, typ, aquisition_delay=0):
        super().__init__(speed, size, start_point, target, damage, typ)
        self.aquisition_delay = aquisition_delay

    def follow(self):
        if self.tc.trigger_1(self.aquisition_delay):
            if abs(self.hitbox.center[0] - self.target.hitbox.center[0]) > 10 or abs(self.hitbox.center[1] - self.target.hitbox.center[1]) > 10:
                self.angle = degrees(self.target.hitbox.center[0], self.hitbox.center[0], self.target.hitbox.center[1], self.hitbox.center[1])

import pygame

from init import *
from astraid_funcs import *
import astraid_data as data
from Gfx import Gfx, Background


class Projectile(Timer):

    projectile_sprites = get_images("projectile")

    def __init__(
            self,
            speed=0,
            size=(0, 0),
            start_point=(0, 0),
            damage=0,
            flag="player",
            gfx_idx=0,
            angle=0,
            angle_variation=0,
            target=None,
            piercing=False,
            gfx_hit_effect="shot_hit",
            hit_effect=None,
            homing=False,
            spez_gfx=None,
            fuse_delay=None,
            decay=None
    ):
        self.speed = speed
        self.size = size
        self.start_point = start_point
        self.start_point = (start_point[0], start_point[1])
        self.damage = damage
        self.flag = flag
        self.gfx_idx = gfx_idx
        if target is None:
            self.angle = angle
        else:
            self.angle = degrees(target[0], start_point[0], target[1], start_point[1])
        self.angle_variation = angle_variation
        self.target = target
        self.piercing = piercing
        self.gfx_hit_effect = gfx_hit_effect
        self.hit_effect = hit_effect
        self.homing = homing
        self.spez_gfx = spez_gfx
        self.fuse_delay = fuse_delay
        self.decay = decay

        Timer.__init__(self)
        self.run_limiter = Run_limiter()
        self.hitbox = pygame.Rect(start_point[0], start_point[1], size[0], size[1])
        self.angles = angles_360(speed)
        self.offset_angles = angles_360(10000)
        self.run_spez_gfx = run_once(spez_gfx)
        self.kill = False
        self.hit_event = False
        if all([data.GROUND, not isinstance(self, Explosion),
                not isinstance(self, Impactor), not isinstance(self, Missile),
                self.flag != "secondary"]):
            self.target_rect = pygame.Rect(0, 0, 50, 50)
            self.target_rect.center = self.target

    def move(self):
        self.hitbox.move_ip(self.angles[self.get_angle()])

    def get_angle(self):
        angle = angle_switcher(self.angle + self.angle_variation)
        if self.homing:
            angle = degrees(
                self.target[0],
                self.hitbox.center[0],
                self.target[1],
                self.hitbox.center[1]
            )
            return angle
        return angle

    def hit(self, obj):
        if self.fuse_delay is not None:
            delay = self.fuse_delay
        else:
            delay = 0
        if self.timer_delay(limit=delay):
            if self.hitbox.colliderect(obj.hitbox):
                if all([self.flag != "secondary",
                        not self.hit_event,
                        self.flag == "player"]):
                    self.gfx_hit()
                    if not isinstance(obj, type):
                        data.TURRET.hit_locations.append(self)
                    self.hit_event = True
                if self.hit_effect is not None:
                    if not issubclass(obj.__class__, Projectile):
                        self.hit_effect(self.hitbox.center, obj)
                if self.damage > 0:
                    return True

    def gfx_hit(self):
        Gfx.create_effect(
            "shot_hit", 4, anchor=self.hitbox, follow=True, x=-50, y=-50)

    def gfx_draw(self):
        # pygame.draw.rect(win, (0, 255, 255), self.hitbox)
        if self.spez_gfx is not None:
            self.run_spez_gfx(self.hitbox)
        if self.run_limiter.run_block_once():
            self.target = self.hitbox.move(self.offset_angles[self.get_angle()]).center
        gfx_angle = degrees(
            self.target[1],
            self.start_point[1],
            self.target[0],
            self.start_point[0]
        )

        win.blit(rot_center(
            Projectile.projectile_sprites[self.gfx_idx], gfx_angle),
            (self.hitbox.topleft[0] - 50, self.hitbox.topleft[1] - 50)
        )

    def ground_behavior(self):
        try:
            if self.hitbox.colliderect(self.target_rect):
                self.kill = True
                data.PLAYER_PROJECTILE_DATA.append(Explosion(
                    location=self.hitbox.center,
                    explo_size=70,
                    damage=0.5,
                    explosion_effect=lambda loc: Gfx.create_effect(
                        "explosion_4", 2, (loc[0] - 80, loc[1] - 80), explo=True),
                    explo_speed=(60, 60)
                ))
        except AttributeError:
            pass

    def out_of_bounds(self):
        return rect_not_on_sreen(self.hitbox)

    def apply_damage(self):
        return self.damage

    def destroy(self):
        return self.kill

    def get_name(self):
        return self.__class__.__name__

    def get_bases_names(self):
        return [base.__name__ for base in self.__class__.__bases__]

    def tick(self):
        if data.GROUND:
            self.ground_behavior()
        if self.decay is not None:
            if self.timer_trigger(self.decay):
                self.kill = True
        self.move()
        self.gfx_draw()
        if self.out_of_bounds():
            self.kill = True
        self.timer_tick()


class Laser_designator(Projectile, Run_limiter):

    def __init__(
            self,
            start_point=(0, 0),
            gfx_idx=2,
            target=None,
            distance=0,
            ttl=1,
            tracking=False
    ):
        super().__init__(
            speed=0,
            size=(5, 5),
            start_point=start_point,
            damage=0,
            flag="secondary",
            gfx_idx=gfx_idx,
            target=target,
            homing=True)
        Run_limiter.__init__(self)
        self.distance = distance
        self.ttl = ttl

    def move(self):
        if self.run_block_once():
            self.hitbox.move_ip(angles_360(self.distance)[self.get_angle()])
        if self.timer_trigger(self.ttl):
            self.kill = True

    # def gfx_draw(self):
    #     win.blit(Projectile.projectile_sprites[self.gfx_idx],
    #              (self.hitbox.topleft[0] - 50, self.hitbox.topleft[1] - 50))


class Impactor(Projectile):

    def __init__(
            self,
            speed=0,
            size=(0, 0),
            start_point=(0, 0),
            damage=0,
            flag="",
            gfx_idx=4,
            target=None,
            impact_effect=None,
            trigger_dist=10
    ):
        super().__init__(
            speed=speed,
            size=size,
            start_point=start_point,
            damage=damage,
            flag=flag,
            gfx_idx=gfx_idx,
            target=target,
            homing=True)
        self.trigger_dist = trigger_dist
        self.impact_effect = impact_effect

    def move(self):
        self.hitbox.move_ip(self.angles[self.get_angle()])
        if self.get_distance():
            self.impact_effect()
            self.kill = True

    def gfx_draw(self):
        win.blit(gfx_rotate(Projectile.projectile_sprites[self.gfx_idx], degrees(
            self.target[1],
            self.hitbox.center[1],
            self.target[0],
            self.hitbox.center[0]
        )),
            (self.hitbox.topleft[0] - 50, self.hitbox.topleft[1] - 50)
        )

    def get_distance(self):
        if abs(
                self.target[0] - self.hitbox.topleft[0]) < self.trigger_dist or abs(
                self.target[1] - self.hitbox.topleft[1]) < self.trigger_dist:
            return True
        else:
            return False


class Dart(Projectile):

    def __init__(
            self,
            start_point=(0, 0),
            damage=1,
            gfx_idx=(9, 8),
            target=None,
            aquisition_delay=60
    ):
        super().__init__(
            speed=80,
            size=(5, 5),
            start_point=start_point,
            damage=damage,
            flag="dart",
            gfx_idx=gfx_idx,
            target=target
        )
        self.aquisition_delay = aquisition_delay
        self.angle = None
        self.gfx_angle = None
        self.aiming = True

    def move(self):
        if self.timer_delay(self.aquisition_delay):
            self.aiming = False
            if self.angle is None:
                self.angle = degrees(
                    self.target[0],
                    self.hitbox.center[0],
                    self.target[1],
                    self.hitbox.center[1]
                )
                self.gfx_angle = degrees(
                    self.target[1],
                    self.hitbox.center[1],
                    self.target[0],
                    self.hitbox.center[0]
                )
            if self.timer_delay(10):
                self.hitbox.move_ip(self.angles[self.angle])

    def gfx_draw(self):
        if self.aiming:
            win.blit(gfx_rotate(
                Projectile.projectile_sprites[self.gfx_idx[0]],
                degrees(
                    self.target[1],
                    self.hitbox.center[1],
                    self.target[0],
                    self.hitbox.center[0]
                )
            ),
                (self.hitbox.topleft[0] - 5, self.hitbox.topleft[1] - 5))
        else:
            win.blit(gfx_rotate(
                Projectile.projectile_sprites[self.gfx_idx[1]],
                self.gfx_angle
            ),
                (self.hitbox.topleft[0] - 5, self.hitbox.topleft[1] - 5))


class Missile(Projectile):

    def __init__(
            self,
            speed=0,
            size=(0, 0),
            start_point=(0, 0),
            target=None,
            damage=0,
            flag="",
            gfx_idx=1,
            aquisition_delay=0,
            enemy_missile=False
    ):
        super().__init__(
            speed=speed,
            size=size,
            start_point=start_point,
            damage=damage,
            flag=flag,
            gfx_idx=gfx_idx,
            target=target
        )
        self.aquisition_delay = aquisition_delay
        self.movement_checker = 0
        self.enemy_missile = enemy_missile
        self.hit_effect = lambda loc, _: Gfx.create_effect(
            "explosion_4", 1, (loc[0] - 90, loc[1] - 90), explo=True)

    def move(self):
        if not self.enemy_missile:
            if self.movement_checker == self.target.center:
                try:
                    self.target = [
                        e for e in data.ENEMY_DATA if not rect_not_on_sreen(e.hitbox, strict=True)][0].hitbox
                except IndexError:
                    self.kill = True
        self.movement_checker = self.target.center
        if self.timer_trigger(self.aquisition_delay):
            if any([abs(self.hitbox.center[0] - self.target.center[0]) > 10,
                    abs(self.hitbox.center[1] - self.target.center[1]) > 10]):
                self.angle = degrees(
                    self.target.center[0],
                    self.hitbox.center[0],
                    self.target.center[1],
                    self.hitbox.center[1]
                )
        self.hitbox.move_ip(self.angles[self.angle])
        if self.timer_delay(limit=480):

            self.kill = True

    def gfx_draw(self):
        win.blit(gfx_rotate(
            Projectile.projectile_sprites[self.gfx_idx],
            degrees(
                self.target.center[1],
                self.hitbox.center[1],
                self.target.center[0],
                self.hitbox.center[0]
            )
        ),
            (self.hitbox.topleft[0] - 50, self.hitbox.topleft[1] - 50))

    def tick(self):
        self.move()
        self.gfx_draw()
        data.TURRET.point_defence(self.hitbox)
        if self.out_of_bounds():
            self.kill = True
        self.timer_tick()


class Mine(Projectile):

    def __init__(
            self,
            speed=0,
            start_point=(0, 0),
            damage=0,
            flag="",
            decay=False,
            oob_check=True,
            moving=False,
            fuse_delay=180
    ):
        super().__init__(
            speed=speed,
            size=(20, 20),
            start_point=start_point,
            damage=damage,
            flag=flag
        )
        self.envelope = pygame.Rect(
            self.hitbox.center[0] - 175, self.hitbox.center[1] - 175, 350, 350
        )
        self.decay = decay
        self.out_of_bounds_check = oob_check
        self.moving = moving
        self.fuse_delay = fuse_delay
        self.draw_envelope = False
        self.move_angles = angles_360(4)
        self.angle = random.randint(0, 359)
        self.direction_interval = random.randint(40, 100)

    def move(self):
        if self.moving:
            if Background.bg_move:
                self.hitbox.move_ip(0, Background.scroll_speed)
                self.envelope.move_ip(0, Background.scroll_speed)
            else:
                if self.hitbox.center[0] < 0:
                    self.angle = 0
                elif self.hitbox.center[0] > winwidth:
                    self.angle = 180
                elif self.hitbox.center[1] < -50:
                    self.angle = 90
                elif self.hitbox.center[1] > winheight:
                    self.angle = 270
            if self.timer_trigger(self.direction_interval):
                self.angle = random.randint(0, 359)
            self.hitbox.move_ip(self.move_angles[self.angle])
            self.envelope.move_ip(self.move_angles[self.angle])

    def hit(self, obj):
        if self.decay:
            if self.timer_trigger(500):
                self.kill = True
        if self.timer_delay(limit=self.fuse_delay):  # Fuse Delay
            self.draw_envelope = True
            # if self.envelope.colliderect(obj.hitbox):
            if self.envelope.collidepoint(obj.hitbox.center):
                self.moving = False
                self.angle = degrees(
                    obj.hitbox.center[0],
                    self.hitbox.center[0],
                    obj.hitbox.center[1],
                    self.hitbox.center[1]
                )
                self.hitbox.move_ip(self.angles[self.angle])
                self.envelope.move_ip(self.angles[self.angle])
                if self.hitbox.collidepoint(obj.hitbox.center):

                    return True

    def gfx_draw(self):
        win.blit(
            Projectile.projectile_sprites[5],
            (self.hitbox.topleft[0] - 5, self.hitbox.topleft[1] - 5)
        )
        if self.draw_envelope:
            win.blit(
                Projectile.projectile_sprites[6],
                (self.envelope.topleft[0] - 27, self.envelope.topleft[1] - 27)
            )

    def tick(self):
        self.move()
        self.gfx_draw()
        data.TURRET.point_defence(self.hitbox)
        if self.out_of_bounds_check:
            if self.out_of_bounds():
                self.kill = True
        self.timer_tick()


class Explosion(Projectile):

    def __init__(
            self,
            location=(0, 0),
            explo_size=0,
            damage=0,
            explo_delay=0,
            explosion_effect=None,
            explo_speed=(30, 30),
            gfx_idx=None
    ):
        super().__init__(damage=damage, flag="explo", piercing=True)
        self.hitbox = pygame.Rect(location[0], location[1], 1, 1)
        self.explo_size = explo_size
        self.explo_delay = explo_delay
        self.piercing = True
        self.explosion_effect = run_once(explosion_effect)
        self.explo_speed = explo_speed
        self.gfx_idx = gfx_idx
        self.flag = "secondary"

    def set_location(self, l):
        self.hitbox.center = l

    def move(self):
        if self.timer_delay(limit=self.explo_delay):
            try:
                self.run_explosion_effect()
            except TypeError:
                pass
            self.hitbox.inflate_ip(self.explo_speed)
            if abs(self.hitbox.topleft[0] - self.hitbox.center[0]) > self.explo_size:
                self.kill = True
        else:
            if self.gfx_idx is not None:
                win.blit(Projectile.projectile_sprites[self.gfx_idx],
                         (self.hitbox.center[0] - 50, self.hitbox.center[1] - 50))

    def run_explosion_effect(self):
        self.explosion_effect(self.hitbox.topleft)

    def gfx_draw(self):
        pass
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)


class Wave(Projectile):

    def __init__(
        self,
        speed=0,
        size=(0, 0),
        start_point=(0, 0),
        damage=0,
        flag="player",
        gfx_idx=0,
        target=None,
        curve_size=0.1,
        fixed_angle=None,
        variation=True
    ):
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

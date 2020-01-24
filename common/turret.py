import pygame
# from pygame.locals import *
import random

from init import *
from astraid_funcs import *
import astraid_data as data
from Gfx import Gfx
from projectiles import Projectile, Missile, Impactor, Explosion, Wave
from phenomenon import Black_hole, Gravity_well


class Turret:

    # normal shot vlaues
    projectile_size = (6, 6)
    projectile_speed = 20
    firing = False
    direction = None
    fire_rate = 35
    raw_fire_rate = fire_rate
    fire_rate_limit = 10
    shot_count = 0
    gfx_idx = 0
    # Overdrive
    overdrive_count = 0
    # ammunition = normal_fire_rate[1]
    fire_limiter = 0
    # super shot values
    super_shot_ammo = 45
    super_shot_limiter = 0
    # star shot values
    star_shot_limiter = 0
    star_shot_ammo = 25
    star_shot_tubes = 12
    # pd values
    pd_ticker = 0
    # Gfx setup
    projectile_sprites = get_images("projectile")
    explosion_sprites = get_images("explosions")

    @classmethod
    def fire(cls, fire):
        cls.firing = fire

    @classmethod
    def shots(cls):
        if cls.firing:
            cls.normal_fire()
            cls.star_fire()
            cls.rapid_fire()
            # cls.test_sin()
            # cls.he_rounds()

    @classmethod
    def bombs(cls):
        cls.nuke_fire()
        cls.gravity_bomb()
        cls.black_hole_bomb()

    @classmethod
    @timer
    def test_sin(cls, timer):
        if timer.trigger_1():
            data.PLAYER_PROJECTILE_DATA.append(Wave(
                speed=10,
                size=(4, 4),
                start_point=data.PLAYER.hitbox.center,
                damage=1,
                gfx_idx=7,
                target=pygame.mouse.get_pos(),
                curve_size=1.2
            ))

    @classmethod
    def nuke_fire(cls):
        if "nuke" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="nuke").active:
                # draw aim ding
                if data.ITEMS.get_item(flag="nuke").engage:
                    pos = pygame.mouse.get_pos()
                    data.PLAYER_PROJECTILE_DATA.append(Impactor(
                        speed=4,
                        size=(4, 4),
                        start_point=data.PLAYER.hitbox.center,
                        damage=0,
                        gfx_idx=3,
                        target=pos,
                        impact_effect=lambda loc=pos: data.PLAYER_PROJECTILE_DATA.append(Explosion(
                            location=loc,
                            explo_size=400,
                            damage=1.5 + data.PLAYER.damage * 0.5))
                    ))
                    data.ITEMS.get_item(flag="nuke").engage = False
                    data.ITEMS.get_item(flag="nuke").end_active()

    @classmethod
    def gravity_bomb(cls):
        if "gravity_bomb" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="gravity_bomb").active:
                # aim effect
                if data.ITEMS.get_item(flag="gravity_bomb").engage:
                    pos = pygame.mouse.get_pos()
                    data.PLAYER_PROJECTILE_DATA.append(Impactor(
                        speed=12,
                        size=(4, 4),
                        start_point=data.PLAYER.hitbox.center,
                        damage=0,
                        gfx_idx=3,
                        target=pos,
                        impact_effect=lambda loc=pos: data.PLAYER_PROJECTILE_DATA.append(Gravity_well(
                            speed=0,
                            size=(500, 500),
                            gfx_idx=(1, 1),
                            gfx_hook=(-300, -300),
                            decay=data.ITEMS.get_item(flag="gravity_bomb").active_time,
                            location=loc,
                            flag="player"))
                    ))
                    data.ITEMS.get_item(flag="gravity_bomb").engage = False
                    data.ITEMS.get_item(flag="gravity_bomb").end_active()

    @classmethod
    def black_hole_bomb(cls):
        if "black_hole_bomb" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="black_hole_bomb").active:
                # aim effect
                if data.ITEMS.get_item(flag="black_hole_bomb").engage:
                    pos = pygame.mouse.get_pos()
                    data.PLAYER_PROJECTILE_DATA.append(Impactor(
                        speed=12,
                        size=(4, 4),
                        start_point=data.PLAYER.hitbox.center,
                        damage=0,
                        gfx_idx=3,
                        target=pos,
                        impact_effect=lambda loc=pos: data.PLAYER_PROJECTILE_DATA.append(Black_hole(
                            speed=0,
                            size=(300, 300),
                            gfx_idx=(1, 1),
                            gfx_hook=(-300, -300),
                            decay=data.ITEMS.get_item(flag="black_hole_bomb").active_time,
                            location=loc,
                            flag="player"))
                    ))
                    data.ITEMS.get_item(flag="black_hole_bomb").engage = False
                    data.ITEMS.get_item(flag="black_hole_bomb").end_active()

    @classmethod
    @timer
    def point_defence(cls, enemy, timer):
        if "point_defence" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="point_defence").active:
                pd_envelope = pygame.Rect(data.PLAYER.hitbox.center[0] - 200, data.PLAYER.hitbox.center[1] - 200, 400, 400)
                # pygame.draw.rect(win, (255, 255, 0), pd_envelope)
                if pd_envelope.colliderect(enemy):
                    if timer.trigger_1(6):
                        data.PLAYER_PROJECTILE_DATA.append(Projectile(
                            speed=30,
                            size=(10, 10),
                            start_point=data.PLAYER.hitbox.center,
                            damage=1 + data.PLAYER.damage * 0.1,
                            flag="point_defence",
                            gfx_idx=10,
                            angle_variation=random.randint(-2, 2),
                            target=enemy
                        ))

    @classmethod
    def missile_aquisition(cls, enemy):
        if "missile" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="missile").active:
                m_pos = pygame.mouse.get_pos()
                aa_target_area = pygame.Rect(m_pos[0] - 100, m_pos[1] - 100, 200, 200)
                # pygame.draw.rect(win, (255, 255, 0), aa_target_area)
                if aa_target_area.colliderect(enemy.hitbox):
                    for x in [-18, 60]:
                        Gfx.create_effect("missilemuzzle", 3, data.PLAYER.hitbox, follow=True, x=x, y=8)
                    for location in [data.PLAYER.hitbox.topleft, data.PLAYER.hitbox.topright]:
                        data.PLAYER_PROJECTILE_DATA.append(Missile(
                            speed=15,
                            size=(5, 5),
                            start_point=location,
                            target=enemy.hitbox,
                            damage=data.PLAYER.damage * 3,
                            flag="missile"
                        ))
                    data.ITEMS.get_item(flag="missile").end_active()

    @classmethod
    def he_rounds(cls):
        if "he_rounds" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="he_rounds").active:
                Gfx.create_effect("shot_muzzle", 2, data.PLAYER.hitbox, follow=True, x=5, y=0)
                data.PLAYER_PROJECTILE_DATA.append(Projectile(
                    speed=cls.projectile_speed,
                    size=cls.projectile_size,
                    start_point=data.PLAYER.hitbox.center,
                    damage=data.PLAYER.damage,
                    gfx_idx=0,
                    target=pygame.mouse.get_pos(),
                    piercing=False,
                    hit_effect=Explosion(
                        explo_size=70,
                        damage=data.PLAYER.damage * 0.2)
                ))
                return True

    @classmethod
    def fan_shot(cls):
        if "fan_shot" in data.ITEMS.active_flag_lst:
            if cls.shot_count % data.ITEMS.get_item(flag="fan_shot").effect_strength == 0:
                for i in [-5, 0, 5]:
                    data.PLAYER_PROJECTILE_DATA.append(Projectile(
                        speed=cls.projectile_speed,
                        size=cls.projectile_size,
                        start_point=data.PLAYER.hitbox.center,
                        damage=data.PLAYER.damage,
                        gfx_idx=2,
                        angle_variation=i,
                        target=pygame.mouse.get_pos(),
                        hit_effect=cls.he_rounds()
                    ))
                return True
            else:
                return False

    @classmethod
    def hammer_shot(cls):
        if "hammer_shot" in data.ITEMS.active_flag_lst:
            if cls.shot_count % 5 == 0:
                data.PLAYER_PROJECTILE_DATA.append(Projectile(
                    speed=cls.projectile_speed,
                    size=cls.projectile_size,
                    start_point=data.PLAYER.hitbox.center,
                    damage=data.ITEMS.get_item(flag="hammer_shot").effect_strength,
                    gfx_idx=2,
                    target=pygame.mouse.get_pos(),
                    hit_explo=cls.he_rounds()
                ))
                return True
            else:
                return False

    @classmethod
    def overdrive(cls):
        if "overdrive" in data.ITEMS.active_flag_lst:
            if cls.overdrive_count < data.ITEMS.get_item(flag="overdrive").effect_strength:
                cls.overdrive_count += 1
                data.PLAYER.damage += 0.05
                cls.fire_rate -= 0.7

    @classmethod
    @timer
    def rapid_fire(cls, timer):
        if "rapid_fire" in data.ITEMS.active_flag_lst:
            rapid_fire = data.ITEMS.get_item(flag="rapid_fire")
            if rapid_fire.active:
                if timer.trigger_2(5):
                    Gfx.create_effect("shot_muzzle", 2, data.PLAYER.hitbox, follow=True, x=5, y=0)
                    cls.super_shot_limiter += 1
                    if cls.super_shot_limiter >= cls.super_shot_ammo:
                        cls.super_shot_limiter = 0
                        rapid_fire.active = False
                        rapid_fire.cooldown = True
                        del rapid_fire

                    data.PLAYER_PROJECTILE_DATA.append(Projectile(
                        speed=cls.projectile_speed,
                        size=cls.projectile_size,
                        start_point=data.PLAYER.hitbox.center,
                        damage=data.PLAYER.damage,
                        gfx_idx=1,
                        target=pygame.mouse.get_pos(),
                    ))

    @classmethod
    @timer
    def star_fire(cls, timer):
        if "star_fire" in data.ITEMS.active_flag_lst:
            star_fire = data.ITEMS.get_item(flag="star_fire")
            if star_fire.active:
                if timer.trigger_1(30):
                    cls.star_shot_limiter += 1
                    Gfx.create_effect("shot_muzzle", 2, data.PLAYER.hitbox, follow=True, x=5, y=0)
                    if cls.star_shot_limiter > cls.star_shot_ammo:
                        cls.star_shot_limiter = 0
                        star_fire.active = False
                        star_fire.cooldown = True
                        del star_fire

                    for angle in range(0, 360, int(360 / cls.star_shot_tubes)):
                        data.PLAYER_PROJECTILE_DATA.append(Projectile(
                            speed=cls.projectile_speed,
                            size=cls.projectile_size,
                            start_point=data.PLAYER.hitbox.center,
                            damage=data.PLAYER.damage,
                            gfx_idx=2,
                            angle=angle
                        ))

    @classmethod
    @timer
    def normal_fire(cls, timer):
        if timer.trigger_1(cls.fire_rate):
            cls.shot_count += 1

            dmg = data.PLAYER.damage
            piercing = False

            ### Special Ammo ###

            if "piercing_shot" in data.ITEMS.active_flag_lst:
                if data.ITEMS.get_item(flag="piercing_shot").active:
                    dmg = data.PLAYER.damage * data.ITEMS.get_item(flag="piercing_shot").effect_strength
                    piercing = True
            if cls.hammer_shot():
                return
            elif cls.fan_shot():
                return
            elif cls.he_rounds():
                return

            Gfx.create_effect("shot_muzzle", 2, data.PLAYER.hitbox, follow=True, x=5, y=0)
            data.PLAYER_PROJECTILE_DATA.append(Projectile(
                speed=cls.projectile_speed,
                size=cls.projectile_size,
                start_point=data.PLAYER.hitbox.center,
                damage=dmg,
                gfx_idx=0,
                target=pygame.mouse.get_pos(),
                piercing=piercing
            ))

    @classmethod
    def set_fire_rate(cls, fr):
        cls.raw_fire_rate += fr
        cls.fire_rate = cls.raw_fire_rate
        if cls.fire_rate < cls.fire_rate_limit:
            cls.fire_rate = cls.fire_rate_limit

    @classmethod
    def gfx_gun_draw(cls):
        win.blit(rot_center(
            data.PLAYER.ship_sprites[18], degrees(pygame.mouse.get_pos()[1], data.PLAYER.hitbox.center[1], pygame.mouse.get_pos()[0], data.PLAYER.hitbox.center[0])),
            (data.PLAYER.hitbox.center[0] - 17, data.PLAYER.hitbox.center[1] - 6))

    @classmethod
    def gfx_pd_draw(cls):
        if "point_defence" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="point_defence").active:
                win.blit(cls.projectile_sprites[14], (data.PLAYER.hitbox.topleft[0] - 190, data.PLAYER.hitbox.topleft[1] - 220))

    @classmethod
    def update(cls):
        cls.gfx_gun_draw()
        cls.gfx_pd_draw()
        cls.shots()
        cls.bombs()


data.TURRET = Turret

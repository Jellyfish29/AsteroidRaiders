import pygame
# from pygame.locals import *
import random

from init import *
from astraid_funcs import *
import astraid_data as data
from Gfx import Gfx
from projectiles import Projectile, Missile, Impactor, Explosion, Wave
from phenomenon import Black_hole, Gravity_well, Implosion
from items_misc import Item_cd_reduction_prog, Item_damage_prog, Item_shield_prog


class Turret:

    # normal shot vlaues
    projectile_size = (12, 6)
    projectile_speed = 35
    firing = False
    direction = None
    base_fire_rate = 2.6
    fire_rate = base_fire_rate  # attacks per second
    raw_fire_rate = fire_rate
    fire_rate_limit = 6
    shot_count = 0
    gfx_idx = 0
    hit_locations = []
    special_damage = 0
    # Overdrive
    overdrive_count = 0
    # ammunition = normal_fire_rate[1]
    fire_limiter = 0
    # special fire
    super_shot_ammo = 30
    super_shot_limiter = 0
    star_shot_limiter = 0
    star_shot_ammo = 25
    star_shot_tubes = 12
    burts_limiter = 0
    scatter_limter = 0
    rail_gun_charge = 0
    shock_burst_limiter = 0
    smart_burst_limiter = 0
    smart_missile_target = 0
    # pd values
    pd_ticker = 0
    # Gfx setup
    projectile_sprites = get_images("projectile")
    explosion_sprites = get_images("explosions")
    muzzle_effect_timer = (i for i in range(1))
    gun_gfx_idx = 8
    gfx_turret_tube = 12
    gfx_turret_tubes = (i for i in range(12, 15))
    gfx_secondary_guns_loc = [(- 64, -50), (0, -50), (-35, 0), (-35, -70)]
    sec_gun_gfx_idx = 10
    item_amount = 0
    # Special Munitions
    snare_charge = 0

    @classmethod
    def fire(cls, fire):
        cls.firing = fire

    @classmethod
    def on_mouse_click_actions(cls):
        if cls.firing:
            cls.normal_fire()
            cls.star_fire()
            cls.rapid_fire()
            # cls.test_sin()

    @classmethod
    def on_item_button_click_actions(cls):
        cls.nuke_fire()
        cls.gravity_bomb()
        cls.black_hole_bomb()
        cls.implosion_bomb()
        cls.burst_fire()
        cls.scatter_fire()
        cls.rail_gun()
        cls.shock_missiles()
        cls.smart_missiles()

    @classmethod
    def passiv_item_actions(cls):
        cls.debris_scanner()

    @classmethod
    @timer
    def normal_fire(cls, timer):
        if timer.trigger(cls.get_fire_rate()):
            cls.muzzle_effect_timer = (i for i in range(8))
            cls.shot_count += 1

            ### Special Ammo ###

            if not any([
                cls.hammer_shot(),
                cls.fan_shot(),
                cls.he_rounds(),
                cls.boss_snare(),
                cls.concussion_rounds(),
                cls.piercing_rounds(),
                cls.fragmentation_rounds(),
            ]):

                # Gfx.create_effect("shot_muzzle", 2, data.PLAYER.hitbox, follow=True, x=5, y=0)
                data.PLAYER_PROJECTILE_DATA.append(Projectile(
                    speed=cls.projectile_speed,
                    size=cls.projectile_size,
                    start_point=data.PLAYER.hitbox.center,
                    damage=data.PLAYER.damage + cls.special_damage,
                    gfx_idx=11,
                    target=pygame.mouse.get_pos(),
                ))
            cls.special_damage = 0

    @classmethod
    @timer
    def test_sin(cls, timer):
        if timer.trigger():
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
                        gfx_idx=1,
                        target=pos,
                        impact_effect=lambda loc=pos: data.PLAYER_PROJECTILE_DATA.append(Explosion(
                            location=loc,
                            explo_size=700,
                            damage=3.5 + data.PLAYER.damage + int(cls.fire_rate),
                            explosion_effect=lambda loc: Gfx.create_effect(
                                "explosion_1", 3, (loc[0] - 400, loc[1] - 400), explo=True),
                            explo_speed=(60, 60)
                        ))
                    ))
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
                        gfx_idx=1,
                        target=pos,
                        impact_effect=lambda loc=pos: data.PHENOMENON_DATA.append(Gravity_well(
                            speed=0,
                            size=(500, 500),
                            gfx_idx=(1, 1),
                            gfx_hook=(-300, -300),
                            decay=data.ITEMS.get_item(flag="gravity_bomb").active_time,
                            location=loc,
                            flag="player"))
                    ))
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
                        gfx_idx=1,
                        target=pos,
                        impact_effect=lambda loc=pos: data.PHENOMENON_DATA.append(Black_hole(
                            speed=0,
                            size=(300, 300),
                            decay=data.ITEMS.get_item(flag="black_hole_bomb").active_time,
                            location=loc,
                            flag="player",
                            damage=data.PLAYER.damage * 0.5 + cls.fire_rate))
                    ))
                    data.ITEMS.get_item(flag="black_hole_bomb").end_active()

    @classmethod
    def implosion_bomb(cls):
        if "implosion_bomb" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="implosion_bomb").active:
                # aim effect
                if data.ITEMS.get_item(flag="implosion_bomb").engage:
                    pos = pygame.mouse.get_pos()
                    data.PLAYER_PROJECTILE_DATA.append(Impactor(
                        speed=20,
                        size=(4, 4),
                        start_point=data.PLAYER.hitbox.topleft,
                        damage=0,
                        gfx_idx=24,
                        target=pos,
                        impact_effect=lambda loc=pos: data.PHENOMENON_DATA.append(Implosion(
                            speed=0,
                            size=(700, 700),
                            decay=10,
                            location=loc,
                            flag="player",
                        ))
                    ))
                    data.ITEMS.get_item(flag="implosion_bomb").end_active()

    @classmethod
    @timer
    def rail_gun(cls, timer):
        if "rail_gun" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="rail_gun").active:
                # aim effect
                if timer.trigger(data.ITEMS.get_item(flag="rail_gun").effect_strength):
                    if cls.rail_gun_charge < 1:
                        cls.rail_gun_charge += 0.01

                data.PLAYER.angles = directions(4)

                if data.ITEMS.get_item(flag="rail_gun").engage:
                    data.PLAYER_PROJECTILE_DATA.append(Projectile(
                        speed=25 * cls.rail_gun_charge + 10,
                        size=(40, 40),
                        start_point=data.PLAYER.hitbox.center,
                        damage=(data.PLAYER.damage * 7) * cls.rail_gun_charge,
                        gfx_idx=18,
                        target=pygame.mouse.get_pos(),
                        piercing=True
                    ))

                    data.PLAYER.angles = directions(data.PLAYER.speed)
                    cls.rail_gun_charge = 0
                    data.ITEMS.get_item(flag="rail_gun").end_active()

    @classmethod
    @timer
    def point_defence(cls, enemy, timer):
        if "point_defence" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="point_defence").active:
                win.blit(cls.projectile_sprites[7], (data.PLAYER.hitbox.topleft[0] - 190, data.PLAYER.hitbox.topleft[1] - 220))
                pd_envelope = pygame.Rect(
                    data.PLAYER.hitbox.center[0] - 200, data.PLAYER.hitbox.center[1] - 200, 600, 600)
                # pygame.draw.rect(win, (255, 255, 0), pd_envelope)
                if pd_envelope.colliderect(enemy):
                    if timer.trigger(6):
                        data.PLAYER_PROJECTILE_DATA.append(Projectile(
                            speed=30,
                            size=(10, 10),
                            start_point=data.PLAYER.hitbox.center,
                            damage=1 + data.PLAYER.damage * 0.2,
                            flag="point_defence",
                            gfx_idx=3,
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
                    for location in [data.PLAYER.hitbox.topleft, data.PLAYER.hitbox.topright]:
                        data.PLAYER_PROJECTILE_DATA.append(Missile(
                            speed=30,
                            size=(5, 5),
                            start_point=location,
                            target=enemy.hitbox,
                            damage=data.PLAYER.damage * int(data.ITEMS.get_item(flag="missile").effect_strength),
                            flag="missile"
                        ))
                    data.ITEMS.get_item(flag="missile").end_active()

    @classmethod
    def fan_shot(cls):
        if "fan_shot" in data.ITEMS.active_flag_lst:
            if cls.shot_count % data.ITEMS.get_item(flag="fan_shot").effect_strength == 0:
                for i in [-5, 0, 5]:
                    data.PLAYER_PROJECTILE_DATA.append(Projectile(
                        speed=cls.projectile_speed,
                        size=cls.projectile_size,
                        start_point=data.PLAYER.hitbox.center,
                        damage=0.1 + data.PLAYER.damage,
                        gfx_idx=11,
                        angle_variation=i,
                        target=pygame.mouse.get_pos(),
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
                    damage=data.PLAYER.damage + data.ITEMS.get_item(flag="hammer_shot").effect_strength,
                    gfx_idx=15,
                    target=pygame.mouse.get_pos(),
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
                cls.set_fire_rate(0.07)

    @classmethod
    @timer
    def rapid_fire(cls, timer):
        if "rapid_fire" in data.ITEMS.active_flag_lst:
            rapid_fire = data.ITEMS.get_item(flag="rapid_fire")
            if rapid_fire.active:
                if timer.trigger(4):
                    Gfx.create_effect("shot_muzzle", 2, data.PLAYER.hitbox, follow=True, x=5, y=0)
                    cls.super_shot_limiter += 1
                    if cls.super_shot_limiter >= cls.super_shot_ammo + int(data.LEVELS.level * 0.66):
                        cls.super_shot_limiter = 0
                        rapid_fire.active = False
                        rapid_fire.cooldown = True
                        del rapid_fire

                    data.PLAYER_PROJECTILE_DATA.append(Projectile(
                        speed=cls.projectile_speed,
                        size=cls.projectile_size,
                        start_point=data.PLAYER.hitbox.center,
                        damage=data.PLAYER.damage * 1.5,
                        gfx_idx=15,
                        target=pygame.mouse.get_pos(),
                    ))

    @classmethod
    @timer
    def star_fire(cls, timer):
        if "star_fire" in data.ITEMS.active_flag_lst:
            star_fire = data.ITEMS.get_item(flag="star_fire")
            if star_fire.active:
                if timer.trigger(30):
                    cls.star_shot_limiter += 1
                    Gfx.create_effect("shot_muzzle", 2, data.PLAYER.hitbox, follow=True, x=5, y=0)
                    if cls.star_shot_limiter > cls.star_shot_ammo + int(data.LEVELS.level / 2):
                        cls.star_shot_limiter = 0
                        star_fire.end_active()
                        del star_fire

                    for angle in range(0, 360, int(360 / cls.star_shot_tubes)):
                        data.PLAYER_PROJECTILE_DATA.append(Projectile(
                            speed=cls.projectile_speed,
                            size=cls.projectile_size,
                            start_point=data.PLAYER.hitbox.center,
                            damage=data.PLAYER.damage,
                            gfx_idx=11,
                            angle=angle
                        ))

    @classmethod
    @timer
    def burst_fire(cls, timer):
        if "burst_fire" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="burst_fire").active:
                if timer.trigger(3):
                    cls.burts_limiter += 1
                    if cls.burts_limiter <= data.ITEMS.get_item(flag="burst_fire").effect_strength:
                        data.PLAYER_PROJECTILE_DATA.append(Projectile(
                            speed=cls.projectile_speed,
                            size=cls.projectile_size,
                            start_point=data.PLAYER.hitbox.center,
                            damage=0.5 + data.PLAYER.damage,
                            gfx_idx=11,
                            angle_variation=random.randint(-5, 5),
                            target=pygame.mouse.get_pos()
                        ))
                    else:
                        cls.burts_limiter = 0
                        data.ITEMS.get_item(flag="burst_fire").end_active()

    @classmethod
    @timer
    def scatter_fire(cls, timer):
        if "scatter_fire" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="scatter_fire").active:
                if timer.trigger(10):
                    cls.scatter_limter += 1
                    if cls.scatter_limter <= data.ITEMS.get_item(flag="scatter_fire").effect_strength:
                        for i in range(-15, 16, 5):
                            data.PLAYER_PROJECTILE_DATA.append(Projectile(
                                speed=cls.projectile_speed,
                                size=cls.projectile_size,
                                start_point=data.PLAYER.hitbox.center,
                                damage=0.1 + data.PLAYER.damage,
                                gfx_idx=11,
                                target=pygame.mouse.get_pos(),
                                angle_variation=i
                            ))
                    else:
                        cls.scatter_limter = 0
                        data.ITEMS.get_item(flag="scatter_fire").end_active()

    @classmethod
    @timer
    def shock_missiles(cls, timer):
        if "shock_missile" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="shock_missile").active:
                if timer.trigger(6):
                    cls.shock_burst_limiter += 1
                    if cls.shock_burst_limiter <= data.ITEMS.get_item(flag="shock_missile").effect_strength:
                        data.PLAYER_PROJECTILE_DATA.append(Projectile(
                            speed=30,
                            size=cls.projectile_size,
                            start_point=data.PLAYER.hitbox.center,
                            damage=2 + data.PLAYER.damage * 2,
                            gfx_idx=24,
                            target=pygame.mouse.get_pos(),
                            hit_effect=lambda _, obj: obj.set_cc(0, 180, stun=True)
                        ))
                    else:
                        cls.shock_burst_limiter = 0
                        data.ITEMS.get_item(flag="shock_missile").end_active()

    @classmethod
    @timer
    def smart_missiles(cls, timer):
        if "smart_missile" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="smart_missile").active:
                if timer.trigger(3):
                    targets = [e for e in data.ENEMY_DATA if not rect_not_on_sreen(e.hitbox, strict=True)]
                    if len(targets) > 0:
                        try:
                            target = targets[cls.smart_missile_target].hitbox
                            cls.smart_missile_target += 1
                        except IndexError:
                            cls.smart_missile_target = 0
                            target = targets[cls.smart_missile_target].hitbox

                        cls.smart_burst_limiter += 1
                        if cls.smart_burst_limiter <= data.ITEMS.get_item(flag="smart_missile").effect_strength:
                            data.PLAYER_PROJECTILE_DATA.append(Missile(
                                speed=25,
                                size=(5, 5),
                                start_point=data.PLAYER.hitbox.center,
                                target=target,
                                damage=0.1 + data.PLAYER.damage * 2,
                                flag="missile",
                                gfx_idx=25
                            ))
                        else:
                            cls.smart_burst_limiter = 0
                            data.ITEMS.get_item(flag="smart_missile").end_active()
                    else:
                        data.ITEMS.get_item(flag="smart_missile").active = False

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
                    gfx_idx=15,
                    target=pygame.mouse.get_pos(),
                    piercing=False,
                    hit_effect=lambda l, _: data.PLAYER_PROJECTILE_DATA.append(Explosion(
                        location=l,
                        explo_size=70,
                        damage=data.PLAYER.damage * 0.35,
                        explosion_effect=lambda loc: Gfx.create_effect(
                            "explosion_4", 1, (loc[0] - 90, loc[1] - 90), explo=True)
                    ))
                ))
                return True

    @classmethod
    @timer
    def fragmentation_rounds(cls, timer):
        if "frag_rounds" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="frag_rounds").active:
                # for projectile in cls.hit_locations:

                data.PLAYER_PROJECTILE_DATA.append(Projectile(
                    speed=cls.projectile_speed,
                    size=cls.projectile_size,
                    start_point=data.PLAYER.hitbox.center,
                    damage=0.1 + data.PLAYER.damage,
                    gfx_idx=11,
                    target=pygame.mouse.get_pos(),
                    piercing=False,
                    hit_effect=lambda _, obj: [data.PLAYER_PROJECTILE_DATA.append(Projectile(
                        speed=20,
                        size=cls.projectile_size,
                        start_point=obj.hitbox.center,
                        damage=data.PLAYER.damage * 0.06,
                        flag="secondary",
                        gfx_idx=3,
                        angle=angle_switcher(projectile.angle + (random.randint(-35, 35))),
                        piercing=True,
                        decay=30
                    )) for _ in range(data.ITEMS.get_item(flag="frag_rounds").effect_strength + 1)
                        for projectile in cls.hit_locations]  # OMEGA LAMBDA
                ))

                return True

    @classmethod
    @timer
    def concussion_rounds(cls, timer):
        if "con_rounds" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="con_rounds").active:
                Gfx.create_effect("shot_muzzle", 2, data.PLAYER.hitbox, follow=True, x=5, y=0)
                data.PLAYER_PROJECTILE_DATA.append(Projectile(
                    speed=cls.projectile_speed,
                    size=cls.projectile_size,
                    start_point=data.PLAYER.hitbox.center,
                    damage=data.PLAYER.damage,
                    gfx_idx=23,
                    target=pygame.mouse.get_pos(),
                    piercing=False,
                    hit_effect=lambda _, obj: obj.set_cc(int(obj.speed * 0.66), 60)
                ))
                return True

    @classmethod
    @timer
    def piercing_rounds(cls, timer):
        if "piercing_shot" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="piercing_shot").active:
                Gfx.create_effect("shot_muzzle", 2, data.PLAYER.hitbox, follow=True, x=5, y=0)
                data.PLAYER_PROJECTILE_DATA.append(Projectile(
                    speed=cls.projectile_speed,
                    size=cls.projectile_size,
                    start_point=data.PLAYER.hitbox.center,
                    damage=data.PLAYER.damage * data.ITEMS.get_item(flag="piercing_shot").effect_strength,
                    flag="secondary",
                    gfx_idx=14,
                    target=pygame.mouse.get_pos(),
                    piercing=True,
                ))

                return True

    @classmethod
    def debris_scanner(cls):
        if "debris_scanner" in data.ITEMS.active_flag_lst:
            for loc in cls.hit_locations:
                if random.randint(1, 100) > 100 - data.ITEMS.get_item(flag="debris_scanner").effect_strength:
                    item = random.choices([Item_damage_prog, Item_cd_reduction_prog, Item_shield_prog], [60, 25, 15], k=1)[0]
                    data.ITEMS.drop(loc.hitbox.center, target=item((100, 100, 200)))

    @classmethod
    def boss_snare(cls):
        if cls.snare_charge > 0:
            cls.snare_charge -= 1
            data.PLAYER_PROJECTILE_DATA.append(Projectile(
                speed=40,
                size=(20, 20),
                start_point=data.PLAYER.hitbox.center,
                damage=0,
                gfx_idx=19,
                target=pygame.mouse.get_pos(),
                hit_effect=lambda a, b: data.ENEMY_DATA[0].set_snared()
            ))
            return True

    @classmethod
    def get_fire_rate(cls):
        return 1 / cls.fire_rate * 60

    @classmethod
    def set_fire_rate(cls, fr):
        cls.raw_fire_rate += fr
        cls.fire_rate = cls.raw_fire_rate
        if cls.fire_rate > cls.fire_rate_limit:
            cls.fire_rate = cls.fire_rate_limit

    @classmethod
    def draw_pd(cls):
        if "point_defence" in data.ITEMS.active_flag_lst:
            if data.ITEMS.get_item(flag="point_defence").active:
                win.blit(cls.projectile_sprites[7], (data.PLAYER.hitbox.topleft[0] - 190, data.PLAYER.hitbox.topleft[1] - 220))

    @classmethod
    @run_limiter
    def gun_gfx_idx_update(cls, limiter):
        if next(cls.muzzle_effect_timer, "stop") == "stop":
            cls.gun_gfx_idx = 8
            cls.sec_gun_gfx_idx = 10
            if limiter.run_block_once():
                try:
                    cls.gfx_turret_tube = next(cls.gfx_turret_tubes)
                except StopIteration:
                    cls.gfx_turret_tubes = (i for i in range(12, 15))
                    cls.gfx_turret_tube = next(cls.gfx_turret_tubes)
        else:
            limiter.run_limiter_reset()
            cls.gun_gfx_idx = cls.gfx_turret_tube
            cls.sec_gun_gfx_idx = 11

        # cls.item_amount = 4 - [data.ITEMS.inventory_dic[k] for k in data.ITEMS.inventory_dic if k < 4].count(None)

    @classmethod
    def gfx_gun_draw(cls):
        win.blit(rot_center(
            Gfx.gun_sprites[cls.gun_gfx_idx], degrees(
                pygame.mouse.get_pos()[1],
                 data.PLAYER.hitbox.center[1],
                 pygame.mouse.get_pos()[0],
                 data.PLAYER.hitbox.center[0])
        ),
            (data.PLAYER.hitbox.center[0] - 35, data.PLAYER.hitbox.center[1] - 35))

        # for loc in cls.gfx_secondary_guns_loc[:cls.item_amount]:
        #     win.blit(rot_center(
        #         Gfx.gun_sprites[cls.sec_gun_gfx_idx], degrees(
        #             pygame.mouse.get_pos()[1],
        #             data.PLAYER.hitbox.center[1],
        #             pygame.mouse.get_pos()[0],
        #             data.PLAYER.hitbox.center[0])
        #     ),
        #         (data.PLAYER.hitbox.center[0] + loc[0], data.PLAYER.hitbox.center[1] + loc[1]))

    @classmethod
    def update(cls):
        cls.gfx_gun_draw()
        cls.draw_pd()
        cls.gun_gfx_idx_update()
        cls.on_mouse_click_actions()
        cls.on_item_button_click_actions()
        cls.passiv_item_actions()
        cls.hit_locations.clear()


data.TURRET = Turret

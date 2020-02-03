import pygame
import random
import astraid_data as data
from init import *
from astraid_funcs import *
from Gfx import Gfx
from projectiles import Projectile, Mine, Missile, Impactor, Explosion, Dart, Wave
from phenomenon import Gravity_well, Force_field
from items import Event_item_boss_snare


class Boss_skills(Timer):

    def __init__(self):
        # Timer.__init__(self)
        self.missile_duration = 480
        self.missile_retarget_trigger = 90
        self.mg_angle = 0
        self.main_gun_angles = angles_360(35)
        self.salvo_start_point = iter([i for i in range(0, self.size[1], int(self.size[1] / 10))])
        self.delta_salvo_limit = (i for i in range(6))
        self.wave_motion_limit = (i for i in range(5))
        self.dart_salvo_start_point = iter([i for i in range(0, self.size[1], int(self.size[1] / 5))])
        self.dummy_targets = [[400, 0], [400, winheight / 2], [400, winheight]]
        self.dart_missiles = 6
        self.jump_charge = False
        self.jump_point = 0
        self.jump_chance = 1100
        self.chaser_hit = False
        self.pd_envelope = pygame.Rect(1500, 0, winwidth - 1500, winheight)

    def skill_mines(self, **kwargs):
        if self.timer_trigger(self.fire_rate * 5):
            data.ENEMY_PROJECTILE_DATA.append(Mine(
                speed=12,
                start_point=self.hitbox.center,
                damage=2,
                flag="en_mine"
            ))

    def skill_missile(self, **kwargs):
        if self.timer_trigger(self.missile_duration):
            self.missile_direction = 270
            data.ENEMY_PROJECTILE_DATA.append(Missile(
                speed=8,
                size=(10, 10),
                start_point=self.hitbox.bottomleft,
                target=data.PLAYER.hitbox,
                damage=2,
                flag="en_missile",
                gfx_idx=4,
                aquisition_delay=self.missile_retarget_trigger,
                enemy_missile=True
            ))

    def skill_star_shot(self, **kwargs):
        if self.timer_trigger(self.fire_rate * 5):
            for i in range(0, 359, 22):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), self.hitbox.center, 1, "enemy", 12, angle=i))

    def skill_salvo_alpha(self, **kwargs):
        if self.timer_trigger(self.fire_rate * 3):
            for i in range(0, self.size[1], int(self.size[1] / 10)):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), (self.hitbox.topleft[0], self.hitbox.topleft[1] + i), 1, "bo_salvo", 12, angle=180))
            for i in range(0, self.size[1], int(self.size[1] / 10)):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), (self.hitbox.topright[0], self.hitbox.topright[1] + i), 1, "bo_salvo", 12, angle=0))

    def skill_salvo_bravo(self, **kwargs):
        if self.timer_trigger(self.fire_rate * 5):
            for i in range(135, 226, 9):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), self.hitbox.center, 1, "enemy", 12, angle=i))
            for i in range(0, 45, 9):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), self.hitbox.center, 1, "enemy", 12, angle=i))
            for i in range(315, 360, 9):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), self.hitbox.center, 1, "enemy", 12, angle=i))

    def skill_salvo_charlie(self, **kwargs):
        if self.timer_key_delay(limit=self.fire_rate * 3, key="salvo_c"):
            if self.timer_trigger(5):
                shot_sp = next(self.salvo_start_point, "stop")
                if shot_sp == "stop":
                    self.salvo_start_point = iter([i for i in range(0, self.size[1], int(self.size[1] / 10))])
                    self.timer_key_delay(reset=True, key="salvo_c")
                else:
                    data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), (self.hitbox.topleft[0], self.hitbox.topleft[1] + shot_sp), 1, "bo_salvo", 12, angle=180))
                    data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), (self.hitbox.topright[0], self.hitbox.topright[1] + shot_sp), 1, "bo_salvo", 12, angle=0))

    def skill_salvo_delta(self, **kwargs):
        if self.timer_key_delay(limit=self.fire_rate * 3, key="salvo_d"):
            if self.timer_trigger(5):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(15, (6, 6), (self.hitbox.center[0], self.hitbox.center[1]), 1, "bo_salvo", 12, target=data.PLAYER.hitbox))
                limit = next(self.delta_salvo_limit, "stop")
                if limit == "stop":
                    self.timer_key_delay(reset=True, key="salvo_d")
                    self.delta_salvo_limit = (i for i in range(6))

    def skill_wave_motion_gun(self):
        if self.timer_key_delay(limit=self.fire_rate * 3, key="laser"):
            limit = next(self.wave_motion_limit, "stop")
            data.ENEMY_PROJECTILE_DATA.append(Wave(
                speed=25,
                size=(5, 5),
                start_point=self.hitbox.center,
                damage=1,
                gfx_idx=16,
                target=data.PLAYER.hitbox,
                curve_size=1.5,
            ))
            if limit == "stop":
                self.wave_motion_limit = (i for i in range(5))
                self.timer_key_delay(reset=True, key="laser")

    def skill_volley(self, **kwargs):
        if self.timer_trigger(self.fire_rate * 3):
            for i in [-5, 0, 5]:
                data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), self.hitbox.center, 1, "benemy", 12, angle_variation=i, target=data.PLAYER.hitbox))

    def skill_jumpdrive(self, **kwargs):
        if not self.jump_charge:
            jumpdrive_trigger = random.randint(1, self.jump_chance)
            if jumpdrive_trigger == 1:
                self.jump_point = self.checkpoints[random.choice([1, 2, 3, 4])]
                jumpdrive_trigger = 0
                self.jump_charge = True
        if self.jump_charge:
            # pygame.draw.rect(win, (0, 0, 100), pygame.Rect(self.jump_point, self.size))
            if self.__class__.__name__ == "Boss_cruiser":
                win.blit(en.Enemy.boss_sprites[40], self.jump_point)
            elif self.__class__.__name__ == "Boss_battleship":
                win.blit(en.Enemy.boss_sprites[41], self.jump_point)
            elif self.__class__.__name__ == "Boss_corvette":
                pygame.draw.rect(win, (0, 0, 100), pygame.Rect(self.jump_point, self.size))
            elif self.__class__.__name__ == "Elite":
                pygame.draw.rect(win, (0, 0, 100), pygame.Rect(self.jump_point, self.size))
            if self.timer_trigger(60):
                Gfx.create_effect("jump", 2, (self.hitbox.topleft[0] - 40, self.hitbox.topleft[1] - 40))
                self.hitbox.topleft = self.jump_point
                self.jump_charge = False

    def skill_main_gun(self, target=data.PLAYER.hitbox):
        if self.__class__.__name__ == "Boss_battleship":
            fire_rate = 120
        else:
            fire_rate = self.fire_rate * 6
        if self.timer_key_delay(limit=fire_rate, key="main_gun"):
            data.ENEMY_PROJECTILE_DATA.append(Projectile(
                speed=70,
                size=(4, 4),
                start_point=self.hitbox.midbottom,
                damage=0,
                flag="neutral",
                gfx_idx=2,
                target=target,
            ))
            if self.timer_trigger(80):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(
                    speed=80,
                    size=(30, 30),
                    start_point=self.hitbox.midbottom,
                    damage=4,
                    flag="enemy",
                    gfx_idx=18,
                    target=target
                ))
                self.timer_key_delay(reset=True, key="main_gun")
                if target is not data.PLAYER.hitbox:
                    self.target = random.choice([(random.randint(0, winwidth), random.randint(0, winheight), data.PLAYER.hitbox.center)])

    def skill_dart_missiles(self):
        if self.timer_key_delay(limit=self.fire_rate * 15, key="darts"):
            if self.trigger(60):
                shot_sp = next(self.dart_salvo_start_point, "stop")
                if shot_sp == "stop":
                    self.dart_salvo_start_point = iter([i for i in range(0, self.size[1], int(self.size[1] / 5))])
                    print(self.timer_calls_per_tick)
                    self.timer_key_delay(reset=True, key="darts")
                else:
                    data.ENEMY_PROJECTILE_DATA.append(Impactor(
                        speed=6,
                        size=(6, 6),
                        start_point=(self.hitbox.topleft[0], self.hitbox.topleft[1] + shot_sp),
                        flag="boss",
                        gfx_idx=9,
                        target=(self.hitbox.topleft[0] - 250, self.hitbox.topleft[1] + shot_sp + 10),
                        impact_effect=lambda shot_sp=shot_sp: data.ENEMY_PROJECTILE_DATA.append(Dart(
                            start_point=(self.hitbox.topright[0] - 250, self.hitbox.topright[1] + shot_sp),
                            damage=3,
                            target=data.PLAYER.hitbox
                        ))
                    ))
                    data.ENEMY_PROJECTILE_DATA.append(Impactor(
                        speed=6,
                        size=(6, 6),
                        start_point=(self.hitbox.topright[0], self.hitbox.topright[1] + shot_sp),
                        flag="boss",
                        gfx_idx=9,
                        target=(self.hitbox.topleft[0] + 250, self.hitbox.topleft[1] + shot_sp + 10),
                        impact_effect=lambda shot_sp=shot_sp: data.ENEMY_PROJECTILE_DATA.append(Dart(
                            start_point=(self.hitbox.topright[0] + 250, self.hitbox.topright[1] + shot_sp),
                            damage=2,
                            target=data.PLAYER.hitbox
                        ))
                    ))

    def skill_point_defence(self):
        # pygame.draw.rect(win, (255, 0, 0), self.pd_envelope)
        if data.PLAYER.hitbox.colliderect(self.pd_envelope):
            if self.timer_trigger(10):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(
                    speed=20,
                    size=(6, 6),
                    start_point=self.hitbox.center,
                    damage=1,
                    flag="boss",
                    gfx_idx=3,
                    target=data.PLAYER.hitbox.center
                ))


# Mineboat Skills

    def skill_chaser(self):
        if not self.chaser_hit:
            self.hitbox.move_ip(self.angles[degrees(data.PLAYER.hitbox.center[0], self.hitbox.center[0], data.PLAYER.hitbox.center[1], self.hitbox.center[1])])
        else:
            if self.timer_trigger(300):
                self.chaser_hit = False
                # self.special_move = True
                self.special_gfx = True
        if self.hitbox.colliderect(data.PLAYER.hitbox):
            self.chaser_hit = True
            # self.special_move = False
            self.special_gfx = False
        if len([e for e in data.ENEMY_DATA if e.__class__.__name__ == "Boss_weakspot"]) == 0:
            self.special_move = False
            # self.special_gfx = False
            self.angles = self.orig_angles
            self.skills_lst.remove(self.skill_chaser)

# Frigatte Skills

    def skill_turret_defence_matrix(self):
        turret_amount = len([e.set_sp_dmg() for e in data.ENEMY_DATA if e.__class__.__name__ == "Boss_turret"])
        if turret_amount > 0:
            self.special_take_damage = lambda dmg, a=turret_amount: [e.set_health((dmg / a), (200, 0, 200)) for e in data.ENEMY_DATA]
        if self.timer_delay(limit=600):
            if turret_amount == 0:
                self.skills_lst.remove(self.skill_turret_defence_matrix)
                self.special_take_damage = None
                self.timer_delay(reset=True)

# Corvette Skills

    def skill_speed_boost(self):
        if self.timer_key_delay(limit=300, key="sboost"):
            self.angles = angles_360(40)
            if self.timer_trigger(15):
                self.timer_key_delay(reset=True, key="sboost")
        else:
            self.angles = angles_360(self.speed)

# Destroyer Skills

    @run_limiter
    def skill_missile_barrage(self, limiter):
        self.special_move = True
        self.hide_health_bar = True
        self.hitbox.move_ip(self.angles[degrees(1000, self.hitbox.center[0], 500, self.hitbox.center[1])])
        # if abs(1000 - self.hitbox.center[0]) < 10 or abs(500 - self.hitbox.center[1]) < 10:
        if self.hitbox.collidepoint((1000, 500)):
            if limiter.run_block_once():
                self.angles = angles_360(0)

        if self.timer_trigger(10):
            target = random.randint(0, winwidth), random.randint(0, winheight)
            data.ENEMY_PROJECTILE_DATA.append(Impactor(
                speed=15,
                size=(6, 6),
                start_point=self.hitbox.center,
                damage=2,
                flag="en_missile",
                target=target,
                impact_effect=lambda loc=target: data.ENEMY_PROJECTILE_DATA.append(Explosion(
                    location=loc,
                    explo_size=100,
                    damage=3,
                    explosion_effect=lambda loc: Gfx.create_effect("explosion_4", 2, (loc[0] - 60, loc[1] - 60), explo=True)
                ))
            ))
        if len([e for e in data.ENEMY_DATA if e.__class__.__name__ == "Boss_weakspot"]) == 0:
            self.special_move = False
            self.special_attack = False
            self.hide_health_bar = False
            self.angles = angles_360(self.speed)
            self.special_skills_lst.remove(self.skill_missile_barrage)

    @run_limiter
    def skill_main_gun_salvo(self, limiter):
        self.special_move = True
        self.hide_health_bar = True
        self.hitbox.move_ip(self.angles[degrees(1000, self.hitbox.center[0], 500, self.hitbox.center[1])])
        # if abs(1000 - self.hitbox.center[0]) < 30 or abs(500 - self.hitbox.center[1]) < 30:
        if self.hitbox.collidepoint((1000, 500)):
            if limiter.run_block_once():
                self.angles = angles_360(0)
        if len([e for e in data.ENEMY_DATA if e.__class__.__name__ == "Boss_weakspot"]) == 0:
            self.special_move = False
            self.special_attack = False
            self.hide_health_bar = False
            self.angles = angles_360(self.speed)
            self.special_skills_lst.remove(self.skill_main_gun_salvo)
            for e in data.ENEMY_DATA:
                if e.__class__.__name__ == "Boss_main_gun_battery":
                    e.kill = True

    @run_limiter
    def skill_laser_storm_laststand(self, limiter):
        self.special_move = True
        # self.hide_health_bar = True
        self.hitbox.move_ip(self.angles[degrees(1850, self.hitbox.center[0], 500, self.hitbox.center[1])])
        # if abs(1850 - self.hitbox.center[0]) < 30 or abs(500 - self.hitbox.center[1]) < 30:
        if self.hitbox.collidepoint((1880, 500)):
            if limiter.run_block_once():
                self.angles = angles_360(0)
                self.special_gfx = True
                self.special_skills_lst.append(self.skill_point_defence)
        if self.health <= 0:
            for e in data.ENEMY_DATA:
                if e.__class__.__name__ == "Boss_laser_battery":
                    e.kill = True

# Cruiser Skills

    @run_limiter
    def skill_dart_missile_last_stand(self, limiter):
        self.special_move = True
        self.hitbox.move_ip(self.angles[degrees(1880, self.hitbox.center[0], 500, self.hitbox.center[1])])
        # if abs(1880 - self.hitbox.center[0]) < 30 or abs(500 - self.hitbox.center[1]) < 30:
        if self.hitbox.collidepoint((1880, 500)):
            if limiter.run_block_once():
                self.angles = angles_360(0)
                self.speed = 0
                self.special_gfx = True
                self.special_skills_lst.append(self.skill_point_defence)
            if self.timer_key_delay(60 - self.dart_missiles, key="darts2"):
                if self.trigger(60 - self.dart_missiles):
                    shot_sp = next(self.dart_salvo_start_point, "stop")
                    if shot_sp == "stop":
                        if self.dart_missiles <= 40:
                            self.dart_missiles += 4
                        self.dart_salvo_start_point = iter([i for i in range(0, self.size[1], int(self.size[1] / self.dart_missiles))])
                        print(self.timer_calls_per_tick)
                        self.timer_key_delay(reset=True, key="darts2")
                    else:
                        data.ENEMY_PROJECTILE_DATA.append(Impactor(
                            speed=6,
                            size=(6, 6),
                            start_point=(self.hitbox.topleft[0], self.hitbox.topleft[1] + shot_sp),
                            flag="boss",
                            gfx_idx=9,
                            target=(self.hitbox.topleft[0] - 250, self.hitbox.topleft[1] + shot_sp + 10),
                            impact_effect=lambda shot_sp=shot_sp: data.ENEMY_PROJECTILE_DATA.append(Dart(
                                start_point=(self.hitbox.topright[0] - 250, self.hitbox.topright[1] + shot_sp),
                                damage=3,
                                target=data.PLAYER.hitbox
                            ))
                        ))
            if self.trigger(600):
                location = random.randint(300, 1500), random.randint(100, 900)
                data.ENEMY_PROJECTILE_DATA.append(Impactor(
                    speed=10,
                    size=(6, 6),
                    start_point=self.hitbox.center,
                    damage=2,
                    flag="en_missile",
                    gfx_idx=9,
                    target=location,
                    impact_effect=lambda location=location: data.PHENOMENON_DATA.append(Gravity_well(
                        speed=0,
                        decay=600,
                        location=location,
                        flag="enemy"
                    ))
                ))

# Scout skills

    @run_limiter
    def skill_scout_hunt(self, limiter):
        self.special_move = True
        self.hitbox.move_ip(self.angles[degrees(900, self.hitbox.center[0], 150, self.hitbox.center[1])])
        if self.hitbox.collidepoint((900, 150)):
            if limiter.run_block_once():
                self.special_gfx = True
                self.angles = angles_360(0)
                Gfx.bg_move = True
                self.hitable = False
                self.hide_health_bar = True

    def skill_scout_force_field_fire(self):
        if self.timer_trigger(self.force_field_rate):
            location = (random.randint(0, 1600), random.randint(-100, 100))
            data.ENEMY_PROJECTILE_DATA.append(Impactor(
                speed=15,
                size=(6, 6),
                start_point=self.hitbox.center,
                damage=0,
                flag="impactor",
                gfx_idx=16,
                target=location,
                impact_effect=lambda location=location: data.ENEMY_PROJECTILE_DATA.append(Force_field(
                    location=location,
                ))
            ))
        if self.timer_trigger(1200):
            data.ITEMS.drop(self.hitbox.center, target=Event_item_boss_snare((100, 100, 200)))

# Battleship skills

    @run_limiter
    def skill_main_gun_fire_position(self, limiter):
        self.special_move = True
        if self.turn_angle < 359:
            self.special_gfx = True
            if self.timer_trigger(3):
                self.turn_angle = next(self.turn_angles_2, 359)
                if self.turn_angle != 359:  # 91 ticks zum drehen
                    self.gun_position[0] += 0.54
                    self.gun_position[1] += 0.73
            win.blit(rot_center(self.sprites[self.gfx_idx[0]], self.turn_angle), (self.hitbox.center[0] + self.gfx_hook[0], self.hitbox.center[1] + self.gfx_hook[1]))
        else:
            self.special_gfx = False

        self.hitbox.move_ip(self.angles[degrees(900, self.hitbox.center[0], 300, self.hitbox.center[1])])
        if self.hitbox.collidepoint((900, 300)):
            self.angles = angles_360(0)
            if self.health < self.max_health / 2:
                self.angles = angles_360(2)
                self.skills_lst.remove(self.skill_main_gun_fire_position)
                self.special_move = False
            # self.special_gfx = True

    @run_limiter
    def skill_radar_guided_gun(self, limiter):
        self.special_move = True
        self.hitbox.move_ip(self.angles[degrees(1700, self.hitbox.center[0], 500, self.hitbox.center[1])])

        if self.hitbox.collidepoint((1700, 500)):

            if limiter.run_block_once():
                self.angles = angles_360(0)
                self.special_gfx = True
                self.special_skills_lst.append(self.skill_point_defence)

            if self.timer_trigger(3):
                self.turn_angle = next(self.turn_angles_1, 270)
                if self.turn_angle != 270:  # 91 ticks zum drehen
                    self.gun_position[0] -= 0.54
                    self.gun_position[1] -= 0.73
            win.blit(rot_center(self.sprites[self.gfx_idx[0]], self.turn_angle), (self.hitbox.center[0] + self.gfx_hook[0], self.hitbox.center[1] + self.gfx_hook[1]))

            if self.timer_trigger(30):
                for dummy in self.dummy_targets:
                    dummy[1] += random.randint(-100, 100)
                    if dummy[1] > 1000:
                        dummy[1] = 100
                    elif dummy[1] < 100:
                        dummy[1] = 1000

                data.ENEMY_PROJECTILE_DATA.append(Projectile(
                    speed=28,
                    size=(20, 200),
                    start_point=self.hitbox.center,
                    damage=0,
                    flag="neutral",
                    gfx_idx=20,
                    target=random.choice([data.PLAYER.hitbox.center, self.dummy_targets[random.randint(0, 2)]]),
                    hit_effect=lambda l: data.ENEMY_PROJECTILE_DATA.append(Projectile(
                        speed=100,
                        size=(30, 30),
                        start_point=self.hitbox.center,
                        damage=4,
                        flag="enemy",
                        gfx_idx=18,
                        target=data.PLAYER.hitbox.center
                    )),
                    spez_gfx=lambda a: Gfx.create_effect("radar", 10, anchor=a, follow=True, x=-170, y=-30)
                ))

        else:
            if self.angles[0] == (0, 0):
                self.angles = angles_360(2)

    @run_limiter
    def skill_death_wave(self, limiter):
        if limiter.run_block_once():
            self.hide_health_bar = True
            self.special_move = True
            if self.angles[0] == (0, 0):
                self.angles = angles_360(2)
        self.hitbox.move_ip(self.angles[degrees(1000, self.hitbox.center[0], 550, self.hitbox.center[1])])

        if self.hitbox.collidepoint((1000, 550)):
            self.angles = angles_360(0)
            trigger_time = 120 + 60 * len([e for e in data.ENEMY_DATA if e.__class__.__name__ == "Boss_weakspot"])
            if self.timer_trigger(trigger_time):
                data.ENEMY_PROJECTILE_DATA.append(Explosion(
                    location=self.hitbox.center,
                    explo_size=3000,
                    damage=4,
                    explo_speed=(80, 80)
                ))
                Gfx.create_effect("circle", 3, anchor=(self.hitbox.topleft[0] - 1400, self.hitbox.topleft[1] - 1400))

            if len([e for e in data.ENEMY_DATA if e.__class__.__name__ == "Boss_weakspot"]) == 0:
                self.health = 0

    @run_limiter
    def skill_sinus_wave_gun(self, limiter):
        self.special_move = True
        self.hitbox.move_ip(self.angles[degrees(1870, self.hitbox.center[0], 500, self.hitbox.center[1])])
        # if abs(1870 - self.hitbox.center[0]) < 30 or abs(500 - self.hitbox.center[1]) < 30:
        if self.hitbox.collidepoint((1880, 500)):
            if limiter.run_block_once():
                self.angles = angles_360(0)
            if self.timer_key_delay(limit=self.sinus_delay, key="sinus"):
                if self.sinus_target is None:
                    self.sinus_target = pygame.Rect(data.PLAYER.hitbox.center[0], data.PLAYER.hitbox.center[1], 1, 1)
                self.sinus_target.move_ip(0, self.sinus_direction)
                if self.sinus_target.center[1] > 800:
                    self.sinus_direction = -2
                elif self.sinus_target.center[1] < 200:
                    self.sinus_direction = 2

                self.sin_wave_offset -= 1
                if self.sin_wave_offset < 50:
                    self.sin_wave_offset = 350

                for sp, target in [
                    (self.hitbox.topleft, (self.sinus_target.center[0], self.sinus_target.center[1] - self.sin_wave_offset)),
                    (self.hitbox.bottomleft, (self.sinus_target.center[0], self.sinus_target.center[1] + self.sin_wave_offset))
                ]:
                    data.ENEMY_PROJECTILE_DATA.append(Wave(
                        speed=40,
                        size=(5, 5),
                        start_point=sp,
                        damage=4,
                        gfx_idx=1,
                        target=target,
                        curve_size=0.2,
                        # fixed_angle=angle + random.randint(-20, 20),
                        variation=False
                    ))

                if self.timer_trigger(600):
                    data.ENEMY_PROJECTILE_DATA.append(Projectile(
                        speed=200,
                        size=(30, 30),
                        start_point=self.hitbox.center,
                        damage=4,
                        flag="enemy",
                        gfx_idx=8,
                        target=data.PLAYER.hitbox.center
                    ))

                    self.sinus_target = None
                    self.timer_key_delay(reset=True, key="sinus")
                    self.sinus_delay = 300

    def get_sinus_wave_target(self):
        return pygame.Rect(data.PLAYER.hitbox.center[0], data.PLAYER.hitbox.center[1], 1, 1)

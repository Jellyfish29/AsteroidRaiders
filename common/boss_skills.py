import pygame
import random
import astraid_data as data
from init import *
from astraid_funcs import *
from Gfx import Gfx
from projectiles import Projectile, Mine, Missile, Impactor, Explosion, Dart
from phenomenon import Gravity_well


class Boss_skills(Timer):

    def __init__(self):
        # Timer.__init__(self)
        self.missile_duration = 480
        self.missile_retarget_trigger = 90
        self.mg_angle = 0
        self.main_gun_angles = angles_360(35)
        self.salvo_start_point = iter([i for i in range(0, self.size[1], int(self.size[1] / 10))])
        self.dart_salvo_start_point = iter([i for i in range(0, self.size[1], int(self.size[1] / 5))])
        self.dart_missiles = 6
        self.jump_charge = False
        self.jump_point = 0
        self.jump_chance = 1100
        self.chaser_hit = False

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
                gfx_idx=11,
                aquisition_delay=self.missile_retarget_trigger,
                enemy_missile=True
            ))

    def skill_star_shot(self, **kwargs):
        if self.timer_trigger(self.fire_rate * 5):
            for i in range(0, 359, 22):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), self.hitbox.center, 1, "enemy", 6, angle=i))

    def skill_salvo_alpha(self, **kwargs):
        if self.timer_trigger(self.fire_rate * 3):
            for i in range(0, self.size[1], int(self.size[1] / 10)):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), (self.hitbox.topleft[0], self.hitbox.topleft[1] + i), 1, "bo_salvo", 6, angle=180))
            for i in range(0, self.size[1], int(self.size[1] / 10)):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), (self.hitbox.topright[0], self.hitbox.topright[1] + i), 1, "bo_salvo", 6, angle=0))

    def skill_salvo_bravo(self, **kwargs):
        if self.timer_trigger(self.fire_rate * 5):
            for i in range(135, 226, 9):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), self.hitbox.center, 1, "enemy", 6, angle=i))
            for i in range(0, 45, 9):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), self.hitbox.center, 1, "enemy", 6, angle=i))
            for i in range(315, 360, 9):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), self.hitbox.center, 1, "enemy", 6, angle=i))

    def skill_salvo_charlie(self, **kwargs):
        if self.timer_key_delay(limit=self.fire_rate * 3, key="salvo_c"):
            if self.trigger(5):
                shot_sp = next(self.salvo_start_point, "stop")
                if shot_sp == "stop":
                    self.salvo_start_point = iter([i for i in range(0, self.size[1], int(self.size[1] / 10))])
                    print(self.timer_calls_per_tick)
                    self.timer_key_delay(reset=True, key="salvo_c")
                else:
                    data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), (self.hitbox.topleft[0], self.hitbox.topleft[1] + shot_sp), 1, "bo_salvo", 6, angle=180))
                    data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), (self.hitbox.topright[0], self.hitbox.topright[1] + shot_sp), 1, "bo_salvo", 6, angle=0))

    def skill_volley(self, **kwargs):
        if self.timer_trigger(self.fire_rate * 3):
            for i in [-5, 0, 5]:
                data.ENEMY_PROJECTILE_DATA.append(Projectile(10, (6, 6), self.hitbox.center, 1, "benemy", 6, angle_variation=i, target=data.PLAYER.hitbox))

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

    def skill_speed_boost(self):
        if self.timer_key_delay(limit=300, key="sboost"):
            self.angles = angles_360(40)
            if self.timer_trigger(15):
                self.timer_key_delay(reset=True, key="sboost")
        else:
            self.angles = angles_360(self.speed)

    def skill_main_gun(self, target=data.PLAYER.hitbox):
        if self.timer_key_delay(limit=self.fire_rate * 6, key="main_gun"):
            data.ENEMY_PROJECTILE_DATA.append(Projectile(
                speed=50,
                size=(4, 4),
                start_point=self.hitbox.center,
                damage=0,
                flag="neutral",
                gfx_idx=7,
                target=target,
            ))
            if self.timer_trigger(60):
                data.ENEMY_PROJECTILE_DATA.append(Projectile(
                    speed=40,
                    size=(30, 30),
                    start_point=self.hitbox.center,
                    damage=4,
                    flag="enemy",
                    gfx_idx=8,
                    target=target
                ))
                self.timer_key_delay(reset=True, key="main_gun")
                if target is not data.PLAYER.hitbox:
                    self.target = (random.randint(0, winwidth), random.randint(0, winheight))

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
                        gfx_idx=15,
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
                        gfx_idx=15,
                        target=(self.hitbox.topleft[0] + 250, self.hitbox.topleft[1] + shot_sp + 10),
                        impact_effect=lambda shot_sp=shot_sp: data.ENEMY_PROJECTILE_DATA.append(Dart(
                            start_point=(self.hitbox.topright[0] + 250, self.hitbox.topright[1] + shot_sp),
                            damage=2,
                            target=data.PLAYER.hitbox
                        ))
                    ))

    def skill_dart_missile_last_stand(self):
        self.special_move = True
        self.hitbox.move_ip(self.angles[degrees(1920, self.hitbox.center[0], 500, self.hitbox.center[1])])
        if abs(1920 - self.hitbox.center[0]) < 30 or abs(500 - self.hitbox.center[1]) < 30:
            self.angles = angles_360(0)
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
                            gfx_idx=15,
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
                    target=location,
                    impact_effect=lambda location=location: data.PHENOMENON_DATA.append(Gravity_well(
                        speed=0,
                        decay=600,
                        location=location,
                        flag="enemy"
                    ))
                ))

    def skill_chaser(self):
        if not self.chaser_hit:
            self.hitbox.move_ip(self.angles[degrees(data.PLAYER.hitbox.center[0], self.hitbox.center[0], data.PLAYER.hitbox.center[1], self.hitbox.center[1])])
        else:
            if self.timer_trigger(300):
                self.chaser_hit = False
                self.special_move = True
        if self.hitbox.colliderect(data.PLAYER.hitbox):
            self.chaser_hit = True
            self.special_move = False
        if len([e for e in data.ENEMY_DATA if e.__class__.__name__ == "Boss_weakspot"]) == 0:
            self.special_move = False
            self.angles = self.orig_angles
            self.skills_lst.remove(self.skill_chaser)

    def skill_turret_defence_matrix(self):
        turret_amount = len([e.set_sp_dmg() for e in data.ENEMY_DATA if e.__class__.__name__ == "Boss_turret"])
        if turret_amount > 0:
            self.special_take_damage = lambda dmg, a=turret_amount: [e.set_health((dmg / a), (200, 0, 200)) for e in data.ENEMY_DATA]
        if self.timer_delay(limit=600):
            if turret_amount == 0:
                self.skills_lst.remove(self.skill_turret_defence_matrix)
                self.special_take_damage = None
                self.timer_delay(reset=True)

    def skill_main_gun_salvo(self):
        self.special_move = True
        self.hide_health_bar = True
        self.hitbox.move_ip(self.angles[degrees(1000, self.hitbox.center[0], 500, self.hitbox.center[1])])
        if abs(1000 - self.hitbox.center[0]) < 30 or abs(500 - self.hitbox.center[1]) < 30:
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

    def skill_missile_barrage(self):
        self.special_move = True
        self.hide_health_bar = True
        self.hitbox.move_ip(self.angles[degrees(1000, self.hitbox.center[0], 500, self.hitbox.center[1])])
        if abs(1000 - self.hitbox.center[0]) < 10 or abs(500 - self.hitbox.center[1]) < 10:
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
                    damage=3
                ))
            ))
        if len([e for e in data.ENEMY_DATA if e.__class__.__name__ == "Boss_weakspot"]) == 0:
            self.special_move = False
            self.special_attack = False
            self.hide_health_bar = False
            self.angles = angles_360(self.speed)
            self.special_skills_lst.remove(self.skill_missile_barrage)

    def skill_laser_storm(self):
        self.special_move = True
        self.hide_health_bar = True
        self.hitbox.move_ip(self.angles[degrees(1920, self.hitbox.center[0], 500, self.hitbox.center[1])])
        if abs(1920 - self.hitbox.center[0]) < 30 or abs(500 - self.hitbox.center[1]) < 30:
            self.angles = angles_360(0)
        if len([e for e in data.ENEMY_DATA if e.__class__.__name__ == "Boss_weakspot"]) == 0:
            self.special_move = False
            self.special_attack = False
            self.hide_health_bar = False
            self.angles = angles_360(self.speed)
            self.special_skills_lst.remove(self.skill_laser_storm)
            for e in data.ENEMY_DATA:
                if e.__class__.__name__ == "Boss_laser_battery":
                    e.kill = True

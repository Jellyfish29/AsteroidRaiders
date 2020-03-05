import pygame
import random

from init import *
from astraid_funcs import *
import astraid_data as data
from Gfx import Gfx, Background
from projectiles import Projectile, Mine, Explosion
from items_misc import Item_upgrade_point_crate, Item_supply_crate


class Enemy(Timer):

    asteroid_sprites = get_images("asteroids")
    spez_sprites = get_images("spez")
    boss_sprites = get_images("boss_ship")
    spez_enemy = []
    spez_spawn_table = []
    health = 2.5
    ttk_ticker = 100
    spez_spawn_time = 480

    def __init__(self, direction, speed, spawn_point, health,
                 size, gfx_idx, gfx_hook, sprites):
        self.spawn_points = {
            # Top
            1: [random.randint(100, winwidth - 100),
                random.randint(-150, -100)],
            # Bot
            2: [random.randint(100, winwidth - 100),
                random.randint(winheight + 100, winheight + 100)],
            # Left
            3: [random.randint(-150, -100),
                random.randint(0, winheight)],
            # Right
            4: [random.randint(winwidth, winwidth + 100),
                random.randint(0, winheight)]
        }
        self.targets = {1: 2, 2: 1, 3: 4, 4: 3}
        self.spawn_point = spawn_point
        self.target = self.spawn_points[self.targets[self.spawn_point]]
        Timer.__init__(self)
        self.direction = degrees(
            self.target[0], self.spawn_points[self.spawn_point][0],
            self.target[1], self.spawn_points[self.spawn_point][1]
        )
        self.angles = angles_360(speed)
        self.orig_angles = self.angles

        self.hitbox = pygame.Rect(
            self.spawn_points[spawn_point][0],
            self.spawn_points[spawn_point][1],
            size[0], size[1]
        )
        self.size = size
        self.health = health
        self.max_health = self.health
        self.healthbar_len = self.size[0]
        self.healthbar_height = 1
        self.healthbar_max_len = self.healthbar_len
        self.score_amount = speed
        self.speed = speed
        self.gfx_idx = gfx_idx
        self.gfx_hook = gfx_hook
        self.sprites = sprites
        self.gfx_speed = 16
        self.orig_direction = self.direction
        self.cced = False
        self.stunned = False
        self.cc_angles = angles_360(2)
        self.cc_time = 0
        self.kill = False
        self.border_check = True
        self.ttk_bonus = 0
        self.projectile_speed = 14
        self.hitable = True
        self.special_take_damage = None
        self.flag = "normal"
        self.fire_rate = 0
        self.buffer_hp = 0
        self.muzzle_effect_timer = (i for i in range(1))
        self.ticker.update({"player_dmg": 29})

    def move(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        self.hitbox.move_ip(self.angles[self.direction])

    def cc_move(self):
        self.hitbox.move_ip(self.cc_angles[self.direction])
        if self.timer_trigger(self.cc_time):
            self.cced = False
            self.stunned = False

    def border_collide(self):
        if rect_not_on_sreen(self.hitbox, bot=False, strict=False):
            self.kill = True

    def player_collide(self):
        if self.hitbox.colliderect(data.PLAYER.hitbox):
            # if self.flag == "boss" or self.flag == "elite":
            if any(["Bosses" in self.get_bases_names(),
                    self.get_name() == "Boss_turret",
                    self.get_name() == "Boss_weakspot"]):
                if self.timer_key_trigger(30, key="player_dmg"):
                    data.PLAYER.take_damage(1)
                    self.health -= 1
                    self.gfx_hit()
            else:
                self.gfx_hit()
                self.kill = True
                data.PLAYER.take_damage(1)

    def take_damage(self, dmg, staggered=False):
        if random.randint(0, 100) > data.PLAYER.crit_chance:
            color = (255, 255, 0)
            dmg *= 2
        else:
            color = (255, 10, 10)

        if staggered:
            if self.timer_trigger(30):
                self.set_health(dmg, color)
        elif self.special_take_damage is not None:
            self.special_take_damage(dmg)
        else:
            self.set_health(dmg, color)

    def set_health(self, hp, color):
        self.health -= hp
        if self.health > self.max_health:
            self.health = self.max_health
        self.healthbar_len -= (self.healthbar_max_len / (self.max_health / hp))

        if hp < 0:
            Gfx.create_effect(
                "dmg_text", 4,
                (self.hitbox.center[0] + random.randint(-10, 10),
                 self.hitbox.center[1] + random.randint(-10, 10)),
                hover=True, follow=True, text=abs(hp), text_size=30, text_color=(10, 255, 10)
            )

        elif hp == data.PLAYER.damage or hp == data.PLAYER.damage * 2:
            text_size = self.get_dmg_text_size(hp)
            Gfx.create_effect(
                "dmg_text", 4,
                (self.hitbox.center[0] + random.randint(-10, 10),
                 self.hitbox.center[1] + random.randint(-10, 10)),
                hover=True, follow=True, text=hp, text_size=text_size, text_color=color
            )

        elif hp < data.PLAYER.damage:
            self.buffer_hp += hp

        elif hp > data.PLAYER.damage:
            self.buffer_hp += hp

    def get_dmg_text_size(self, hp):
        p_dmg = data.PLAYER.damage
        text_size = 20
        if hp >= p_dmg:
            if p_dmg <= hp < p_dmg * 1.5:
                text_size = 25
            elif p_dmg * 1.5 <= hp < p_dmg * 2:
                text_size = 30
            elif p_dmg * 2 <= hp < p_dmg * 2.5:
                text_size = 35
            elif p_dmg * 2.5 <= hp < p_dmg * 3:
                text_size = 40
            elif p_dmg * 3 <= hp < p_dmg * 8:
                text_size = 50
            elif hp >= p_dmg * 8:
                text_size = 60
        return text_size

    def dmg_text_buffer(self):
        if self.timer_trigger(15):
            if self.buffer_hp > 0:
                text_size = self.get_dmg_text_size(self.buffer_hp)
                if self.buffer_hp > data.PLAYER.damage:
                    color = (222, 91, 22)  # de5b16
                else:
                    color = (255, 10, 10)
                Gfx.create_effect(
                    "dmg_text", 4,
                    (self.hitbox.center[0] + random.randint(-10, 10),
                     self.hitbox.center[1] + random.randint(-10, 10)),
                    hover=True, follow=True, text=self.buffer_hp, text_size=text_size, text_color=color
                )
                self.buffer_hp = 0

    def set_fire_rate(self, fr):
        self.fire_rate += fr

    def set_cc(self, s, t, stun=False):
        self.cced = True
        self.stunned = stun
        self.cc_time = t
        self.cc_angles = angles_360(s)

    def skill(self):
        pass

    def hit(self, obj):
        pass

    def destroy(self):
        return self.kill

    def gfx_health_bar(self):
        if self.health < self.max_health:
            pygame.draw.rect(win, (200, 0, 0),
                             (pygame.Rect(self.hitbox.topleft[0],
                                          self.hitbox.topleft[1] - 30,
                                          self.healthbar_max_len,
                                          self.healthbar_height
                                          )))
            if not self.healthbar_len < 0:
                pygame.draw.rect(win, (0, 200, 0),
                                 (pygame.Rect(self.hitbox.topleft[0],
                                              self.hitbox.topleft[1] - 30,
                                              self.healthbar_len,
                                              self.healthbar_height
                                              )))

    def gfx_animation(self):
        animation_ticker = self.timer_animation_ticker(self.gfx_speed)
        gfx_angle = degrees(
            self.target[1],
            self.spawn_points[self.spawn_point][1],
            self.target[0],
            self.spawn_points[self.spawn_point][0]
        )
        if animation_ticker < self.gfx_speed / 2:
            win.blit(rot_center(
                self.sprites[self.gfx_idx[0]], gfx_angle),
                (self.hitbox.topleft[0] + self.gfx_hook[0] - 50,
                 self.hitbox.topleft[1] + self.gfx_hook[1] - 50)
            )
        else:
            win.blit(rot_center(
                self.sprites[self.gfx_idx[1]], gfx_angle),
                (self.hitbox.topleft[0] + self.gfx_hook[0] - 50,
                 self.hitbox.topleft[1] + self.gfx_hook[1] - 50)
            )

    def gfx_hit(self):
        Gfx.create_effect(
            "explosion_2", 2,
            (self.hitbox.topleft[0] - 120, self.hitbox.topleft[1] - 130),
            explo=True
        )

    def drops(self):
        it.Items.drop(
            (self.hitbox.topleft), target=it.Item_upgrade_point_crate((100, 100, 100))
        )

    def death(self):
        data.LEVELS.elite_spawn_time -= Enemy.ttk_ticker + self.ttk_bonus
        Enemy.ttk_ticker = 100
        data.TURRET.overdrive()
        self.gfx_hit()
        data.LEVELS.interval_score += self.score_amount
        data.LEVELS.display_score += self.score_amount
        if self.buffer_hp > 0:
            text_size = self.get_dmg_text_size(self.buffer_hp)
            if self.buffer_hp > data.PLAYER.damage:
                color = (222, 91, 22)  # de5b16
            else:
                color = (255, 10, 10)
            Gfx.create_effect(
                "dmg_text", 4,
                (self.hitbox.center[0] + random.randint(-10, 10),
                 self.hitbox.center[1] + random.randint(-10, 10)),
                hover=True, follow=True, text=self.buffer_hp, text_size=text_size, text_color=color
            )

        self.kill = True

    def get_class(self):
        return self.__class__

    def get_name(self):
        return self.__class__.__name__

    def get_bases_names(self):
        return [base.__name__ for base in self.__class__.__bases__]

    def tick(self):
        self.gfx_animation()
        self.gfx_health_bar()
        self.dmg_text_buffer()
        if not self.cced:
            self.move()
        else:
            self.cc_move()
        if self.border_check:
            self.border_collide()
        if not data.GROUND:
            self.player_collide()
        if not self.stunned:
            self.skill()
        data.TURRET.missile_aquisition(self)
        data.TURRET.point_defence(self.hitbox)
        if any([self.get_name() == "Boss_turret"]):
            self.guns_gfx_animation()
            self.gun_gfx_idx_update()
        if self.health <= 0:
            self.death()
        self.timer_tick()

    @classmethod
    def set_spawn_table(cls, e):
        cls.spez_spawn_table.append(e)

    @classmethod
    @timer
    def update(cls, timer):

        if Enemy.ttk_ticker > 0:
            Enemy.ttk_ticker -= 0.4

        if not any((
            data.LEVELS.boss_fight,
            data.LEVELS.elite_fight,
            data.LEVELS.after_boss,
            data.LEVELS.special_events
        )):
            if len([e for e in data.ENEMY_DATA if isinstance(e, Asteroid)]) < data.LEVELS.asteroid_enemy_amount:
                data.ENEMY_DATA.append(Asteroid())
            if Background.y == 1070:
                for _ in range(data.LEVELS.mining_ast_enemy_amount):
                    m_ast = Mining_asteroid(spawn=get_random_top_point())
                    data.ENEMY_DATA.append(m_ast)
                    for _ in range(data.LEVELS.extractor_enemy_amount):
                        loc = random.choice([
                            (m_ast.hitbox.topleft[0] + random.randint(-20, 20), m_ast.hitbox.topleft[1] + random.randint(-20, 20)),
                            (m_ast.hitbox.topright[0] + random.randint(-20, 20), m_ast.hitbox.topright[1] + random.randint(-20, 20)),
                            (m_ast.hitbox.bottomleft[0] + random.randint(-20, 20), m_ast.hitbox.bottomleft[1] + random.randint(-20, 20)),
                            (m_ast.hitbox.bottomright[0] + random.randint(-20, 20), m_ast.hitbox.bottomright[1] + random.randint(-20, 20))
                        ])
                        data.ENEMY_DATA.append(Extractor(target=m_ast.hitbox, spawn=loc, ast=m_ast))
            if timer.trigger(Enemy.spez_spawn_time):
                data.ENEMY_DATA.append(random.choice(cls.spez_spawn_table)())


data.ENEMY = Enemy


class Asteroid(Enemy):

    def __init__(self, spawn=1, target=None):
        # if spawn is None:
        #     spawn = random.randint(1, 4)
        super().__init__(
            random.randint(0, 360),
            random.randint(2, 8),
            spawn,
            Enemy.health * 0.50,
            (80, 80),
            0,
            (0, 0),
            Enemy.asteroid_sprites
        )
        if target is not None:
            self.target = target
            self.direction = degrees(
                self.target[0], self.spawn_points[self.spawn_point][0],
                self.target[1], self.spawn_points[self.spawn_point][1]
            )
        self.score_amount = 1
        if self.speed >= 6:
            self.score_amount = 2
        self.gfx_offset = [8 * i for i in range(8)]
        self.gfx_idx = random.choice([0, 4, 64, 68])
        self.orig_gfx_idx = self.gfx_idx
        self.frame_counter = 0
        self.animation_speed = 3  # 10 - self.speed
        # if self.animation_speed > 6:
        #     self.animation_speed = 6

    def gfx_animation(self):
        """Weil die Bilder in eine beschissenne reinfolge sind
           muss der schmutz hier gemacht werden Big OOF"""
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        win.blit(
            Enemy.asteroid_sprites[self.gfx_idx + self.gfx_offset[self.frame_counter]],
            (self.hitbox.topleft[0] - 25, self.hitbox.topleft[1] - 25)
        )
        if self.trigger(self.animation_speed):
            self.frame_counter += 1
            if self.frame_counter == 8:
                self.gfx_idx += 1
                self.frame_counter = 0
            if self.gfx_idx > self.orig_gfx_idx + 3:
                self.gfx_idx = self.orig_gfx_idx


class Jumper(Enemy):

    def __init__(self, spawn=None):
        if spawn is None:
            spawn = random.randint(1, 4)
        super().__init__(
            random.randint(0, 360),
            random.randint(2, 8),
            spawn,
            Enemy.health,
            (70, 70),
            0,
            (-40, -40),
            Enemy.asteroid_sprites
        )
        self.score_amount = 8
        self.ttk_bonus = 30
        self.animation_speed = {
            self.speed + 1 - i: i * 15 for i in range(1, self.speed + 1)
        }[self.speed]

    def gfx_animation(self):
        animation_ticker = self.timer_animation_ticker(
            self.animation_speed * len(Enemy.asteroid_sprites)
        )
        if animation_ticker == (self.animation_speed * len(Enemy.asteroid_sprites)):  # 480
            self.gfx_idx = 0
        if animation_ticker % self.animation_speed == 0:
            self.gfx_idx += 1
            if self.gfx_idx == len(Enemy.asteroid_sprites):
                self.gfx_idx = 0
        win.blit(
            Enemy.asteroid_sprites[self.gfx_idx],
            (self.hitbox.topleft[0] - 8,
             self.hitbox.topleft[1] - 15)
        )
        if self.timer_trigger(60):
            Gfx.create_effect("lightning", 8, anchor=self.hitbox, follow=True, x=-30, y=-30)

    def skill(self):
        if self.timer_trigger(35):
            self.direction = random.randint(0, 359)


class Shooter(Enemy):

    def __init__(self, spawn=None):
        if spawn is None:
            spawn = random.randint(1, 4)
        super().__init__(
            random.randint(0, 359),
            random.randint(4, 6),
            spawn,
            Enemy.health + 2,
            (80, 80),
            (7, 8),
            (0, 0),
            Enemy.spez_sprites
        )

        self.score_amount = 10
        self.shot_angles = angles_360(8)
        self.fire_rate = random.randint(80, 140)
        self.ttk_bonus = 40

        # self.hitbox.move_ip(self.angles[self.direction])
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)

    def skill(self):
        if len([a for a in data.PLAYER_DATA if a.hitable]) == 0:
            target = data.PLAYER.hitbox.center
        else:
            target = random.choices([
                data.PLAYER_DATA[random.randint(0, len(data.PLAYER_DATA) - 1)].hitbox.center,
                data.PLAYER.hitbox.center], weights=[80, 20], k=1)[0]

        if self.timer_trigger(self.fire_rate):
            angle_variation = random.choices([-20, 0, 20], [10, 80, 10], k=1)[0]
            self.muzzle_effect_timer = (i for i in range(8))
            data.ENEMY_PROJECTILE_DATA.append(Projectile(
                speed=self.projectile_speed,
                size=(6, 6),
                start_point=self.hitbox.center,
                damage=1,
                flag="spez_enemy",
                gfx_idx=12,
                target=target,
                angle_variation=angle_variation
            ))


class Seeker(Enemy):

    def __init__(self, spawn=None):
        if spawn is None:
            spawn = random.randint(1, 4)
        super().__init__(
            random.randint(0, 360),
            4,
            spawn,
            Enemy.health + 2,
            (80, 80),
            (2, 3),
            (-10, -10),
            Enemy.spez_sprites
        )
        self.score_amount = 8
        self.ttk_bonus = 20
        self.target = data.PLAYER.hitbox

    def skill(self):
        if self.trigger(30):
            Gfx.create_effect(
                "smoke1", 4, anchor=self.hitbox, follow=True, x=-50, y=-50
            )
        self.direction = degrees(
            data.PLAYER.hitbox.center[0],
            self.spawn_points[self.spawn_point][0],
            data.PLAYER.hitbox.center[1],
            self.spawn_points[self.spawn_point][1]
        )
        if any([abs(data.PLAYER.hitbox.center[0] - self.hitbox.center[0]) > 20,
                abs(data.PLAYER.hitbox.center[1] - self.hitbox.center[1]) > 20]):
            self.spawn_points[self.spawn_point][0] = self.hitbox.center[0]
            self.spawn_points[self.spawn_point][1] = self.hitbox.center[1]


class Strafer(Enemy):

    def __init__(self, spawn=None):
        if spawn is None:
            spawn = random.randint(1, 4)
        super().__init__(
            random.randint(0, 360),
            8,
            spawn,
            Enemy.health + 2,
            (80, 80),
            (0, 1),
            (0, 0),
            Enemy.spez_sprites
        )
        self.score_amount = 12
        self.shot_angles = angles_360(12)
        self.fire_rate = 35
        self.ttk_bonus = 40

    def skill(self):
        if self.timer_trigger(self.fire_rate):
            data.ENEMY_PROJECTILE_DATA.append(Projectile(
                speed=25,
                size=(6, 6),
                start_point=self.hitbox.center,
                damage=1,
                flag="spez_enemy",
                gfx_idx=12,
                angle=self.direction
            ))


class Miner(Enemy):

    def __init__(self, spawn=None):
        if spawn is None:
            spawn = random.randint(1, 4)
        super().__init__(
            0,
            5,
            spawn,
            Enemy.health + 2,
            (80, 80),
            (4, 5),
            (-30, -30),
            Enemy.spez_sprites
        )
        self.score_amount = 10
        self.fire_rate = 100
        self.ttk_bonus = 50
        self.delays = (i for i in range(500, 0, -100))

    def skill(self):
        if self.timer_trigger(self.fire_rate):
            delay = next(self.delays, -1)
            if delay > -1:
                data.ENEMY_PROJECTILE_DATA.append(Explosion(
                    location=self.hitbox.center,
                    explo_size=200,
                    damage=1,
                    explo_delay=delay,
                    explosion_effect=lambda loc: Gfx.create_effect(
                        "explosion_3", 1, (loc[0] - 300, loc[1] - 300), explo=True),
                    explo_speed=(50, 50),
                    gfx_idx=22
                ))


class Mine_layer(Enemy):

    def __init__(self, spawn=None):
        if spawn is None:
            spawn = random.randint(1, 4)
        super().__init__(
            0,
            4,
            spawn,
            Enemy.health + 2,
            (80, 80),
            (9, 10),
            (0, 0),
            Enemy.spez_sprites
        )
        self.score_amount = 11
        self.fire_rate = 180
        self.ttk_bonus = 50

    def skill(self):
        if self.timer_trigger(self.fire_rate):
            data.ENEMY_PROJECTILE_DATA.append(Mine(
                speed=12,
                start_point=self.hitbox.center,
                damage=1,
                flag="en_mine",
                decay=True
            ))


class Mining_asteroid(Enemy):

    def __init__(self, spawn=None):
        super().__init__(0, 0, 1, Enemy.health * 2, (80, 80), None, (0, 0), Enemy.asteroid_sprites)
        self.gfx_idx = random.randint(0, 100)
        self.score_amount = 1
        if spawn is not None:
            self.hitbox.center = spawn

    def move(self):
        if Background.bg_move:
            self.hitbox.move_ip(0, Background.scroll_speed)

    def border_collide(self):
        if rect_not_on_sreen(self.hitbox, bot=True, strict=False):
            self.kill = True

    def gfx_animation(self):
        # pygame.draw.rect(win, (255, 255, 255), self.hitbox)
        win.blit(self.sprites[self.gfx_idx], (self.hitbox.topleft[0] - 30, self.hitbox.topleft[1] - 30))
        if self.trigger(30):
            Gfx.create_effect(
                "smoke1", 4, anchor=self.hitbox, follow=True, x=-50, y=-50
            )


class Extractor(Enemy):

    def __init__(self, target=None, spawn=None, ast=None):
        super().__init__(0, 3, 1, Enemy.health * 0.3, (40, 40), (18, 19), (15, 15), Enemy.spez_sprites)
        self.gfx_speed = random.randint(30, 90)
        self.orig_gfx_speed = self.gfx_speed
        self.target = target
        self.ast = ast
        self.zero_angles = angles_360(0)
        self.orig_angles = angles_360(3)
        self.hitbox.center = spawn
        self.score_amount = 0.5
        self.bg_speed = Background.scroll_speed
        self.atk_cd = False
        try:
            while any([self.hitbox.colliderect(e.hitbox) for e in data.ENEMY_DATA if isinstance(e, Extractor)]):
                self.hitbox.move_ip(random.randint(-10, 10), random.randint(-10, 10))
        except IndexError:
            pass

    def move(self):
        if Background.bg_move:
            self.hitbox.move_ip(0, self.bg_speed)

    def border_collide(self):
        if rect_not_on_sreen(self.hitbox, bot=True, strict=False):
            self.kill = True

    def gfx_animation(self):
        # pygame.draw.rect(win, (255, 0, 255), self.hitbox)
        animation_ticker = self.timer_animation_ticker(self.gfx_speed)
        gfx_angle = degrees(
            self.target[1],
            self.hitbox.center[1],
            self.target[0],
            self.hitbox.center[0]
        )
        if animation_ticker < self.gfx_speed / 2:
            win.blit(rot_center(
                self.sprites[self.gfx_idx[0]], gfx_angle),
                (self.hitbox.topleft[0] + self.gfx_hook[0] - 50,
                 self.hitbox.topleft[1] + self.gfx_hook[1] - 50)
            )
        else:
            win.blit(rot_center(
                self.sprites[self.gfx_idx[1]], gfx_angle),
                (self.hitbox.topleft[0] + self.gfx_hook[0] - 50,
                 self.hitbox.topleft[1] + self.gfx_hook[1] - 50)
            )

    def gfx_hit(self):
        Gfx.create_effect(
            "explosion_4", 2,
            (self.hitbox.topleft[0] - 80, self.hitbox.topleft[1] - 80),
            explo=True
        )

    def skill(self):
        if get_distance(self, data.PLAYER) < 300 or self.ast.kill:
            self.bg_speed = 0
            self.gfx_idx = (20, 21)
            self.gfx_speed = 14
            self.target = data.PLAYER.hitbox
            self.direction = degrees(
                data.PLAYER.hitbox.center[0],
                self.hitbox.center[0],
                data.PLAYER.hitbox.center[1],
                self.hitbox.center[1]
            )
            self.hitbox.move_ip(self.angles[self.direction])

            if self.hitbox.colliderect(data.PLAYER.hitbox):
                self.angles = self.zero_angles
                self.gfx_idx = (18, 19)
                if not self.atk_cd:
                    if self.timer_key_trigger(20, key="atk_delay"):
                        data.PLAYER.take_damage(1)
                        self.atk_cd = True
            else:
                self.angles = self.orig_angles

            if self.atk_cd:
                if self.timer_key_trigger(120, key="melee_atk_speed"):
                    self.atk_cd = False
        else:
            self.bg_speed = Background.scroll_speed
            self.gfx_idx = (18, 19)
            self.gfx_speed = self.orig_gfx_speed

    def player_collide(self):
        pass


spez_spawn_table = [Jumper, Seeker]

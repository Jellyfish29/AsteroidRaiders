import pygame
import random

from init import *
from astraid_funcs import *
import astraid_data as data
from Gfx import Gfx
from projectiles import Projectile, Mine, Explosion
from items_misc import Event_item_battleship_heal


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
        self.orig_direction = self.direction
        self.kill = False
        self.border_ckeck = True
        self.ttk_bonus = 0
        self.projectile_speed = 20
        self.hitable = True
        self.special_take_damage = None
        self.flag = "normal"
        self.fire_rate = 0
        self.buffer_hp = 0
        self.muzzle_effect_timer = (i for i in range(1))

    def move(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        self.hitbox.move_ip(self.angles[self.direction])
        if self.direction != self.orig_direction:
            if self.timer_key_trigger(1, key="collsion"):
                self.direction = self.orig_direction

    def border_collide(self):
        if rect_not_on_sreen(self.hitbox, bot=False, strict=False):
            self.kill = True

    def player_collide(self):
        if self.hitbox.colliderect(data.PLAYER.hitbox):
            self.gfx_hit()
            if self.flag == "boss" or self.flag == "elite":
                data.PLAYER.take_damage(0.05)
            else:
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
        self.healthbar_len -= (self.healthbar_max_len / (self.max_health / hp))
        if hp >= 0.5:
            Gfx.create_effect(
                "dmg_text", 4,
                (self.hitbox.center[0] + random.randint(-10, 10),
                 self.hitbox.center[1] + random.randint(-10, 10)),
                hover=True, follow=True, text=hp, text_color=color
            )
        elif hp < 0:
            Gfx.create_effect(
                "dmg_text", 4,
                (self.hitbox.center[0] + random.randint(-10, 10),
                 self.hitbox.center[1] + random.randint(-10, 10)),
                hover=True, follow=True, text=hp, text_color=color
            )
        else:
            self.dmg_text_buffer(hp)
        if self.health > self.max_health:
            self.health = self.max_health
            if self.buffer_hp > 0:
                self.dmg_text_buffer(0, force=True)

    def dmg_text_buffer(self, hp, force=False):
        self.buffer_hp += hp
        if self.buffer_hp >= 1.5 or force:
            Gfx.create_effect(
                "dmg_text", 4,
                (self.hitbox.center[0] + random.randint(-10, 10),
                 self.hitbox.center[1] + random.randint(-10, 10)),
                hover=True, follow=True, text=self.buffer_hp, text_color=(255, 10, 10)
            )
            self.buffer_hp = 0

    def set_fire_rate(self, fr):
        self.fire_rate += fr

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
        animation_ticker = self.timer_animation_ticker(16)
        gfx_angle = degrees(
            self.target[1],
            self.spawn_points[self.spawn_point][1],
            self.target[0],
            self.spawn_points[self.spawn_point][0]
        )
        if animation_ticker < 8:
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
            (self.hitbox.topleft), target=it.Item_upgrade_point_drop((100, 100, 100))
        )

    def death(self):
        data.LEVELS.elite_spawn_time -= Enemy.ttk_ticker + self.ttk_bonus
        Enemy.ttk_ticker = 100
        data.TURRET.overdrive()
        self.gfx_hit()
        data.LEVELS.interval_score += self.score_amount
        data.LEVELS.display_score += self.score_amount

        self.kill = True

    def get_name(self):
        return self.__class__.__name__

    def tick(self):
        self.gfx_animation()
        self.gfx_health_bar()
        self.move()
        if self.border_ckeck:
            self.border_collide()
        self.player_collide()
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
            if len(data.ENEMY_DATA) < data.LEVELS.enemy_amount:
                data.ENEMY_DATA.append(Asteroid())
            if timer.trigger(Enemy.spez_spawn_time):
                data.ENEMY_DATA.append(random.choice(cls.spez_spawn_table)())


data.ENEMY = Enemy


class Asteroid(Enemy):

    def __init__(self, spawn=1):
        # if spawn is None:
        #     spawn = random.randint(1, 4)
        super().__init__(
            random.randint(0, 360),
            random.randint(2, 8),
            spawn,
            Enemy.health,
            (80, 80),
            0,
            (0, 0),
            Enemy.asteroid_sprites
        )
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
        self.score_amount = 7
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
            (0, 1),
            (0, 0),
            Enemy.spez_sprites
        )

        self.score_amount = 8
        self.shot_angles = angles_360(8)
        self.fire_rate = random.randint(80, 140)
        self.ttk_bonus = 40

        self.hitbox.move_ip(self.angles[self.direction])
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)

    def skill(self):
        # print(f"shooter {self.timer_calls_per_tick}")
        if len(data.PLAYER_DATA) == 0:
            target = data.PLAYER.hitbox.center
        else:
            target = random.choices([
                data.PLAYER_DATA[random.randint(0, len(data.PLAYER_DATA) - 1)].hitbox.center,
                data.PLAYER.hitbox.center], weights=[80, 20], k=1)[0]

        if self.timer_trigger(self.fire_rate):
            self.muzzle_effect_timer = (i for i in range(8))
            data.ENEMY_PROJECTILE_DATA.append(Projectile(
                speed=self.projectile_speed,
                size=(6, 6),
                start_point=self.hitbox.center,
                damage=1,
                flag="spez_enemy",
                gfx_idx=12,
                target=target
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
        self.score_amount = 6
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
            (7, 8),
            (0, 0),
            Enemy.spez_sprites
        )
        self.score_amount = 10
        self.shot_angles = angles_360(12)
        self.fire_rate = 20
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
        self.score_amount = 8
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
        self.score_amount = 8
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


class Comet(Enemy):
    def __init__(self,):
        super().__init__(
            0,
            20,
            1,
            Enemy.health,
            (60, 60),
            (13, 13),
            (-50, -50),
            Enemy.spez_sprites
        )
        self.hitable = False
        self.score_amount = 8
        self.fire_rate = 180
        self.ttk_bonus = 50


spez_spawn_table = [Jumper, Seeker]


# Event Ships

class Event_shooter(Shooter):

    def __init__(self, dest, spawn=None):
        if spawn is None:
            spawn = random.randint(1, 4)
        super().__init__(spawn=spawn)
        self.dest = dest
        self.gfx_hook = (-50, -50)
        self.border_ckeck = False

    def move(self):
        self.hitbox.move_ip(self.angles[degrees(
            self.dest[0], self.hitbox.center[0],
            self.dest[1], self.hitbox.center[1]
        )])

        if self.hitbox.collidepoint(self.dest):
            self.angles = angles_360(0)
            self.gfx_idx = (14, 14)

    def gfx_animation(self):
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)
        animation_ticker = self.timer_animation_ticker(8)

        if len(data.PLAYER_DATA) > 0:
            target = data.PLAYER_DATA[0].hitbox.center
        else:
            target = data.PLAYER.hitbox.center

        gfx_angle = degrees(
            target[1],
            self.hitbox.center[1],
            target[0],
            self.hitbox.center[0]
        )

        if animation_ticker < 4:
            win.blit(rot_center(
                self.sprites[self.gfx_idx[0]], gfx_angle),
                (self.hitbox.topleft[0] + self.gfx_hook[0],
                 self.hitbox.topleft[1] + self.gfx_hook[1])
            )
        else:
            win.blit(rot_center(
                self.sprites[self.gfx_idx[1]], gfx_angle),
                (self.hitbox.topleft[0] + self.gfx_hook[0],
                 self.hitbox.topleft[1] + self.gfx_hook[1])
            )


class Event_supply_ship(Shooter):

    def __init__(self):
        super().__init__()
        self.gfx_idx = (11, 12)

    def skill(self):
        pass

    def death(self):
        data.TURRET.overdrive()
        self.gfx_hit()
        data.ITEMS.drop(self.hitbox.topleft, target=Event_item_battleship_heal((100, 100, 200)))
        self.kill = True

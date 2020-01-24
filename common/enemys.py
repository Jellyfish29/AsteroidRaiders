import pygame
import random

from init import *
from astraid_funcs import *
import astraid_data as data
from Gfx import Gfx
from projectiles import Projectile, Mine, Explosion


class Enemy(Timer):

    asteroid_sprites = get_images("asteroids")
    spez_sprites = get_images("spez")
    boss_sprites = get_images("boss_ship")
    spez_enemy = []
    spez_spawn_table = []
    health = 2.6
    ttk_ticker = 100
    spez_spawn_time = 420

    def __init__(self, direction, speed, spawn_point, health, size, gfx_idx, gfx_hook, sprites):
        self.spawn_points = {
            1: [random.randint(100, winwidth - 50), random.randint(-150, -50)],  # Top
            2: [random.randint(100, winwidth - 50), random.randint(winheight + 50, winheight + 100)],  # Bot
            3: [random.randint(-150, -100), random.randint(0, winheight)],  # random.random.randint(0, winheight)),  # Left
            4: [random.randint(winwidth, winwidth + 50), random.randint(0, winheight)]  # Right
        }
        Timer.__init__(self)
        self.spawn_point = spawn_point
        self.direction = direction
        self.angles = angles_360(speed)
        self.orig_angles = self.angles
        self.hitbox = pygame.Rect(self.spawn_points[spawn_point][0], self.spawn_points[spawn_point][1], size[0], size[1])
        self.health = health
        self.max_health = self.health
        self.healthbar_len = 70
        self.healthbar_height = 1
        self.healthbar_max_len = self.healthbar_len
        self.score_amount = speed
        self.speed = speed
        self.gfx_idx = gfx_idx
        self.gfx_hook = gfx_hook
        self.sprites = sprites
        self.kill = False
        self.ttk_bonus = 0
        self.projectile_speed = 14
        self.hitable = True
        self.special_take_damage = None
        self.flag = "normal"

    def move(self):
        self.hitbox.move_ip(self.angles[int(self.direction)])
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)

    def border_collide(self):
        if rect_not_on_sreen(self.hitbox, bot=False, strict=False):
            self.kill = True

    def player_collide(self):
        if self.hitbox.colliderect(data.PLAYER.hitbox):
            Gfx.create_effect("enexplo", 5, (self.hitbox.topleft[0] - 20, self.hitbox.topleft[1] - 30))
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
            if self.timer_trigger(60):
                self.set_health(dmg, color)
        elif self.special_take_damage is not None:
            self.special_take_damage(dmg)
        else:
            self.set_health(dmg, color)

    def set_health(self, hp, color):
        self.health -= hp
        self.healthbar_len -= (self.healthbar_max_len / (self.max_health / hp))
        Gfx.create_effect("dmg_txt", 4, (self.hitbox.center[0] + random.randint(-10, 10), self.hitbox.center[1] + random.randint(-10, 10)), hover=True, follow=True, dmg_text=hp, text_color=color)

    def skill(self):
        pass

    def hit(self, obj):
        pass

    def destroy(self):
        return self.kill

    def gfx_health_bar(self):
        if self.health < self.max_health:
            pygame.draw.rect(win, (200, 0, 0), (pygame.Rect(self.hitbox.topleft[0], self.hitbox.topleft[1] - 30, self.healthbar_max_len, self.healthbar_height)))
            if not self.healthbar_len < 0:
                pygame.draw.rect(win, (0, 200, 0), (pygame.Rect(self.hitbox.topleft[0], self.hitbox.topleft[1] - 30, self.healthbar_len, self.healthbar_height)))

    def gfx_animation(self):
        animation_ticker = self.timer_animation_ticker(10)
        if animation_ticker < 4:
            win.blit(self.sprites[self.gfx_idx[0]], (self.hitbox.center[0] + self.gfx_hook[0], self.hitbox.center[1] + self.gfx_hook[1]))
        else:
            win.blit(self.sprites[self.gfx_idx[1]], (self.hitbox.center[0] + self.gfx_hook[0], self.hitbox.center[1] + self.gfx_hook[1]))

    def gfx_hit(self):
        Gfx.create_effect("enexplo", 5, (self.hitbox.topleft[0] - 20, self.hitbox.topleft[1] - 30))

    def drops(self):
        it.Items.drop((self.hitbox.topleft), target=it.Item_upgrade_point_drop((100, 100, 100)))

    def death(self):
        data.LEVELS.elite_spawn_time -= Enemy.ttk_ticker + self.ttk_bonus
        Enemy.ttk_ticker = 100
        data.TURRET.overdrive()
        self.gfx_hit()  # Gfx.create_effect("enexplo", 5, (self.hitbox.topleft[0] - 20, self.hitbox.topleft[1] - 30))
        data.LEVELS.interval_score += self.score_amount
        data.LEVELS.display_score += self.score_amount

        self.kill = True

    def tick(self):
        self.gfx_animation()
        self.gfx_health_bar()
        self.move()
        self.border_collide()
        self.player_collide()
        self.skill()
        data.TURRET.missile_aquisition(self)
        data.TURRET.point_defence(self.hitbox)
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

        if not any((data.LEVELS.boss_fight, data.LEVELS.elite_fight, data.LEVELS.after_boss)):
            # if len(data.ENEMY_DATA) == 0:
            #     data.ENEMY_DATA.append(Asteroid())
            if len(data.ENEMY_DATA) < data.LEVELS.enemy_amount:
                data.ENEMY_DATA.append(Asteroid())
                # data.ENEMY_DATA.append(*random.random.choices([Asteroid(), Jumper(), Shooter(), Seeker(), Strafer(), Miner(), Mine_layer()], weights=[70, c, c, c, c, c, c]))
                # data.ENEMY_DATA.append(Shooter())
            if timer.trigger(Enemy.spez_spawn_time):
                data.ENEMY_DATA.append(random.choice(cls.spez_spawn_table)())


data.ENEMY = Enemy


class Asteroid(Enemy):

    # direction, speed, spawn_point, health, size, gfx_idx, gfx_hook
    def __init__(self, event=False):
        super().__init__(random.randint(0, 360), random.randint(2, 8), random.randint(1, 4), Enemy.health, (80, 80), 0, (0, 0), Enemy.asteroid_sprites)
        self.animation_speed = {self.speed + 1 - i: i * 15 for i in range(1, self.speed + 1)}[self.speed]

    def gfx_animation(self):
        animation_ticker = self.timer_animation_ticker(self.animation_speed * len(Enemy.asteroid_sprites))
        if animation_ticker == (self.animation_speed * len(Enemy.asteroid_sprites)):  # 480
            self.gfx_idx = 0
        if animation_ticker % self.animation_speed == 0:
            self.gfx_idx += 1
            if self.gfx_idx == len(Enemy.asteroid_sprites):
                self.gfx_idx = 0
        win.blit(Enemy.asteroid_sprites[self.gfx_idx], (self.hitbox.topleft[0] - 8, self.hitbox.topleft[1] - 15))


class Jumper(Enemy):

    def __init__(self):
        super().__init__(random.randint(0, 360), random.randint(2, 8), random.randint(1, 4), Enemy.health, (70, 70), 0, (0, 0), Enemy.asteroid_sprites)
        self.score_amount = 7
        self.ttk_bonus = 30
        self.animation_speed = {self.speed + 1 - i: i * 15 for i in range(1, self.speed + 1)}[self.speed]

    def gfx_animation(self):
        animation_ticker = self.timer_animation_ticker(self.animation_speed * len(Enemy.asteroid_sprites))
        if animation_ticker == (self.animation_speed * len(Enemy.asteroid_sprites)):  # 480
            self.gfx_idx = 0
        if animation_ticker % self.animation_speed == 0:
            self.gfx_idx += 1
            if self.gfx_idx == len(Enemy.asteroid_sprites):
                self.gfx_idx = 0
        win.blit(Enemy.asteroid_sprites[self.gfx_idx], (self.hitbox.topleft[0] - 8, self.hitbox.topleft[1] - 15))

    def skill(self):
        if self.timer_trigger(35):
            self.direction = random.randint(0, 359)


class Shooter(Enemy):

    def __init__(self):
        super().__init__(0, random.randint(4, 6), random.randint(1, 4), Enemy.health + 2, (80, 80), 0, (0, 0), Enemy.spez_sprites)
        self.score_amount = 8
        for sp, direction, gfx_idx, gfx_hook in [(1, 90, (2, 3), (-30, -70)), (2, 270, (6, 7), (-30, -70)), (3, 359, (0, 1), (-70, -30)), (4, 180, (4, 5), (-70, -30))]:
            if self.spawn_point == sp:
                self.direction = direction
                self.gfx_idx = gfx_idx
                self.gfx_hook = gfx_hook
        self.shot_angles = angles_360(8)
        self.fire_rate = random.randint(80, 140)
        self.ttk_bonus = 40

    def skill(self):
        # print(f"shooter {self.timer_calls_per_tick}")
        if self.timer_trigger(self.fire_rate):
            data.ENEMY_PROJECTILE_DATA.append(Projectile(
                speed=self.projectile_speed,
                size=(6, 6),
                start_point=self.hitbox.center,
                damage=1,
                flag="spez_enemy",
                gfx_idx=6,
                target=data.PLAYER.hitbox.center
            ))


class Seeker(Enemy):

    def __init__(self):
        super().__init__(random.randint(0, 360), 4, random.randint(1, 4), Enemy.health + 2, (80, 80), (8, 9), (-40, -30), Enemy.spez_sprites)
        self.score_amount = 6
        self.ttk_bonus = 20

    def skill(self):
        self.direction = degrees(data.PLAYER.hitbox.center[0], self.spawn_points[self.spawn_point][0], data.PLAYER.hitbox.center[1], self.spawn_points[self.spawn_point][1])
        if abs(data.PLAYER.hitbox.center[0] - self.hitbox.center[0]) > 20 or abs(data.PLAYER.hitbox.center[1] - self.hitbox.center[1]) > 20:
            self.spawn_points[self.spawn_point][0] = self.hitbox.center[0]
            self.spawn_points[self.spawn_point][1] = self.hitbox.center[1]


class Strafer(Enemy):

    def __init__(self):
        super().__init__(random.randint(0, 360), 8, random.randint(1, 4), Enemy.health + 2, (80, 80), (2, 3), (0, 0), Enemy.spez_sprites)
        self.score_amount = 10
        self.shot_angles = angles_360(12)
        self.fire_rate = 20
        self.ttk_bonus = 40

    def skill(self):
        if self.timer_trigger(self.fire_rate):
            data.ENEMY_PROJECTILE_DATA.append(Projectile(
                speed=20,
                size=(6, 6),
                start_point=self.hitbox.center,
                damage=1,
                flag="spez_enemy",
                gfx_idx=6,
                angle=self.direction
            ))


class Miner(Enemy):

    def __init__(self):
        super().__init__(0, 5, random.randint(3, 4), Enemy.health + 2, (80, 80), 0, (0, 0), Enemy.spez_sprites)
        self.score_amount = 8
        for sp, direction, gfx_idx, gfx_hook in [(3, 359, (0, 1), (-70, -30)), (4, 180, (4, 5), (-70, -30))]:
            if self.spawn_point == sp:
                self.direction = direction
                self.gfx_idx = gfx_idx
                self.gfx_hook = gfx_hook
        self.fire_rate = 100
        self.ttk_bonus = 50
        self.delays = iter([540, 420, 300, 180, 60, 0])

    def skill(self):
        if self.timer_trigger(self.fire_rate):
            data.ENEMY_PROJECTILE_DATA.append(Explosion(
                loation=self.hitbox.center,
                explo_size=200,
                damage=1,
                explo_delay=next(self.delays)
            ))


class Mine_layer(Enemy):

    def __init__(self):
        super().__init__(0, 2, random.randint(1, 2), Enemy.health + 2, (80, 80), 0, (0, 0), Enemy.spez_sprites)
        self.score_amount = 8
        for sp, direction, gfx_idx, gfx_hook in [(1, 90, (2, 3), (-30, -70)), (2, 270, (6, 7), (-30, -70))]:
            if self.spawn_point == sp:
                self.direction = direction
                self.gfx_idx = gfx_idx
                self.gfx_hook = gfx_hook
        self.fire_rate = 150
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


spez_spawn_table = [Jumper, Seeker]

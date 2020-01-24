import pygame
from pygame.locals import *

from init import *
from astraid_funcs import *
from Gfx import Gfx
import astraid_data as data
from projectiles import Projectile, Missile
from items import Item_shield, Item_jump_drive, Item_afterburner, Active_Items


class Player:

    hitbox = pygame.Rect(winwidth / 2, winheight / 2, 70, 50)
    flag = "player"

    # Health
    health = 5
    max_health = 5
    raw_max_health = max_health
    heal_amount = 1
    health_limit = 26
    # Movement
    speed = 6
    raw_speed = speed
    speed_limit = 14
    direction = "idle"
    directions = directions(speed)
    orig_directions = directions
    jumpdrive = Item_jump_drive((0, 0, 0))
    afterburner = Item_afterburner((0, 0, 0,))
    # Damage
    base_damage = 1.0
    damage = base_damage
    crit_chance = 95
    raw_crit_chance = crit_chance
    crit_limit = 50
    # Shield
    shield = Item_shield((0, 0, 0))
    shield_strength = 2
    max_shield_strength = 2
    # Gfx
    gfx_idx = {
        "up": 0, "down": 2, "right": 4, "left": 6, "right up": 8, "right down": 10, "left up": 12, "left down": 14, "idle": 16}
    ship_sprites = get_images("player_ship")
    effects_sprites = get_images("hit_effects")
    gfx_ticker = 0
    # Time
    restart_timer = False

    @classmethod
    def move(cls, direction):
        cls.direction = direction

    @classmethod
    def take_damage(cls, damage, sure_death=False):
        if damage > 0:
            if cls.shield.active:
                cls.shield_strength -= 1
                # cls.gfx_hit_effect()
                if cls.shield_strength < 1:
                    cls.shield.end_active()
                    cls.shield_strength = cls.max_shield_strength
            else:  # not cls.shield.active:
                cls.health -= damage
                cls.gfx_hit_effect()
                cls.reset_overdrive()
                if int(cls.health) <= 0:
                    cls.quit_game_WIP()

    @classmethod
    def quit_game_WIP(cls):
        state = data.LEVELS.load_game()
        state.load_save()
        data.LEVELS.display_score -= 50
        if data.LEVELS.display_score < 0:
            quit()
        else:
            data.INTERFACE.pause_menu(True)

    @classmethod
    def reset_overdrive(cls):
        if "overdrive" in data.ITEMS.active_flag_lst:
            cls.damage -= 0.05 * data.TURRET.overdrive_count
            data.TURRET.fire_rate += 0.7 * data.TURRET.overdrive_count
            data.TURRET.overdrive_count = 0

    @classmethod
    def shield_update(cls):
        cls.shield.effect()
        if cls.shield.active:
            win.blit(cls.ship_sprites[29], (cls.hitbox.topleft[0] - 38, cls.hitbox.topleft[1] - 60))

    @classmethod
    def use_heal(cls):
        if cls.heal_amount > 0 and cls.health < cls.max_health:
            Gfx.create_effect("heal", 20, (cls.hitbox.topleft[0] - 25, cls.hitbox.topleft[1] - 25), hover=True)
            cls.heal_amount -= 1
            cls.health = cls.max_health

    @classmethod
    def jumpdrive_update(cls):
        cls.jumpdrive.effect()
        if cls.jumpdrive.active:
            cls.draw_jump_dest()
            if cls.jumpdrive.engage:
                Gfx.create_effect("jump", 2, (cls.hitbox.topleft[0] - 40, cls.hitbox.topleft[1] - 40))
                cls.hitbox.center = pygame.mouse.get_pos()
                Gfx.create_effect("jumpa", 2, (cls.hitbox.topleft[0] - 60, cls.hitbox.topleft[1] - 60))
                cls.jumpdrive.end_active()
                cls.jumpdrive.engage = False

    @classmethod
    def afterburner_update(cls):
        cls.afterburner.effect()
        if cls.afterburner.active:
            cls.directions = directions(40)
        if cls.afterburner.cooldown:
            cls.directions = directions(cls.speed)

    @classmethod
    def draw_jump_dest(cls):
        win.blit(cls.ship_sprites[20], (pygame.mouse.get_pos()[0] - 41, pygame.mouse.get_pos()[1] - 50))

    @classmethod
    def gfx_animation(cls, idx):
        if cls.gfx_ticker < 3:
            win.blit(cls.ship_sprites[cls.gfx_idx[idx]], (cls.hitbox.topleft[0] - 6, cls.hitbox.topleft[1] - 25))
            cls.gfx_ticker += 1
        else:
            win.blit(cls.ship_sprites[cls.gfx_idx[idx] + 1], (cls.hitbox.topleft[0] - 6, cls.hitbox.topleft[1] - 25))
            cls.gfx_ticker += 1
        if cls.gfx_ticker == 6:
            cls.gfx_ticker = 0

    @classmethod
    def gfx_hit_effect(cls):
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect(0, 0, winwidth, winheight))
        win.blit(cls.effects_sprites[3], (cls.hitbox.topleft[0] - 20, cls.hitbox.topleft[1] - 20))

    @classmethod
    @timer
    def gfx_warning_lights(cls, timer):
        if cls.health < 2:
            ticker = timer.timer_animation_ticker(30)
            if ticker < 20:
                win.blit(cls.ship_sprites[21], (cls.hitbox.topleft[0] - 6, cls.hitbox.topleft[1] - 25))
            else:
                win.blit(cls.ship_sprites[22], (cls.hitbox.topleft[0] - 6, cls.hitbox.topleft[1] - 25))

    @classmethod
    def set_player_speed(cls, sp):
        cls.raw_speed += sp
        cls.speed = cls.raw_speed
        if cls.speed > cls.speed_limit:
            cls.speed = cls.speed_limit
        cls.directions = directions(cls.speed)
        cls.orig_directions = directions(cls.speed)

    @classmethod
    def set_player_health(cls, hp):
        cls.raw_max_health += hp
        cls.max_health = cls.raw_max_health
        if cls.max_health > cls.health_limit:
            cls.max_health = cls.health_limit

    @classmethod
    def set_player_crit_chance(cls, cc):
        cls.raw_crit_chance -= cc
        cls.crit_chance = cls.raw_crit_chance
        if cls.crit_chance < cls.crit_limit:
            cls.crit_chance = cls.crit_limit

    @classmethod
    @timer
    def update(cls, timer):

        for operator, position, con, direction in [
            ("<", cls.hitbox.center[0], 0, (1, 0)),
            (">", cls.hitbox.center[0], winwidth, (-1, 0)),
            ("<", cls.hitbox.center[1], 0, (0, 1)),
            (">", cls.hitbox.center[1], winheight, (0, -1))
        ]:
            if operator == "<":
                if position < con:
                    cls.hitbox.move_ip(direction)
                    break
            if operator == ">":
                if position > con:
                    cls.hitbox.move_ip(direction)
                    break
        else:
            cls.hitbox.move_ip(cls.directions[cls.direction])

        if data.LEVELS.after_boss:
            if cls.hitbox.colliderect(pygame.Rect(0, -10, winwidth, 15)):
                cls.hitbox.center = (cls.hitbox.center[0], winheight)
                Gfx.y += 1080
                data.ITEMS.dropped_lst.clear()
                data.PHENOMENON_DATA.clear()

                data.LEVELS.save_game()

                cls.restart_timer = True
                Gfx.bg_move = True

        if cls.restart_timer:
            if timer.trigger(120):
                data.LEVELS.after_boss = False
                cls.restart_timer = False

        # pygame.draw.rect(win, (255, 0, 0), cls.hitbox)
        cls.jumpdrive_update()
        cls.afterburner_update()
        cls.gfx_animation(cls.direction)
        cls.shield_update()
        cls.gfx_warning_lights()

        Escort.spawn()


class Escort(Timer):

    lst = []
    spawned = False
    fire_rate = 100

    def __init__(self, typ, color, gfx_idx, second=False):
        Timer.__init__(self)
        self.typ = typ
        self.color = color
        self.gfx_idx = gfx_idx
        self.second = second
        self.tc = Time_controler()
        if self.second:
            self.hitbox = pygame.Rect(Player.hitbox.center[0] + 100, Player.hitbox.center[1], 50, 50)
        else:
            self.hitbox = pygame.Rect(Player.hitbox.center[0] - 100, Player.hitbox.center[1], 50, 50)
        self.kill = False

    def move(self):
        if self.second:
            self.hitbox.center = (Player.hitbox.center[0] + 100, Player.hitbox.center[1])
        else:
            self.hitbox.center = (Player.hitbox.center[0] - 100, Player.hitbox.center[1])
        # pygame.draw.circle(win, self.color, self.hitbox.center, 25)

    def destroy(self):
        return self.kill

    def gfx_draw(self):
        animation_ticker = self.timer_animation_ticker(10)
        if animation_ticker < 5:
            win.blit(Player.ship_sprites[self.gfx_idx[0]], (self.hitbox.topleft[0] - 0, self.hitbox.topleft[1] - 0))
        else:
            win.blit(Player.ship_sprites[self.gfx_idx[1]], (self.hitbox.topleft[0] - 0, self.hitbox.topleft[1] - 0))

    def skills(self):
        if not data.LEVELS.after_boss:
            try:
                targets = [enemy for enemy in data.ENEMY_DATA if enemy.__class__.__name__ != "Asteroid"]
            except IndexError:
                pass

            if self.typ == "escort_missile":
                if self.timer_trigger(Escort.fire_rate * 5):
                    for target in targets:
                        data.PLAYER_PROJECTILE_DATA.append(Missile(15,
                                                                   (5, 5),
                                                                   self.hitbox.center,
                                                                   target.hitbox,
                                                                   Player.damage * 3,
                                                                   "es_missile"))

            elif self.typ == "escort_gun":
                if self.timer_trigger(Escort.fire_rate):
                    for target in targets:
                        data.PLAYER_PROJECTILE_DATA.append(Projectile(data.TURRET.projectile_speed,
                                                                      data.TURRET.projectile_size,
                                                                      self.hitbox.center,
                                                                      Player.damage,
                                                                      "es_normal",
                                                                      0,
                                                                      target=target.hitbox.center))

            elif self.typ == "escort_gunship":
                if self.timer_trigger(Escort.fire_rate * 0.65):
                    for angle in [280, 283, 286]:
                        if self.second:
                            data.PLAYER_PROJECTILE_DATA.append(Projectile(data.TURRET.projectile_speed,
                                                                          data.TURRET.projectile_size,
                                                                          self.hitbox.center,
                                                                          Player.damage,
                                                                          "gs_normal",
                                                                          0,
                                                                          angle=angle,
                                                                          angle_variation=-30))
                        else:
                            data.PLAYER_PROJECTILE_DATA.append(Projectile(data.TURRET.projectile_speed,
                                                                          data.TURRET.projectile_size,
                                                                          self.hitbox.center,
                                                                          Player.damage,
                                                                          "gs_normal",
                                                                          0,
                                                                          angle=angle))

    def tick(self):
        self.move()
        self.skills()
        self.gfx_draw()
        self.timer_tick()
        if not Escort.spawned:
            self.kill = True

    @classmethod
    def spawn(cls):
        if not Escort.spawned:
            for typ, c, gfx in [
                ("escort_missile", (255, 0, 00), (23, 24)),
                ("escort_gun", (0, 0, 255), (25, 26)),
                ("escort_gunship", (0, 255, 255), (27, 28))
            ]:
                if typ in data.ITEMS.active_flag_lst:
                    if "2nd_escort" in data.ITEMS.active_flag_lst:
                        data.PLAYER_DATA.append(Escort(typ, c, gfx, second=True))
                    data.PLAYER_DATA.append(Escort(typ, c, gfx))
                    Escort.spawned = True


data.PLAYER = Player

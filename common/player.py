import pygame
from pygame.locals import *

from init import *
from astraid_funcs import *
from Gfx import Gfx, Background
from ui import *
import astraid_data as data
from projectiles import Projectile, Missile
from items_active import Item_shield, Item_jump_drive, Item_afterburner


class Player:

    hitbox = pygame.Rect(winwidth / 2, winheight / 2, 80, 80)
    flag = "player"
    interaction_button_pressed = False

    # Health
    health = 5
    max_health = 5
    raw_max_health = max_health
    heal_amount = 2
    health_limit = 20
    heal_strenght = 4
    hitable = True
    # Movement
    speed = 6
    raw_speed = speed
    speed_limit = 14
    direction = "idle"
    angles = directions(speed)
    jumpdrive = Item_jump_drive((0, 0, 0))
    jumpdrive_disabled = False
    afterburner = Item_afterburner((0, 0, 0,))
    # Damage
    base_damage = 1
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
        "up": 0,
        "down": 0,
        "right": 1,
        "left": 2,
        "right up": 3,
        "right down": 3,
        "left up": 4,
        "left down": 4,
        "idle": 0
    }
    effect_name = {
        "up": "p_up",
        "down": "p_down",
        "right": "p_right",
        "left": "p_left",
        "right up": "p_right",
        "right down": "p_right",
        "left up": "p_left",
        "left down": "p_left",
        "idle": "p_idle"
    }
    ship_sprites = get_images("new_player")
    item_locs = [((-25, -30), 5), ((20, -30), 6), ((-25, 0), 7), ((20, 0), 8)]
    item_amount = 0
    gfx_ticker = 0
    # Time
    restart_timer = False

    @classmethod
    def move(cls, direction):
        cls.direction = direction

    @classmethod
    @timer
    def take_damage(cls, damage, timer, staggered=0):
        if cls.hitable:
            if timer.trigger(staggered):
                if damage > 0:
                    if cls.shield.active:
                        cls.shield_strength -= damage
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
        penalty_lvl = int(data.LEVELS.level / 6) * 6
        data.LEVELS.display_score -= data.LEVELS.death_score_panalties[penalty_lvl]
        if data.LEVELS.display_score < 0:
            quit()
            # reset save
        else:
            data.LEVELS.save_game()

    @classmethod
    def reset_overdrive(cls):
        if "overdrive" in data.ITEMS.active_flag_lst:
            cls.damage -= 0.05 * data.TURRET.overdrive_count
            data.TURRET.set_fire_rate(-0.1 * data.TURRET.overdrive_count)
            data.TURRET.overdrive_count = int(data.TURRET.overdrive_count / 2)

    @classmethod
    def shield_update(cls):
        cls.shield.effect()
        if cls.shield_strength == 0:
            cls.shield.end_active()

    @classmethod
    def use_heal(cls):
        if cls.heal_amount > 0 and cls.health < cls.max_health:
            Gfx.create_effect(
                "heal", 20, (cls.hitbox.topleft[0] - 25, cls.hitbox.topleft[1] - 25), hover=True)
            cls.heal_amount -= 1
            cls.health += cls.heal_strenght
            if cls.health > cls.max_health:
                cls.health = cls.max_health

    @classmethod
    def jumpdrive_update(cls):
        cls.jumpdrive.effect()
        if cls.jumpdrive.active:
            # cls.draw_jump_dest()
            if cls.jumpdrive.engage:
                Gfx.create_effect(
                    "jump", 2, (cls.hitbox.topleft[0] - 40, cls.hitbox.topleft[1] - 40))
                cls.hitbox.center = pygame.mouse.get_pos()
                Gfx.create_effect(
                    "jumpa", 2, (cls.hitbox.topleft[0] - 60, cls.hitbox.topleft[1] - 60))
                cls.jumpdrive.end_active()
                cls.jumpdrive.engage = False

    @classmethod
    def afterburner_update(cls):
        cls.afterburner.effect()
        if cls.afterburner.active:
            cls.angles = directions(40)
        if cls.afterburner.cooldown:
            cls.angles = directions(cls.speed)

    @classmethod
    def draw_jump_dest(cls):
        win.blit(
            cls.ship_sprites[20], (pygame.mouse.get_pos()[0] - 41, pygame.mouse.get_pos()[1] - 50))

    @classmethod
    @timer
    def gfx_animation(cls, timer):
        # pygame.draw.rect(win, (255, 255, 255), cls.hitbox)
        win.blit(
            cls.ship_sprites[cls.gfx_idx[cls.direction]], (cls.hitbox.topleft[0] - 57, cls.hitbox.topleft[1] - 50))
        if timer.trigger(12):
            Gfx.create_effect(
                cls.effect_name[cls.direction], 6, anchor=cls.hitbox, rot=0,
                x=-95, y=-90, layer=3
            )

    @classmethod
    def gfx_hit_effect(cls):
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect(0, 0, winwidth, winheight))
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect(0, 0, winwidth, winheight))

    @classmethod
    def set_player_speed(cls, sp):
        cls.raw_speed += sp
        cls.speed = cls.raw_speed
        if cls.speed > cls.speed_limit:
            cls.speed = cls.speed_limit
        cls.angles = directions(cls.speed)

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
    def get_name(cls):
        return cls.__name__

    @classmethod
    def interaction_button(cls, p):
        cls.interaction_button_pressed = p

    @classmethod
    def gfx_item_extensions(cls):

        cls.item_amount = 4 - [data.ITEMS.inventory_dic[k] for k in data.ITEMS.inventory_dic if k >= 4].count(None)

        for loc, idx in cls.item_locs[:cls.item_amount]:
            win.blit(
                cls.ship_sprites[idx], (cls.hitbox.center[0] + loc[0], cls.hitbox.center[1] + loc[1]))

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
            cls.hitbox.move_ip(cls.angles[cls.direction])

        if data.LEVELS.after_boss:
            if timer.timer_delay(120):
                if cls.hitbox.colliderect(pygame.Rect(0, -10, winwidth, 15)):
                    cls.hitbox.center = (cls.hitbox.center[0], winheight)

                    Background.bg_move = True
                    Background.y += 1080
                    for bg_obj in Background.bg_objs:
                        bg_obj.y += 1080

                    data.ITEMS.dropped_lst.clear()
                    data.PHENOMENON_DATA.clear()
                    data.PLAYER_DATA.clear()
                    data.ENEMY_DATA.clear()

                    data.LEVELS.save_game()

                    cls.restart_timer = True

        if cls.restart_timer:
            if timer.trigger(120):
                data.LEVELS.after_boss = False
                cls.restart_timer = False

        # pygame.draw.rect(win, (255, 0, 0), cls.hitbox)
        cls.jumpdrive_update()
        cls.afterburner_update()
        cls.gfx_animation()
        # cls.gfx_item_extensions()
        cls.shield_update()


data.PLAYER = Player

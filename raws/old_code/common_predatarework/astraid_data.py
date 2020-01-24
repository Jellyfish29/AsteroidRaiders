import pygame
import player as pl
import turret as tr
import items as it
from Gfx import Gfx


ENEMY_DATA = []
PROJECTILE_DATA = []
BLOCKER_DATA = []


def GAME_UPDATE():

    for enemy in ENEMY_DATA:
        enemy.gfx_animation()
        enemy.gfx_health_bar()
        tr.Turret.missile_aquisition(enemy)
        if enemy.border_collide():
            ENEMY_DATA.remove(enemy)
        if enemy.player_collide():
            if enemy.__class__.__name__ == "Bosses" or enemy.__class__.__name__ == "Elites":
                pl.Player.hit(0.05)
            else:
                pl.Player.hit(1)
            ENEMY_DATA.remove(enemy)
        if enemy.__class__.__name__ == "Enemy":
            enemy.draw()
        elif enemy.__class__.__name__ == "Spez_enemy":
            enemy.skills()
            tr.Turret.point_defence(enemy.hitbox)
        elif enemy.__class__.__name__ == "Bosses":
            enemy.move()
            enemy.skills()
            enemy.boss_skills()
            enemy.gfx_direction()
            enemy.enrage()
        elif enemy.__class__.__name__ == "Elites":
            enemy.move()
            enemy.skills()
            enemy.boss_skills()
            enemy.elite_skills()
            enemy.gfx_direction()
        elif enemy.__class__.__name__ == "Boss_adds":
            enemy.move()
            enemy.skills()
            enemy.boss_skills()
            tr.Turret.point_defence(enemy.hitbox)

        for projectile, direction, dmg, typ in PROJECTILE_DATA:
            if typ == "normal":
                if enemy.hitbox.colliderect(projectile):
                    Gfx.shot_hit_effect(projectile)
                    enemy.health -= dmg
                    enemy.healthbar_len -= (enemy.healthbar_max_len / (enemy.max_health / dmg))
                    # Special Ammo
                    if "piercing_projectile" not in it.Items.active_flag_lst:
                        PROJECTILE_DATA.remove((projectile, direction, dmg, typ))
                    if it.Item_he_rounds.active:
                        tr.Turret.he_round_hit(projectile.center)
            elif typ == "point_defence":
                if projectile.colliderect(enemy.hitbox):
                    Gfx.shot_hit_effect(projectile)
                    enemy.health -= 1
                    enemy.healthbar_len -= (enemy.healthbar_max_len / (enemy.max_health / 1))
                    PROJECTILE_DATA.remove((projectile, direction, dmg, typ))

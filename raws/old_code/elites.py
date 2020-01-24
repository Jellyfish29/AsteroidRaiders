
import random

from init import *
from astraid_funcs import *
import astraid_data as data
import bosses as bo
import levels as lvl
import items as it
import turret as tr
import player as pl


class Elites(bo.Bosses):

    health = 25

    def __init__(self, typ, health, speed, fire_rate, boss_skill, move_pattern, size, gfx_idx, gfx_hook, drop_amount):
        super().__init__(typ, health, speed, fire_rate, boss_skill, move_pattern, size, gfx_idx, gfx_hook, drop_amount)
        self.score_amount = 100
        self.drop_amount = 1
        self.shot_angles = angles_360(8)  # projectilespeed
        self.orig_angles = self.angles

    def elite_skills(self):
        pass

    def border_collide(self):
        pass

    def death(self):
        lvl.Levels.elite_fight = False
        if random.randint(0, 100) > 95:
            it.Items.drop((self.hitbox.topleft), amount=1)
        else:
            random.choice([
                lambda: it.Items.drop((self.hitbox.topleft), target=it.Item_supply_crate((100, 100, 100))),
                lambda: it.Items.drop((self.hitbox.topleft), target=it.Item_heal_crate((100, 100, 100))),
                lambda: it.Items.drop((self.hitbox.topleft), target=it.Item_upgrade_point_drop((100, 100, 100)))
            ])()
        self.kill = True

    def tick(self):
        self.gfx_animation()
        self.gfx_health_bar()
        self.move()
        self.player_collide()
        self.skill()
        self.boss_skills()
        self.elite_skills()
        self.gfx_direction()
        tr.Turret.missile_aquisition(self)
        if self.hitbox.colliderect(tr.Turret.nuke):
            self.take_damage(1.5 + pl.Player.damage * 0.1)
        if self.health <= 0:
            self.death()

    @classmethod
    def spawn(cls):
        data.ENEMY_DATA.append(random.choice([
            lambda: Elites("elite", Elites.health, 2, 170, ["mines"], [random.randint(0, 9) for _ in range(40)], (80, 180), [0, 1], (-50, -120), 0),
            lambda: Elites("elite", Elites.health + Elites.health * 0.2, 4, 120, ["seeker_missiles"], [random.randint(0, 9) for _ in range(40)], (80, 180), [0, 1], (-50, -120), 0),
            lambda: Elites("elite", Elites.health - Elites.health * 0.2, 8, 80, ["jumpdrive"], [random.randint(0, 9) for _ in range(40)], (80, 180), [0, 1], (-50, -120), 0),
            lambda: Elites("elite", Elites.health + Elites.health, 3, 100, ["salvo"], [random.randint(0, 9) for _ in range(40)], (80, 180), [0, 1], (-50, -120), 0),
            lambda: Elites("elite", Elites.health, 2, 120, ["adds"], [random.randint(0, 9) for _ in range(40)], (80, 180), [0, 1], (-50, -120), 0),
            lambda: Elites("elite", Elites.health + Elites.health * 0.1, 2, 200, ["main_gun"], [random.randint(0, 9) for _ in range(40)], (80, 180), [0, 1], (-50, -120), 0),
            lambda: Elites("elite", Elites.health + Elites.health * 0.1, 6, 200, ["star_shot"], [random.randint(0, 9) for _ in range(40)], (80, 180), [0, 1], (-50, -120), 0)
        ])())

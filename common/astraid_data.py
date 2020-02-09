ENEMY_DATA = []
ENEMY_PROJECTILE_DATA = []

PLAYER_DATA = []
PLAYER_PROJECTILE_DATA = []

PHENOMENON_DATA = []

PLAYER = None
TURRET = None
ITEMS = None
ACTIVE_ITEMS = None
BOSS = None
ELITES = None
PHENOM = None
LEVELS = None
ENEMY = None
INTERFACE = None


def GAME_UPDATE():

    for phenom in PHENOMENON_DATA:

        if phenom.destroy():
            PHENOMENON_DATA.remove(phenom)
        else:
            phenom.tick()

            if phenom.flag != "player":
                phenom.hit(PLAYER)

    for projectile in PLAYER_PROJECTILE_DATA:

        if projectile.destroy():
            PLAYER_PROJECTILE_DATA.remove(projectile)
        else:
            projectile.tick()

            for phenom in PHENOMENON_DATA:
                if phenom.flag != "player":
                    phenom.hit(projectile)

    for projectile in ENEMY_PROJECTILE_DATA:

        if projectile.destroy():
            ENEMY_PROJECTILE_DATA.remove(projectile)
        else:
            projectile.tick()

            for phenom in PHENOMENON_DATA:
                if phenom.flag != "enemy":
                    phenom.hit(projectile)

            if projectile.hit(PLAYER):
                PLAYER.take_damage(projectile.apply_damage())
                projectile.kill = True

            if projectile.flag == "en_mine" or projectile.flag == "en_missile":
                for pd in PLAYER_PROJECTILE_DATA:
                    if pd.hit(projectile):
                        projectile.kill = True
                        if not pd.piercing:
                            pd.kill = True

            if projectile.flag == "shield":
                for pd in PLAYER_PROJECTILE_DATA:
                    if pd.hit(projectile):
                        pd.kill = True

    for enemy in ENEMY_DATA:

        if enemy.destroy():
            ENEMY_DATA.remove(enemy)
        else:
            enemy.tick()

            for projectile in PLAYER_PROJECTILE_DATA:
                if projectile.hit(enemy):
                    if not projectile.piercing:
                        projectile.kill = True
                    if enemy.hitable:
                        enemy.take_damage(projectile.apply_damage())

            for phenom in PHENOMENON_DATA:
                if phenom.flag != "enemy":
                    if phenom.hit(enemy):
                        if enemy.hitable:
                            enemy.take_damage(phenom.apply_damage())

            for pl_obj in PLAYER_DATA:
                if pl_obj.hit(enemy):
                    if pl_obj.hitable:
                        pl_obj.kill = True
                    if enemy.hitable:
                        enemy.kill = True

        enemy.hit(PLAYER)

    for pl_obj in PLAYER_DATA:

        if pl_obj.destroy():
            PLAYER_DATA.remove(pl_obj)
        else:
            pl_obj.tick()

            for projectile in ENEMY_PROJECTILE_DATA:
                if projectile.hit(pl_obj):
                    if not projectile.piercing:
                        projectile.kill = True
                    if pl_obj.hitable:
                        pl_obj.take_damage(projectile.apply_damage())

            for phenom in PHENOMENON_DATA:
                if phenom.flag != "player":
                    if phenom.hit(pl_obj):
                        if phenom.hitable:
                            pl_obj.take_damage(phenom.apply_damage())

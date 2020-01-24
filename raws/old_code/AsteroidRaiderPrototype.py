import pygame
from pygame.locals import *
import random
import sys
import time

pygame.init()
Clock = pygame.time.Clock()
winwidth = 1800
winheight = 900
white = (255, 255, 255)
black = (0, 0, 0)
fps = 60
win = pygame.display.set_mode((winwidth, winheight))

class Player():

	health = 3
	hitbox =  pygame.Rect(winwidth / 2, winheight / 2, 50, 50)
	speed = 3
	direction = "idle"
	directions = 	[("up", (0, -speed)), 
					("down", (0, speed)),
					("right", (speed, 0)),
					("left", (-speed, 0)),
					("right up", (speed, -speed)),
					("right down", (speed, speed)),
					("left up", (-speed, -speed)),
					("left down", (-speed, speed)),
					("idle", (0, 0))]
	borders = 	[pygame.Rect(-100, -100, winwidth + 200, 10),	# Top
				 pygame.Rect(-100, winheight + 100, winwidth + 200, 10 ), # Bot
				 pygame.Rect(-100, -100, 10, winheight + 200), # Left
				 pygame.Rect(winwidth + 100, -100, 10, winheight +200)] # Right
											
	def move(direction):
		Player.direction = direction


class Turret():

	shot_lst = []
	projectile_speed = 10
	ammunition = 10
	angle = 0
	firing = False
	fire_rate = 10
	projectile_size = 5
	time_rate = 21
	angles = [	(0, (0,-projectile_speed)),
		 		(1, (projectile_speed,-projectile_speed)),
		  		(2 ,(projectile_speed,0)),
		   		(3, (projectile_speed,projectile_speed)),
		    	(4, (0,projectile_speed)),
		     	(5, (-projectile_speed,projectile_speed)),
		      	(6, (-projectile_speed,0)),
		      	(7 ,(-projectile_speed,-projectile_speed))]

	def turn(direction):
		if direction == "right":
			Turret.angle += 1
			if Turret.angle == 8:
				Turret.angle = 0
		elif direction == "left":
			Turret.angle -= 1
			if Turret.angle == -1:
				Turret.angle = 7

	def fire(fire):
		Turret.firing = fire
		if not fire:
			Turret.time_rate = 21

	def get_time_rate():
		tr = int(Clock.get_time() / 10)
		Turret.time_rate += tr


class Enemy:

	enemy_lst = []
	speed = (2, 6)
	direction = (0, 7)
	size = (10, 70)
	spawn_point = (1, 4)

	def __init__(self, size, direction, speed, spawn_point):
		self.spawn_points = {1 : (random.randint(0, winwidth), -50),# Top
							 2 : (random.randint(0, winwidth), winheight + 50),# Bot
							 3 : (-50, random.randint(0, winheight)), # Left
							 4 : (winwidth + 50, random.randint(0, winheight))} # Right
		self.direction = direction
		self.hitbox = pygame.Rect(self.spawn_points[spawn_point][0], self.spawn_points[spawn_point][1] , size, size)
		self.directions = [	(0, (0,-speed)),
			 				(1, (speed,-speed)),
			  				(2 ,(speed,0)),
			   				(3, (speed,speed)),
			    			(4, (0,speed)),
			     			(5, (-speed,speed)),
			      			(6, (-speed,0)),
			      			(7 ,(-speed,-speed))]
		self.health = int(size/10)
		self.score_amount = int(size/10)

	def spawn(self):
		for direction, x_y in self.directions:
			if self.direction == direction:
				self.hitbox.move_ip(x_y)
			pygame.draw.rect(win, white, self.hitbox)

	def border_collide(self):
		for border in Player.borders:
			if self.hitbox.colliderect(border):
				return True

	def player_collide(self):
		if self.hitbox.colliderect(Player.hitbox):
			return True

	def hit_detection(self):
		for shot, _ in Turret.shot_lst:
			if self.hitbox.colliderect(shot):
				Turret.shot_lst.remove((shot, _ ))
				self.health -= 1
				if self.health == 0:
					Levels.interval_score += self.score_amount
					Levels.display_score += self.score_amount
					return True


class Levels:

	interval_score = 0
	display_score = 0
	level_interval = 40
	enemy_amount = 20 # at Start
	enemys_per_level = 10
	level = 1

	def level_up():
		if Levels.interval_score > Levels.level_interval:
			Levels.enemy_amount += Levels.enemys_per_level
			Levels.level += 1
			Levels.interval_score = 0
		return Levels.enemy_amount


class Rect_Objects:

	# Main class for updating all Pygame Rect objects

	def update():
		# Player move and draw
		for direction, x_y in Player.directions:
			if Player.direction == direction:
				Player.hitbox.move_ip(x_y)
			pygame.draw.rect(win, white, Player.hitbox)
		# border draw and player out of bounds 
		for border in Player.borders:
			pygame.draw.rect(win, white, border)
			if Player.hitbox.colliderect(border):
				print("out") # Player collides with border Game Over
		# Turret: shot creation
		if Turret.firing:
			Turret.get_time_rate()
			if Turret.time_rate > Turret.fire_rate:
				for angle, x_y in Turret.angles:
						if Turret.angle == angle:
							Turret.shot_lst.append((pygame.Rect(Player.hitbox.center[0], Player.hitbox.center[1], Turret.projectile_size, Turret.projectile_size), x_y))
				Turret.time_rate = 0
		# Turret: shot draw and border/enemy collision
		for shot, direction in Turret.shot_lst:
				shot.move_ip(direction)
				pygame.draw.rect(win, white, shot)
				for border in Player.borders:
					if shot.colliderect(border):
						Turret.shot_lst.remove((shot, direction))
		if len(Turret.shot_lst) > Turret.ammunition :
			del(Turret.shot_lst)[Turret.ammunition]
		# Create enemy instances
		for _ in range(Levels.level_up()):
			while len(Enemy.enemy_lst) < Levels.enemy_amount:
				Enemy.enemy_lst.append(Enemy(random.randint(Enemy.size[0], Enemy.size[1]),
											 random.randint(Enemy.direction[0], Enemy.direction[1]), 
											 random.randint(Enemy.speed[0], Enemy.speed[1]),
											 random.randint(Enemy.spawn_point[0], Enemy.spawn_point[1])))
		# Collision detection for enemy rects with border and player
		for enemy in Enemy.enemy_lst:
			enemy.spawn()
			if enemy.border_collide() or enemy.hit_detection():
				Enemy.enemy_lst.remove(enemy)
			if enemy.player_collide():
				Player.health -= 1


def main():

	right, left, up, down = [False, False, False, False]
	enemy_lst = []

	def move_condition(bool_1, str_1, bool_2, str_2, str_3): # move_condition(if, move, elif, move ,"(else)" move)
		if bool_1:    
			Player.move(str_1)
		elif bool_2: 
			Player.move(str_2)
		else:
			Player.move(str_3)

	while True:
		#print(Clock.get_fps())
		win.fill(black)
		Rect_Objects.update()
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RIGHT:
					right = True
					move_condition(up, "right up", down, "right down", "right")
					right = True
					move_condition(up, "right up", down, "right down", "right")
				elif event.key == K_LEFT:
					left = True
					move_condition(up, "left up", down, "left down", "left")
				elif event.key == K_UP:
					up = True
					move_condition(left, "left up", right, "right up", "up")
				elif event.key == K_DOWN:
					down = True
					move_condition(left, "left down", right, "right down", "down")
				if event.key == K_a:
					Turret.turn("left")
				elif event.key == K_d:
					Turret.turn("right")
				elif event.key == K_SPACE:
					Turret.fire(True)
			elif event.type == KEYUP:
				if event.key == K_UP:
					up = False
				elif event.key == K_DOWN:
					down = False
				elif event.key == K_RIGHT:
					right = False
				elif event.key == K_LEFT:
					left = False
				elif event.key == K_SPACE:
					Turret.fire(False)
				# Damit der Spieler beim heben der Tasten stopt	
				# if [up, down, left, right].count(True) < 2:
					# for con, cmd in [(up, "up"),
					#   				(down, "down"),
					# 	 			(right, "right"),
					# 	   			(left, "left"),
					# 	    		(not any([up, down, right, left]), "idle")]:
						# if con:
						# 	Player.move(cmd)
			elif event.type == QUIT:
				pygame.quit()
				exit()
		Clock.tick(fps)
		pygame.display.update()

if __name__ == "__main__":
	main()

# Todo:
# - Power ups
# - Player health
# - gfx
# - special shot
# - special enemys (Boss)
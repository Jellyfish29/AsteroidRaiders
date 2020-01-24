import pygame
from pygame.locals import *
import random
import sys

pygame.init()
winwidth = 1900
winheight = 900
white = (255, 255, 255)
black = (0, 0, 0)
fps = 60
win = pygame.display.set_mode((winwidth, winheight))

class Player():

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
	borders = 	[pygame.Rect(0, -10, winwidth, 10),	# Top
				 pygame.Rect(0, winheight + 10, winwidth, 10 ), # Bot
				 pygame.Rect(-10, 0, 10, winheight), # Left
				 pygame.Rect(winwidth + 10, 0, 10, winheight)] # Right
											
	def move(direction):
		Player.direction = direction

	def draw():
		for direction, x_y in Player.directions:
			if Player.direction == direction:
				Player.hitbox.move_ip(x_y)
		for border in Player.borders:
			pygame.draw.rect(win, white, border)
			if Player.hitbox.colliderect(border):
				print("out") # Player colides with border Game Over
		pygame.draw.rect(win, white, Player.hitbox) 


class Turret():

	shot_lst = []
	projectile_speed = 5
	angle = 0
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
		print(f"angle = {Turret.angle}")

	def fire(fire, shot_angles = []):
		if fire:
			for angle, x_y in Turret.angles:
				if Turret.angle == angle:
					shot_angles.append((pygame.Rect(Player.hitbox.center[0], Player.hitbox.center[1], 4, 4), x_y))
		if not fire:
			for shot, direction in shot_angles:
				shot.move_ip(direction)
			Turret.shot_lst = [shot for shot, _ in shot_angles]
			for shot in Turret.shot_lst:
				pygame.draw.rect(win, white, shot)
				for border in Player.borders:
					if shot.colliderect(border):
						Turret.shot_lst.remove(shot)
						del(shot_angles)[0]
			if len(Turret.shot_lst) > 10 :
				del(shot_angles)[10]
				del(Turret.shot_lst)[10]



		
def main():
	fpsClock = pygame.time.Clock()
	right, left, up, down = [False, False, False, False]

	def move_condition(bool_1, str_1, bool_2, str_2, str_3): # move_condition(if, move, elif, move ,"(else)" move)
		if bool_1: 
			Player.move(str_1)
		elif bool_2: 
			Player.move(str_2)
		else:
			Player.move(str_3)

	while True:
		win.fill(black)
		Player.draw()
		Turret.fire(False)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RIGHT:
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

				if [up, down, left, right].count(True) < 2:
					for con, cmd in [(up, "up"),
					  				(down, "down"),
						 			(right, "right"),
						   			(left, "left"),
						    		(not any([up, down, right, left]), "idle")]:
						if con:
							Player.move(cmd)

			elif event.type == QUIT:
				pygame.quit()
				exit()

		fpsClock.tick(fps)
		pygame.display.update()

if __name__ == "__main__":
	main()
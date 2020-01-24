import pygame

pygame.init()
Clock = pygame.time.Clock()
winwidth = 1920
winheight = 1080
white = (255, 255, 255)
black = (0, 0, 0)
fps = 63
win = pygame.display.set_mode((winwidth, winheight), pygame.FULLSCREEN | pygame.DOUBLEBUF)
# win = pygame.display.set_mode((winwidth, winheight))
# pygame.mouse.set_visible(False)

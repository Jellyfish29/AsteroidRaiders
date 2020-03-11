import pygame

pygame.init()
Clock = pygame.time.Clock()
winwidth = 1920
winheight = 1080
white = (255, 255, 255)
black = (0, 0, 0)
FONTS = {
    5: pygame.font.SysFont("Consolas", 5),
    10: pygame.font.SysFont("Consolas", 10),
    15: pygame.font.SysFont("Consolas", 15),
    20: pygame.font.SysFont("Consolas", 20),
    25: pygame.font.SysFont("Consolas", 25),
    30: pygame.font.SysFont("Consolas", 30),
    35: pygame.font.SysFont("Consolas", 35),
    40: pygame.font.SysFont("Consolas", 40),
    50: pygame.font.SysFont("Consolas", 50),
    60: pygame.font.SysFont("Consolas", 60),
}
fps = 60
win = pygame.display.set_mode((winwidth, winheight), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
# win = pygame.display.set_mode((winwidth, winheight), pygame.FULLSCREEN | pygame.HWSURFACE)
# win = pygame.display.set_mode((winwidth, winheight))
# pygame.mouse.set_visible(False)

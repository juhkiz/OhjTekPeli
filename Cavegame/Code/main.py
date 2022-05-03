import pygame, sys
from settings import *
from level import Level
from gamedata import main_level

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(main_level, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.exit()
            sys.exit()

    screen.fill('black')
    level.run()
    
    pygame.display.update()
    clock.tick(60)
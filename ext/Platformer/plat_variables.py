import pygame
from ext.Core import variables as varia

resolution = varia.resolution
mid_screen = tuple(i/2 for i in resolution)

mi,ma = sorted(resolution)

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
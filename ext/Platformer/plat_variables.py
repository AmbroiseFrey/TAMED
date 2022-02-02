import pygame
from ext.Core import variables as varia

resolution = varia.resolution
mid_screen = tuple(int(i/2) for i in resolution)

mi,ma = sorted(resolution)

x,y = varia.resolution
screen = pygame.display.set_mode((int(x),int(y)))
clock = pygame.time.Clock()
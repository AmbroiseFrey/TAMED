import pygame
from ext.Core.variables import resolution

mid_screen = tuple(i/2 for i in resolution)

mi,ma = sorted(resolution)

checkpoints = []

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()